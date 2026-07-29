# 入口：新需求

## 触发条件

用户提出一个此前未在 `subtasks.json` 中记录的功能需求。

## 流程

1. **设计稿收料**
   - 收集 PRD、设计稿、协议、任务单链接。
   - 每类物料走专用通道（脚本/MCP），禁止通用 web_fetch。
   - 输出候选物料清单。

2. **需求拆解**
   - 按 `stage_breakdown.md` 五规则翻译需求。
   - 输出五列表格与 `runtime/subtasks.json`。
   - **HK-1**：等待用户确认 subtasks。

3. **代码定位**
   - 对每个 subtask 执行五步定位法。
   - 输出改动点清单。

4. **编码实现**
   - 按定位结果自底向上改动。
   - 每步小步验证。

5. **编译验证**
   - 运行 `tools/build_verify.sh`。
   - 最多 3 轮自修复。

6. **运行验证**
   - 启动程序/测试，截图/日志核对。

7. **沉淀归档**
   - 更新 `runtime/TECH_SPEC.md` §3/§7/§8/§9。
   - 更新 `runtime/subtasks.json` 状态为 DONE。
   - **HK-2**：等待用户"沉淀 ok"。

8. **提交收尾**
   - 渲染三段式 commit message。
   - 运行 `tools/check_project_wiki_stale.py`。
   - **HK-3**：等待用户"提交/go"。
