---
name: engineering-workflow
description: |
  项目工程化需求开发工作流。为任意语言项目提供端到端需求开发能力：代码侧地图（project_wiki）、需求侧语义翻译、红线约束（含候选挖掘/隔离区/衰减的生命周期）、脚本兜底验证、跨会话记忆（TECH_SPEC/subtasks/timeline + handoff 结构化交接块）、分层记忆与 SDD 蒸馏（工作层→回合层 digest→长期层）、工程经验库（experience/，提炼工序委托 team-experience-curator）。
  当用户请求涉及已启用本工作流的项目（存在 AIRunWorkDocs/project_wiki/overview.md 或 AIRunWorkDocs/red_lines/red_lines.yaml）时触发；也用于为新项目生成该工程骨架。
  触发场景：
  (1) 为项目初始化工程规范骨架；
  (2) 在项目中开发新需求 / 修复 bug / 增量迭代 / 推倒重来；
  (3) 需要定位改动点、生成/更新 TECH_SPEC.md、执行构建验证或沉淀跨会话知识。
  注意：本 Skill 替代 spec-driven-agent 在具体项目上的设计与执行角色，但仍受 spec-driven-dev 总入口的质量门约束。语言相关细节（代码风格、构建命令、语义桥）由项目级 agents/ 与 semantic_bridge/ 承载。
---

# Engineering Workflow

## 核心目标

让未参与过原始实现的新会话 AI，能在项目里像老同事一样按工程规范独立跑完一个需求，且构建可验证、知识可跨会话接力。

## 与 spec-driven-dev 的关系

- `spec-driven-dev` 是总入口与质量网关：负责需求澄清、用户确认、最终验收。
- 本 Skill 负责项目内厚执行：项目地图、语义翻译、红线、脚本验证、跨会话记忆。
- 当项目存在 `AIRunWorkDocs/project_wiki/overview.md` 或 `AIRunWorkDocs/red_lines/red_lines.yaml` 时，阶段 2（方案设计）和阶段 4（代码执行）优先调用本 Skill。

**任务分级对接（S/M/L）**：spec-driven-dev 的任务分级在本工作流中同样生效，映射如下：

| 档位 | 流水线执行 | 产物 |
|---|---|---|
| S 小修 | 免独立设计文档，简版确认单 + subtasks 即设计；pre_review 并入 review 环节 | TECH_SPEC 增量从简 |
| M 标准 | 完整流水线 | TECH_SPEC/subtasks 标准更新 |
| L 重型 | 完整流水线 + 评审团（有 rubric 时） | 完整更新，复杂时可拆出 test-cases |

典型对应：Bug 修复多为 S/M，推倒重来必为 L。**档位差异是 spec-driven-dev 授权的合法路径，不触发 RL-02（禁跳阶段）**；拿不准从高不就低，范围扩大必须升档。

## 8 阶段流水线

严格顺序执行，子步骤统一采用「阶段·动作」命名：

> 阶段集可扩展：接入 SDD 的项目通常在「编码实现」前后增加**设计（design）**、**预自检（pre_review）**与**审查（review）**环节，`red_lines_by_stage/` 的文件集合随之扩展（如 `design.md`）。以项目 `agents/pipeline.md` 的阶段定义为准，本表为最小基线。

```
设计稿收料 → 需求拆解 → 代码定位 → 编码实现 → 构建验证 → 运行验证 → 沉淀归档 → 提交收尾
```

| 阶段 | 输入 | 关键产出 | 退出标准 |
|------|------|---------|---------|
| 设计稿收料 | PRD/设计稿/协议/任务单链接 | 候选物料清单 | 每份物料来源走专用通道 |
| 需求拆解 | 物料 | 五列表格 + `subtasks.json` | 每项归宿明确，拦截点有依据 |
| 代码定位 | 需求项 | 文件 + 行号 + 调用链 | 五步定位法完成 |
| 编码实现 | 调用链 + 上下文 | 代码改动 | 自底向上，先看后写 |
| 构建验证 | 源码改动 | `build_report.txt` + sentinel | 退出码 0 + BUILD_PASS + sentinel 未过期，自修复 ≤3 轮 |
| 运行验证 | 构建产物 | 运行日志/截图/`result.md` | 关键路径命中 |
| 沉淀归档 | git diff + 时间线 | 更新 `TECH_SPEC.md` + SDD 蒸馏（digest + index 登记）+ 经验条目（可选） | §7/§8/§9 同步，蒸馏完成，经验提炼检查完成 |
| 提交收尾 | 全部产物 | git commit + 分支 | `git log -1` hash 更新为据 |

## 四类入口

根据用户请求选择入口：

- **新需求**：从「设计稿收料」开始，新建 `AIRunWorkDocs/runtime/TECH_SPEC.md` 与 `subtasks.json`。
- **Bug 修复**：从「需求拆解」开始，复用现有 TECH_SPEC，新增 BUG-N 记录。
- **增量迭代**：从「代码定位」开始，读取 `AIRunWorkDocs/runtime/subtasks.json` 中 PENDING 条目继续。
- **推倒重来**：清空当前需求相关改动，保留 TECH_SPEC §7 演进记录，重新走完整流程。

## 加载策略（Progressive Disclosure）

按以下顺序加载，禁止一次性灌入全量代码：

0. **项目治理文件优先**：项目根的 `AGENTS.md` / `constitution.md`（如存在）是最高优先级约束，先于本 Skill 通用规则加载；冲突时以项目治理文件为准。
1. 启动时加载：`SKILL.md` + `AIRunWorkDocs/project_wiki/overview.md` + `AIRunWorkDocs/red_lines/red_lines_critical.md`。
2. 进入阶段后加载对应 `references/stage_<name>.md` 与 `AIRunWorkDocs/red_lines/red_lines_by_stage/<stage>.md`。
3. 命中模块后加载 `AIRunWorkDocs/project_wiki/<module>.md`；经验库必须先查 `AIRunWorkDocs/experience/README.md` 的 component 索引，仅在索引命中时加载其映射文件，**禁止按类名猜文件名**，未命中不加载。
4. 涉及 UI/DB/协议时强制加载对应语义桥。
5. **wiki 两趟扫描**：wiki 模块页顶部携带机器可读元数据（front-matter 或 `root_dirs` 注释块，至少含覆盖目录/关键符号/加载成本/最近校验时间）。第一趟只读各页元数据，决定加载哪几页正文；第二趟按需加载正文与图谱邻域。每阶段设 token 预算，超预算必须裁剪或请示，禁止默认全量灌入。
6. **SDD 只读索引**：项目存在 `sdd_index.yaml` 时，恢复现场只读索引与命中需求的 `digest.md`，禁止扫描 SDD 原文目录；回溯冷存储原文（`.archive/`）仅限 digest 明确引用时。

大文件（>10k 词）使用给定 grep 检索式，不直接全读。

## 知识库三级金字塔

- **L1 `AIRunWorkDocs/project_wiki/overview.md`**：模块名 + 一句话职责，<5KB，定位阶段默认 preload。
- **L2 `AIRunWorkDocs/project_wiki/<module>.md`**：顶部机器可读元数据 + 文件登记表，命中模块后加载。
- **L3 `AIRunWorkDocs/project_wiki/semantic_bridge/`**：需求术语↔代码、UI Token↔框架封装、DB/协议字段↔代码结构的精确映射。
- **经验层 `AIRunWorkDocs/experience/`**：按 component 分文件的结构化工程经验（反直觉约束、隐式机制、非常规坑），经 `experience/README.md` 索引命中后与 L2 同步加载；经验条目须带审计注释（镜头判定/垃圾过滤/事实校验结论）。

经验层分界规则（防重复建设）：

- 术语黑话映射 → 进 `semantic_bridge`，不入经验库；
- 结构/位置问题 → 优先更新 `project_wiki`（治本），经验只承载 wiki 表达不了的反直觉路径；
- 红线内容 → 不入经验库（已是启动加载的可发现知识）；
- 同一经验被 ≥2 个 session 踩中 → 升级为红线候选，交用户裁决；
- 经验的提炼、去重、合并、垃圾过滤一律委托 `team-experience-curator` skill 执行，本 Skill 不复制其规则。

每次代码改动后必须运行 `AIRunWorkDocs/tools/validate_constraints.py` 与 `AIRunWorkDocs/tools/check_project_wiki_stale.py`，任一不过阻断提交。

## 分层记忆与 SDD 蒸馏

记忆按半衰期分三层，各回答一个问题，禁止混写：

| 层 | 载体 | 回答 | 生命周期 |
|---|---|---|---|
| L0 工作层 | `runtime/timeline.txt`、会话内 worklog | 当时经历了什么 | 会话级，验收后可弃 |
| L1 回合层 | `Agentic/sdd/<需求>/digest.md` + `sdd_index.yaml` | 这轮需求做了什么、结果如何 | 一页摘要；原文入 `.archive/` 冷存储 |
| L2 长期层 | `project_wiki/`、`decisions/`（ADR）、`red_lines/`、`experience/` | 现在是什么样 / 为什么 / 不许做什么 / 别踩什么坑 | 长期，只留结论 |

**蒸馏工序**（沉淀归档阶段必做，HK-2 确认点）：

1. 从本轮 SDD 全套文档中只抽四类产物：有理由的决策 → `decisions/` 一段式 ADR；被违反或差点违反的约定 → 红线候选（进隔离区，见「红线生命周期」）；模块地图变化 → project_wiki 增量；反直觉坑 → experience（委托 team-experience-curator）。
2. 需求目录压缩为一页 `digest.md`（目标/关键决策引用/结果/遗留项，≤2KB），原文移入 `Agentic/sdd/.archive/`；在 `sdd_index.yaml` 登记（req、status、digest 路径、关联 ADR/经验 ID、流程完整度标记）。蒸馏时若治理豁免清单等文件按目录名引用该需求，必须同步改写引用，禁止断链。
3. 蒸馏后索引与 digest 是后续会话唯一允许读取的 SDD 内容。蒸馏是有损压缩，digest 必须保留指向冷存储原文的引用。

**防囤积门禁**：骨架与记忆文件受字节预算机器约束（基线：overview ≤5KB / TECH_SPEC ≤16KB / timeline ≤4KB / digest ≤2KB / ADR 一段式），由 `validate_constraints.py` 执行。做骨架精简时遵循三层分流——当前事实留骨架、流水留 Git/SDD、根因进经验库；禁止把反直觉根因连同流水一起删除。

## 五步定位法

执行代码定位阶段时遵循：

1. **意图消歧**：只读 `overview.md` + 用户原话，输出 2-4 种技术解读。
2. **模块定位**：读 `<module>.md`，输出 2-3 个候选文件路径。
3. **关键词搜索**：项目存在 codegraph 索引（`.codegraph/`）时优先 `codegraph query <symbol>`；否则调用 `rg`/ctags 脚本，**不进 LLM**。
4. **调用链追踪**：有索引时用 `codegraph callers/callees → impact --depth 2` 取静态调用链与影响面，再读相关文件片段（~10K token）确认。注意：图谱只覆盖静态结构；Qt 信号/槽、事件、回调等**运行时连接图谱不可见**，其注册-触发-注销链路必须以 wiki/经验库记录为准，不得因图谱无记录而判定不存在。
5. **验证确认**：读函数实现（~5K token），确认最终改动点 + 理由。

## 需求翻译五规则

拆解阶段必须执行：

1. **范围识别**：使用硬关键词表打标签，禁止 LLM 凭语义判断。
2. **归宿校验**：每张设计稿/每项物料必须归为「载体/状态变体/纯参考」三类之一，禁止"参考图"垃圾桶。
3. **拦截点清单**：任何"X 触发 Y"必须有文档/设计稿/用户原话依据，禁止语义联想扩大范围。
4. **领域联想**：用 5 维搜索矩阵（平台 API/功能语义/命名习惯/协议代理/通知回调）扩展代码搜索词。
5. **翻译产物**：输出五列表格 + `subtasks.json`（id/title/type/data_source/figma_node/depends_on/status/current_stage/related_commit）。

## 角色治理（可选模式）

部分项目会在本工作流之上启用角色治理（是否启用、角色集如何划分，以项目 `AGENTS.md` 为准）。启用时的通用规则：

- 动手前必须先声明本次角色并**经用户明确确认**（模型不得自行确认），声明与确认记录写入项目 SDD 产物目录的状态文件（如 `Agentic/sdd/<需求>/workflow-state.md` 的 `roles` 段，含 `user_confirmed` 标记）。
- 每个角色有明确的允许修改范围；发现任务超出自身角色范围必须停止并报告，不得越权修改。
- 角色可由同一执行者兼任，但每个角色声明都须经用户确认；roles 记录用于追溯。

一种源自实践的典型三分法（项目可自定义角色集与范围）：

| 角色 | 负责阶段 | 允许修改范围 |
|------|---------|-------------|
| 设计 | 需求澄清、spec-plan/tasks、TECH_SPEC/subtasks 设计产物 | 设计文档与状态文件设计字段 |
| 编码 | 按已确认 plan 执行、预自检、审查、验证 | plan 列明的业务文件 + tasks 状态/执行记录 |
| 更新骨架 | 代码地图与跨会话记忆同步 | `project_wiki/`、`runtime/` |

顺序依赖：设计 → 编码 → 更新骨架；无已确认设计产物禁止编码，验收通过前不得同步骨架。

## 设计阶段强制自检清单

设计产物（spec-plan/tasks 或 TECH_SPEC/subtasks）交付前逐条自检，违反任一条视为设计未完成。清单从真实项目评审复盘中泛化而来，**项目可按领域增删**；以下为通用基线：

1. **需求邻域确认**：主路径之外的行为（非主路径状态语义、删除既有功能的动机与影响、默认值语义）必须有用户原话级证据，设计推断不得冒充"已确认"。
2. **框架行为取证**：涉及"回调/信号触发时序、默认行为、自动分配"等框架行为时，必须引用官方文档或既有代码证据，不得凭经验假设；"碰巧对上"一律视为未验证。
3. **复用三问**：写"复用 X"前回答——可见性（文件私有/公共）？调用场景数？签名/上下文适配？任一存疑即显式化取舍，不留"可选复用"含糊措辞。
4. **修订传播复扫**：任何新决策落地后，全文档 grep 旧编号/旧决策名/矛盾措辞，各设计产物一次扫净同步。

UI 类项目追加两条：

5. **风险导向测试**：像素探针、信号副作用回归、几何断言、语言切换等回归手段默认必选；新增纯逻辑必有直测，禁"可选"降级。
6. **几何逐层核算**：尺寸预算按布局树逐层计算（宿主 margin → 内层布局 margin → 控件 padding），并配几何断言兜底，禁估算口径。

## 红线机制

`AIRunWorkDocs/red_lines/red_lines.yaml` 是唯一真源，启动时加载 Critical（≤6 条），按阶段加载 Standard。

触发红线时必须按模板报告并停下：

```
⛔ 触发红线 RL-XX：<标题>
当前情形：<具体说明>
建议处理：<回退到哪个步骤 / 需要用户确认什么>
```

Critical 红线至少包括：

- RL-01：构建成功必须同时满足退出码 0、报告标记（如 BUILD_PASS）与 sentinel 未过期三重判据，自修复 ≤3 轮；引用既有构建结果（非本轮新跑）前必须先跑 `check_build_freshness.py` 校验时效。
- RL-02：未按阶段执行禁止，后一阶段输入必须等于前一阶段产出。
- RL-03：先看后写/模仿已有，禁止发明项目里独此一家的新模式。
- RL-04：禁止硬编码样式/字段/连接串/密钥。
- RL-05：多源物料必须走专用通道，禁止通用 web_fetch 替代。
- RL-06：知识库漂移检测不过禁止提交。

项目实例化时允许按项目风险本地化 Critical 的内容与编号（如合并、拆分或替换为项目特有基线），但必须保持语义覆盖（先读后写、禁硬编码、物料专用通道、构建判据、禁跳阶段、机器门禁），且与上述 SKILL 编号的映射关系须在项目 `red_lines.yaml` 中可溯源。

### 红线生命周期（候选挖掘、隔离区与衰减）

红线不再只靠人工提出与复盘，流转管道：

1. **挖掘**：复盘/归档时把 review 报告的阻塞问题与已处理过程问题、timeline 用户纠正、验收整改记录规范化为 `violations.jsonl`；同一 pattern 累计 ≥2 次 → 起草候选红线写入 `red_lines_candidates.yaml`（status: proposed）。单次违规只进经验库，不进红线。
2. **可机器化分级**：每条候选必须归类——脚本可执行（生成检查脚本进 pre-commit）/ 清单项（进对应阶段审查清单）/ 建议级（只进经验库，不配当门禁）。
3. **隔离区**：候选先 probation（warn-only 不阻断），统计命中数与误报数；误报高自动降级淘汰，表现干净由用户在 HK 关卡裁决晋升正式红线。隔离区文件结构对齐治理豁免清单模式（owner / reason / user_confirmed），挖掘时必须跳过已被豁免的存量记录。
4. **衰减**：正式红线记录命中数，连续 N 个 session 零命中 → 标记移除候选交用户裁决。规则囤积与文档囤积同为负资产，门禁清单无限变长本身就是上下文污染。

## 脚本兜底

LLM 只读结果 + 下决策；精确数值与幂等执行下沉脚本：

- `AIRunWorkDocs/tools/build_verify.sh`：按项目构建契约执行验证（单平台直接构建，多平台由脚本显式分发），产出 `build_report.txt` 与 sentinel。
- `AIRunWorkDocs/tools/validate_constraints.py`：仓库治理约束机器校验（必备文件、目录结构、章程合规），提交前第一道门禁；校验项由项目按 constitution/AGENTS 定制。
- `AIRunWorkDocs/tools/check_project_wiki_stale.py`：project_wiki 漂移检测（实现可为 SHA 基线缓存或 staged 同步校验），pre-commit 阻断。
- `AIRunWorkDocs/tools/check_build_freshness.py`：复用既有构建结果前校验 sentinel 未过期（sentinel mtime 不早于源码与构建登记文件的最新 mtime）。
- `AIRunWorkDocs/tools/new_tech_spec.py`：按模板渲染 `runtime/TECH_SPEC.md`。
- `AIRunWorkDocs/tools/render_commit_msg.py`：三段式 commit 渲染。
- `AIRunWorkDocs/tools/validate_handoff.py`：workflow-state 内嵌 handoff 块 schema 校验（context_manifest / decisions.trust / open_items 齐全性），纳入提交门禁。
- `AIRunWorkDocs/tools/distill_sdd.py`：SDD 需求目录蒸馏（生成 digest.md、登记 sdd_index.yaml、原文移入 .archive/），存量批处理与增量单需求两用。

任何长跑命令成功以 sentinel 文件或目标文件更新为唯一判据，不信 stdout。sentinel 的时效性由项目侧脚本（如 `check_build_freshness.py`）校验，防止引用过期构建结果。

## 跨会话记忆三件套

- **`AIRunWorkDocs/runtime/TECH_SPEC.md`**：永久单一事实源，典型含 §0 进场自检/§1 功能边界/模块地图/不变式/演进事件/产物清单等；**章节集合与编号由项目裁剪，以项目 TECH_SPEC 实际目录为准**，不得凭本 Skill 的示例编号引用章节。
- **`AIRunWorkDocs/runtime/subtasks.json`**：跨会话台账，记录每个子需求状态、当前阶段、关联 commit。
- **`AIRunWorkDocs/runtime/timeline.txt`**：会话内 start/human-correction/commit 流水。

新会话入场按项目 README 与 TECH_SPEC §0 指定的顺序扫描（模板默认 §0 → §1 → §3 → §5 → §7，项目裁剪章节后以其自身指引为准），目标 5 分钟恢复现场；随后按本次任务涉及模块，经 `experience/README.md` 索引加载对应经验条目，带项目语境进场。

**结构化交接块（handoff）**：需求状态文件（workflow-state.md）内嵌 `handoff:` YAML 块作为机器真源，自然语言 notes 只作人类摘要、不再承担状态同步职责。字段至少含：

- `context_manifest`：恢复现场的确定性取件单（`preload` / `on_demand` / `skip` / `budget_tokens`）。跨会话或高低成本模型接力时，接力方只读 manifest 指定文件，不自行猜测现场。
- `decisions[].trust`：每条已决约束标注 `user_confirmed` / `ai_generated` / `stale`；接力方不得重开 `user_confirmed` 决策，`ai_generated` 允许质疑。
- `open_items[]`：未完成项清单（blocker / todo / question + owner）。

schema 由 `AIRunWorkDocs/tools/validate_handoff.py` 校验，纳入提交门禁。

## 初始化新项目

当用户要求"为项目初始化工程骨架"时：

1. 读取 `assets/` 下的模板。
2. 在项目根目录生成 `AIRunWorkDocs/`，包含：`docs/`、`project_wiki/`、`red_lines/`（含 `red_lines_candidates.yaml` 隔离区）、`tools/`、`runtime/`、`agents/`、`experience/`（含 `experience/README.md` 索引模板，条目由沉淀归档阶段按需填充）、`decisions/`（ADR 一段式条目）、`quality/`（`rubric.yaml` 锚定评审标尺 + `calibration.yaml` 校准记录）。
3. 根据用户提供的模块清单填充 `AIRunWorkDocs/project_wiki/overview.md` 与 `<module>.md`。
4. 生成 `AIRunWorkDocs/red_lines/red_lines.yaml` 并派生 `red_lines_critical.md` 与 `red_lines_by_stage/`。
5. 安装版本化 pre-commit hook：提交 `.githooks/pre-commit` 并执行 `git config core.hooksPath .githooks`（随仓库版本化、跨平台）；hook 按失败关闭策略依次调用 `AIRunWorkDocs/tools/validate_constraints.py` 与 `check_project_wiki_stale.py`。

语言相关细节通过 `--language` 参数注入：C++ 项目生成 CMake/Qt 专用工具与模板，其他语言生成通用占位符，由项目后续自行填充。

## 硬关卡 HK

自动化与可控性的平衡点：

- **HK-0 现场快报**：接力入口进入后，先确认当前进度/改哪个子需求。
- **HK-1 拆解确认**：`subtasks.json` 翻译完成后，等待用户"确认/改 xxx"。
- **HK-2 沉淀确认**：`TECH_SPEC.md` 落盘前，等待用户"沉淀 ok"。
- **HK-3 commit 确认**：`git commit` 前，等待用户"提交/go"。

## 参考文档索引

- 阶段细则：`references/stage_collect.md`、`stage_breakdown.md`、`stage_locate.md`、`stage_implement.md`、`stage_verify.md`、`stage_archive.md`、`stage_commit.md`
- 入口流程：`references/workflow_new_feature.md`、`workflow_bug_fix.md`、`workflow_incremental.md`
- 模板：`references/tech_spec_template.md`
- 工具死角清单：`references/toolbox.md`
- 红线说明：`references/red_lines_guide.md`
- 完整走查案例：`references/example_cpp_qt.md`（C++/Qt 实例）、`references/example_generic.md`（通用实例）
