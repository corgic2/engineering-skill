red_lines:
  - id: RL-01
    level: critical
    scope: global
    stage: verify
    trigger: 构建退出码非0、缺少 BUILD_PASS 标记或 sentinel 过期，或自修复超过3轮仍失败
    action: 停止执行，报告用户
    message: 构建成功以退出码0+BUILD_PASS+sentinel未过期三重判据为准，自修复硬上限3轮；引用既有构建结果前先跑 check_build_freshness.py

  - id: RL-02
    level: critical
    scope: global
    stage: archive
    trigger: 构建/运行验证未通过就将任务标记为 DONE 或写入 TECH_SPEC §8
    action: 回到验证步骤，补齐验证证据
    message: 未验证禁止归档

  - id: RL-03
    level: critical
    scope: implement
    stage: implement
    trigger: 未通读完整方法/未搜索同类分支就新增独特模式
    action: 回到定位步骤，先读后写
    message: 先看后写，模仿已有，禁止发明项目里独此一家的新模式

  - id: RL-04
    level: critical
    scope: implement
    stage: implement
    trigger: 代码中出现硬编码字号、颜色、协议字段、DB连接串、密钥
    action: 回到定位步骤，加载语义桥后重改
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

  - id: RL-07
    level: standard
    scope: implement
    stage: implement
    trigger: 改动了定位步骤未确认的文件
    action: 撤销越界改动，重新定位
    message: 只改定位确认的改动点，禁止顺手改未涉及文件

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
