#!/usr/bin/env python3
"""Validate handoff blocks (structured handoff for cross-session / cross-model relay).

校验对象（自动发现，也可用参数显式指定文件）：
1. AIRunWorkDocs/runtime/handoff.yaml（无 SDD 项目）
2. Agentic/sdd/*/workflow-state.md 中内嵌的 `handoff:` YAML 块（SDD 项目）

校验项（缺任一即 FAIL）：
- context_manifest 四字段：preload / on_demand / skip / budget_tokens（数值）
- decisions[].trust 取值合法：user_confirmed / ai_generated / stale
- open_items[].type 取值合法：blocker / todo / question

退出码：0 = PASS；1 = 存在违规。无 handoff 文件/块时 PASS（未启用不强制）。
"""

from __future__ import print_function

import re
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
WORKFLOW_ROOT = SCRIPT_PATH.parent.parent  # AIRunWorkDocs/
PROJECT_ROOT = WORKFLOW_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent if (PROJECT_ROOT.parent / ".git").exists() else PROJECT_ROOT

ALLOWED_TRUST = ("user_confirmed", "ai_generated", "stale")
ALLOWED_ITEM = ("blocker", "todo", "question")


def find_targets(argv):
    if len(argv) > 1:
        return [Path(a) for a in argv[1:]]
    targets = []
    standalone = WORKFLOW_ROOT / "runtime" / "handoff.yaml"
    if standalone.is_file():
        targets.append(standalone)
    for base in (REPO_ROOT / "Agentic" / "sdd", PROJECT_ROOT / "Agentic" / "sdd",
                 REPO_ROOT / "sdd", PROJECT_ROOT / "sdd"):
        if base.is_dir():
            for ws in sorted(base.glob("*/workflow-state.md")):
                targets.append(ws)
    # 去重保序
    seen, uniq = set(), []
    for t in targets:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def extract_block(text):
    """提取 handoff: 顶层键开始的 YAML 块（到下一个顶层键或文件尾）。"""
    m = re.search(r"^handoff:\s*\n((?:[ \t]+.*\n|\s*\n)+)", text, re.M)
    return m.group(1) if m else None


def validate_block(name, block):
    errors = []
    for key in ("context_manifest:", "preload:", "on_demand:", "skip:"):
        if key not in block:
            errors.append("{0}: handoff 缺字段 {1}".format(name, key))
    m = re.search(r"budget_tokens:\s*(\d+)", block)
    if not m:
        errors.append("{0}: handoff 缺 budget_tokens 数值".format(name))
    if "decisions:" not in block:
        errors.append("{0}: handoff 缺 decisions 段".format(name))
    if "open_items:" not in block:
        errors.append("{0}: handoff 缺 open_items 段".format(name))
    for tm in re.finditer(r"trust:\s*([\w\-]+)", block):
        if tm.group(1) not in ALLOWED_TRUST:
            errors.append("{0}: 非法 trust 值 {1}".format(name, tm.group(1)))
    for im in re.finditer(r"type:\s*([\w\-]+)", block):
        if im.group(1) not in ALLOWED_ITEM:
            errors.append("{0}: 非法 open_items.type 值 {1}".format(name, im.group(1)))
    return errors


def validate_file(path):
    text = path.read_text(encoding="utf-8", errors="replace")
    if path.name == "handoff.yaml":
        block = text if re.search(r"^context_manifest:", text, re.M) else None
        if block is None:
            return ["{0}: handoff.yaml 缺 context_manifest".format(path.name)]
        return validate_block(path.name, text)
    block = extract_block(text)
    if block is None:
        return []  # 无 handoff 块：未启用，不强制
    return validate_block(path.parent.name + "/workflow-state.md", block)


def main():
    targets = find_targets(sys.argv)
    errors = []
    for t in targets:
        if not t.is_file():
            errors.append("文件不存在: {0}".format(t))
            continue
        errors.extend(validate_file(t))
    if errors:
        print("[validate_handoff] FAIL:")
        for e in errors:
            print("  - {0}".format(e))
        return 1
    print("[validate_handoff] PASS ({0} 个文件)".format(len(targets)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
