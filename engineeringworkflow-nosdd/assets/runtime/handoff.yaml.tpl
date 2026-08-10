# handoff：结构化交接块（机器真源）。每轮沉淀时刷新，validate_handoff.py 校验。
# 跨会话/跨模型接力时只读 context_manifest 指定文件；不得重开 trust=user_confirmed 的决策。
# SDD 项目：本块内嵌于 Agentic/sdd/<需求>/workflow-state.md；无 SDD 项目：独立为 runtime/handoff.yaml。
schema_version: 1
task:
  id: "{{req_id}}"
  title: "{{title}}"
  requirement_digest: "{{一句话需求摘要}}"
stage: "{{当前阶段}}"
context_manifest:          # 恢复现场的确定性取件单
  preload:                 # 必读（有序）
    - "AIRunWorkDocs/runtime/TECH_SPEC.md"
    - "AIRunWorkDocs/red_lines/red_lines_critical.md"
  on_demand: []            # 命中模块后按需加载
  skip: []                 # 明确不读（如已蒸馏的 SDD 原文）
  budget_tokens: 8000
decisions: []              # - {id: D1, summary: "...", trust: user_confirmed|ai_generated|stale, adr: "decisions/ADR-NNN.md"}
open_items: []             # - {type: blocker|todo|question, desc: "...", owner: "..."}
