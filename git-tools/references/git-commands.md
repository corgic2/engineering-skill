# Git 命令完整参考

## 配置

```bash
# 全局配置
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
git config --global core.editor "vim"

# 查看配置
git config --list
git config user.name

# 设置别名
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --oneline --graph --decorate"
```

## 仓库操作

```bash
# 创建新仓库
git init

# 克隆仓库
git clone <url>
git clone <url> <directory>
git clone --depth 1 <url>  # 浅克隆

# 查看远程仓库
git remote -v
git remote show origin

# 添加/删除远程仓库
git remote add origin <url>
git remote remove origin
```

## 日常开发

```bash
# 查看状态
git status
git status -s  # 简短格式

# 添加文件
git add <file>
git add .
git add -p  # 交互式添加

# 提交
git commit -m "message"
git commit -am "message"  # 跳过 add
git commit --amend  # 修改最后一次提交

# 查看历史
git log
git log --oneline
git log --graph
git log --author="name"
git log --since="2024-01-01"

# 查看差异
git diff
git diff --staged
git diff HEAD~1
```

## 分支操作

```bash
# 查看分支
git branch
git branch -v
git branch -a  # 所有分支
git branch -r  # 远程分支

# 创建/切换分支
git branch <name>
git checkout <name>
git checkout -b <name>  # 创建并切换
git switch <name>       # 新版本
git switch -c <name>    # 新版本

# 合并分支
git merge <branch>
git merge --no-ff <branch>  # 禁用快进

# 删除分支
git branch -d <name>   # 已合并
git branch -D <name>   # 强制删除
git push origin --delete <name>  # 删除远程分支
```

## 撤销与重置

```bash
# 撤销工作区修改
git checkout -- <file>
git restore <file>  # 新版本

# 撤销暂存
git reset HEAD <file>
git restore --staged <file>  # 新版本

# 重置提交
git reset --soft HEAD~1   # 保留修改到暂存区
git reset --mixed HEAD~1  # 保留修改到工作区
git reset --hard HEAD~1   # 丢弃修改

# 查看 reflog
git reflog

# 撤销指定提交
git revert <commit>
```

## 储藏

```bash
# 储藏修改
git stash
git stash push -m "message"
git stash push -p  # 交互式

# 查看储藏
git stash list

# 应用储藏
git stash pop       # 应用并删除
git stash apply     # 应用不删除
git stash apply stash@{1}

# 删除储藏
git stash drop stash@{0}
git stash clear
```

## 标签

```bash
# 创建标签
git tag <name>
git tag -a <name> -m "message"
git tag -a <name> <commit>

# 推送标签
git push origin <tag>
git push origin --tags

# 删除标签
git tag -d <name>
git push origin --delete <tag>
```

## 高级操作

```bash
# 变基
git rebase <branch>
git rebase -i HEAD~3  # 交互式

# Cherry-pick
git cherry-pick <commit>

# Bisect 二分查找
git bisect start
git bisect bad
git bisect good <commit>

# 子模块
git submodule add <url>
git submodule update --init --recursive
```
