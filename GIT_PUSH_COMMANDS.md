# Git Commands for Release v1.1.0 / 发布 v1.1.0 的 Git 命令

Copy and paste these commands in PowerShell (one at a time or all together):

在 PowerShell 中复制并粘贴这些命令（一次一个或全部一起）：

```powershell
# Navigate to project directory / 导航到项目目录
cd "C:\Users\sishu\Desktop\MBS\Nyingma Ba\tibetan_ocr_tool"

# Check status / 检查状态
git status

# Add all changes / 添加所有更改
git add .

# Commit with release message / 使用发布消息提交
git commit -m "Release v1.1.0: Add parallel processing and error detection

- Add parallel processing support (--workers option)
- Add error detection for empty/error pages (白页, Result:, etc.)
- Add diagnostic tool (diagnose_ocr_failures.py)
- Improve error handling and reporting
- Update CHANGELOG and documentation"

# Push to GitHub / 推送到 GitHub
git push origin main
```

---

## If you need to check remote URL / 如果需要检查远程 URL

```powershell
git remote -v
```

If the remote is not set correctly, update it:

如果远程 URL 不正确，更新它：

```powershell
git remote set-url origin https://github.com/sishuoliu/tibetan_ocr_tool.git
```

---

## After pushing, create release on GitHub / 推送后，在 GitHub 上创建发布

1. Go to: https://github.com/sishuoliu/tibetan_ocr_tool/releases/new
2. Follow the instructions in `RELEASE_GUIDE.md`

访问：https://github.com/sishuoliu/tibetan_ocr_tool/releases/new
按照 `RELEASE_GUIDE.md` 中的说明操作

