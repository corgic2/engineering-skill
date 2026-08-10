# Workflow State 模板

每个开发任务创建一份状态文件，防止跨会话丢失进度。

## 存放位置

放在项目根目录或 `Agentic/sdd/<需求名称>/` 目录下（一个需求一个子目录）：
- `Agentic/sdd/<需求名称>/workflow-state.md`（推荐，与 SDD 产物放在一起）
- 如项目未使用 `Agentic` 目录，也可放在 `sdd/<需求名称>/workflow-state.md`

## 模板

```markdown
# Workflow State

task: "<一句话描述任务>"
tier: "<S / M / L>"   # 任务分级（阶段 1 随需求一并确认）；S 档免 spec-plan、阶段 5 并入阶段 6
stage: "<当前阶段>"
  # 可选值：requirement-clarification / solution-design / user-confirmation / code-execution
  #         / post-execution-self-review / code-review / compilation-verification / acceptance-retrospective

created_at: "YYYY-MM-DD HH:MM"
updated_at: "YYYY-MM-DD HH:MM"

confirmed:
  requirement: false  # 需求已确认
  design: false       # 设计方案已确认
  execution: false    # 代码已执行
  review: false       # 审查已通过

roles:                # 角色确认记录（顺序：设计→编码→骨架；声明须用户确认）
  design:
    owner: ""         # <模型名或人名>@<git user.name>
    declared_at: ""
    user_confirmed: false
  coding:
    owner: ""
    declared_at: ""
    user_confirmed: false
  skeleton:
    owner: ""
    declared_at: ""
    user_confirmed: false

review:
  score: 0            # 审查综合评分
  passed: false       # 是否通过
  blockers: []        # 阻塞问题列表

artifacts:            # 按档位登记；S 档只有 requirement + tasks
  requirement: ""     # 需求确认单路径
  spec_plan: ""       # spec-plan.md 路径（M/L 档：spec+plan 合并，含验证方案专章）
  tasks: ""           # tasks.md 路径（勾选项清单，不复述 spec-plan 步骤）
  test_cases: ""      # 可选，L 档复杂时拆出
  review: ""          # 审查报告路径
  retrospective: ""   # 复盘报告路径

handoff:              # 结构化交接块（机器真源；工程化项目由 validate_handoff.py 校验）
  context_manifest:   # 恢复现场的确定性取件单；跨会话/跨模型接力只读此处指定文件
    preload: []
    on_demand: []
    skip: []
    budget_tokens: 8000
  decisions: []       # {id, summary, trust}；trust: user_confirmed / ai_generated / stale
  open_items: []      # {type: blocker|todo|question, desc, owner}

notes: "<额外备注，如用户特殊要求、阻塞原因>"
```

## 阶段流转示例

### Bug 修复任务

```markdown
# Workflow State

task: "修复搜索分页切换后数据不刷新"
tier: "S"             # 单点 bug，≤3 文件，免 spec-plan
stage: "code-review"
created_at: "2026-05-08 10:00"
updated_at: "2026-05-08 11:30"

confirmed:
  requirement: true
  design: true
  execution: true
  review: false

review:
  score: 8.6
  passed: true
  blockers: []

artifacts:            # S 档示例：无 spec-plan
  requirement: "Agentic/sdd/<需求名称>/req-confirm.md"
  tasks: "Agentic/sdd/<需求名称>/tasks.md"
  review: "Agentic/sdd/<需求名称>/review-report.md"

notes: "用户验收通过，无需复盘"
```

## 跨会话恢复

新会话开始时，先检查项目目录是否存在 `workflow-state.md`：
- 存在且 `stage` 不是 `acceptance-retrospective` → 按 `handoff.context_manifest` 取件恢复现场，按 stage 继续流程；不得重开 `decisions` 中 `trust: user_confirmed` 的决策
- 不存在或 stage 已结束 → 视为新任务，从入口判断开始
