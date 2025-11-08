# Pre-Release Checklist / 发布前检查清单

## ✅ 文件完整性检查 / File Completeness Check

- [x] `ocr_simple_batch.py` - 主批处理脚本
- [x] `ocr_dharmamitra_playwright.py` - OCR 引擎核心
- [x] `requirements.txt` - Python 依赖
- [x] `README.md` - 使用说明（中英双语）
- [x] `.gitignore` - Git 忽略规则
- [x] `LICENSE` - MIT 许可证
- [x] `CHANGELOG.md` - 更新日志
- [x] `CONTRIBUTING.md` - 贡献指南
- [x] `GITHUB_RELEASE_GUIDE.md` - GitHub 发布指南

## ✅ 代码质量检查 / Code Quality Check

- [x] 无硬编码路径（已修复示例路径）
- [x] 无敏感信息（用户名、密码等）
- [x] 无个人路径泄露
- [x] 代码注释清晰
- [x] 错误处理完善

## ✅ 文档检查 / Documentation Check

- [x] README.md 完整且准确
- [x] 安装说明清晰
- [x] 使用示例正确
- [x] 故障排除部分完整
- [x] 中英双语对照

## ✅ 依赖检查 / Dependencies Check

- [x] requirements.txt 版本已固定
- [x] 所有依赖都是公开可用的
- [x] 无私有或内部依赖

## ✅ 功能测试建议 / Functional Testing Recommendations

建议在发布前测试：
- [ ] 基本功能：单文件夹处理
- [ ] 递归处理：子文件夹
- [ ] TIF 转换：TIF 图片处理
- [ ] 合并文件生成：检查格式和内容
- [ ] 单独文件选项：`--individual-files`
- [ ] 错误处理：无效路径、网络错误等

## 📝 发布步骤 / Release Steps

1. **清理临时文件**
   ```powershell
   cd tibetan_ocr_tool
   Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
   ```

2. **初始化 Git 仓库**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit: Tibetan OCR Tool v1.0.0"
   ```

3. **创建 GitHub 仓库**
   - 使用 `GITHUB_RELEASE_GUIDE.md` 中的指导

4. **推送代码**
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/tibetan-ocr-tool.git
   git branch -M main
   git push -u origin main
   ```

5. **创建 Release**
   - Tag: `v1.0.0`
   - 标题: `v1.0.0 - Initial Release`
   - 描述: 参考 CHANGELOG.md

## 🎯 发布后建议 / Post-Release Recommendations

- 添加仓库 Topics（标签）
- 考虑添加 GitHub Actions（CI/CD，可选）
- 准备回应 Issues 和 Pull Requests
- 考虑添加示例图片（如果需要）

