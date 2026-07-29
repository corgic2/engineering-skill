# 入口：增量迭代

## 触发条件

用户要求继续一个已有需求，或 `subtasks.json` 中存在 PENDING/IN_PROGRESS 条目。

## 流程

1. **现场快报（HK-0）**
   - 读取 `runtime/TECH_SPEC.md` §0/§1/§3/§5/§7。
   - 读取 `runtime/subtasks.json`。
   - 输出：接下来要做的子需求 / 当前阶段 / 关联 commit / 不变式检查。

2. **选择继续点**
   - 若所有 subtasks 为 DONE → 进入新需求流程。
   - 若有 PENDING → 从「代码定位」开始。
   - 若有 IN_PROGRESS → 从当前阶段继续。

3. **恢复上下文**
   - 按 `timeline.txt` 最后一次 commit 拉取相关 diff。
   - 加载对应 `project_wiki/<module>.md`。

4. **执行剩余阶段**
   - 按 8 阶段流水线推进。
   - 每完成一个 subtask，更新状态为 DONE 并记录 commit。

5. **沉淀与提交**
   - `TECH_SPEC.md` §7 新增 ITER-N 记录本次迭代变更。
   - **HK-2/HK-3**：沉淀与提交确认。
