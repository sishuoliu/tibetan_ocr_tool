#!/usr/bin/env python3
"""
Automate OCR on dharmamitra.org for Tibetan text extraction using Playwright.

Site (as referenced): https://dharmamitra.org/zh-hant?view=ocr
- This script opens the OCR page, uploads an image, triggers OCR, and extracts Tibetan text
  (Unicode range U+0F00–U+0FFF) from the resulting page content.
- It supports single-file test mode and batch mode over a directory (recursively optional).

IMPORTANT:
- The website UI may change. This script uses heuristics:
  1) Prefer to find <input type="file"> and set files directly.
  2) If not present, attempt a file chooser by clicking common buttons (Upload/選擇/上傳/OCR).
  3) Wait for Tibetan characters to appear and then persist the extracted text.
- Use responsibly and in accordance with the website’s terms of use.

Usage examples (PowerShell):
  # Single image test
  python scripts/ocr_dharmamitra_playwright.py --image "sources\\pics\\folderA\\page01.png"

  # Batch over a directory
  python scripts/ocr_dharmamitra_playwright.py --input-dir "sources\\pics" --output-dir "sources\\ocr" --recursive
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


OCR_URL_DEFAULT = "https://dharmamitra.org/zh-hant?view=ocr"
TIBETAN_REGEX = re.compile(r"[\u0F00-\u0FFF]+")
DESKTOP_CHROME_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0 Safari/537.36"
)

def log(msg: str) -> None:
    print(f"[OCR] {msg}")

def find_file_input(page) -> Optional[str]:
    """
    Try to find a file input selector. Return selector string if found, else None.
    """
    candidates = [
        'input[type="file"]',
        'input[type=file]',
        'input#file',
        'input[name="file"]',
        'input[accept*="image"]',
        'input[accept*="png"]',
        'input[accept*="jpg"]',
    ]
    for sel in candidates:
        try:
            el = page.query_selector(sel)
            if el:
                return sel
        except Exception:
            pass
    return None

def set_files_if_input_exists(page, image_path: Path) -> bool:
    sel = find_file_input(page)
    if sel:
        try:
            page.set_input_files(sel, str(image_path))
            log(f"Set input files via selector: {sel}")
            return True
        except Exception as e:
            log(f"Failed set_input_files on {sel}: {e}")
    return False


def try_click_filechooser(page) -> None:
    """
    Attempt to trigger a file chooser by clicking common button texts.
    """
    candidates = [
        'text=/^Upload$/i', 'text=/^Choose/i', 'text=/^Select/i', 'text=/^OCR$/i',
        'text=/上傳/', 'text=/選擇/', 'text=/選取/', 'text=/開始辨識/', 'text=/開始/', 'text=/辨識/',
    ]
    role_candidates = [
        'role=button[name=/OCR|Upload|上傳|選擇|開始|辨識/i]',
    ]
    def click_in_context(ctx) -> bool:
        for sel in candidates:
            try:
                if ctx.query_selector(sel):
                    log(f"Clicking candidate: {sel}")
                    ctx.click(sel, timeout=1000)
                    return True
            except Exception:
                continue
        for sel in role_candidates:
            try:
                if ctx.query_selector(sel):
                    log(f"Clicking role-candidate: {sel}")
                    ctx.click(sel, timeout=1000)
                    return True
            except Exception:
                continue
        try:
            log("Clicking the first <button> as fallback")
            ctx.click("button", timeout=1000)
            return True
        except Exception:
            return False
    # Try main page then frames
    if click_in_context(page):
        return
    try:
        for frame in page.frames:
            if click_in_context(frame):
                return
    except Exception:
        pass

def set_files_in_any_context(page, image_path: Path) -> bool:
    """
    Try setting files on main page and then on each iframe.
    """
    if set_files_if_input_exists(page, image_path):
        return True
    try:
        for frame in page.frames:
            if set_files_if_input_exists(frame, image_path):
                log("Set files via iframe context.")
                return True
    except Exception as e:
        log(f"Frame scan error: {e}")
    return False

def debug_list_frames(page) -> None:
    try:
        frames = page.frames
        log(f"Frame count: {len(frames)}")
        for i, fr in enumerate(frames):
            url = ""
            try:
                url = fr.url
            except Exception:
                url = "<no-url>"
            log(f"  [frame {i}] {url}")
    except Exception:
        pass
def debug_probe_inputs(page) -> None:
    try:
        count_main = page.locator('input[type="file"]').count()
        log(f"Main page file inputs: {count_main}")
    except Exception:
        pass
    try:
        for i, fr in enumerate(page.frames):
            try:
                c = fr.locator('input[type="file"]').count()
                log(f"  [frame {i}] file inputs: {c}")
            except Exception:
                continue
    except Exception:
        pass

def navigate_with_retries(page, primary_url: str, timeout_ms: int, retries: int = 2) -> None:
    """
    Navigate to the OCR URL with a couple of alternate forms and sanity checks
    to avoid about:blank / blocked loads.
    """
    alt_urls = [
        primary_url,
        primary_url.replace("https://dharmamitra.org", "https://www.dharmamitra.org"),
        "https://dharmamitra.org/zh-hant?view=ocr",
        "https://www.dharmamitra.org/zh-hant?view=ocr",
    ]
    tried = 0
    last_err = None
    for url in alt_urls:
        if tried > retries:
            break
        try:
            log(f"Navigating to OCR URL: {url}")
            page.goto(url, timeout=timeout_ms, wait_until="load")
            # Basic sanity: ensure not stuck on about:blank
            current = ""
            try:
                current = page.url or ""
            except Exception:
                current = ""
            log(f"After goto, page.url = {current}")
            debug_list_frames(page)
            debug_probe_inputs(page)
            if current and "about:blank" not in current:
                return
        except Exception as e:
            last_err = e
        tried += 1
    if last_err:
        raise last_err
    raise PlaywrightTimeout("Navigation failed: ended up on about:blank or could not load OCR page.")

def click_start_trigger(page, click_timeout_ms: int = 1500) -> bool:
    """
    Try to click the 'start' control (triangle/Start) to begin OCR.
    Attempts selectors on main page and iframes. Returns True if clicked.
    """
    selectors = [
        'text=/▶/',                         # triangle glyph
        'role=button[name=/▶/]',
        'role=button[name=/開始|開始辨識|辨識|啟動/i]',
        'role=button[name=/Start|Recognize|OCR/i]',
        'button:has-text("▶")',
        'button[aria-label*="▶"]',
        'button[aria-label*="Start" i]',
        'button[title*="Start" i]',
        'button[aria-label*="開始"]',
        'button[title*="開始"]',
        'button[aria-label*="辨識"]',
        'button[title*="辨識"]',
        'button:has(svg[class*="play"])',
        'button:has(svg[aria-label*="play" i])',
        'button:has(i[class*="play"])',
        '[data-icon*=play]',
    ]
    def try_click(ctx) -> bool:
        for sel in selectors:
            try:
                el = ctx.query_selector(sel)
                if el:
                    log(f"Clicking start trigger: {sel}")
                    ctx.click(sel, timeout=click_timeout_ms)
                    return True
            except Exception:
                continue
        return False
    # main page first
    if try_click(page):
        return True
    # then frames
    try:
        for fr in page.frames:
            if try_click(fr):
                return True
    except Exception:
        pass
    return False

def debug_probe_inputs(page) -> None:
    try:
        count_main = page.locator('input[type="file"]').count()
        log(f"Main page file inputs: {count_main}")
    except Exception:
        pass
    try:
        for i, fr in enumerate(page.frames):
            try:
                c = fr.locator('input[type="file"]').count()
                log(f"  [frame {i}] file inputs: {c}")
            except Exception:
                continue
    except Exception:
        pass


def robust_upload_image(page, image_path: Path, timeout_ms: int = 12000) -> None:
    """
    Try multiple strategies to upload the image:
      1) Direct set_input_files on any visible/hidden file input
      2) Click labels/buttons to reveal inputs, then set_input_files
      3) As last resort, wait for filechooser event briefly and click triggers
    """
    # 1) Direct try
    if set_files_in_any_context(page, image_path):
        return
    # 2) Click labels commonly associated with file inputs
    label_candidates = [
        'label[for]',
        'label:has-text("上傳")',
        'label:has-text("選擇")',
        'label:has-text("OCR")',
    ]
    for sel in label_candidates:
        try:
            els = page.query_selector_all(sel)
            if not els:
                continue
            for _ in els:
                log(f"Clicking label candidate: {sel}")
                page.click(sel, timeout=1000)
                if set_files_in_any_context(page, image_path):
                    return
        except Exception:
            continue
    # 3) File chooser event (short attempts with different triggers)
    try:
        with page.expect_file_chooser(timeout=timeout_ms) as fc_info:
            try_click_filechooser(page)
        file_chooser = fc_info.value
        file_chooser.set_files(str(image_path))
        log("Uploaded via file chooser event.")
        return
    except PlaywrightTimeout:
        # As final fallback, try clicking triggers again then re-scan inputs
        log("File chooser timeout; attempting re-scan for inputs after trigger clicks.")
        try_click_filechooser(page)
        if set_files_in_any_context(page, image_path):
            return
        raise PlaywrightTimeout('Could not upload image: no file input and file chooser did not appear.')

def wait_for_tibetan_text(page, timeout_ms: int = 15000) -> str:
    """
    Wait until Tibetan characters appear in the page text, then return extracted Tibetan lines.
    """
    page.wait_for_timeout(500)
    elapsed = 0
    step = 250
    while elapsed < timeout_ms:
        try:
            body_text = page.inner_text("body")
        except Exception:
            body_text = ""
        if TIBETAN_REGEX.search(body_text):
            # Extract lines containing Tibetan
            lines = []
            for line in body_text.splitlines():
                if TIBETAN_REGEX.search(line):
                    lines.append(line.strip())
            # Deduplicate while preserving order
            seen = set()
            uniq = []
            for l in lines:
                if l not in seen:
                    seen.add(l)
                    uniq.append(l)
            return "\n".join(uniq).strip()
        page.wait_for_timeout(step)
        elapsed += step
    raise PlaywrightTimeout("Timed out waiting for Tibetan OCR text to appear.")


def ocr_single_image(image_path: Path, output_dir: Path, url: str, headless: bool = True, timeout_ms: int = 15000) -> Path:
    """
    Perform OCR for a single image by automating the dharmamitra OCR page.
    Writes the Tibetan text to a .txt file under output_dir (same stem as image).
    Returns the path to the written text file.
    """
    if not image_path.exists() or not image_path.is_file():
        raise FileNotFoundError(f"Image not found: {image_path}")
    output_dir.mkdir(parents=True, exist_ok=True)
    out_txt = output_dir / (image_path.stem + ".txt")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(ignore_https_errors=True, user_agent=DESKTOP_CHROME_UA)
        page = context.new_page()
        # Try robust navigation with sanity checks
        navigate_with_retries(page, url, timeout_ms=timeout_ms)

        # Robust upload with multiple strategies
        robust_upload_image(page, image_path, timeout_ms=min(12000, timeout_ms))

        # Try to trigger OCR if a start button exists
        if click_start_trigger(page):
            log("Clicked start trigger (triangle/Start).")
        trigger_candidates = [
            'text=/^OCR$/i', 'text=/開始辨識/', 'text=/^Start$/i', 'text=/Recognize/i', 'text=/辨識/', 'text=/^開始$/',
        ]
        for sel in trigger_candidates:
            try:
                if page.query_selector(sel):
                    log(f"Clicking trigger: {sel}")
                    page.click(sel, timeout=1000)
                    break
            except Exception:
                continue

        # Wait for Tibetan text to appear and extract
        log("Waiting for Tibetan OCR text...")
        tibetan_text = wait_for_tibetan_text(page, timeout_ms=timeout_ms)
        out_txt.write_text(tibetan_text, encoding="utf-8")
        log(f"Wrote OCR text: {out_txt}")

        context.close()
        browser.close()
    return out_txt


def find_images(input_dir: Path, recursive: bool) -> List[Path]:
    exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}
    if recursive:
        return sorted([p for p in input_dir.rglob("*") if p.is_file() and p.suffix.lower() in exts])
    return sorted([p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in exts])


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Automate dharmamitra.org OCR to extract Tibetan text.")
    parser.add_argument("--url", type=str, default=OCR_URL_DEFAULT, help="OCR page URL")
    parser.add_argument("--image", type=Path, help="Single image path for test mode")
    parser.add_argument("--input-dir", type=Path, help="Batch mode: directory containing images (e.g., sources/pics)")
    parser.add_argument("--output-dir", type=Path, default=Path("sources") / "ocr", help="Directory to write OCR .txt files")
    parser.add_argument("--recursive", action="store_true", help="Search input directory recursively")
    parser.add_argument("--headed", action="store_true", help="Run browser headed (for debugging)")
    parser.add_argument("--timeout-ms", type=int, default=15000, help="Timeout per page (ms)")
    parser.add_argument("--file-input-selector", type=str, help="Force a specific CSS selector for file input")
    parser.add_argument("--trigger-selector", action="append", help="Additional trigger selector(s) to click for OCR")
    args = parser.parse_args(argv)

    if not args.image and not args.input_dir:
        print("Error: provide --image for single test or --input-dir for batch.", file=sys.stderr)
        return 2

    try:
        if args.image:
            out_path = ocr_single_image(
                image_path=args.image,
                output_dir=args.output_dir,
                url=args.url,
                headless=not args.headed,
                timeout_ms=args.timeout_ms,
            )
            print(f"OCR written: {out_path}")
            return 0

        # Batch mode
        input_dir = args.input_dir
        if not input_dir.exists() or not input_dir.is_dir():
            print(f"Error: input directory not found: {input_dir}", file=sys.stderr)
            return 2
        images = find_images(input_dir, recursive=args.recursive)
        if not images:
            print(f"No images found under {input_dir} (recursive={args.recursive}).")
            return 0

        # Reuse a single browser session for batch
        args.output_dir.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=not args.headed)
            context = browser.new_context(ignore_https_errors=True, user_agent=DESKTOP_CHROME_UA)
            page = context.new_page()
            wrote = 0
            for img in images:
                try:
                    log(f"Processing: {img}")
                    navigate_with_retries(page, args.url, timeout_ms=args.timeout_ms)
                    # If user supplied a specific file input selector, try it first
                    if args.file_input_selector:
                        try:
                            page.set_input_files(args.file_input_selector, str(img))
                            log(f"Set input via user selector: {args.file_input_selector}")
                        except Exception as e:
                            log(f"User selector failed ({args.file_input_selector}): {e}; falling back to robust upload.")
                            robust_upload_image(page, img, timeout_ms=min(20000, args.timeout_ms))
                    else:
                        robust_upload_image(page, img, timeout_ms=min(20000, args.timeout_ms))

                    # Trigger OCR if possible
                    if click_start_trigger(page):
                        log("Clicked start trigger (triangle/Start).")
                    trigger_list = []
                    if args.trigger_selector:
                        trigger_list.extend(args.trigger_selector)
                    trigger_list.extend(['text=/^OCR$/i', 'text=/開始辨識/', 'text=/^Start$/i', 'text=/Recognize/i', 'text=/辨識/', 'text=/^開始$/'])
                    for sel in trigger_list:
                        try:
                            if page.query_selector(sel):
                                log(f"Clicking trigger: {sel}")
                                page.click(sel, timeout=1000)
                                break
                        except Exception:
                            continue

                    log("Waiting for Tibetan OCR text...")
                    tibetan_text = wait_for_tibetan_text(page, timeout_ms=args.timeout_ms)
                    out_txt = args.output_dir / (img.stem + ".txt")
                    out_txt.write_text(tibetan_text, encoding="utf-8")
                    print(f"OCR: {img} -> {out_txt}")
                    wrote += 1
                except Exception as e:
                    print(f"Failed OCR for {img}: {e}", file=sys.stderr)
            context.close()
            browser.close()
        print(f"Done. Wrote {wrote} OCR text files to {args.output_dir}")
        return 0
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


