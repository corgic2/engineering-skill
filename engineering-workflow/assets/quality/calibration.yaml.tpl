# 校准记录：AI 评审预测 vs 验收现实。复盘工序回写（见 execution-retrospective「数据回写义务」）。
version: 1
history: []
  # - req: "<需求名>"
  #   review_score: 9.5
  #   acceptance_rounds: 3            # 验收整改轮次；评分≥阈值且轮次>0 → 漏判（逃逸）
  #   escaped_blockers: ["..."]       # 验收才发现的问题
  #   missed_by_dimensions: ["acceptance_alignment"]
metrics:                     # 由复盘工序计算更新
  escape_rate: null          # 阻塞逃逸率 = 高分仍被打回的需求占比
  agreement_rate: null       # 评分-验收一致率
  last_updated: null
