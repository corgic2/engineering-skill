---
name: engineering-workflow
description: |
  项目工程化需求开发工作流。为任意语言项目提供端到端需求开发能力：代码侧地图（project_wiki）、需求侧语义翻译、红线约束、脚本兜底验证、跨会话记忆（TECH_SPEC/subtasks/timeline）。
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

## 8 阶段流水线

严格顺序执行，子步骤统一采用「阶段·动作」命名：

```
设计稿收料 → 需求拆解 → 代码定位 → 编码实现 → 构建验证 → 运行验证 → 沉淀归档 → 提交收尾
```

| 阶段 | 输入 | 关键产出 | 退出标准 |
|------|------|---------|---------|
| 设计稿收料 | PRD/设计稿/协议/任务单链接 | 候选物料清单 | 每份物料来源走专用通道 |
| 需求拆解 | 物料 | 五列表格 + `subtasks.json` | 每项归宿明确，拦截点有依据 |
| 代码定位 | 需求项 | 文件 + 行号 + 调用链 | 五步定位法完成 |
| 编码实现 | 调用链 + 上下文 | 代码改动 | 自底向上，先看后写 |
| 构建验证 | 源码改动 | `build_report.txt` + sentinel | 退出码 0，自修复 ≤3 轮 |
| 运行验证 | 构建产物 | 运行日志/截图/`result.md` | 关键路径命中 |
| 沉淀归档 | git diff + 时间线 | 更新 `TECH_SPEC.md` | §7/§8/§9 同步 |
| 提交收尾 | 全部产物 | git commit + 分支 | `git log -1` hash 更新为据 |

## 四类入口

根据用户请求选择入口：

- **新需求**：从「设计稿收料」开始，新建 `AIRunWorkDocs/runtime/TECH_SPEC.md` 与 `subtasks.json`。
- **Bug 修复**：从「需求拆解」开始，复用现有 TECH_SPEC，新增 BUG-N 记录。
- **增量迭代**：从「代码定位」开始，读取 `AIRunWorkDocs/runtime/subtasks.json` 中 PENDING 条目继续。
- **推倒重来**：清空当前需求相关改动，保留 TECH_SPEC §7 演进记录，重新走完整流程。

## 加载策略（Progressive Disclosure）

按以下顺序加载，禁止一次性灌入全量代码：

1. 启动时加载：`SKILL.md` + `AIRunWorkDocs/project_wiki/overview.md` + `AIRunWorkDocs/red_lines/red_lines_critical.md`。
2. 进入阶段后加载对应 `references/stage_<name>.md` 与 `AIRunWorkDocs/red_lines/red_lines_by_stage/<stage>.md`。
3. 命中模块后加载 `AIRunWorkDocs/project_wiki/<module>.md`。
4. 涉及 UI/DB/协议时强制加载对应语义桥。

大文件（>10k 词）使用给定 grep 检索式，不直接全读。

## 知识库三级金字塔

- **L1 `AIRunWorkDocs/project_wiki/overview.md`**：模块名 + 一句话职责，<5KB，定位阶段默认 preload。
- **L2 `AIRunWorkDocs/project_wiki/<module>.md`**：顶部机器可读元数据 + 文件登记表，命中模块后加载。
- **L3 `AIRunWorkDocs/project_wiki/semantic_bridge/`**：需求术语↔代码、UI Token↔框架封装、DB/协议字段↔代码结构的精确映射。

每次代码改动后必须运行 `AIRunWorkDocs/tools/check_project_wiki_stale.py`，知识库漂移时阻断提交。

## 五步定位法

执行代码定位阶段时遵循：

1. **意图消歧**：只读 `overview.md` + 用户原话，输出 2-4 种技术解读。
2. **模块定位**：读 `<module>.md`，输出 2-3 个候选文件路径。
3. **关键词搜索**：调用 `rg`/ctags 脚本，**不进 LLM**。
4. **调用链追踪**：读相关文件片段（~10K token），给出完整调用链。
5. **验证确认**：读函数实现（~5K token），确认最终改动点 + 理由。

## 需求翻译五规则

拆解阶段必须执行：

1. **范围识别**：使用硬关键词表打标签，禁止 LLM 凭语义判断。
2. **归宿校验**：每张设计稿/每项物料必须归为「载体/状态变体/纯参考」三类之一，禁止"参考图"垃圾桶。
3. **拦截点清单**：任何"X 触发 Y"必须有文档/设计稿/用户原话依据，禁止语义联想扩大范围。
4. **领域联想**：用 5 维搜索矩阵（平台 API/功能语义/命名习惯/协议代理/通知回调）扩展代码搜索词。
5. **翻译产物**：输出五列表格 + `subtasks.json`（id/title/type/data_source/figma_node/depends_on/status/current_stage/related_commit）。

## 红线机制

`AIRunWorkDocs/red_lines/red_lines.yaml` 是唯一真源，启动时加载 Critical（≤6 条），按阶段加载 Standard。

触发红线时必须按模板报告并停下：

```
⛔ 触发红线 RL-XX：<标题>
当前情形：<具体说明>
建议处理：<回退到哪个步骤 / 需要用户确认什么>
```

Critical 红线至少包括：

- RL-01：构建退出码 0 为唯一判据，自修复 ≤3 轮。
- RL-02：未按阶段执行禁止，后一阶段输入必须等于前一阶段产出。
- RL-03：先看后写/模仿已有，禁止发明项目里独此一家的新模式。
- RL-04：禁止硬编码样式/字段/连接串/密钥。
- RL-05：多源物料必须走专用通道，禁止通用 web_fetch 替代。
- RL-06：知识库漂移检测不过禁止提交。

项目实例化时允许按项目风险本地化 Critical 的内容与编号（如合并、拆分或替换为项目特有基线），但必须保持语义覆盖（先读后写、禁硬编码、物料专用通道、构建判据、禁跳阶段、机器门禁），且与上述 SKILL 编号的映射关系须在项目 `red_lines.yaml` 中可溯源。

## 脚本兜底

LLM 只读结果 + 下决策；精确数值与幂等执行下沉脚本：

- `AIRunWorkDocs/tools/build_verify.sh`：按项目构建契约执行验证（单平台直接构建，多平台由脚本显式分发），产出 `build_report.txt` 与 sentinel。
- `AIRunWorkDocs/tools/check_project_wiki_stale.py`：project_wiki 漂移检测（实现可为 SHA 基线缓存或 staged 同步校验），pre-commit 阻断。
- `AIRunWorkDocs/tools/new_tech_spec.py`：按模板渲染 `runtime/TECH_SPEC.md`。
- `AIRunWorkDocs/tools/render_commit_msg.py`：三段式 commit 渲染。

任何长跑命令成功以 sentinel 文件或目标文件更新为唯一判据，不信 stdout。sentinel 的时效性由项目侧脚本（如 `check_build_freshness.py`）校验，防止引用过期构建结果。

## 跨会话记忆三件套

- **`AIRunWorkDocs/runtime/TECH_SPEC.md`**：永久单一事实源，含 §0 自检/§1 边界/§3 模块地图/§5 不变式/§7 演进/§8 产物/§9 版本。
- **`AIRunWorkDocs/runtime/subtasks.json`**：跨会话台账，记录每个子需求状态、当前阶段、关联 commit。
- **`AIRunWorkDocs/runtime/timeline.txt`**：会话内 start/human-correction/commit 流水。

新会话入场扫描顺序固定为 §0 → §1 → §3 → §5 → §7，目标 5 分钟恢复现场。

## 初始化新项目

当用户要求"为项目初始化工程骨架"时：

1. 读取 `assets/` 下的模板。
2. 在项目根目录生成 `AIRunWorkDocs/`，包含：`docs/`、`project_wiki/`、`red_lines/`、`tools/`、`runtime/`、`agents/`。
3. 根据用户提供的模块清单填充 `AIRunWorkDocs/project_wiki/overview.md` 与 `<module>.md`。
4. 生成 `AIRunWorkDocs/red_lines/red_lines.yaml` 并派生 `red_lines_critical.md` 与 `red_lines_by_stage/`。
5. 安装 pre-commit hook 调用 `AIRunWorkDocs/tools/check_project_wiki_stale.py`。

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
