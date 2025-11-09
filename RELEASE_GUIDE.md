# GitHub Release Guide / GitHub 发布指南

This guide explains how to create a new release on GitHub for the Tibetan OCR Tool.

本指南说明如何为藏文 OCR 工具在 GitHub 上创建新版本。

---

## Prerequisites / 前置要求

1. **Git installed** / Git 已安装
2. **GitHub account** / GitHub 账户
3. **Repository access** / 仓库访问权限
4. **All changes committed** / 所有更改已提交

---

## Step 1: Prepare Files / 步骤 1：准备文件

Make sure all files are ready:

确保所有文件已准备好：

```bash
# Check current status / 检查当前状态
cd tibetan_ocr_tool
git status
```

Required files should include:
必需的文件应包括：

- ✅ `ocr_simple_batch.py` - Main script / 主脚本
- ✅ `ocr_dharmamitra_playwright.py` - OCR engine / OCR 引擎
- ✅ `requirements.txt` - Dependencies / 依赖
- ✅ `README.md` - Documentation (bilingual) / 文档（双语）
- ✅ `CHANGELOG.md` - Version history / 版本历史
- ✅ `LICENSE` - MIT License / MIT 许可证
- ✅ `.gitignore` - Git ignore rules / Git 忽略规则
- ✅ `diagnose_ocr_failures.py` - Diagnostic tool / 诊断工具

---

## Step 2: Commit and Push / 步骤 2：提交并推送

```bash
# Navigate to the project directory / 导航到项目目录
cd "C:\Users\sishu\Desktop\MBS\Nyingma Ba\tibetan_ocr_tool"

# Check what files need to be added / 检查需要添加的文件
git status

# Add all files / 添加所有文件
git add .

# Commit with a descriptive message / 使用描述性消息提交
git commit -m "Release v1.1.0: Add parallel processing and error detection

- Add parallel processing support (--workers option)
- Add error detection for empty/error pages
- Add diagnostic tool (diagnose_ocr_failures.py)
- Improve error handling and reporting
- Update documentation"

# Push to GitHub / 推送到 GitHub
git push origin main
```

**Note**: If your default branch is `master` instead of `main`, use `git push origin master`

**注意**：如果默认分支是 `master` 而不是 `main`，请使用 `git push origin master`

---

## Step 3: Create Release on GitHub / 步骤 3：在 GitHub 上创建发布

### Option A: Using GitHub Web Interface (Recommended) / 选项 A：使用 GitHub 网页界面（推荐）

1. **Go to your repository** / 访问你的仓库
   - Navigate to: `https://github.com/sishuoliu/tibetan_ocr_tool`
   - 导航到：`https://github.com/sishuoliu/tibetan_ocr_tool`

2. **Click "Releases"** / 点击"Releases"
   - On the right sidebar, click "Releases"
   - 在右侧边栏，点击"Releases"

3. **Click "Create a new release"** / 点击"Create a new release"
   - Or go directly to: `https://github.com/sishuoliu/tibetan_ocr_tool/releases/new`
   - 或直接访问：`https://github.com/sishuoliu/tibetan_ocr_tool/releases/new`

4. **Fill in release details** / 填写发布详情

   **Tag version** / 标签版本：
   ```
   v1.1.0
   ```

   **Release title** / 发布标题：
   ```
   v1.1.0 - Parallel Processing & Error Detection
   ```

   **Description** / 描述（从 CHANGELOG.md 复制）：
   ```markdown
   ## What's New / 新功能

   ### Parallel Processing / 并行处理
   - Process multiple images simultaneously for faster results
   - 同时处理多张图片以获得更快的结果
   - Default: 4 workers (adjustable with `--workers` option)
   - 默认：4 个工作线程（可通过 `--workers` 选项调整）

   ### Error Detection / 错误检测
   - Automatically detects error messages (e.g., "白页", "Result:")
   - 自动检测错误信息（如"白页"、"Result:"）
   - Immediately stops waiting when errors are detected
   - 检测到错误时立即停止等待

   ### Diagnostic Tool / 诊断工具
   - New `diagnose_ocr_failures.py` script to analyze OCR failures
   - 新的 `diagnose_ocr_failures.py` 脚本用于分析 OCR 失败

   ### Improved Error Handling / 改进的错误处理
   - Failed OCR attempts now save error messages to combined output
   - OCR 失败现在会将错误信息保存到合并输出中

   ## Installation / 安装

   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```

   ## Usage / 用法

   ```bash
   python ocr_simple_batch.py "path/to/images" --workers 4
   ```

   See [README.md](README.md) for full documentation.
   查看 [README.md](README.md) 获取完整文档。
   ```

5. **Attach files (optional)** / 附加文件（可选）
   - You can attach a ZIP file of the release if needed
   - 如果需要，可以附加发布版本的 ZIP 文件

6. **Publish release** / 发布版本
   - Click "Publish release" button
   - 点击"Publish release"按钮

### Option B: Using GitHub CLI / 选项 B：使用 GitHub CLI

If you have GitHub CLI installed:

如果你已安装 GitHub CLI：

```bash
# Install GitHub CLI first if needed / 如需要，先安装 GitHub CLI
# Windows: winget install GitHub.cli

# Authenticate / 认证
gh auth login

# Create release / 创建发布
gh release create v1.1.0 \
  --title "v1.1.0 - Parallel Processing & Error Detection" \
  --notes-file CHANGELOG.md
```

---

## Step 4: Verify Release / 步骤 4：验证发布

1. **Check release page** / 检查发布页面
   - Visit: `https://github.com/sishuoliu/tibetan_ocr_tool/releases`
   - 访问：`https://github.com/sishuoliu/tibetan_ocr_tool/releases`

2. **Test download** / 测试下载
   - Click "Source code (zip)" to download
   - 点击"Source code (zip)"下载

3. **Update repository description** / 更新仓库描述（可选）
   - Go to repository Settings → General
   - 前往仓库 Settings → General
   - Add description: "Batch OCR tool for Tibetan text extraction from images"
   - 添加描述："批量 OCR 工具，用于从图片中提取藏文文本"

---

## Release Checklist / 发布检查清单

Before creating a release, make sure:

创建发布前，请确保：

- [ ] All code is tested / 所有代码已测试
- [ ] README.md is up to date and bilingual / README.md 已更新且为双语
- [ ] CHANGELOG.md is updated / CHANGELOG.md 已更新
- [ ] All files are committed / 所有文件已提交
- [ ] Code is pushed to GitHub / 代码已推送到 GitHub
- [ ] Version number is consistent / 版本号一致
- [ ] License file is included / 包含许可证文件
- [ ] .gitignore is properly configured / .gitignore 配置正确

---

## Version Numbering / 版本号规则

Follow [Semantic Versioning](https://semver.org/):

遵循[语义化版本](https://semver.org/)：

- **MAJOR.MINOR.PATCH** (e.g., 1.1.0)
- **MAJOR**: Breaking changes / 重大变更
- **MINOR**: New features (backward compatible) / 新功能（向后兼容）
- **PATCH**: Bug fixes / 错误修复

Examples / 示例：
- `1.0.0` → `1.1.0`: Added parallel processing (new feature)
- `1.1.0` → `1.1.1`: Fixed a bug
- `1.1.1` → `2.0.0`: Breaking changes

---

## Troubleshooting / 故障排除

### Issue: "Repository not found" / 问题："找不到仓库"

**Solution** / 解决方案：
```bash
# Check remote URL / 检查远程 URL
git remote -v

# Update remote if needed / 如需要，更新远程
git remote set-url origin https://github.com/sishuoliu/tibetan_ocr_tool.git
```

### Issue: "Permission denied" / 问题："权限被拒绝"

**Solution** / 解决方案：
- Make sure you're logged in to GitHub / 确保已登录 GitHub
- Check repository access permissions / 检查仓库访问权限
- Use SSH instead of HTTPS if needed / 如需要，使用 SSH 代替 HTTPS

### Issue: "Tag already exists" / 问题："标签已存在"

**Solution** / 解决方案：
```bash
# Delete existing tag / 删除现有标签
git tag -d v1.1.0
git push origin :refs/tags/v1.1.0

# Then create new release / 然后创建新发布
```

---

## Quick Reference / 快速参考

### Common Git Commands / 常用 Git 命令

```bash
# Check status / 检查状态
git status

# Add all files / 添加所有文件
git add .

# Commit / 提交
git commit -m "Your message"

# Push / 推送
git push origin main

# Create and push tag / 创建并推送标签
git tag v1.1.0
git push origin v1.1.0
```

### Release URLs / 发布 URL

- **Repository**: `https://github.com/sishuoliu/tibetan_ocr_tool`
- **Releases**: `https://github.com/sishuoliu/tibetan_ocr_tool/releases`
- **New Release**: `https://github.com/sishuoliu/tibetan_ocr_tool/releases/new`

---

## Next Steps After Release / 发布后的后续步骤

1. **Share on social media** / 在社交媒体上分享
2. **Update documentation** / 更新文档
3. **Monitor issues** / 监控问题
4. **Plan next version** / 规划下一个版本

---

**Good luck with your release! / 祝发布顺利！** 🚀

