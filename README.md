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
- **Serial Processing / 串行处理**: Processes images one by one by default to avoid rate limiting (default: 1 worker)
  - 默认逐个处理图片以避免速率限制（默认：1 个工作线程）
- **Optional Parallel Processing / 可选并行处理**: Can use multiple workers, but may trigger rate limiting
  - 可以使用多个工作线程，但可能触发速率限制
- **Rate Limit Handling / 速率限制处理**: Automatic retry with exponential backoff for rate limit errors
  - 自动重试速率限制错误，使用指数退避策略

---

## Installation / 安装

### 1. Create and Activate Virtual Environment / 创建并激活虚拟环境（强烈推荐）

**Why use a virtual environment? / 为什么使用虚拟环境？**
A virtual environment isolates project dependencies and avoids conflicts with your system Python environment. This is a Python best practice.

虚拟环境可以隔离项目依赖，避免与系统 Python 环境冲突。这是 Python 开发的最佳实践。

**Windows (PowerShell):**
```powershell
# 1. Verify Python is installed
# 确认已安装 Python
python --version

# 2. Navigate to project directory
# 进入项目目录
cd tibetan-ocr-tool

# 3. Create virtual environment (creates .venv folder in current directory)
# 创建虚拟环境（会在当前目录生成 .venv 文件夹）
python -m venv .venv

# 4. Activate virtual environment
# 激活虚拟环境
.\.venv\Scripts\Activate.ps1

# If you encounter execution policy error, run this first (requires admin):
# 如果遇到执行策略限制错误，先运行（需要管理员权限）:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Windows (Command Prompt):**
```cmd
# 1. Verify Python is installed
python --version

# 2. Navigate to project directory
cd tibetan-ocr-tool

# 3. Create virtual environment
python -m venv .venv

# 4. Activate virtual environment
.venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
# 1. Verify Python is installed
# 确认已安装 Python
python3 --version

# 2. Navigate to project directory
# 进入项目目录
cd tibetan-ocr-tool

# 3. Create virtual environment
# 创建虚拟环境
python3 -m venv .venv

# 4. Activate virtual environment
# 激活虚拟环境
source .venv/bin/activate
```

**How to confirm virtual environment is activated? / 如何确认虚拟环境已激活？**
After activation, you'll see `(.venv)` at the beginning of your command prompt, for example:
激活后，命令行提示符前会显示 `(.venv)`，例如：
```
(.venv) PS C:\Users\...\tibetan-ocr-tool>
```

**Deactivate virtual environment / 退出虚拟环境：**
```bash
deactivate
```

### 2. Install Python Dependencies / 安装 Python 依赖

In the activated virtual environment, run:
在激活的虚拟环境中运行：

```bash
pip install -r requirements.txt
```

**Windows users note / Windows 用户注意事项：**
- If `pip` command is not available, try `python -m pip install -r requirements.txt`
- 如果 `pip` 命令不可用，尝试 `python -m pip install -r requirements.txt`
- If you encounter permission errors, make sure the virtual environment is activated
- 如果遇到权限错误，确保虚拟环境已激活

**Linux/Mac users note / Linux/Mac 用户注意事项：**
- If `pip` command is not available, try `python3 -m pip install -r requirements.txt`
- 如果 `pip` 命令不可用，尝试 `python3 -m pip install -r requirements.txt`
- Some systems may require `sudo` (but usually not needed in virtual environment)
- 某些系统可能需要 `sudo` 权限（但在虚拟环境中通常不需要）

### 3. Install Playwright Browser / 安装 Playwright 浏览器

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

### Parallel Processing (Not Recommended) / 并行处理（不推荐）

```powershell
# Default: Serial processing (1 worker) - RECOMMENDED
# 默认：串行处理（1 个工作线程）- 推荐
python ocr_simple_batch.py "C:\path\to\images"

# Use multiple workers (may trigger rate limiting / 可能触发速率限制)
python ocr_simple_batch.py "C:\path\to\images" --workers 2
```

**Important Notes / 重要提示**: 
- **Default is 1 worker (serial processing)** to avoid rate limiting from the OCR website
  - **默认是 1 个工作线程（串行处理）**，以避免 OCR 网站的速率限制
- **Recommended: Use 1 worker** - Multiple workers often trigger "請求過多" (rate limit) errors
  - **推荐：使用 1 个工作线程** - 多个工作线程经常触发"請求過多"（速率限制）错误
- If you must use parallel processing, try 2 workers maximum, but expect rate limiting
  - 如果必须使用并行处理，最多尝试 2 个工作线程，但可能会遇到速率限制
- The tool automatically retries rate limit errors with exponential backoff (if they occur)
  - 工具会自动重试速率限制错误，使用指数退避策略（如果发生）
- Each worker uses a separate browser instance, so more workers = more memory usage
  - 每个工作线程使用独立的浏览器实例，因此更多工作线程 = 更多内存使用

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

<<<<<<< HEAD
=======
### "No OCR backend available" / "没有可用的 OCR 后端"

Make sure you have installed either:
- Tesseract OCR (recommended for Tibetan)
- PaddleOCR (optional)

确保已安装以下之一：
- Tesseract OCR（推荐用于藏文）
- PaddleOCR（可选）

### "Tesseract not found" / "找不到 Tesseract"

- Make sure Tesseract is installed and added to your system PATH
- On Windows, you may need to specify the Tesseract path in your code or environment

确保 Tesseract 已安装并添加到系统 PATH
在 Windows 上，可能需要在代码或环境中指定 Tesseract 路径

### "Virtual environment activation failed" / "虚拟环境激活失败"

**Windows PowerShell error / Windows PowerShell 错误：**
```
无法加载文件 .venv\Scripts\Activate.ps1，因为在此系统上禁止运行脚本
```

**Solution / 解决方案：**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### "Dependencies installation failed" / "依赖安装失败"

**Solution / 解决方案：**
1. Make sure virtual environment is activated
   确保虚拟环境已激活
2. Upgrade pip: `python -m pip install --upgrade pip` or `python3 -m pip install --upgrade pip`
   升级 pip：`python -m pip install --upgrade pip` 或 `python3 -m pip install --upgrade pip`
3. Use a mirror source if needed (e.g., Tsinghua mirror):
   如需要，使用国内镜像源（如清华镜像）：
   ```bash
   pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

>>>>>>> c6f6671 (docs: 娣诲姞铏氭嫙鐜鍒涘缓璇存槑鍒?README)
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

### "Executable doesn't exist" / "可执行文件不存在"

**Error message / 错误信息：**
```
BrowserType.launch: Executable doesn't exist at ...
Looks like Playwright was just installed or updated.
Please run the following command to download new browsers:
    playwright install
```

**Solution / 解决方案：**

This error occurs when Playwright Python package is installed but the browser binaries are missing. Run:
此错误发生在 Playwright Python 包已安装但浏览器二进制文件缺失时。运行：

```bash
# In your activated virtual environment / 在激活的虚拟环境中
python -m playwright install chromium
```

**Note / 注意：**
- Make sure you're in the activated virtual environment when running this command
- 运行此命令时确保在激活的虚拟环境中
- This command downloads the Chromium browser (about 200-300 MB)
- 此命令会下载 Chromium 浏览器（约 200-300 MB）
- The download only needs to be done once per environment
- 每个环境只需下载一次

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

