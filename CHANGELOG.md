# Changelog / 更新日志

All notable changes to this project will be documented in this file.

本项目的所有重要变更将记录在此文件中。

## [1.1.0] - 2025-01-XX

### Added / 新增
- **Serial Processing by Default / 默认串行处理**: Default to 1 worker (serial processing) to avoid rate limiting
  - 默认使用 1 个工作线程（串行处理）以避免速率限制
- **Optional Parallel Processing / 可选并行处理**: Multi-threaded OCR processing available, but not recommended due to rate limiting
  - 多线程 OCR 处理可用，但由于速率限制不推荐使用
- **Rate Limit Handling / 速率限制处理**: Automatic retry with exponential backoff for "請求過多" (rate limit) errors
  - 自动重试"請求過多"（速率限制）错误，使用指数退避策略
- **Error Detection / 错误检测**: Smart detection distinguishing real errors from progress messages
  - 智能检测，区分真正的错误和进度消息
  - Detects errors like "請求過多", "白页" but continues waiting for "大型檔案可能需要較長時間"
  - 检测"請求過多"、"白页"等错误，但继续等待"大型檔案可能需要較長時間"等进度消息
- **Diagnostic Tool / 诊断工具**: `diagnose_ocr_failures.py` script to analyze OCR failure reasons
  - `diagnose_ocr_failures.py` 脚本用于分析 OCR 失败原因
- **Improved Error Handling / 改进的错误处理**: Failed OCR attempts now save error messages to combined output file
  - OCR 失败现在会将错误信息保存到合并输出文件中

### Improved / 改进
- Changed default workers from 4 to 1 (serial processing) to avoid rate limiting issues / 将默认工作线程从 4 改为 1（串行处理），以避免速率限制问题
- Better error messages in combined output / 合并输出中更好的错误信息
- Immediate error detection for real errors, continued waiting for progress messages / 对真正错误立即检测，对进度消息继续等待
- Added warnings when using too many workers / 使用过多工作线程时添加警告

### Fixed / 修复
- Fixed issue where error messages were not saved to combined file / 修复了错误信息未保存到合并文件的问题
- Fixed false positive error detection for progress messages like "大型檔案可能需要較長時間" / 修复了对"大型檔案可能需要較長時間"等进度消息的误报
- Improved handling of rate limit errors with automatic retry / 改进了对速率限制错误的处理，添加自动重试

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

