#!/usr/bin/env python3
"""
render_commit_msg.py - 渲染三段式 commit message。
用法：
    python3 render_commit_msg.py --type feat --scope MList --subject "新增域名过期提示条" --body "M1..." --footer "Closes FEAT-2026-001"
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def detect_code_ratio(project_root: Path):
    """粗略估计本次改动的 AI 生成率，仅作署名参考。"""
    try:
        result = subprocess.run(
            ["git", "diff", "--stat"],
            capture_output=True, text=True, check=True, cwd=project_root
        )
        lines = result.stdout.strip().splitlines()
        return f"{len(lines)} files changed"
    except Exception:
        return "N/A"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--type", required=True, choices=["feat", "fix", "refactor", "docs", "test"])
    parser.add_argument("--scope", required=True)
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--footer", default="")
    args = parser.parse_args()

    workflow_root = Path(os.environ.get("WORKFLOW_ROOT", Path(__file__).resolve().parent.parent)).resolve()
    project_root = Path(os.environ.get("PROJECT_ROOT", workflow_root.parent)).resolve()
    git_dir = project_root / ".git"
    if not git_dir.exists():
        print(f"[render_commit_msg] Not a git repo: {project_root}", file=sys.stderr)
        sys.exit(1)

    msg = f"{args.type}({args.scope}): {args.subject}\n\n{args.body}\n\n"
    if args.footer:
        msg += f"{args.footer}\n"
    msg += f"AI-Generated-Portion: {detect_code_ratio(project_root)}\n"
    msg += "Signed-off-by: AI-Engineer <ai@example.com>\n"

    out_path = git_dir / "COMMIT_EDITMSG_CPP_WORKFLOW"
    out_path.write_text(msg, encoding="utf-8")
    print(f"[render_commit_msg] Wrote {out_path}")
    print(msg)


if __name__ == "__main__":
    main()
