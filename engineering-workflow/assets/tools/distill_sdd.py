#!/usr/bin/env python3
"""Distill SDD requirement directories into one-page digests + cold archive.

用法：
  distill_sdd.py                # dry-run：打印计划，不动文件
  distill_sdd.py --apply        # 执行蒸馏
  distill_sdd.py <需求名> --apply   # 只蒸馏指定需求

蒸馏动作（每个需求目录）：
1. 生成 digest.md（≤2KB：目标/关键决策引用/结果/遗留项/原文指针）
2. 除 workflow-state.md 与 digest.md 外，原文移入 Agentic/sdd/.archive/<需求>/
3. 登记 Agentic/sdd/sdd_index.yaml（req/status/digest/归档路径/流程完整度）

注意：蒸馏是有损压缩，digest 保留指向 .archive 的引用；豁免清单等按目录名引用
本需求的文件需人工或脚本同步改写（本脚本只警告，不擅自改）。
"""

from __future__ import print_function

import re
import shutil
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
WORKFLOW_ROOT = SCRIPT_PATH.parent.parent
PROJECT_ROOT = WORKFLOW_ROOT.parent
REPO_ROOT = PROJECT_ROOT.parent if (PROJECT_ROOT.parent / ".git").exists() else PROJECT_ROOT

CANDIDATES = [
    REPO_ROOT / "Agentic" / "sdd",
    PROJECT_ROOT / "Agentic" / "sdd",
    REPO_ROOT / "sdd",
    PROJECT_ROOT / "sdd",
]

DIGEST_LIMIT = 2 * 1024
KEEP = ("workflow-state.md", "digest.md")


def find_sdd_root():
    for c in CANDIDATES:
        if c.is_dir():
            return c
    return None


def parse_state(text):
    def field(name):
        m = re.search(r"^{0}:\s*\"?([^\n\"]+)\"?\s*$".format(name), text, re.M)
        return m.group(1).strip() if m else ""
    score = re.search(r"score:\s*([\d.]+)", text)
    return {
        "task": field("task"),
        "tier": field("tier") or "?",
        "stage": field("stage"),
        "score": score.group(1) if score else "",
    }


def make_digest(name, info, files):
    lines = [
        "# Digest: {0}".format(name),
        "",
        "- 目标：{0}".format(info["task"] or "<见归档 req-confirm>"),
        "- 档位/终态：{0} / {1}".format(info["tier"], info["stage"] or "?"),
        "- 评审分：{0}".format(info["score"] or "无"),
        "- 关键决策：<蒸馏时填写 ADR 引用，无则写「无」>",
        "- 遗留项：<蒸馏时填写，无则写「无」>",
        "- 关联经验/红线候选：<蒸馏时填写，无则写「无」>",
        "- 原文：`.archive/{0}/`（{1} 个文件）".format(name, len(files)),
        "",
    ]
    return "\n".join(lines)


def main():
    apply = "--apply" in sys.argv
    only = [a for a in sys.argv[1:] if not a.startswith("--")]
    sdd = find_sdd_root()
    if sdd is None:
        print("[distill_sdd] 未找到 sdd 目录，跳过")
        return 0
    archive = sdd / ".archive"
    index = sdd / "sdd_index.yaml"
    plan = []
    for d in sorted(sdd.iterdir()):
        if not d.is_dir() or d.name == ".archive" or d.name.startswith("."):
            continue
        if only and d.name not in only:
            continue
        if (d / "digest.md").exists():
            continue  # 已蒸馏
        ws = d / "workflow-state.md"
        info = parse_state(ws.read_text(encoding="utf-8", errors="replace")) if ws.exists() \
            else {"task": "", "tier": "?", "stage": "无 workflow-state", "score": ""}
        files = [f for f in d.iterdir() if f.is_file() and f.name not in KEEP]
        plan.append((d, info, files))
    if not plan:
        print("[distill_sdd] 无待蒸馏目录")
        return 0
    print("[distill_sdd] {0}（{1} 个需求）".format("执行蒸馏" if apply else "DRY-RUN 计划", len(plan)))
    entries = []
    for d, info, files in plan:
        print("  - {0}: {1} 个文件 → .archive/，digest {2}".format(d.name, len(files), d.name))
        entries.append((d, info, files))
    if not apply:
        print("[distill_sdd] dry-run 结束，加 --apply 执行")
        return 0
    archive.mkdir(exist_ok=True)
    if not index.exists():
        index.write_text("# SDD 蒸馏索引。恢复现场只读本索引与 digest.md，禁止扫描 .archive 原文。\nversion: 1\nentries:\n", encoding="utf-8")
    with index.open("a", encoding="utf-8") as fh:
        for d, info, files in entries:
            dest = archive / d.name
            dest.mkdir(exist_ok=True)
            for f in files:
                shutil.move(str(f), str(dest / f.name))
            digest = make_digest(d.name, info, files)
            if len(digest.encode("utf-8")) > DIGEST_LIMIT:
                print("  ! digest 超 2KB 预算: {0}".format(d.name))
            (d / "digest.md").write_text(digest, encoding="utf-8")
            fh.write("  - req: \"{0}\"\n    status: distilled\n    stage: \"{1}\"\n    digest: \"{2}/digest.md\"\n    archive: \".archive/{2}/\"\n".format(d.name, info["stage"], d.name))
    print("[distill_sdd] 完成。请检查豁免清单等文件中按目录名的引用是否断链。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
