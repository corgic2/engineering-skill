# 入口：增量迭代

## 触发条件

用户要求继续一个已有需求，或 `subtasks.json` 中存在 PENDING/IN_PROGRESS 条目。

## 流程

1. **恢复现场**
   - 读取 `runtime/TECH_SPEC.md` §0/§1/§3/§5/§7。
   - 读取 `runtime/subtasks.json`（如存在）。
   - 向用户输出一句现场快报：上次做到哪、接下来做什么，然后直接继续，不等待确认。

2. **恢复上下文**
   - 按 `timeline.txt` 最后一次 commit 拉取相关 diff。
   - 加载对应 `project_wiki/<module>.md`。

3. **继续主循环**
   - 定位 → 实现 → 验证 → 沉淀。
   - 每完成一个子任务，更新状态为 DONE 并记录 commit。

4. **沉淀**
   - `TECH_SPEC.md` §7 新增 ITER-N 记录本次迭代变更。
