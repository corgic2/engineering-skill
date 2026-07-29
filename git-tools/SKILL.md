---
name: git-tools
description: Git 版本控制工具辅助 Skill，提供常用 Git 命令的快速参考、操作指导和最佳实践。当用户需要执行 Git 操作（如提交、分支管理、合并、回滚、查看历史等）或遇到 Git 相关问题时使用此 Skill。
---

# Git Tools

此 Skill 提供 Git 操作的指导和常用命令参考。

## 常用操作速查

### 基础操作
```bash
# 查看状态
git status

# 添加文件到暂存区
git add <文件名>
git add .  # 添加所有更改

# 提交更改（提交信息必须经用户确认，禁止代写）
git commit -m "<用户确认的提交信息>"

# 推送代码
git push origin <分支名>
```

### 分支管理
```bash
# 查看分支
git branch          # 本地分支
git branch -r       # 远程分支
git branch -a       # 所有分支

# 创建并切换分支
git checkout -b <新分支名>
git switch -c <新分支名>  # 新版本 Git

# 切换分支
git checkout <分支名>
git switch <分支名>       # 新版本 Git

# 合并分支
git checkout main
git merge <要合并的分支>

# 删除分支
git branch -d <分支名>    # 已合并的分支
git branch -D <分支名>    # 强制删除
```

### 查看历史与对比
```bash
# 查看提交历史
git log --oneline --graph -20

# 查看文件更改
git diff

# 查看某文件的修改历史
git log -p <文件名>

# 查看指定提交的更改
git show <commit-id>
```

### 撤销操作
```bash
# 撤销工作区的修改
git checkout -- <文件名>

# 撤销暂存区的文件
git reset HEAD <文件名>

# 回滚到指定版本（保留修改）
git reset --soft HEAD~1

# 回滚到指定版本（丢弃修改）
git reset --hard <commit-id>

# 查看所有操作记录（用于找回）
git reflog
```

### 远程操作
```bash
# 查看远程仓库
git remote -v

# 添加远程仓库
git remote add origin <仓库地址>

# 拉取代码
git pull origin <分支名>

# 获取远程分支到本地
git fetch origin
git checkout -b <本地分支名> origin/<远程分支名>
```

### 储藏（Stash）
```bash
# 储藏当前更改
git stash push -m "储藏说明"

# 查看储藏列表
git stash list

# 应用最近一次储藏
git stash pop

# 应用指定储藏
git stash apply stash@{n}
```

## 提交信息规范

使用约定式提交（Conventional Commits）：

```
<类型>(<可选的作用域>): <描述>

[可选的正文]

[可选的脚注]
```

**类型：**
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响功能）
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例：**
```
feat(user): 添加用户登录功能

- 实现 JWT 认证
- 添加登录页面

Closes #123
```

## 工作流最佳实践

### 功能分支工作流（含审查节点）

```
1. 从 main 创建功能分支
   git checkout -b feature/xxx

2. 开发完成 → git add

3. [门控 1] diff 审查（快速自检）
   git diff --staged

4. [门控 2] code-review 正式审查（五维评分）
   → 发现问题 → 修复 → 回到步骤 3
   → 审查通过 → 继续

5. git commit（提交信息需用户输入/确认）
   git commit -m "<用户确认的提交信息>"

6. [门控 3] 提交后轻量复核
   git show --stat HEAD
   git log -1 --oneline
   → 有问题 → git commit --amend → 回到步骤 3（重大变更）或仅修正信息
   → 没问题 → 继续

7. [门控 4] 推送前质量门控检查清单

8. git push origin feature/xxx

9. 创建 Pull Request（如需要）
```

## 故障排除

### 常见错误处理

**1. 冲突解决**
- `git status` 查看冲突文件列表
- 手动编辑解决冲突标记（`<<<<<` `=====` `>>>>>`）
- `git add <冲突文件>` 标记已解决
- `git merge --continue` / `git rebase --continue` 完成操作

**2. 误删文件恢复**
- 工作区误删：`git restore <文件>`
- 恢复已提交删除的文件：`git checkout HEAD~1 -- <文件>`

**3. 修改最后一次提交**
- 修改信息：`git commit --amend -m "新信息"`
- 追加文件：`git add <文件>` + `git commit --amend --no-edit`
- 已 push 后修改： amend 后 `git push --force-with-lease`

> 更详细的恢复命令参考见 [references/git-recovery.md](references/git-recovery.md)

## 决策树：何时用 merge / rebase / squash

```
是否需要保留完整分支历史？
    │
    ├── 是 → 需要看到每个提交和合并点
    │       └── git merge --no-ff <branch>
    │           └── 保留分支拓扑，适合 feature 合入 main
    │
    └── 否 → 历史可以线性化
            │
            ├── 分支仅本地开发，未推送远程
            │       └── git rebase main
            │           └── 变基后提交历史更整洁
            │
            └── 分支已推送或多人协作
                    └── git merge --squash <branch>
                        └── 压缩为单个提交，适合小功能/修复
```

**选择原则**：
- **merge**：团队需要看到完整开发脉络，或长期维护分支
- **rebase**：个人本地分支，希望提交历史线性、干净
- **squash**：小改动/单功能，不需要保留中间调试提交
- **禁止对已推送的公共分支做 rebase**

## 冲突解决流程

```
git merge / rebase / cherry-pick 冲突
    ↓
git status  ←── 查看冲突文件列表
    ↓
逐文件编辑，解决冲突标记（<<<<< ===== >>>>>）
    ↓
git add <已解决文件>
    ↓
全部解决后：
    - merge:  git commit（或 git merge --continue）
    - rebase: git rebase --continue
    - cherry-pick: git cherry-pick --continue
```

**冲突解决原则**：
- 先理解双方意图，不要只保留"自己的"
- 解决后必须编译/运行验证，不能盲目标记 resolved
- 复杂冲突时，优先保留功能完整性，而非历史整洁

## 误操作回滚决策树

```
发生了什么？
    │
    ├── 工作区改错了，未 add → git restore
    ├── 已 add 但未 commit → git restore --staged
    ├── 已 commit，未 push，想修改 → git commit --amend
    ├── 已 commit，未 push，想撤销 → git reset --soft HEAD~1
    ├── 已 push，想撤销（公共历史）→ git revert
    ├── 已 push，允许 force-push → git reset --hard + force-with-lease
    └── 误删分支/提交 → git reflog
```

**核心原则**：
- **已 push 的公共历史**：只能用 `revert`（生成反向提交），禁止 force-push
- **未 push 的本地历史**：可用 `reset --soft` 重新组织，或 `commit --amend` 修改
- **force-push 仅限个人分支**，且必须加 `--force-with-lease`

> 各场景完整命令参见 [references/git-recovery.md](references/git-recovery.md)

## 代码审查与质量门控

### 完整提交流程（含审查节点）

```
git add 完成
    ↓
[门控 1] 提交前 diff 审查（快速自检）
    ↓
[门控 2] 提交前 code-review 正式审查（五维评分）
    │   ←── 发现问题 → 用户确认 → 修复 → 重新 git add → 重新审查
    ↓
git commit
    ↓
[门控 3] 提交后轻量复核（提交信息、完整快照确认）
    ↓
git push 前
    ↓
[门控 4] 推送前质量门控（最终检查清单）
    ↓
git push
```

> **为什么 code-review 放在 commit 前？**
> - commit 前审查基于 `git diff --staged`，发现问题可直接修改工作区文件，无需 `--amend`
> - 修改成本低，不污染 commit 历史，不改动 commit hash
> - commit 后仅做轻量复核，确认提交形态正确即可

---

### 门控 1：提交前 diff 审查（快速自检）

在 `git commit` 前，先执行 diff 审查以发现潜在 Bug：

```bash
# 查看已暂存的变更
git diff --staged
```

**审查要点：**
- [ ] **逻辑正确性**：条件判断、循环边界、算法实现是否正确
- [ ] **异常处理**：是否遗漏空值、越界、并发等异常情况
- [ ] **资源泄漏**：文件、连接、锁是否正确释放
- [ ] **副作用**：修改是否影响无关模块或功能
- [ ] **临时代码**：是否误提交测试代码、硬编码值、调试开关

> **原则**：只要 diff 中发现疑似 Bug，必须先确认再提交。宁可延迟提交，也不要把已知问题带入版本历史。

---

### 门控 2：提交前 code-review 正式审查（必选）

**diff 审查通过后、commit 之前，必须触发 `code-review` Skill 进行正式代码评审。**

**审查触发方式**：
```bash
# 获取本次暂存区的变更内容
git diff --staged --stat       # 查看修改了哪些文件
git diff --staged              # 查看完整 diff
```

**审查流程**：

```
git add 后、commit 前
    ↓
触发 code-review Skill 审查暂存区变更
    ↓
是否有阻塞问题（blocker）或建议项（suggestion）？
    │
    ├── 是 → 输出审查报告，向用户指出具体问题及影响
    │       └── 等待用户确认
    │           ├── 用户确认修改 → 修正代码 → 重新 git add → 重新 diff 审查 → 重新 code-review
    │           └── 阻塞问题不允许跳过；建议项可记录原因 → 继续
    │
    └── 否 → 审查通过 → 向用户确认提交信息 → 用户输入/确认后执行 git commit
```

**用户确认机制**：
- 若 code-review 发现 **阻塞问题（blocker）**：**必须修复，不允许跳过**
  - 用户选择"修复" → 进入修复流程 → 修复完成后重新 `git add` → 重新 diff 审查 → 重新触发 code-review
  - 阻塞问题未修复前，**禁止执行 `git commit`**
- 若 code-review 仅有 **建议项（suggestion）**：向用户展示建议，询问"是否采纳？"
  - 用户选择"采纳" → 优化代码 → 重新 `git add` → 重新触发 code-review
  - 用户选择"不采纳" → 记录原因 → 继续 `git commit`
- 若 code-review **通过（≥8.0 且无功能错误）**：告知用户审查通过，**询问并确认提交信息** → 用户输入/确认后执行 `git commit`

> **提交信息确认原则**：`git commit -m "..."` 中的提交信息必须来自用户输入或用户明确确认。禁止 AI 在未经用户确认的情况下代写提交信息并直接执行 commit。

> **原则**：阻塞问题（blocker）是代码质量的红线，与 SDD 流程一致——功能错误必须打回修复，架构/质量违规必须修正。不允许以"记录风险"为由绕过 blocker。

> **原则**：提交前审查与 SDD 流程中的阶段 6（代码审查）标准一致，使用相同的五维评分和阻塞/建议分类机制。

---

### 门控 3：提交后轻量复核

`git commit` 完成后，进行轻量复核，确保提交形态正确：

```bash
# 查看刚提交的变更
git show --stat HEAD           # 确认修改了预期的文件
git show HEAD                  # 确认 diff 内容正确
git log -1 --oneline           # 确认提交信息规范
```

**复核要点**：
- [ ] **提交信息**：是否符合约定式提交规范
- [ ] **文件范围**：是否只包含预期文件，无遗漏或混入
- [ ] **完整 diff**：与审查时看到的 `git diff --staged` 一致

**amend 后的审查策略**：
- 仅修改提交信息（`--message`）：无需重新触发 code-review
- 追加文件或修改代码内容（`--no-edit`）：视为新的代码变更，必须重新走门控 1 + 门控 2

> 如发现提交信息写错或有文件遗漏：使用 `git commit --amend` 修正（未 push 时）。

---

### 门控 4：推送前质量门控（必选）

**`git push` 之前，必须完成以下最终检查清单**：

#### 4.1 代码质量检查
- [ ] **code-review 已通过**：本次 commit 已完成 code-review 且评分 ≥ 8.0，无阻塞问题
- [ ] **编译/构建通过**：项目能在现有构建系统中编译成功（如为编译型语言）
- [ ] **测试通过**：单元测试 / 集成测试 / 手动自测至少通过一种
- [ ] **无调试代码**：确认没有遗留 `console.log`、`debugger`、`printf` 等临时调试语句

#### 4.2 提交规范检查
- [ ] **提交信息规范**：符合约定式提交（Conventional Commits）
- [ ] **单 commit 单意图**：一个 commit 只做一件事
- [ ] **敏感信息检查**：确认无密钥、密码、内网地址提交

#### 4.3 分支与远程检查
- [ ] **目标分支正确**：确认要 push 到的远程分支是预期分支
- [ ] **远程已更新**：执行 `git fetch` 确认远程是否有新提交，避免覆盖他人代码
- [ ] **冲突已解决**：如存在冲突，已解决并验证
- [ ] **force-push 审慎**：如必须使用 force-push，仅限个人分支且加 `--force-with-lease`

#### 4.4 审查状态追踪

推送前在审查日志中记录状态：

```yaml
# 审查状态记录示例
review:
  commit: "<commit-hash>"
  reviewer: "code-review Skill"
  score: "X.X / 10"
  blockers: []          # 阻塞问题清单，空表示无
  suggestions: []       # 建议项清单
  push-approved: true   # 质量门控是否通过
```

#### 4.5 用户最终确认（必选）

**即使门控 4.1 - 4.4 全部通过，执行 `git push` 前也必须经用户最终确认。**

```
质量门控全部通过
    ↓
向用户汇报门控结果（通过项清单 + 目标分支 + 命令预览）
    ↓
用户确认是否执行 push？
    │
    ├── 用户确认 → 执行 git push
    │
    └── 用户拒绝或要求修改 → 回到对应阶段处理
```

**汇报内容示例**：
```
推送前质量门控检查结果：
✅ code-review 已通过（评分 X.X / 10，无 blocker）
✅ 编译/测试通过
✅ 提交信息符合规范：feat(xxx): xxxxx
✅ 目标分支：origin/feature/xxx
✅ 远程已更新，无冲突

即将执行：git push origin feature/xxx
是否确认推送？
```

> **原则**：`git push` 是将代码永久写入团队协作历史的操作，必须由用户最终拍板。AI 禁止在未经用户明确确认的情况下自动执行 push。

**未通过质量门控的处理**：
- **code-review 未通过**：回到门控 2，修复后重新 commit
- **编译/测试失败**：回到开发阶段修复，重新 add → commit → 审查
- **发现敏感信息**：立即 `git reset --soft HEAD~1` 或 `git commit --amend` 修正

> **原则**：push 是代码进入团队协作的入口，质量门控是最后一道闸。未通过门控的代码禁止 push。

## 连接指南

### 入口
- 任何涉及 Git 操作的场景（提交、分支、合并、回滚、冲突解决）
- `spec-driven-agent` 阶段 4（代码执行）和阶段 5（编译验证）中涉及版本控制时隐式触发

### 出口
- diff 审查完成后 → 触发 **code-review** 进行提交前正式审查
- code-review 通过后 → 执行 `git commit`
- commit 后 → 轻量复核（可选）
- push 前 → 质量门控检查
- 质量门控通过后 → **向用户确认** → 用户同意后执行 `git push`
- 误操作恢复后 → 回到原工作流继续执行

## 参考资料

- 详细 Git 命令参考：见 [references/git-commands.md](references/git-commands.md)
- Git 误操作恢复参考：见 [references/git-recovery.md](references/git-recovery.md)
