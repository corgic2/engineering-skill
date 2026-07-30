# 入口：新需求

## 触发条件

用户提出一个此前未在 `subtasks.json` 中记录的功能需求。

## 流程

1. **理解需求**
   - 读用户原话 + `AIRunWorkDocs/docs/` 下相关物料（如有）。
   - 存在多种技术解读且影响改动范围时，向用户澄清一轮；否则直接继续。
   - 复杂需求写简版任务清单到 `runtime/subtasks.json`；简单需求跳过。

2. **代码定位**
   - 按五步定位法（`stage_locate.md`）找到改动点。
   - 涉及 UI/DB/协议时加载对应语义桥。

3. **编码实现**
   - 按定位结果自底向上改动，先看后写，模仿项目已有模式。

4. **验证**
   - 运行 `tools/build_verify.sh`，退出码 0 为判据，自修复 ≤3 轮。
   - 有条件时启动程序/测试，核对关键路径。

5. **沉淀归档**
   - 更新 `runtime/TECH_SPEC.md` §3/§7/§8/§9。
   - 有任务清单的话更新 `runtime/subtasks.json` 状态为 DONE。
   - 运行 `tools/check_project_wiki_stale.py` 同步 wiki。

6. **提交收尾**（用户要求提交时）
   - 渲染三段式 commit message，commit 前向用户确认一次。
