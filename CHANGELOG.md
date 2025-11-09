# Changelog / 更新日志

All notable changes to this project will be documented in this file.

本项目的所有重要变更将记录在此文件中。

## [1.1.0] - 2025-01-XX

### Added / 新增
- **Parallel Processing / 并行处理**: Multi-threaded OCR processing for faster batch operations (default: 4 workers)
  - 多线程 OCR 处理，加快批量操作速度（默认：4 个工作线程）
- **Error Detection / 错误检测**: Automatic detection of error messages (e.g., "白页", "Result:") to avoid unnecessary waiting
  - 自动检测错误信息（如"白页"、"Result:"），避免不必要的等待
- **Diagnostic Tool / 诊断工具**: `diagnose_ocr_failures.py` script to analyze OCR failure reasons
  - `diagnose_ocr_failures.py` 脚本用于分析 OCR 失败原因
- **Improved Error Handling / 改进的错误处理**: Failed OCR attempts now save error messages to combined output file
  - OCR 失败现在会将错误信息保存到合并输出文件中

### Improved / 改进
- Faster processing with parallel workers / 并行工作线程加快处理速度
- Better error messages in combined output / 合并输出中更好的错误信息
- Immediate error detection instead of waiting for timeout / 立即检测错误，而不是等待超时

### Fixed / 修复
- Fixed issue where error messages were not saved to combined file / 修复了错误信息未保存到合并文件的问题
- Improved handling of empty/error page responses / 改进了对空页面/错误页面响应的处理

---

## [1.0.0] - 2025-01-XX

### Added / 新增
- Initial release / 初始版本
- Simple batch OCR script with automatic folder processing / 简单的批量 OCR 脚本，支持自动文件夹处理
- Combined output file with source annotations / 带来源标注的合并输出文件
- Optional individual file output / 可选的单独文件输出
- Automatic TIF to PNG conversion / 自动 TIF 转 PNG 转换
- Headless browser mode / 无界面浏览器模式
- Bilingual documentation (English/Chinese) / 双语文档（英文/中文）

### Features / 功能
- Recursive image processing / 递归图片处理
- Smart caching (skip already processed images) / 智能缓存（跳过已处理图片）
- Support for PNG, JPG, TIF, WebP formats / 支持 PNG、JPG、TIF、WebP 格式
- Automatic cleanup of temporary files / 自动清理临时文件

