# Tibetan OCR Tool / 藏文 OCR 工具

A simple batch OCR tool for extracting Tibetan text from images using [dharmamitra.org OCR](https://dharmamitra.org/zh-hant?view=ocr).

一个简单的批量 OCR 工具，使用 [dharmamitra.org OCR](https://dharmamitra.org/zh-hant?view=ocr) 从图片中提取藏文文本。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

---

## Quick Links / 快速链接

- [Installation / 安装](#installation--安装)
- [Quick Start / 快速开始](#quick-start--快速开始)
- [Features / 功能特点](#features--功能特点)
- [Documentation / 文档](#documentation--文档)

---

## Features / 功能特点

- **Simple Usage / 简单易用**: Just point to an image folder, the tool handles everything
  - 只需指定图片文件夹，工具自动处理一切
- **Auto-Organization / 自动整理**: Automatically creates `ocr/` subfolder in your image folder
  - 自动在图片文件夹下创建 `ocr/` 子文件夹
- **Batch Processing / 批量处理**: Recursively processes all images (PNG, JPG, TIF, etc.)
  - 递归处理所有图片（PNG、JPG、TIF 等）
- **Smart Caching / 智能缓存**: Skips already-processed images (saves time)
  - 自动跳过已处理的图片（节省时间）
- **Format Conversion / 格式转换**: Automatically converts TIF to PNG for better compatibility
  - 自动将 TIF 转换为 PNG 以提高兼容性
- **Headless Mode / 无界面模式**: Runs without browser window (quiet background processing)
  - 无浏览器窗口运行（安静的后台处理）

---

## Installation / 安装

### 1. Install Python Dependencies / 安装 Python 依赖

```bash
pip install -r requirements.txt
```

### 2. Install Playwright Browser / 安装 Playwright 浏览器

```bash
python -m playwright install chromium
```

---

## Quick Start / 快速开始

### Basic Usage / 基本用法

```powershell
# Point to your image folder / 指向你的图片文件夹
python ocr_simple_batch.py "C:\path\to\your\images"
```

The tool will:
- 工具将：
  - Process all images recursively
    - 递归处理所有图片
  - Create a single combined file `<folder_name>_all_ocr.txt` with all results
    - 创建一个合并文件 `<文件夹名>_all_ocr.txt` 包含所有结果
  - No extra folders created (temporary files are cleaned up automatically)
    - 不创建额外文件夹（临时文件会自动清理）

**By default, only the combined file is created. Use `--individual-files` to also save separate .txt files for each image.**

**默认只创建合并文件。使用 `--individual-files` 可同时为每张图片保存单独的 .txt 文件。**

### Example Output / 输出示例

```
Found 150 image(s) to process...
[1/150] Processing: page001.jpg
[2/150] Processing: page002.tif
...
Done!
  Processed: 150
  Skipped (already exist): 0
  Failed: 0
  Combined file: your_images_all_ocr.txt
```

---

## Advanced Options / 高级选项

### Custom OCR Folder Name / 自定义 OCR 文件夹名称

```powershell
python ocr_simple_batch.py "C:\path\to\images" --ocr-folder "ocr_results"
```

### Non-Recursive (Only Direct Children) / 非递归（仅直接子文件）

```powershell
python ocr_simple_batch.py "C:\path\to\images" --no-recursive
```

### Verbose Output / 详细输出

```powershell
python ocr_simple_batch.py "C:\path\to\images" --verbose
```

### Save Individual Files / 保存单独文件

```powershell
# Also create individual .txt files in ocr/ folder (one per image)
# 同时在 ocr/ 文件夹中创建单独的 .txt 文件（每张图片一个）
python ocr_simple_batch.py "C:\path\to\images" --individual-files
```

### Force Re-Processing / 强制重新处理

```powershell
# Re-process all images even if results already exist
# 即使结果已存在也重新处理所有图片
python ocr_simple_batch.py "C:\path\to\images" --force
```

### Adjust Timeout / 调整超时时间

```powershell
# Increase timeout for large/slow images (default: 15000ms)
# 为大型/慢速图片增加超时时间（默认：15000ms）
python ocr_simple_batch.py "C:\path\to\images" --timeout-ms 30000
```

---


---

## Output Format / 输出格式

The tool creates two types of output:

工具会创建两种类型的输出：

### Default: Combined TXT File Only / 默认：仅合并 TXT 文件

By default, the tool creates a single combined file with all OCR results. No `ocr/` folder is created:

默认情况下，工具创建一个包含所有 OCR 结果的合并文件。不创建 `ocr/` 文件夹：

```
your_images/
├── page001.jpg
├── page002.tif
└── your_images_all_ocr.txt  # Combined file with all results + source annotations
```

### Optional: Individual TXT Files / 可选：单独的 TXT 文件

If you use `--individual-files`, separate `.txt` files are also created:

如果使用 `--individual-files`，也会创建单独的 `.txt` 文件：

```
your_images/
├── page001.jpg
├── page002.tif
├── ocr/
│   ├── page001.txt    # OCR result for page001.jpg
│   └── page002.txt    # OCR result for page002.tif
└── your_images_all_ocr.txt  # Combined file with all results
```

If processing recursively, subfolder structure is preserved:

如果递归处理，子文件夹结构会被保留：

```
your_images/
├── volume1/
│   ├── page001.jpg
│   └── ocr/
│       └── volume1/
│           └── page001.txt
└── your_images_all_ocr.txt
```

### Combined TXT File Format / 合并 TXT 文件格式

A single combined file (`<folder_name>_all_ocr.txt`) is created in the parent folder, containing all OCR results with source annotations:

在父文件夹中创建一个合并文件（`<文件夹名>_all_ocr.txt`），包含所有 OCR 结果并标注来源：

```
================================================================================
Combined OCR Results / 合并 OCR 结果
Source Folder / 源文件夹: C:\path\to\your_images
Total Images / 总图片数: 150
Processed / 已处理: 150
Skipped / 已跳过: 0
Failed / 失败: 0
================================================================================

================================================================================
Source / 来源: page001.jpg
Full Path / 完整路径: C:\path\to\your_images\page001.jpg
--------------------------------------------------------------------------------
<藏文 OCR 文本内容...>

================================================================================
Source / 来源: page002.tif
Full Path / 完整路径: C:\path\to\your_images\page002.tif
--------------------------------------------------------------------------------
<藏文 OCR 文本内容...>
...
```

This combined file makes it easy to:
- 合并文件便于：
  - Search all text at once / 一次性搜索所有文本
  - Review all results in one place / 在一个地方查看所有结果
  - Share complete OCR results / 分享完整的 OCR 结果
  - Track source images for each text segment / 追踪每段文本的来源图片

---

## Supported Image Formats / 支持的图片格式

- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- TIFF (`.tif`, `.tiff`) - automatically converted to PNG
  - TIFF（`.tif`、`.tiff`）- 自动转换为 PNG
- WebP (`.webp`)

---

## Troubleshooting / 故障排除

### "No images found" / "未找到图片"

- Check that your folder path is correct
  - 检查文件夹路径是否正确
- Ensure images have supported extensions (`.png`, `.jpg`, `.tif`, etc.)
  - 确保图片具有支持的扩展名（`.png`、`.jpg`、`.tif` 等）

### "Timed out waiting for Tibetan OCR text" / "等待藏文 OCR 文本超时"

- The image may be too large or the website is slow
  - 图片可能太大或网站响应慢
- Try increasing timeout: `--timeout-ms 30000`
  - 尝试增加超时时间：`--timeout-ms 30000`
- Check your internet connection
  - 检查网络连接

### "Playwright not installed" / "未安装 Playwright"

```bash
pip install playwright
python -m playwright install chromium
```

### "Pillow not available" / "Pillow 不可用"

```bash
pip install Pillow
```

Note: TIF conversion will be skipped if Pillow is not available, but the tool will still work.
注意：如果 Pillow 不可用，TIF 转换将被跳过，但工具仍可正常工作。

---

## Important Notes / 重要说明

- **Respect Website Terms / 遵守网站条款**: This tool uses dharmamitra.org OCR service. Please use responsibly and in accordance with their terms of use.
  - 本工具使用 dharmamitra.org OCR 服务。请负责任地使用并遵守其使用条款。

- **Network Required / 需要网络**: The tool requires an active internet connection to access the OCR service.
  - 工具需要活跃的网络连接以访问 OCR 服务。

- **Processing Time / 处理时间**: Processing time depends on image count and size. Large batches may take hours.
  - 处理时间取决于图片数量和大小。大批量处理可能需要数小时。

---

## License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件。

## Disclaimer / 免责声明

This tool uses dharmamitra.org OCR service. Please use responsibly and in accordance with their terms of use.

本工具使用 dharmamitra.org OCR 服务。请负责任地使用并遵守其使用条款。

---

## Credits / 致谢

- OCR Service: [dharmamitra.org](https://dharmamitra.org/zh-hant?view=ocr)
- Powered by Playwright for browser automation
  - 由 Playwright 提供浏览器自动化支持

---

## Support / 支持

For issues or questions, please check:
如有问题或疑问，请查看：

1. This README file / 本 README 文件
2. Command-line help: `python ocr_simple_batch.py --help`
   - 命令行帮助：`python ocr_simple_batch.py --help`

