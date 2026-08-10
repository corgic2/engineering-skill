# 红线候选隔离区。probation 期 warn-only 不阻断；晋升/淘汰由用户在 HK 关卡裁决。
# 结构对齐治理豁免清单模式（owner/reason/user_confirmed）。挖掘时跳过已豁免的存量记录。
# 晋升后条目移入 red_lines.yaml（正式红线）；正式红线连续 N 个 session 零命中 → 标记移除候选。
version: 1
candidates: []
  # - id: CAND-001
  #   status: proposed          # proposed → probation → active / rejected
  #   title: "..."
  #   trigger: "..."
  #   action: "..."
  #   source_violations: []     # ≥2 次同类违规证据（violations 条目引用）
  #   enforce: script           # script（进 pre-commit）/ checklist（进阶段清单）/ advisory（只进经验库）
  #   probation:
  #     since: "YYYY-MM-DD"
  #     hits: 0
  #     false_positives: 0
  #   owner: "<模型名或人名>@<git user.name>"
  #   reason: "..."
  #   user_confirmed: false
