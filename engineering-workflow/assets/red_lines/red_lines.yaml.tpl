red_lines:
  - id: RL-01
    level: critical
    scope: global
    stage: verify
    trigger: 编译未通过或自修复超过3轮仍失败
    action: 停止执行，报告用户
    message: 编译退出码0为唯一判据，自修复硬上限3轮

  - id: RL-02
    level: critical
    scope: global
    stage: all
    trigger: 后一阶段输入不等于前一阶段产出，或跳过阶段
    action: 回退到前一阶段补齐产物
    message: 未按阶段执行禁止

  - id: RL-03
    level: critical
    scope: implement
    stage: implement
    trigger: 未通读完整方法/未搜索同类分支就新增独特模式
    action: 回退到定位阶段，先读后写
    message: 先看后写，模仿已有，禁止发明项目里独此一家的新模式

  - id: RL-04
    level: critical
    scope: implement
    stage: implement
    trigger: 代码中出现硬编码字号、颜色、协议字段、DB连接串、密钥
    action: 回退到定位阶段，加载语义桥后重改
    message: 禁止硬编码样式/字段/连接串/密钥

  - id: RL-05
    level: critical
    scope: global
    stage: all
    trigger: 用通用 web_fetch 替代专用脚本/MCP 收料
    action: 停止，改用专用通道
    message: 多源物料必须走专用通道

  - id: RL-06
    level: critical
    scope: global
    stage: commit
    trigger: check_project_wiki_stale.py 退出码1
    action: 先同步 project_wiki 再提交
    message: 知识库漂移检测不过禁止提交

  - id: RL-12
    level: standard
    scope: breakdown
    stage: breakdown
    trigger: 候选清单里存在未归类设计稿/物料
    action: 停止拆解，补全归宿
    message: 每张设计稿必须归宿明确

  - id: RL-17
    level: standard
    scope: design
    stage: design
    trigger: LLM 直接凭印象分桶设计稿
    action: 改用 scan_figma_frames.py 直方图分桶
    message: 严禁LLM手工分桶，须脚本直方图+白名单

  - id: RL-21
    level: standard
    scope: breakdown
    stage: breakdown
    trigger: 拦截点清单中 X触发Y 无文档/设计稿/用户原话依据
    action: 删除该行，不实施
    message: 拦截点须带依据，禁止语义联想

  - id: RL-29
    level: standard
    scope: implement
    stage: implement
    trigger: UI改动未比对 ui_mapping.md
    action: 加载语义桥后重改
    message: UI改动必须比对语义桥，禁止硬编码字号颜色

  - id: RL-31
    level: standard
    scope: commit
    stage: commit
    trigger: commit 后未确认 git log -1 hash 更新
    action: 重跑 finalize_commit.sh
    message: commit以git log -1 hash更新为据

  - id: RL-32
    level: standard
    scope: global
    stage: all
    trigger: 长跑命令仅靠 stdout 报告成功
    action: 补 sentinel 文件落盘判定
    message: 长跑命令成功以sentinel文件存在为据
