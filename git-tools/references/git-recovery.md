# Git 误操作恢复详细参考

## 工作区改错，未 add

```bash
# 恢复单个文件到上次提交状态
git restore <file>

# 恢复整个目录
git restore <directory>

# 恢复到指定提交版本
git restore --source=<commit> <file>
```

## 已 add 但未 commit

```bash
# 从暂存区移除，保留工作区修改
git restore --staged <file>

# 如需同时丢弃工作区修改
git restore --staged <file>
git restore <file>
```

## 已 commit，未 push，想修改

```bash
# 修改最后一次提交信息
git commit --amend -m "新的提交信息"

# 追加遗漏的文件到最后一次提交
git add <遗漏文件>
git commit --amend --no-edit
```

## 已 commit，未 push，想撤销

```bash
# 软重置：保留修改到暂存区，可重新组织提交
git reset --soft HEAD~1

# 混合重置：保留修改到工作区
git reset --mixed HEAD~1

# 硬重置：完全丢弃（谨慎使用）
git reset --hard HEAD~1
```

## 已 push，想撤销（公共历史）

```bash
# 生成反向提交，安全撤销已 push 的改动
git revert <commit-hash>

# 如需撤销连续多个提交
git revert <oldest-commit-hash>^..<newest-commit-hash>
```

## 已 push，团队允许 force-push（仅限个人分支）

```bash
# 1. 确认当前分支无他人基于其工作
# 2. 重置到目标提交
git reset --hard <目标提交>

# 3. 强制推送（使用 --force-with-lease 防止覆盖他人新提交）
git push --force-with-lease origin <分支名>
```

> ⚠️ **警告**：force-push 会破坏公共历史。仅限个人 feature 分支，且确保无人基于该分支开发。

## 误删分支/提交恢复

```bash
# 查看 reflog 找到删除前的 commit hash
git reflog

# 基于该 hash 创建新分支
git checkout -b <新分支名> <hash>

# 或直接用 hash 查看内容
git show <hash>
```

## 储藏误删恢复

```bash
# 查看储藏列表
git stash list

# 如误 drop 了某个 stash，通过 reflog 找回
git fsck --unreachable | grep commit
# 或查看 git reflog 中的 stash 引用
```
