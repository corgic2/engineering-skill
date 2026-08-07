---
name: engineeringworkflow-nosdd
description: |
  轻量项目工程化工作流（无 SDD 重型流程）。为任意语言项目提供基于知识库的开发能力：代码侧地图（project_wiki）、红线约束、脚本兜底验证、跨会话记忆（TECH_SPEC/subtasks/timeline）、工程经验库（experience/，提炼工序委托 team-experience-curator）。
  当用户请求涉及已启用本工作流的项目（存在 AIRunWorkDocs/project_wiki/overview.md 或 AIRunWorkDocs/red_lines/red_lines.yaml）时触发；也用于为新项目生成该工程骨架。
  触发场景：
  (1) 为项目初始化工程规范骨架；
  (2) 在项目中开发新需求 / 修复 bug / 增量迭代；
  (3) 需要定位改动点、更新 TECH_SPEC.md、执行构建验证或沉淀跨会话知识。
  注意：本 Skill 完全独立，不依赖 spec-driven-dev / spec-driven-agent。无强制确认关卡、无重型需求拆解仪式，默认自主跑完整流程，仅在真正歧义或触发红线时才停下来问用户。
---

# Engineering Workflow (No-SDD, Lightweight)

## 核心目标

让未参与过原始实现的新会话 AI，能在项目里像老同事一样独立跑完一个需求：靠 project_wiki 快速定位、靠红线守住质量底线、靠脚本验证构建、靠 TECH_SPEC 跨会话接力。

## 设计原则：轻量优先

- **自主执行**：默认一口气跑完「定位 → 实现 → 验证 → 沉淀」，不中途打断用户。
- **按需澄清**：只有需求存在多种技术解读且影响改动范围时，才向用户提问；能合理推断的一律推断并继续。
- **wiki 是核心资产**：流程可以极简，但 project_wiki / red_lines / TECH_SPEC 的构建与保鲜不打折。

## 轻量主循环

```
定位（五步定位法）→ 实现（先看后写）→ 验证（脚本构建 + 关键路径运行）→ 沉淀（TECH_SPEC + wiki 同步）
```

| 步骤 | 关键产出 | 完成判据 |
|------|---------|---------|
| 定位 | 文件 + 行号 + 调用链 | 五步定位法完成 |
| 实现 | 代码改动 | 自底向上，先看后写 |
| 验证 | `build_report.txt` + `result.md`/运行证据 | 退出码 0 + BUILD_PASS + sentinel 未过期，关键路径命中 |
| 沉淀 | 更新 `TECH_SPEC.md` / wiki + 经验条目（可选） | §3/§7/§8 同步，wiki 无漂移，经验提炼检查完成 |

复杂需求（改动跨多模块）先写一份简版任务清单到 `runtime/subtasks.json`（id/title/status/related_commit 即可），做完一项勾一项；简单需求直接干，不必建清单。

## 四类入口

- **新需求**：直接进主循环；需求模糊且影响范围时先花一轮对话澄清。
- **Bug 修复**：从定位开始，区分症状点与根因点；修完在 TECH_SPEC §7 补 BUG-N 记录。
- **增量迭代**：读 `runtime/TECH_SPEC.md` §0/§1/§3/§5/§7 + `subtasks.json`，5 分钟恢复现场后继续。
- **推倒重来**：清空当前需求相关改动，保留 TECH_SPEC §7 演进记录，重新走主循环。

## 何时停下来问用户

仅三种情况，其余一律自主决策：

1. **真实歧义**：需求有 2 种以上技术解读，且选错会导致返工。
2. **触发红线**：按红线模板报告并停下。
3. **破坏性操作**：删除大量代码、`git commit/push` 等不可逆操作前确认一次。

## 加载策略（Progressive Disclosure）

1. **项目治理文件优先**：项目根的 `AGENTS.md` / `constitution.md`（如存在）是最高优先级约束，先于本 Skill 通用规则加载；冲突时以项目治理文件为准。
2. 启动时加载：`SKILL.md` + `AIRunWorkDocs/project_wiki/overview.md` + `AIRunWorkDocs/red_lines/red_lines_critical.md`。
3. 命中模块后加载 `AIRunWorkDocs/project_wiki/<module>.md` 与对应红线；经验库必须先查 `AIRunWorkDocs/experience/README.md` 的 component 索引，仅在索引命中时加载其映射文件，**禁止按类名猜文件名**，未命中不加载。
4. 涉及 UI/DB/协议时加载对应语义桥 `project_wiki/semantic_bridge/`。

大文件（>10k 词）使用 grep 检索式，不直接全读。

## 知识库三级金字塔

- **L1 `AIRunWorkDocs/project_wiki/overview.md`**：模块名 + 一句话职责，<5KB，定位时默认 preload。
- **L2 `AIRunWorkDocs/project_wiki/<module>.md`**：顶部机器可读元数据 + 文件登记表，命中模块后加载。
- **L3 `AIRunWorkDocs/project_wiki/semantic_bridge/`**：需求术语↔代码、UI Token↔框架封装、DB/协议字段↔代码结构的精确映射。
- **经验层 `AIRunWorkDocs/experience/`**：按 component 分文件的结构化工程经验（反直觉约束、隐式机制、非常规坑），经 `experience/README.md` 索引命中后与 L2 同步加载；经验条目须带审计注释（镜头判定/垃圾过滤/事实校验结论）。

经验层分界规则（防重复建设）：

- 术语黑话映射 → 进 `semantic_bridge`，不入经验库；
- 结构/位置问题 → 优先更新 `project_wiki`（治本），经验只承载 wiki 表达不了的反直觉路径；
- 红线内容 → 不入经验库（已是启动加载的可发现知识）；
- 同一经验被 ≥2 个 session 踩中 → 升级为红线候选，交用户裁决；
- 经验的提炼、去重、合并、垃圾过滤一律委托 `team-experience-curator` skill 执行，本 Skill 不复制其规则。

每次代码改动后运行 `AIRunWorkDocs/tools/validate_constraints.py` 与 `AIRunWorkDocs/tools/check_project_wiki_stale.py`，任一不过阻断提交。

## 五步定位法

1. **意图消歧**：只读 `overview.md` + 用户原话，形成技术解读（有歧义才问用户）。
2. **模块定位**：读 `<module>.md`，输出 2-3 个候选文件路径。
3. **关键词搜索**：调用 `rg`/ctags 脚本，**不进 LLM**。
4. **调用链追踪**：读相关文件片段（~10K token），给出完整调用链。
5. **验证确认**：读函数实现（~5K token），确认最终改动点 + 理由。

## 红线机制

`AIRunWorkDocs/red_lines/red_lines.yaml` 是唯一真源，启动时加载 Critical（≤6 条）。

触发红线时必须按模板报告并停下：

```
⛔ 触发红线 RL-XX：<标题>
当前情形：<具体说明>
建议处理：<回退到哪个步骤 / 需要用户确认什么>
```

Critical 红线至少包括：

- RL-01：构建成功必须同时满足退出码 0、报告标记（如 BUILD_PASS）与 sentinel 未过期三重判据，自修复 ≤3 轮；引用既有构建结果（非本轮新跑）前必须先跑 `check_build_freshness.py` 校验时效。
- RL-02：未验证禁止归档——构建/运行验证通过前，禁止把任务标记为 DONE 或写入 TECH_SPEC §8。
- RL-03：先看后写/模仿已有，禁止发明项目里独此一家的新模式。
- RL-04：禁止硬编码样式/字段/连接串/密钥。
- RL-05：外部物料（TAPD/Figma/协议等）必须走专用通道，禁止通用 web_fetch 替代。
- RL-06：知识库漂移检测不过禁止提交。

项目实例化时允许按项目风险本地化 Critical 的内容与编号，但必须保持语义覆盖（先读后写、禁硬编码、构建判据、验证后归档、机器门禁），且与上述编号的映射关系须在项目 `red_lines.yaml` 中可溯源。

## 脚本兜底

LLM 只读结果 + 下决策；精确数值与幂等执行下沉脚本：

- `AIRunWorkDocs/tools/build_verify.sh`：按项目构建契约执行验证，产出 `build_report.txt` 与 sentinel。
- `AIRunWorkDocs/tools/validate_constraints.py`：仓库治理约束机器校验（必备文件、目录结构、章程合规），提交前第一道门禁；校验项由项目按 constitution/AGENTS 定制。
- `AIRunWorkDocs/tools/check_project_wiki_stale.py`：project_wiki 漂移检测，pre-commit 阻断。
- `AIRunWorkDocs/tools/check_build_freshness.py`：复用既有构建结果前校验 sentinel 未过期（sentinel mtime 不早于源码与构建登记文件的最新 mtime）。
- `AIRunWorkDocs/tools/new_tech_spec.py`：按模板渲染 `runtime/TECH_SPEC.md`。
- `AIRunWorkDocs/tools/render_commit_msg.py`：三段式 commit 渲染。

任何长跑命令成功以 sentinel 文件或目标文件更新为唯一判据，不信 stdout。

## 跨会话记忆三件套

- **`AIRunWorkDocs/runtime/TECH_SPEC.md`**：永久单一事实源，典型含 §0 进场自检/§1 功能边界/模块地图/不变式/演进事件/产物清单等；**章节集合与编号由项目裁剪，以项目 TECH_SPEC 实际目录为准**，不得凭本 Skill 的示例编号引用章节。
- **`AIRunWorkDocs/runtime/subtasks.json`**：跨会话台账，记录每个子需求状态与关联 commit（复杂需求才建）。
- **`AIRunWorkDocs/runtime/timeline.txt`**：会话内 start/human-correction/commit 流水。

新会话入场按项目 README 与 TECH_SPEC §0 指定的顺序扫描（模板默认 §0 → §1 → §3 → §5 → §7，项目裁剪章节后以其自身指引为准），目标 5 分钟恢复现场；随后按本次任务涉及模块，经 `experience/README.md` 索引加载对应经验条目，带项目语境进场。

## 初始化新项目

当用户要求"为项目初始化工程骨架"时：

1. 读取 `assets/` 下的模板。
2. 在项目根目录生成 `AIRunWorkDocs/`，包含：`docs/`、`project_wiki/`、`red_lines/`、`tools/`、`runtime/`、`agents/`、`experience/`（含 `experience/README.md` 索引模板，条目由沉淀步骤按需填充）。
3. 根据用户提供的模块清单填充 `AIRunWorkDocs/project_wiki/overview.md` 与 `<module>.md`。
4. 生成 `AIRunWorkDocs/red_lines/red_lines.yaml` 并派生 `red_lines_critical.md`。
5. 安装版本化 pre-commit hook：提交 `.githooks/pre-commit` 并执行 `git config core.hooksPath .githooks`（随仓库版本化、跨平台）；hook 按失败关闭策略依次调用 `AIRunWorkDocs/tools/validate_constraints.py` 与 `check_project_wiki_stale.py`。

语言相关细节通过 `--language` 参数注入：C++ 项目生成 CMake/Qt 专用工具与模板，其他语言生成通用占位符，由项目后续自行填充。

## 参考文档索引

- 步骤细则：`references/stage_locate.md`、`stage_implement.md`、`stage_verify.md`、`stage_archive.md`、`stage_commit.md`
- 入口流程：`references/workflow_new_feature.md`、`workflow_bug_fix.md`、`workflow_incremental.md`
- 模板：`references/tech_spec_template.md`
- 工具死角清单：`references/toolbox.md`
- 红线说明：`references/red_lines_guide.md`
- 完整走查案例：`references/example_cpp_qt.md`（C++/Qt 实例）、`references/example_generic.md`（通用实例）
