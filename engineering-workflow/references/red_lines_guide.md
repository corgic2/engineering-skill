# 红线机制说明

## YAML 结构

`red_lines/red_lines.yaml` 是唯一真源：

```yaml
red_lines:
  - id: RL-01
    level: critical
    scope: global
    stage: verify
    trigger: 编译未通过或自修复超过3轮仍失败
    action: 停止执行，报告用户
    message: 编译退出码0为唯一判据，自修复硬上限3轮

  - id: RL-04
    level: standard
    scope: implement
    stage: implement
    trigger: 代码中出现硬编码字号、颜色、协议字段、DB连接串、密钥
    action: 回退到定位阶段，加载语义桥后重改
    message: 禁止硬编码样式/字段/连接串/密钥
```

## 分层加载

- `red_lines_critical.md`：启动即加载，≤6 条。
- `red_lines_by_stage/<stage>.md`：进入对应阶段后加载。

## 触发报告模板

触发红线时，严格按以下格式输出，禁止继续执行：

```
⛔ 触发红线 RL-XX：<标题>
当前情形：<具体说明>
建议处理：<回退到哪个步骤 / 需要用户确认什么>
```

## Critical 红线（初始 6 条）

1. **RL-01 编译通过**：退出码 0 唯一判据；自修复 ≤3 轮。
2. **RL-02 阶段顺序**：禁止跳阶段，后一阶段输入必须等于前一阶段产出。
3. **RL-03 先看后写**：修改前先通读完整方法 + 搜索同类分支，禁止发明新模式。
4. **RL-04 禁止硬编码**：样式/字段/连接串/密钥必须走映射或配置。
5. **RL-05 专用物料通道**：TAPD/Figma/协议等必须走专用脚本/MCP，禁止通用 web_fetch。
6. **RL-06 知识库保鲜**：`check_project_wiki_stale.py` 不过禁止提交。

## Standard 红线示例

- **RL-12 设计稿归宿**：每张图必须归类为载图/变体/参考，禁止未归类。
- **RL-17 禁止 LLM 手工分桶**：设计稿筛选必须脚本直方图 + 白名单。
- **RL-21 拦截点依据**：X 触发 Y 必须有文档/设计稿/用户原话依据。
- **RL-29 UI 语义桥**：UI 改动必须比对 `ui_mapping.md`。
- **RL-30 视觉对齐**：UI 改动必须存在 `ui_alignment_spec.md` 且未对齐项为 0。
- **RL-31 commit 判据**：以 `git log -1` hash 更新为成功证据。
- **RL-32 落盘判定**：长跑命令成功以 sentinel 文件存在为据。

## 红线生命周期

候选挖掘（同一 violations pattern ≥2 次）→ 隔离区 probation（warn-only 不阻断）→ 用户裁决晋升 → 零命中衰减，详见 SKILL.md「红线生命周期」。候选写入 `red_lines_candidates.yaml`，只有正式红线才进 `red_lines.yaml`。
