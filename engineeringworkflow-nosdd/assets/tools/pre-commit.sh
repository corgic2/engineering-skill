#!/usr/bin/env bash
# pre-commit hook for engineeringworkflow-nosdd
# 安装：cp tools/pre-commit.sh .git/hooks/pre-commit

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKFLOW_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

PY="python3"
if ! python3 -c "import sys" >/dev/null 2>&1; then
    PY="python"
fi
if ! "${PY}" -c "import sys" >/dev/null 2>&1; then
    echo "[pre-commit] 找不到可用 Python，跳过漂移检测。"
    exit 0
fi

echo "[pre-commit] Running project_wiki stale check..."
"${PY}" "${WORKFLOW_ROOT}/tools/check_project_wiki_stale.py" || {
    echo "[pre-commit] project_wiki 漂移检测失败，请先同步知识库再提交。"
    exit 1
}

echo "[pre-commit] PASS."
exit 0
