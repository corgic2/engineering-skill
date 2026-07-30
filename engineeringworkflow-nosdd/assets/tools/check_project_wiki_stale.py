#!/usr/bin/env python3
"""
check_project_wiki_stale.py - 扫描 project_wiki 与实际源码是否脱节。
用法：
    python3 check_project_wiki_stale.py [--patch]
退出码：
    0 - 无漂移
    1 - 有漂移（或 --patch 后仍有未处理）
"""

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def find_module_files(workflow_root: Path, project_root: Path):
    """解析 project_wiki/*.md 顶部元数据，返回登记的文件集合。"""
    wiki_dir = workflow_root / "project_wiki"
    registered = {}  # rel_path -> {"module": str, "sha": str|null}
    for md_path in wiki_dir.glob("*.md"):
        if md_path.name == "overview.md":
            continue
        text = md_path.read_text(encoding="utf-8")
        m = re.search(r"<!--\s*root_dirs:\s*(.*?)-->", text, re.S)
        if not m:
            continue
        dirs_raw = m.group(1)
        root_dirs = re.findall(r"-\s*(\S+)", dirs_raw)
        for d in root_dirs:
            full_dir = project_root / d
            if not full_dir.exists():
                continue
            for ext in ("*.h", "*.hpp", "*.cpp", "*.cc", "*.mm"):
                for f in full_dir.rglob(ext):
                    rel = f.relative_to(project_root).as_posix()
                    registered[rel] = {"module": md_path.stem, "sha": None}
    return registered


def scan_disk(project_root: Path, source_dirs):
    """扫描磁盘上的源码文件。"""
    actual = set()
    for d in source_dirs:
        full_dir = project_root / d
        if not full_dir.exists():
            continue
        for ext in ("*.h", "*.hpp", "*.cpp", "*.cc", "*.mm"):
            for f in full_dir.rglob(ext):
                actual.add(f.relative_to(project_root).as_posix())
    return actual


def load_cache(workflow_root: Path):
    cache_path = workflow_root / ".review_cache.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    return {}


def save_cache(workflow_root: Path, cache):
    cache_path = workflow_root / ".review_cache.json"
    cache_path.write_text(json.dumps(cache, indent=2, ensure_ascii=False), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--patch", action="store_true", help="自动把新增文件补登到对应 module.md")
    args = parser.parse_args()

    # 脚本位于 <project>/<root_dir>/tools/ 下，向上两级到项目根，向上级到 workflow_root
    default_workflow_root = Path(__file__).resolve().parent.parent
    default_project_root = default_workflow_root.parent
    workflow_root = Path(os.environ.get("WORKFLOW_ROOT", default_workflow_root)).resolve()
    project_root = Path(os.environ.get("PROJECT_ROOT", default_project_root)).resolve()

    wiki_dir = workflow_root / "project_wiki"
    if not wiki_dir.exists():
        print(f"[check_wiki_stale] {wiki_dir} not found, skip.")
        sys.exit(0)

    registered = find_module_files(workflow_root, project_root)
    source_dirs = list({Path(p).parts[0] for p in registered})

    if not source_dirs:
        # 模板项目或 module.md 未填写 root_dirs 时，扫描常见源码目录
        fallback_dirs = ["src", "source", "app", "lib", "libs"]
        source_dirs = [d for d in fallback_dirs if (project_root / d).exists()]
        if source_dirs:
            print(f"[check_wiki_stale] module.md 中未发现有效 root_dirs，回退扫描：{source_dirs}")
        else:
            print("[check_wiki_stale] 未发现任何源码目录，跳过漂移检测。")
            save_cache(workflow_root, {})
            sys.exit(0)

    actual = scan_disk(project_root, source_dirs)

    cache = load_cache(workflow_root)
    new_cache = {}

    added = actual - set(registered.keys())
    deleted = set(registered.keys()) - actual
    changed = []

    for rel in registered:
        fpath = project_root / rel
        if not fpath.exists():
            continue
        current_sha = sha256_file(fpath)
        new_cache[rel] = current_sha
        last_sha = cache.get(rel)
        if last_sha and last_sha != current_sha:
            changed.append(rel)

    # 三色分诊输出
    print("=== project_wiki stale check ===")
    print(f"新增文件 ({len(added)}):")
    for rel in sorted(added):
        print(f"  + {rel}")
    print(f"删除文件 ({len(deleted)}):")
    for rel in sorted(deleted):
        print(f"  - {rel}")
    print(f"大改文件 ({len(changed)}):")
    for rel in sorted(changed):
        print(f"  ~ {rel}")

    if args.patch and added:
        # 按目录找到对应 module.md 补登
        by_module = {}
        for rel in added:
            # 简单启发：取第一级目录匹配 root_dirs 中的模块
            module = None
            for reg_rel, info in registered.items():
                if rel.startswith(str(Path(reg_rel).parent)):
                    module = info["module"]
                    break
            if not module:
                module = "overview"
            by_module.setdefault(module, []).append(rel)

        for module, files in by_module.items():
            md_path = wiki_dir / f"{module}.md"
            if not md_path.exists():
                md_path = wiki_dir / "overview.md"
            with open(md_path, "a", encoding="utf-8") as f:
                f.write("\n## 自动补登文件\n\n")
                for rel in files:
                    f.write(f"- `{rel}`\n")
        print(f"[check_wiki_stale] --patch: appended {len(added)} files to module docs.")

    save_cache(workflow_root, new_cache)

    has_stale = bool(added or deleted or changed)
    if has_stale and not (args.patch and not deleted and not changed):
        print("[check_wiki_stale] FAIL: project_wiki is stale.")
        sys.exit(1)

    print("[check_wiki_stale] PASS.")
    sys.exit(0)


if __name__ == "__main__":
    main()
