---
name: team-experience-curator
description: 团队工程经验提炼与经验库治理 Skill。把 AI 编码 session 中"踩坑 → 纠偏 → 解决"的过程，提炼为结构化、低噪声、可复用的团队工程经验，维护一个随项目生长的仓库内 markdown 经验库，让后续 session 的 AI 带着项目语境进场。当且仅当以下场景时触发：(1) 用户在 session 中纠正了 AI 的实现或判断，且纠正涉及项目隐性约束；(2) 用户明确要求"沉淀/记录这次经验""更新经验库"；(3) 排查完一个反直觉 bug 之后；(4) 用户要求审查、整理、去重现有经验库。不满足触发条件时禁止主动提炼——不加过滤的自动提取是垃圾放大器。注意：本 Skill 是 agent 工作流而非自动化系统，所有判断由 AI 在会话内完成。
---

# Team Experience Curator

## 定位

把 session 中"踩坑 → 纠偏 → 解决"的过程提炼为**结构化、低噪声、可复用**的团队工程经验，写入项目仓库内的 markdown 经验库。后续 session 的 AI 通过阅读经验库带着项目语境进场。

本 Skill 是 agent 工作流：所有判断由 AI 在会话内完成，经验库就是仓库内的 markdown 文件，无外部系统依赖。

## 经验库约定

- 默认位置：项目仓库内 `docs/team-experiences/`；若项目已有约定的经验文档位置，沿用项目约定。
- 组织方式：按 `component`/`scope` 分文件（如 `network.md`、`build-system.md`），每条经验为文件内一个条目。
- 条目格式：**写入前必须读取** [references/experience-schema.md](references/experience-schema.md) 获取字段定义、正反例与审计说明格式。

## 工作流

按顺序执行，每步的详细规则在 references 中，SKILL.md 只保留骨架：

### 1. 触发检查

对照 description 中的四个触发场景。不满足任何一条 → 不做提炼，继续当前任务。不要"顺手"自动提炼。

### 2. 证据定位

回到对话历史，定位与本次经验相关的原始轮次：用户的纠正原话、报错日志、验证结果、最终确认。证据必须可引用到具体轮次，凭印象概括的内容不算证据。

### 3. 候选提炼（三镜头判定）

用核心判定标准（见下节）筛候选。三镜头都不命中 → 默认不入库，本轮工作流结束。

### 4. 垃圾过滤

读取 [references/garbage-patterns.md](references/garbage-patterns.md)，逐条对照九类垃圾特征，命中任一类 → 排除。多个候选时逐个独立判断。

### 5. 事实校验

经验声称某 API/方法/类/配置项存在时，必须在代码库中实际检索验证（Grep/Glob/读文件）。验证不通过 → 拦截；无法验证 → 在条目中标记「存疑」并说明原因。**不得放行未验证的技术事实。**

### 6. 结构化

按 experience-schema.md 的字段模板写成条目，并附可审计说明。

### 7. 治理合并

读取 [references/governance-rules.md](references/governance-rules.md)，依次执行：
- **Review**：默认保留、定向过滤，宁可放过边缘经验，不可误杀好经验；
- **Dedup**：候选集内去重，宁严勿宽，禁止桥接合并；
- **Merge**：与历史经验库合并，四动作 create / update / skip / contradict，无唯一目标时默认回退 create。

### 8. 写入与汇报

写入经验库文件，向用户汇报：新增/更新/跳过了哪些条目、各自原因、拦截了哪些候选及命中的垃圾类别。

## 核心判定标准

一条信息是"经验"的**唯一标准**：被召回后能让 Agent 产生正向行为变更。

合格经验必须**同时满足**：来自真实对话、有证据支撑、项目特有、非通用常识、可复用，且"不容易直接发现"。

按认知障碍分三个镜头，候选须**命中至少其一**：

| 镜头 | 不可发现性 | 典型内容 |
|---|---|---|
| 黑话镜头 | 语义不可发现 | 内部黑话、缩写、代称的显式映射 |
| 索引镜头 | 位置不可发现 | 能力入口、关键类、目录不在直觉路径上 |
| 逻辑镜头 | 行为不可发现 | 反直觉的工程约束、隐式机制、常规推理推不出的坑 |

三镜头都不命中 → 默认不入库。

## references 读取时机

| 文件 | 何时读取 |
|---|---|
| [references/experience-schema.md](references/experience-schema.md) | 第 6 步结构化时（字段定义、正反例、审计格式） |
| [references/garbage-patterns.md](references/garbage-patterns.md) | 第 4 步垃圾过滤时（九类硬性排除规则） |
| [references/governance-rules.md](references/governance-rules.md) | 第 7 步 Review/Dedup/Merge 时，以及用户要求整理经验库时 |

## 迭代机制

当用户反馈经验质量问题时，按"错例分析 → 规则抽象 → 评测验证"闭环处理：

1. **错例分析**：定位错例命中了哪一类垃圾特征，或在 Review / Dedup / Merge 哪一层失守；
2. **规则抽象**：把教训固化为对应 references 文件中的规则更新（修改本 Skill 文件，而非只口头总结）；
3. **评测验证**：用历史样本回归验证新规则——修正的错例被拦截，且原有合格经验不被误杀。

评估时 Recall / Precision / Garbage Rate 三个指标一起看，禁止只优化单一指标（例如靠收紧规则把 Garbage Rate 降到 0 但 Recall 崩掉，是失败的迭代）。
