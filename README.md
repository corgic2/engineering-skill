# Engineering Skill

一套面向任意AI的工程化 AI 协作技能包。将「需求 → 设计 → 编码 → 审查 → 复盘」全流程固化为可复用的 Skills，让 AI 从"一次性帮手"升级为"项目级工程伙伴"。

## 核心理念

**让未参与过原始实现的新会话 AI，能在项目里像老同事一样按工程规范独立跑完一个需求。**

手段是两件事的结合：

1. **SDD（Spec-Driven Development）** —— 需求澄清 → 方案设计 → 用户确认 → 编码执行 → 审查 → 复盘，强制闭环，禁止跳步。
2. **项目级 AI 产物库** —— 为每个项目构建代码侧地图（project_wiki）、红线约束、构建脚本、跨会话状态文件。知识不随会话结束而消失，下一轮 AI 进场 5 分钟恢复现场。

两者配合，构建可验证、知识可跨会话接力的项目级 AI 工作流。

## Skill 清单

### 核心闭环（7 个）

| Skill | 阶段 | 职责 |
|-------|------|------|
| `spec-driven-dev` | 总入口 | 判断开发任务、路由阶段、拦截跳步 |
| `requirement-clarifier` | 需求澄清 | 模糊描述 → 结构化确认单 |
| `spec-driven-agent` | 设计 + 执行 | 产出 spec/plan/tasks，按 tasks 逐步编码 |
| `mermaid-diagrams` | 可视化 | 流程图/时序图/类图绘制规范 |
| `testing-strategy` | 测试 | 测试方案设计与用例生成 |
| `code-review` | 审查 | 五维评分审查，功能错误阻塞交付 |
| `execution-retrospective` | 复盘 | 复盘偏差根因，自动修补 Skill 文件 |

### 项目工程化（1 个）

| Skill | 职责 |
|-------|------|
| `engineering-workflow` | 构建项目级 AI 产物库：代码侧地图（project_wiki）、红线约束、脚本兜底验证、跨会话记忆（TECH_SPEC / subtasks / timeline）。替代 `spec-driven-agent` 在具体项目上的设计与执行角色。 |

### 辅助工具（3 个）

| Skill | 职责 |
|-------|------|
| `solution-validator` | 纯方案评估（五维评分，不写代码） |
| `code-architecture-analyzer` | 现有代码架构分析与文档生成 |
| `git-tools` | Git 操作参考 + 提交前质量门控 |

## 流程总览

```
需求进来
  → 澄清（需求确认单）
  → 设计（spec / plan / tasks + Mermaid 图 + 测试方案）
  → 用户确认
  → 编码（小步验证，逐 task 推进）
  → 自检
  → 审查（五维评分 ≥ 8.0）
  → 编译运行
  → 验收 / 复盘（Skill 自进化）
```

启用 `engineering-workflow` 时，设计阶段会额外生成项目地图、红线检查、编译验证脚本；执行结束后产物自动沉淀到 `TECH_SPEC.md`，下一轮 AI 会话可直接接力。

## 安装

将整个目录复制到AI模型的 skills 目录：

重启后自动加载。

## 使用

正常对话即可，`spec-driven-dev` 会自动拦截开发类请求：

| 你说 | 效果 |
|------|------|
| "帮我修一下搜索分页的 bug" | 自动走完整 SDD 流程 |
| "分析一下这段代码的问题" | 纯咨询，不触发流程 |
| "看看这个模块的架构" | 路由到 `code-architecture-analyzer` |
| "这个方案怎么样" | 路由到 `solution-validator` |
| "为项目初始化工程骨架" | 触发 `engineering-workflow` 生成产物库 |
