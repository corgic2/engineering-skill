#!/usr/bin/env bash
# Versioned fail-closed pre-commit gate. Product compilation is not run here.
# 安装（推荐，随仓库版本化、跨平台）：
#   1) 将本文件提交为 <repo>/.githooks/pre-commit（hook 内路径据此调整）
#   2) git config core.hooksPath .githooks
# 也可直接复制到 .git/hooks/pre-commit 使用。

set -euo pipefail

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || {
  echo "[pre-commit] 无法定位 Git 仓库根目录。" >&2
  exit 1
}
# 若 AIRunWorkDocs 不在仓库根，按项目实际层级调整本变量。
WORKFLOW_ROOT="${REPO_ROOT}/AIRunWorkDocs"

if [[ ! -d "${WORKFLOW_ROOT}" ]]; then
  echo "[pre-commit] 缺少工程目录: ${WORKFLOW_ROOT}" >&2
  exit 1
fi

if command -v python >/dev/null 2>&1; then
  PYTHON=python
elif command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v py >/dev/null 2>&1; then
  PYTHON=py
else
  echo "[pre-commit] 找不到 Python，按失败关闭策略阻断提交。" >&2
  exit 1
fi

echo "[pre-commit] Validating AI engineering constraints..."
"${PYTHON}" "${WORKFLOW_ROOT}/tools/validate_constraints.py" || {
  echo "[pre-commit] 约束校验失败，请修复后重新提交。" >&2
  exit 1
}

echo "[pre-commit] Running project_wiki stale check..."
"${PYTHON}" "${WORKFLOW_ROOT}/tools/check_project_wiki_stale.py" || {
  echo "[pre-commit] project_wiki 漂移检测失败，请先同步知识库再提交。" >&2
  exit 1
}

if [[ -f "${WORKFLOW_ROOT}/tools/validate_handoff.py" ]]; then
  echo "[pre-commit] Validating handoff blocks..."
  "${PYTHON}" "${WORKFLOW_ROOT}/tools/validate_handoff.py" || {
    echo "[pre-commit] handoff 交接块校验失败，请修复后重新提交。" >&2
    exit 1
  }
fi

echo "[pre-commit] PASS."
exit 0
