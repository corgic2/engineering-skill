# 阶段：提交收尾

## 目标

生成规范 commit，以 `git log -1` hash 更新为成功判据。

## 动作

1. 运行 `tools/render_commit_msg.py` 生成三段式 commit message。
2. 运行 `tools/check_project_wiki_stale.py`，确保知识库无漂移。
3. 执行 `git add` 与 `git commit -F .git/COMMIT_EDITMSG_CPP_WORKFLOW`。
4. 验证成功：
   - 退出码 0。
   - `git log -1` 的 hash 与上一版本不同。
   - 更新 `runtime/subtasks.json` 的 related_commit。
5. 追加 `runtime/timeline.txt`：记录 commit 事件。

## 硬关卡 HK-3

提交前必须输出 commit message 全文，等待用户回复"提交 / go / 改 xxx"，否则禁止执行 commit。

## 红线

- **RL-06**：知识库漂移检测不过禁止提交。
- **RL-31**：commit 以 `git log -1` hash 更新为据。
- **RL-32**：长跑命令成功以 sentinel 文件存在为据。
