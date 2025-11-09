#!/usr/bin/env python3
"""
Diagnostic script to check OCR failure reasons from the combined output file.
诊断脚本：检查合并输出文件中的 OCR 失败原因。
"""
import re
import sys
from pathlib import Path

def analyze_combined_file(combined_file: Path):
    """Analyze the combined OCR file to find failures."""
    if not combined_file.exists():
        print(f"Error: File not found: {combined_file}", file=sys.stderr)
        return
    
    content = combined_file.read_text(encoding="utf-8", errors="ignore")
    
    # Find all "OCR not completed" entries
    not_completed = re.findall(
        r"Source / 来源: (.+?)\nFull Path / 完整路径: (.+?)\n-+\n\[OCR not completed",
        content,
        re.MULTILINE
    )
    
    # Find all "OCR Failed" entries
    failed = re.findall(
        r"Source / 来源: (.+?)\nFull Path / 完整路径: (.+?)\n-+\n\[OCR Failed / OCR 失败\] (.+?)\n",
        content,
        re.MULTILINE | re.DOTALL
    )
    
    # Extract summary stats
    stats_match = re.search(
        r"Total Images / 总图片数: (\d+)\nProcessed / 已处理: (\d+)\nSkipped / 已跳过: (\d+)\nFailed / 失败: (\d+)",
        content
    )
    
    print("=" * 80)
    print("OCR Failure Diagnosis / OCR 失败诊断")
    print("=" * 80)
    
    if stats_match:
        total, processed, skipped, failed_count = stats_match.groups()
        print(f"\nSummary / 摘要:")
        print(f"  Total Images / 总图片数: {total}")
        print(f"  Processed / 已处理: {processed}")
        print(f"  Skipped / 已跳过: {skipped}")
        print(f"  Failed / 失败: {failed_count}")
    
    if failed:
        print(f"\n❌ Found {len(failed)} images with explicit error messages:")
        print(f"   发现 {len(failed)} 张图片有明确的错误信息：")
        error_types = {}
        for source, path, error in failed[:10]:  # Show first 10
            error_type = error.split(":")[0] if ":" in error else error[:50]
            error_types[error_type] = error_types.get(error_type, 0) + 1
            print(f"\n  - {source}")
            print(f"    Error: {error[:100]}...")
        
        if len(failed) > 10:
            print(f"\n  ... and {len(failed) - 10} more")
        
        print(f"\n  Error Type Summary / 错误类型摘要:")
        for err_type, count in sorted(error_types.items(), key=lambda x: x[1], reverse=True):
            print(f"    {err_type}: {count}")
    
    if not_completed:
        print(f"\n⚠️  Found {len(not_completed)} images with 'OCR not completed' (no error saved):")
        print(f"   发现 {len(not_completed)} 张图片显示 'OCR 未完成'（未保存错误信息）：")
        print(f"   This usually means:")
        print(f"   这通常意味着：")
        print(f"     1. OCR process was interrupted / OCR 进程被中断")
        print(f"     2. Exception occurred but wasn't caught / 发生异常但未被捕获")
        print(f"     3. File write failed silently / 文件写入静默失败")
        print(f"\n   First 5 examples / 前 5 个示例：")
        for source, path in not_completed[:5]:
            print(f"     - {source}")
    
    if not failed and not not_completed:
        print("\n✅ No failures found in the combined file!")
        print("   在合并文件中未发现失败！")
    
    print("\n" + "=" * 80)
    print("Recommendations / 建议：")
    print("=" * 80)
    if failed or not_completed:
        print("1. Try reducing parallel workers to avoid rate limiting:")
        print("   尝试减少并行工作线程以避免速率限制：")
        print("   python ocr_simple_batch.py <folder> --workers 2")
        print()
        print("2. Increase timeout for slow images:")
        print("   为慢速图片增加超时时间：")
        print("   python ocr_simple_batch.py <folder> --timeout-ms 30000")
        print()
        print("3. Use verbose mode to see detailed errors:")
        print("   使用详细模式查看详细错误：")
        print("   python ocr_simple_batch.py <folder> --verbose")
        print()
        print("4. Re-process failed images with --force:")
        print("   使用 --force 重新处理失败的图片：")
        print("   python ocr_simple_batch.py <folder> --force")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python diagnose_ocr_failures.py <combined_ocr_file.txt>")
        print("用法: python diagnose_ocr_failures.py <合并的OCR文件.txt>")
        sys.exit(1)
    
    combined_file = Path(sys.argv[1])
    analyze_combined_file(combined_file)

