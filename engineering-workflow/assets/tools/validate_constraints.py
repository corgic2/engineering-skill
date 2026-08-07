#!/usr/bin/env python3
"""Validate the repository's AI engineering constraints without building products.

提交前第一道门禁（pre-commit 调用，失败关闭）。本文件为通用骨架：
结构完整性检查开箱即用；项目应按自身 constitution.md / AGENTS.md 在
PROJECT_CHECKS 中追加定制校验项（命名规范、依赖方向、配置唯一真源等）。

退出码：0 = PASS；1 = 存在违规。
"""

from __future__ import print_function

import sys
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve()
WORKFLOW_ROOT = SCRIPT_PATH.parent.parent  # AIRunWorkDocs/
PROJECT_ROOT = WORKFLOW_ROOT.parent

# 结构完整性：骨架必需文件，缺失即违规。按项目裁剪。
REQUIRED_FILES = (
    "AIRunWorkDocs/project_wiki/overview.md",
    "AIRunWorkDocs/red_lines/red_lines.yaml",
    "AIRunWorkDocs/red_lines/red_lines_critical.md",
    "AIRunWorkDocs/runtime/TECH_SPEC.md",
    "AIRunWorkDocs/runtime/subtasks.json",
)

# 项目定制校验项：每项为 (名称, callable(PROJECT_ROOT) -> str|None)，
# 返回 None 表示通过，返回字符串表示违规描述。
# 示例：
#   def check_no_hardcoded_secrets(root): ...
# PROJECT_CHECKS = (("禁止硬编码密钥", check_no_hardcoded_secrets),)
PROJECT_CHECKS = ()


def main():
    violations = []

    for rel in REQUIRED_FILES:
        if not (PROJECT_ROOT / rel).is_file():
            violations.append("缺少骨架必需文件: {0}".format(rel))

    for name, check in PROJECT_CHECKS:
        result = check(PROJECT_ROOT)
        if result:
            violations.append("{0}: {1}".format(name, result))

    if violations:
        print("[validate_constraints] FAIL:")
        for item in violations:
            print("  - {0}".format(item))
        return 1

    print("[validate_constraints] PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
