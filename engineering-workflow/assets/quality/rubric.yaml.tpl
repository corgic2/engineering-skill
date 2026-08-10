# 评审标尺（锚定清单）。评审者逐条判定 是/否/不适用，维度得分 = 命中项加总折算 10 分制。
# 校准环根据 calibration.yaml 的漏判/误判记录调整本文件清单项与阈值，禁止拍脑袋改分。
# 由 spec-driven-dev 阶段 6「评审团与校准协议」解释执行；无本文件时五维评分为默认基线。
version: 1
pass_threshold: 8.0
dimensions:
  acceptance_alignment:      # 验收对齐（不可缺省）：高分与验收通过无必然相关性，此维度专拦
    weight: 2
    items:
      - "每条验收标准都有可执行证据（测试/截图/日志），无'应然'措辞"
      - "需求邻域行为（非主路径语义）有用户原话级证据"
  plan_alignment:
    weight: 2
    items:
      - "spec-plan 所有步骤均已实现，无遗漏"
      - "无计划外文件修改（git diff 与文件清单一致）"
  constitution:
    weight: 2
    items:
      - "目录结构、命名、模块边界、依赖方向符合 constitution"
      - "无红线违规；probation 候选红线的警告项已逐条确认"
  logic_correctness:
    weight: 2
    items:
      - "主流程正确，异常分支覆盖"
      - "空值/越界/空集合/并发边界已处理"
      - "运行时连接（信号/事件/回调）注册-触发-注销链路完整"
  maintainability:
    weight: 1
    items:
      - "命名与项目风格一致；重复逻辑 ≥3 处已提取"
      - "无不必要依赖，无过度设计"
  verifiability:
    weight: 1
    items:
      - "关键路径有测试/断言/日志覆盖"
      - "测试可独立运行，断言明确"
review_protocol:
  reviewers: 2               # S 档为 1；跨模型可用时含对立模型
  aggregation: median
  divergence_escalate: 2     # 任一维度评审者分差 > 此值 → low-confidence，升级用户或 judge
