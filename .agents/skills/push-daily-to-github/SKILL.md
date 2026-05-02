---
name: push-daily-to-github
description: >
  将AI日报推送到GitHub仓库。自动检查Git状态、提交更改并推送到远程仓库。
  使用场景：当用户要求推送日报到GitHub、发布最新早报、同步日报数据时触发。
  触发词：推送日报、发布到GitHub、同步到远程、push daily。
license: MIT
metadata:
  version: "1.0"
  category: deployment
---
# Push Daily Report to GitHub Skill

将AI智能研发早报推送到GitHub仓库，确保最新的日报数据可以通过GitHub Pages访问。

## 项目路径

**AI日报项目根目录（也是Git仓库根目录）**：`/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank/`

**重要说明**：
- AI-Daily-for-bank 是一个**独立的 Git 项目**，有自己的 `.git` 目录
- 所有 git 命令必须在此目录下执行
- 不要在上层 agent-docs 目录执行 git 命令

---

## 工作流程（4步骤）

### Step 1: 检查Git状态

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git status
```

检查以下项目：
- 是否有未提交的更改（特别是 `daily/YYYY-MM-DD/` 目录）
- 确认当前分支是 `master`
- 查看哪些文件需要添加

**关键文件**：
- `daily/YYYY-MM-DD/` - 当日日报数据（包含 index.html 和 sources/*.md）
- `daily-index.json` - 日报索引
- `search-index.json` - 搜索索引
- `README.md` - 项目说明（如有更新）

---

### Step 2: 添加需要提交的文件

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank

# 添加当日日报数据（包括 HTML 和 Markdown 原文）
git add daily/YYYY-MM-DD/

# 添加索引文件
git add daily-index.json
git add search-index.json

# 如果有 README 更新（可选）
git add README.md
```

**注意**：
- ✅ 添加 `daily/YYYY-MM-DD/sources/*.md` - 原文文件（viewer.html 需要）
- ❌ 不要添加 scripts 目录（已被 .gitignore 排除）
- ❌ 不要添加 config.json（配置文件，敏感信息）
- ❌ 不要添加临时文件或调试脚本
- ✅ 只添加本次生成的新日报和相关更新

---

### Step 3: 提交更改

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git commit -m "推送YYYY-MM-DD AI日报

主要更新：
1. YYYY-MM-DD早报数据：
   - 国际X篇、国内X篇、同业X篇、其他X篇，共X篇
   - 特色内容（如文章合并、特殊打标等）

2. 脚本优化（如有）：
   - generate_html.py修复多来源渲染逻辑

3. 索引文件更新：
   - daily-index.json和search-index.json同步更新"
```

**提交信息要点**：
- 清晰说明本次更新的主要内容
- 列出统计数字（各分类文章数）
- 标注特殊处理（如文章合并、大模型打标等）
- 区分代码更新和数据更新

---

### Step 4: 推送到GitHub

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git push origin master
```

**认证方式**：
- **SSH方式**（推荐）：`git@github.com:keejo125/AI_Daily_For_Bank.git`
  - 需要配置SSH密钥
  - 可能需要输入SSH密钥密码
  
- **HTTPS方式**：`https://github.com/keejo125/AI_Daily_For_Bank.git`
  - 需要Personal Access Token
  - Token需要有repo权限

**常见问题**：
1. **Repository not found**：检查仓库地址是否正确，确认有访问权限
2. **Authentication failed**：检查SSH密钥或Token是否有效
3. **Permission denied**：确认对仓库有write权限

---

## Git配置

### 远程仓库地址

```bash
# 查看当前配置
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git remote -v

# 应该显示：
# origin  git@github.com:keejo125/AI_Daily_For_Bank.git (fetch)
# origin  git@github.com:keejo125/AI_Daily_For_Bank.git (push)
```

### 切换认证方式

**从HTTPS切换到SSH**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git remote set-url origin git@github.com:keejo125/AI_Daily_For_Bank.git
```

**从SSH切换到HTTPS**：
```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
git remote set-url origin https://github.com/keejo125/AI_Daily_For_Bank.git
```

### 用户信息

```bash
git config user.name    # 当前配置：lingma
git config user.email   # 当前配置：lingma@aliyun.com
```

**注意**：这是项目的 Git 提交者身份，用于标识代码提交的作者。

---

### 验证推送

推送完成后，验证以下内容：

### 1. 检查GitHub仓库

访问：https://github.com/keejo125/AI_Daily_For_Bank

确认：
- 最新commit已显示
- commit信息与预期一致
- 文件变更正确

### 2. 检查GitHub Pages

访问：https://keejo125.github.io/AI_Daily_For_Bank/daily/YYYY-MM-DD/

确认：
- 页面可以正常访问
- HTML渲染正确
- 所有资源加载正常
- 多来源标签、大模型标签显示正确

### 3. 检查索引文件

```bash
cd /Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank
cat daily-index.json | grep YYYY-MM-DD
```

确认新日期已添加到索引中。

---

## 自动化脚本（本地使用）

可以在**本地**创建一键推送脚本（不会被推送到GitHub）：

在项目根目录创建 `push_daily.sh`：

```bash
#!/bin/bash
set -e

DATE=${1:-$(date -v-1d +%Y-%m-%d)}  # 默认昨天
PROJECT_DIR="/Users/zhengk/GitProjects/agent-docs/projects/AI-Daily-for-bank"

cd $PROJECT_DIR

echo "📊 检查Git状态..."
git status

echo ""
echo "📝 添加文件..."
git add daily/$DATE/
git add daily-index.json
git add search-index.json

echo ""
echo "💾 提交更改..."
git commit -m "推送$DATE AI日报到GitHub"

echo ""
echo "🚀 推送到GitHub..."
git push origin master

echo ""
echo "✅ 推送完成！"
echo "📱 访问: https://keejo125.github.io/AI_Daily_For_Bank/daily/$DATE/"
```

使用方法：
```bash
chmod +x push_daily.sh
./push_daily.sh 2026-05-01  # 指定日期
./push_daily.sh              # 默认昨天
```

**注意**：此脚本保存在项目根目录，不会被推送到GitHub（因为只推送 daily/ 目录和数据文件）。

---

## 关键规则

1. **只推送新数据**：不要重复推送已存在的日报
2. **清理临时文件**：不推送调试脚本、临时JSON文件
3. **完整提交信息**：详细说明更新内容，便于追溯
4. **验证后再推送**：先在本地预览HTML，确认无误再推送
5. **保持原子性**：一次推送一个日期的日报，避免混合多个日期
6. **索引同步**：确保daily-index.json和search-index.json同时更新
7. **安全隔离**：
   - ✅ 只推送最终产物（HTML、Markdown原文、索引文件）
   - ❌ 不推送 scripts 目录（包含API调用逻辑）
   - ❌ 不推送 config.json（包含敏感配置）
   - ❌ 不推送中间数据文件（articles_raw.json等）

---

## 故障排查

### 问题1：推送被拒绝

**原因**：远程仓库有本地没有的提交

**解决**：
```bash
git pull origin master --rebase
git push origin master
```

### 问题2：大文件推送失败

**原因**：某些source文件过大

**解决**：
- 检查`.gitignore`是否正确配置（已排除 scripts/、config.json等）
- 考虑压缩或删除过大的Markdown文件
- 使用Git LFS管理大文件

### 问题3：GitHub Pages未更新

**原因**：GitHub Pages有缓存或构建延迟

**解决**：
- 等待1-2分钟让GitHub重新构建
- 清除浏览器缓存
- 检查GitHub Actions是否有构建错误

---

## 最佳实践

1. **每日定时推送**：建议在早报生成后立即推送
2. **备份重要数据**：推送前备份classification.json等重要文件
3. **记录推送日志**：在wiki或README中记录每次推送的日期和内容
4. **监控页面访问**：定期检查GitHub Pages是否正常访问
5. **版本标记**：重要更新可以打tag，如 `v2026-04-27`

---

## 相关技能

- [ai-daily-report](../ai-daily-report/SKILL.md) - 生成AI日报
- [create-skill](../../.qoder/skills/create-skill/SKILL.md) - 创建新技能
