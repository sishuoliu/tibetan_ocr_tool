#!/usr/bin/env python3
"""
Test script to check if increasing worker count increases error rate.
测试脚本：检查增加工作线程数是否会增加错误率。
"""
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Tuple

def run_ocr_test(image_folder: Path, workers: int, timeout_ms: int = 30000) -> Tuple[int, int, int, float]:
    """
    Run OCR with specified worker count and return statistics.
    使用指定的工作线程数运行 OCR 并返回统计信息。
    
    Returns: (processed, skipped, failed, elapsed_time)
    """
    print(f"\n{'='*80}")
    print(f"Testing with {workers} worker(s) / 使用 {workers} 个工作线程测试")
    print(f"{'='*80}")
    
    # Run the OCR script
    cmd = [
        sys.executable,
        "ocr_simple_batch.py",
        str(image_folder),
        "--workers", str(workers),
        "--timeout-ms", str(timeout_ms),
        "--force",  # Force re-processing to get accurate results
    ]
    
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 minute max per test
        )
        elapsed = time.time() - start_time
        
        # Parse output to extract statistics
        output = result.stdout + result.stderr
        processed = 0
        skipped = 0
        failed = 0
        
        for line in output.splitlines():
            if "Processed:" in line:
                try:
                    processed = int(line.split("Processed:")[1].strip().split()[0])
                except:
                    pass
            if "Skipped" in line and "already exist" in line:
                try:
                    skipped = int(line.split("Skipped")[1].strip().split()[0])
                except:
                    pass
            if "Failed:" in line:
                try:
                    failed = int(line.split("Failed:")[1].strip())
                except:
                    pass
        
        print(f"Results / 结果:")
        print(f"  Processed / 已处理: {processed}")
        print(f"  Skipped / 已跳过: {skipped}")
        print(f"  Failed / 失败: {failed}")
        print(f"  Time / 时间: {elapsed:.2f}s")
        
        if processed + skipped > 0:
            error_rate = (failed / (processed + skipped)) * 100 if (processed + skipped) > 0 else 0
            print(f"  Error Rate / 错误率: {error_rate:.2f}%")
        else:
            error_rate = 0
            print(f"  Error Rate / 错误率: N/A (no images processed)")
        
        return processed, skipped, failed, elapsed
        
    except subprocess.TimeoutExpired:
        print(f"  ⚠️  Test timed out after 10 minutes / 测试在10分钟后超时")
        return 0, 0, 0, 600.0
    except Exception as e:
        print(f"  ❌ Error running test / 运行测试时出错: {e}")
        return 0, 0, 0, 0.0

def main():
    image_folder = Path(r"C:\Users\sishu\Desktop\MBS\Nyingma Ba\pics_test")
    
    if not image_folder.exists():
        print(f"Error: Image folder not found: {image_folder}", file=sys.stderr)
        return 1
    
    # Count total images
    image_exts = {".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp"}
    images = [p for p in image_folder.rglob("*") if p.is_file() and p.suffix.lower() in image_exts]
    total_images = len(images)
    
    print(f"Found {total_images} image(s) to test / 找到 {total_images} 张图片用于测试")
    print(f"Testing folder: {image_folder}")
    
    # Test different worker counts
    worker_counts = [1, 2, 4, 8]
    results: Dict[int, Tuple[int, int, int, float]] = {}
    
    for workers in worker_counts:
        processed, skipped, failed, elapsed = run_ocr_test(image_folder, workers)
        results[workers] = (processed, skipped, failed, elapsed)
        
        # Small delay between tests
        print("\nWaiting 5 seconds before next test...")
        time.sleep(5)
    
    # Print summary
    print(f"\n{'='*80}")
    print("Summary / 摘要")
    print(f"{'='*80}")
    print(f"{'Workers':<10} {'Processed':<12} {'Failed':<10} {'Error Rate':<15} {'Time (s)':<12}")
    print(f"{'工作线程':<10} {'已处理':<12} {'失败':<10} {'错误率':<15} {'时间(秒)':<12}")
    print("-" * 80)
    
    for workers in worker_counts:
        processed, skipped, failed, elapsed = results[workers]
        total = processed + skipped
        error_rate = (failed / total * 100) if total > 0 else 0
        print(f"{workers:<10} {processed:<12} {failed:<10} {error_rate:>6.2f}%{'':<8} {elapsed:>8.2f}")
    
    print(f"\n{'='*80}")
    print("Analysis / 分析")
    print(f"{'='*80}")
    
    # Compare error rates
    error_rates = {}
    for workers, (processed, skipped, failed, _) in results.items():
        total = processed + skipped
        error_rates[workers] = (failed / total * 100) if total > 0 else 0
    
    if len(error_rates) > 1:
        baseline = error_rates[1]  # 1 worker as baseline
        print(f"\nBaseline (1 worker) error rate / 基准（1个工作线程）错误率: {baseline:.2f}%")
        
        for workers in [2, 4, 8]:
            if workers in error_rates:
                rate = error_rates[workers]
                diff = rate - baseline
                if diff > 0:
                    print(f"  {workers} workers: {rate:.2f}% (+{diff:.2f}% increase / 增加)")
                elif diff < 0:
                    print(f"  {workers} workers: {rate:.2f}% ({abs(diff):.2f}% decrease / 减少)")
                else:
                    print(f"  {workers} workers: {rate:.2f}% (no change / 无变化)")
    
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

