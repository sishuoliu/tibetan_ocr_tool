#!/usr/bin/env python3
"""
Simple batch OCR script: point to an image folder, auto-create ocr/ subfolder, process all images.

Usage (PowerShell):
  python ocr_simple_batch.py "C:\path\to\images"

  # With custom OCR output folder name (default: "ocr")
  python ocr_simple_batch.py "C:\path\to\images" --ocr-folder "ocr_results"

  # Non-recursive (only direct children)
  python ocr_simple_batch.py "C:\path\to\images" --no-recursive

  # Verbose output
  python ocr_simple_batch.py "C:\path\to\images" --verbose

  # Parallel processing (faster for large batches)
  python ocr_simple_batch.py "C:\path\to\images" --workers 8

Features:
- Automatically creates <image_folder>/ocr/ subfolder
- Recursively finds all images (PNG, JPG, TIF, etc.)
- For each image, creates a corresponding .txt file in ocr/ with OCR results
- Reuses existing OCR results if .txt already exists (skip re-processing)
- Converts TIF to PNG for better compatibility
- Headless mode (no browser window) by default
- Parallel processing support (default: 4 workers) for faster batch processing
"""
from __future__ import annotations

import argparse
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock
from typing import List

# Import from same directory
THIS_FILE = Path(__file__).resolve()
SCRIPTS_DIR = THIS_FILE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from ocr_dharmamitra_playwright import (  # type: ignore
    ocr_single_image,
    OCR_URL_DEFAULT,
)

try:
    from PIL import Image
except Exception:
    Image = None

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}


def find_images(input_dir: Path, recursive: bool = True) -> List[Path]:
    """Find all image files under input_dir."""
    if recursive:
        return sorted([p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in IMAGE_EXTS])
    return sorted([p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in IMAGE_EXTS])


def convert_image_for_upload(src: Path, tmp_dir: Path, verbose: bool = False) -> Path:
    """Convert TIF/TIFF to PNG for better OCR compatibility."""
    suffix = src.suffix.lower()
    if suffix in {".tif", ".tiff"}:
        if Image is None:
            if verbose:
                print(f"[OCR] Pillow not available; uploading TIF directly: {src.name}")
            return src
        try:
            tmp_dir.mkdir(parents=True, exist_ok=True)
            out_path = tmp_dir / (src.stem + ".png")
            if verbose:
                print(f"[OCR] Converting TIF->PNG: {src.name} -> {out_path.name}")
            with Image.open(src) as im:
                im = im.convert("RGB")
                im.save(out_path, format="PNG", optimize=True)
            return out_path
        except Exception as e:
            if verbose:
                print(f"[OCR] TIF conversion failed ({src.name}), using original: {e}")
            return src
    return src


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Simple batch OCR: process all images in a folder, save results to <folder>/ocr/",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage (recursive, creates combined file only)
  python ocr_simple_batch.py "C:\\path\\to\\your\\images"

  # Custom OCR folder name
  python ocr_simple_batch.py "C:\\path\\to\\images" --ocr-folder "ocr_results"

  # Non-recursive (only direct children)
  python ocr_simple_batch.py "C:\\path\\to\\images" --no-recursive

  # Verbose output
  python ocr_simple_batch.py "C:\\path\\to\\images" --verbose

  # Parallel processing (faster for large batches)
  python ocr_simple_batch.py "C:\\path\\to\\images" --workers 8
        """,
    )
    parser.add_argument(
        "image_folder",
        type=Path,
        help="Path to folder containing images (will create <folder>/ocr/ for results)",
    )
    parser.add_argument(
        "--ocr-folder",
        type=str,
        default="ocr",
        help="Name of OCR output subfolder (default: 'ocr')",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Only process direct children (don't recurse into subfolders)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed progress for each image",
    )
    parser.add_argument(
        "--timeout-ms",
        type=int,
        default=15000,
        help="Timeout per image OCR (ms, default: 15000)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process images even if .txt already exists",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=OCR_URL_DEFAULT,
        help="OCR page URL (default: dharmamitra.org)",
    )
    parser.add_argument(
        "--individual-files",
        action="store_true",
        help="Also create individual .txt files in ocr/ folder (default: only combined file)",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=1,
        help="Number of parallel workers for OCR processing (default: 1, recommended: 1 to avoid rate limiting)",
    )
    parser.add_argument(
        "--retry-rate-limit",
        type=int,
        default=3,
        help="Number of retries for rate limit errors (default: 3)",
    )
    parser.add_argument(
        "--retry-delay",
        type=int,
        default=5,
        help="Delay in seconds before retrying after rate limit error (default: 5)",
    )
    args = parser.parse_args(argv)

    image_folder = args.image_folder.resolve()
    if not image_folder.exists() or not image_folder.is_dir():
        print(f"Error: image folder not found: {image_folder}", file=sys.stderr)
        return 2

    # Auto-create OCR output folder only if individual files are requested
    # Otherwise, we'll use a hidden temp folder that gets cleaned up
    if args.individual_files:
        ocr_output_dir = image_folder / args.ocr_folder
        ocr_output_dir.mkdir(parents=True, exist_ok=True)
        if args.verbose:
            print(f"[OCR] Output folder: {ocr_output_dir}")
    else:
        # Use a hidden temp folder that will be cleaned up
        ocr_output_dir = image_folder / ".ocr_temp"
        ocr_output_dir.mkdir(parents=True, exist_ok=True)
        if args.verbose:
            print(f"[OCR] Using temporary folder (will be cleaned up): {ocr_output_dir}")

    # Find all images
    images = find_images(image_folder, recursive=not args.no_recursive)
    if not images:
        print(f"No images found in {image_folder} (recursive={not args.no_recursive})")
        return 0

    print(f"Found {len(images)} image(s) to process...")
    if args.verbose:
        print(f"  Output folder: {ocr_output_dir}")

    # Temporary folder for TIF->PNG conversions
    tmp_dir = ocr_output_dir / ".tmp_conversions"
    tmp_dir.mkdir(parents=True, exist_ok=True)

    # Thread-safe counters and progress tracking
    processed_lock = Lock()
    processed = 0
    skipped = 0
    failed = 0
    total = len(images)

    def process_single_image(args_tuple):
        """Process a single image - designed for parallel execution."""
        i, img_path, args, image_folder, ocr_output_dir, tmp_dir = args_tuple
        nonlocal processed, skipped, failed
        
        # Determine output TXT path (preserve relative structure if recursive)
        if args.no_recursive:
            out_txt = ocr_output_dir / (img_path.stem + ".txt")
        else:
            # Preserve subfolder structure in OCR output
            rel_path = img_path.relative_to(image_folder)
            out_txt = ocr_output_dir / rel_path.with_suffix(".txt")
            out_txt.parent.mkdir(parents=True, exist_ok=True)

        # Skip if individual file already exists (only if --individual-files is enabled)
        # But we still need to track it for the combined file
        if args.individual_files and not args.force and out_txt.exists():
            if args.verbose:
                with processed_lock:
                    print(f"[{i}/{total}] Skipped (exists): {img_path.name}")
            with processed_lock:
                skipped += 1
            # Still process for combined file, but read from existing file
            try:
                existing_content = out_txt.read_text(encoding="utf-8", errors="ignore")
                temp_content_file = ocr_output_dir / ".temp_contents" / f"{img_path.stem}.txt"
                temp_content_file.parent.mkdir(parents=True, exist_ok=True)
                temp_content_file.write_text(existing_content, encoding="utf-8")
            except Exception:
                pass
            return (img_path, True, None)  # (path, skipped, error)

        try:
            if args.verbose:
                with processed_lock:
                    print(f"[{i}/{total}] Processing: {img_path.name}")

            # Convert TIF to PNG if needed
            upload_path = convert_image_for_upload(img_path, tmp_dir, verbose=args.verbose)

            # Run OCR (headless mode) with retry logic for rate limiting
            # Use a temp directory for OCR output, we'll handle file placement ourselves
            temp_ocr_dir = ocr_output_dir / ".temp_ocr"
            temp_ocr_dir.mkdir(parents=True, exist_ok=True)
            
            # Retry logic for rate limiting
            import time
            last_error = None
            for retry in range(args.retry_rate_limit + 1):
                try:
                    result_txt = ocr_single_image(
                        image_path=upload_path,
                        output_dir=temp_ocr_dir,
                        url=args.url,
                        headless=True,  # No browser window
                        timeout_ms=args.timeout_ms,
                    )
                    # Success - break out of retry loop
                    break
                except Exception as e:
                    error_msg = str(e)
                    # Check if it's a rate limit error
                    if "請求過多" in error_msg or "请求过多" in error_msg or "rate limit" in error_msg.lower():
                        if retry < args.retry_rate_limit:
                            wait_time = args.retry_delay * (retry + 1)  # Exponential backoff
                            if args.verbose:
                                with processed_lock:
                                    print(f"  ⚠️  Rate limit detected, waiting {wait_time}s before retry {retry + 1}/{args.retry_rate_limit}...")
                            time.sleep(wait_time)
                            last_error = e
                            continue
                        else:
                            # Out of retries
                            raise ValueError(f"Rate limit error after {args.retry_rate_limit} retries: {error_msg}")
                    else:
                        # Not a rate limit error, don't retry
                        raise

            # Read OCR result
            ocr_content = result_txt.read_text(encoding="utf-8", errors="ignore")
            
            # Save individual file only if requested
            if args.individual_files:
                if result_txt != out_txt:
                    out_txt.write_text(ocr_content, encoding="utf-8")
                    if args.verbose:
                        with processed_lock:
                            print(f"  -> Saved: {out_txt.relative_to(image_folder)}")
                else:
                    # Already in right place
                    if args.verbose:
                        with processed_lock:
                            print(f"  -> Saved: {out_txt.relative_to(image_folder)}")
            else:
                # Just keep in temp for later combined file generation
                pass

            # Clean up temp OCR file
            try:
                if result_txt.exists():
                    result_txt.unlink()
            except Exception:
                pass

            # Store OCR content for combined file (we'll collect all at the end)
            # Actually, let's save to a hidden temp file that we'll read later
            temp_content_file = ocr_output_dir / ".temp_contents" / f"{img_path.stem}.txt"
            temp_content_file.parent.mkdir(parents=True, exist_ok=True)
            temp_content_file.write_text(ocr_content, encoding="utf-8")

            with processed_lock:
                processed += 1
            if args.verbose:
                size = len(ocr_content.encode('utf-8'))
                with processed_lock:
                    print(f"  -> OK ({size} bytes)")

            return (img_path, False, None)  # (path, skipped, error)

        except Exception as e:
            error_msg = str(e)
            with processed_lock:
                failed += 1
                print(f"[{i}/{total}] Failed: {img_path.name} - {error_msg}", file=sys.stderr)
            if args.verbose:
                import traceback
                with processed_lock:
                    traceback.print_exc()
            
            # Save error marker file so combined file can show the error
            try:
                temp_content_file = ocr_output_dir / ".temp_contents" / f"{img_path.stem}.txt"
                temp_content_file.parent.mkdir(parents=True, exist_ok=True)
                # Save error info as a special marker
                error_content = f"[OCR Failed / OCR 失败] {error_msg}"
                temp_content_file.write_text(error_content, encoding="utf-8")
            except Exception:
                pass  # If we can't save error marker, that's okay
            
            return (img_path, False, error_msg)  # (path, skipped, error)

    # Prepare arguments for parallel processing
    if args.workers > 1:
        print(f"Processing {total} images with {args.workers} parallel workers...")
        print(f"  ⚠️  Warning: Using multiple workers may trigger rate limiting (請求過多). Recommended: --workers 1")
        print(f"  警告：使用多个工作线程可能触发速率限制（請求過多）。推荐：--workers 1")
        # Add a small delay between worker starts to avoid overwhelming the website
        import time
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            # Submit all tasks
            futures = {
                executor.submit(
                    process_single_image,
                    (i, img_path, args, image_folder, ocr_output_dir, tmp_dir)
                ): (i, img_path)
                for i, img_path in enumerate(images, 1)
            }
            # Wait for completion and handle results
            for future in as_completed(futures):
                try:
                    future.result()  # This will raise any exceptions
                except Exception as e:
                    i, img_path = futures[future]
                    with processed_lock:
                        print(f"Unexpected error for {img_path.name}: {e}", file=sys.stderr)
    else:
        # Serial processing (original behavior)
        print(f"Processing {total} images sequentially...")
        for i, img_path in enumerate(images, 1):
            process_single_image((i, img_path, args, image_folder, ocr_output_dir, tmp_dir))

    # Cleanup temp conversions
    try:
        if tmp_dir.exists():
            import shutil
            shutil.rmtree(tmp_dir)
    except Exception:
        pass

    # Create combined TXT file with all results
    combined_txt_path = ocr_output_dir.parent / f"{ocr_output_dir.parent.name}_all_ocr.txt"
    combined_lines = []
    combined_lines.append("=" * 80)
    combined_lines.append(f"Combined OCR Results / 合并 OCR 结果")
    combined_lines.append(f"Source Folder / 源文件夹: {image_folder}")
    combined_lines.append(f"Total Images / 总图片数: {len(images)}")
    combined_lines.append(f"Processed / 已处理: {processed}")
    combined_lines.append(f"Skipped / 已跳过: {skipped}")
    combined_lines.append(f"Failed / 失败: {failed}")
    combined_lines.append("=" * 80)
    combined_lines.append("")

    temp_contents_dir = ocr_output_dir / ".temp_contents"
    
    for img_path in images:
        # Try to read from temp contents first (for newly processed images)
        temp_content_file = temp_contents_dir / f"{img_path.stem}.txt"
        
        # Also check individual files if they exist
        if args.no_recursive:
            txt_path = ocr_output_dir / (img_path.stem + ".txt")
        else:
            rel_path = img_path.relative_to(image_folder)
            txt_path = ocr_output_dir / rel_path.with_suffix(".txt")

        txt_content = None
        source_type = None
        
        # Priority: temp content (newly processed) > individual file > not found
        if temp_content_file.exists():
            try:
                txt_content = temp_content_file.read_text(encoding="utf-8", errors="ignore").strip()
                source_type = "temp"
            except Exception:
                pass
        
        if not txt_content and txt_path.exists():
            try:
                txt_content = txt_path.read_text(encoding="utf-8", errors="ignore").strip()
                source_type = "individual"
            except Exception:
                pass

        # Add to combined file
        combined_lines.append("=" * 80)
        combined_lines.append(f"Source / 来源: {img_path.relative_to(image_folder)}")
        combined_lines.append(f"Full Path / 完整路径: {img_path}")
        combined_lines.append("-" * 80)
        
        if txt_content:
            # Check if it's an error marker
            if txt_content.startswith("[OCR Failed / OCR 失败]"):
                combined_lines.append(txt_content)
            else:
                combined_lines.append(txt_content)
        else:
            combined_lines.append("[OCR not completed / OCR 未完成]")
        
        combined_lines.append("")

    # Cleanup temp directories
    try:
        temp_ocr_dir = ocr_output_dir / ".temp_ocr"
        if temp_ocr_dir.exists():
            import shutil
            shutil.rmtree(temp_ocr_dir)
        if temp_contents_dir.exists():
            import shutil
            shutil.rmtree(temp_contents_dir)
        # If not using individual files, remove the entire temp folder
        if not args.individual_files and ocr_output_dir.exists():
            import shutil
            shutil.rmtree(ocr_output_dir)
            if args.verbose:
                print(f"[OCR] Cleaned up temporary folder: {ocr_output_dir}")
    except Exception:
        pass

    # Write combined file
    try:
        combined_txt_path.write_text("\n".join(combined_lines), encoding="utf-8")
        print(f"  Combined file: {combined_txt_path.name}")
    except Exception as e:
        print(f"  Warning: Failed to create combined file: {e}", file=sys.stderr)

    # Summary
    print(f"\nDone!")
    print(f"  Processed: {processed}")
    print(f"  Skipped (already exist): {skipped}")
    print(f"  Failed: {failed}")
    if args.individual_files:
        print(f"  Individual files folder: {ocr_output_dir}")
    print(f"  Combined file: {combined_txt_path}")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

