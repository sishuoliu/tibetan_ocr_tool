# GitHub 发布指南 / GitHub Release Guide

## 准备工作 / Preparation

### 1. 检查文件完整性 / Check File Completeness

确保以下文件存在：
- ✅ `ocr_simple_batch.py` - 主脚本
- ✅ `ocr_dharmamitra_playwright.py` - OCR 引擎
- ✅ `requirements.txt` - 依赖列表
- ✅ `README.md` - 使用说明
- ✅ `.gitignore` - Git 忽略文件
- ✅ `LICENSE` - 许可证
- ✅ `CHANGELOG.md` - 更新日志（可选）

### 2. 清理临时文件 / Clean Temporary Files

```powershell
# 删除 __pycache__ 文件夹
Remove-Item -Recurse -Force tibetan_ocr_tool\__pycache__ -ErrorAction SilentlyContinue
```

## 创建 GitHub 仓库 / Create GitHub Repository

### 方法 1: 使用 GitHub CLI (推荐) / Using GitHub CLI (Recommended)

```powershell
# 安装 GitHub CLI (如果还没有)
# Install GitHub CLI if not already installed

# 登录 GitHub
gh auth login

# 在 tibetan_ocr_tool 目录下
cd tibetan_ocr_tool

# 初始化 Git 仓库
git init
git add .
git commit -m "Initial commit: Tibetan OCR Tool"

# 创建 GitHub 仓库并推送
gh repo create tibetan-ocr-tool --public --source=. --remote=origin --push
```

### 方法 2: 手动创建 / Manual Creation

1. **在 GitHub 上创建新仓库**
   - 访问 https://github.com/new
   - Repository name: `tibetan-ocr-tool` (或你喜欢的名字)
   - Description: "Simple batch OCR tool for extracting Tibetan text from images"
   - 选择 Public 或 Private
   - **不要**勾选 "Initialize this repository with a README"（我们已经有了）

2. **在本地初始化并推送**
   ```powershell
   cd tibetan_ocr_tool
   git init
   git add .
   git commit -m "Initial commit: Tibetan OCR Tool"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/tibetan-ocr-tool.git
   git push -u origin main
   ```

## 添加仓库描述和标签 / Add Repository Description and Tags

在 GitHub 仓库页面：
1. 点击 "Settings" / 设置
2. 在 "Topics" 中添加标签：
   - `tibetan`
   - `ocr`
   - `tibetan-language`
   - `text-extraction`
   - `playwright`
   - `python`
   - `buddhist-texts`

## 创建 Release / Create Release

### 使用 GitHub Web 界面 / Using GitHub Web Interface

1. 在仓库页面，点击 "Releases" → "Create a new release"
2. Tag version: `v1.0.0`
3. Release title: `v1.0.0 - Initial Release`
4. Description:
   ```
   ## Features
   - Simple batch OCR processing
   - Combined output file with source annotations
   - Optional individual file output
   - Automatic TIF to PNG conversion
   - Headless browser mode
   - Bilingual documentation (English/Chinese)
   
   ## Installation
   ```bash
   pip install -r requirements.txt
   python -m playwright install chromium
   ```
   
   ## Usage
   ```bash
   python ocr_simple_batch.py "path/to/your/images"
   ```
   ```

### 使用 GitHub CLI / Using GitHub CLI

```powershell
gh release create v1.0.0 --title "v1.0.0 - Initial Release" --notes "Initial release of Tibetan OCR Tool"
```

## 添加徽章（可选）/ Add Badges (Optional)

在 README.md 顶部已包含基本徽章。如需更多，可访问：
- https://shields.io/

## 发布检查清单 / Release Checklist

- [ ] 所有文件已提交
- [ ] `.gitignore` 已配置
- [ ] `README.md` 完整且准确
- [ ] `LICENSE` 文件存在
- [ ] 代码中无硬编码路径
- [ ] 无敏感信息泄露
- [ ] 依赖版本已固定（requirements.txt）
- [ ] 已测试基本功能
- [ ] 已创建 GitHub Release

## 后续维护 / Maintenance

### 更新版本 / Update Version

1. 更新 `CHANGELOG.md`
2. 提交更改
3. 创建新的 Release tag
4. 推送代码

### 接收反馈 / Handle Feedback

- 及时回复 Issues
- 考虑 Pull Requests
- 根据反馈改进工具

## 常见问题 / FAQ

**Q: 需要添加 .github/workflows 吗？**
A: 可选。如果需要 CI/CD，可以添加 GitHub Actions。

**Q: 需要 setup.py 吗？**
A: 不需要。这是一个简单的脚本工具，直接运行即可。

**Q: 如何添加贡献者？**
A: 在 README.md 中添加 Contributors 部分，或在仓库 Settings → Collaborators 中添加。

