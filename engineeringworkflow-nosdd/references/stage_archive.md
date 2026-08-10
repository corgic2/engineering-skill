# 阶段：沉淀归档

## 目标

把本次需求的改动沉淀为 git-tracked 的 `runtime/TECH_SPEC.md`，让下次会话能 5 分钟恢复现场。

## 动作

1. 汇总 `git diff` 与 `runtime/timeline.txt`。
2. 更新 `TECH_SPEC.md`：
   - §3 模块地图：新增/修改文件与关键方法。
   - §7 演进事件：新增 ITER-N / BUG-N / REV-N。
   - §8 产物清单：子需求 → 文件 → commit。
   - §9 版本号：递增。
3. 更新 `runtime/subtasks.json`：对应条目状态改为 DONE，记录 commit hash。
4. 追加 `runtime/timeline.txt`：记录沉淀事件。
5. 运行 `tools/check_project_wiki_stale.py` 并同步 project_wiki。
6. **经验提炼检查**：扫描本次 `timeline.txt` 的 human-correction 事件与反直觉 bug 排查过程，对照 `team-experience-curator` 的四条触发条件——满足才调用该 skill 提炼入库（目标 `AIRunWorkDocs/experience/<component>.md`），不满足直接跳过。禁止"顺手"自动提炼；不满足触发条件时本步输出"无经验产出"即可。写入前先做分界检查：术语黑话 → semantic_bridge，结构位置 → project_wiki，已属红线内容 → 不入库。
7. **提炼分流**（无 SDD 文档可蒸馏，当场分流进长期层）：有理由的决策 → `decisions/` ADR（一段式）；被用户纠正的约定 → 红线候选隔离区（同 pattern ≥2 次才起草）；反直觉坑 → 经验库（上一步已查）；纯流水留 timeline 或丢弃。
8. **刷新 `runtime/handoff.yaml`**：更新 context_manifest / decisions.trust / open_items，跑 `tools/validate_handoff.py`。

## 输出

- 更新后的 `TECH_SPEC.md`
- 更新后的 `subtasks.json`
- `timeline.txt` 沉淀记录
- 刷新后的 `runtime/handoff.yaml`（validate_handoff.py 通过）
- 经验库更新（可选，或"无经验产出"说明）
