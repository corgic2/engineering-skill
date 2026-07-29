# 常见根因与 Skill 改进模式速查

复盘时按根因类型快速定位改进目标。

## 需求阶段失效

| 现象 | 根因 | 改进动作 |
|------|------|----------|
| "我以为你知道要兼容旧数据" | 漏问数据兼容性 | requirement-clarifier/clarification-template.md：增加"数据兼容性"追问项 |
| "加 Redis"但实际要的是缓存 | 把解决方案当需求 | requirement-clarifier/SKILL.md：在案例区补充"Redis vs 缓存"的典型误判 |
| "用户说随便做做，结果要求很高" | 对"随便"的隐含需求未挖掘 | requirement-clarifier/SKILL.md：增加"用户说随便时的追问清单" |
| 需求确认后用户又补充了 3 条 | 一次澄清不够，需要多轮 | spec-driven-agent/SKILL.md：连接指南增加"需求有新增时回到 requirement-clarifier" |

## 设计阶段失效

| 现象 | 根因 | 改进动作 |
|------|------|----------|
| 并发场景出 bug | plan 没考虑并发 | spec-driven-agent/SKILL.md：自评维度"边界完整"权重提高，增加并发检查提示 |
| 改完发现回退不了 | plan 没写回退方案 | spec-driven-agent/references/sdd-templates.md：plan.md 模板增加"风险评估/回退方案"栏 |
| 明明有漏洞，自评 9 分 | 自评标准不具体 | spec-driven-agent/SKILL.md：在评分参考中补充该类漏洞的典型扣分示例 |
| 验收时发现标准太模糊 | 验收标准用"优化""完善" | spec-driven-agent/SKILL.md：在"可验证性"扣分项中增加典型案例 |

## 执行阶段失效

| 现象 | 根因 | 改进动作 |
|------|------|----------|
| 代码改了 plan 之外的文件 | 执行偏离设计 | spec-driven-agent/references/sdd-templates.md：tasks.md 增加"涉及文件对齐检查" |
| 实现比 plan 复杂很多 | 擅自发挥过度工程 | spec-driven-agent/SKILL.md：铁律中强化"不要在执行阶段追加设计" |
| 用了新技术栈但 plan 没提 | 擅自引入依赖 | code-review/references/review-checklist.md：Constitution 检查增加"依赖是否在 plan 中" |

## 审查阶段失效

| 现象 | 根因 | 改进动作 |
|------|------|----------|
| 空指针线上故障 | 审查没检查空值 | code-review/references/review-checklist.md：逻辑正确检查增加"空值防护清单" |
| 违背架构约束但给 9 分 | constitution 检查走过场 | code-review/SKILL.md：评分参考补充"constitution 违反直接扣至 5 分以下" |
| 审查通过了但用户发现 bug | 未对照 plan 审查 | code-review/SKILL.md：强制要求审查报告必须关联 plan.md 步骤 |
| 同类 bug 重复 3 次 | 检查清单未更新 | code-review/references/review-checklist.md：增加该类 bug 的检查项 |

## 流程阶段失效

| 现象 | 根因 | 改进动作 |
|------|------|----------|
| 需求模糊就直接写代码 | 跳过了 requirement-clarifier | spec-driven-agent/SKILL.md：连接指南加粗"需求不清时必须触发 requirement-clarifier" |
| 没写 plan 就动手 | 跳过了 SDD | 在用户项目 constitution.md 增加"无 plan 不开发"红线 |
| 执行完没审查就交付 | 跳过了 code-review | spec-driven-agent/SKILL.md：出口强制要求"执行后必须触发 code-review" |
| 出问题不复盘 | 缺少 retrospective 意识 | 在 code-review/SKILL.md 出口增加"审查 < 8.0 时强制触发 retrospective" |

## 改进优先级

复盘后按以下优先级执行改进：

1. **P0（立即执行）**：检查清单补充、评分参考补充、模板字段增加。这些改动小、见效快。
2. **P1（本轮内执行）**：SKILL.md 流程或连接指南的调整。影响后续所有同类任务。
3. **P2（观察后再执行）**：评分维度权重调整、新增 Skill。需观察 2-3 次执行验证效果。
