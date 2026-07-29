#!/usr/bin/env python3
"""
init_engineering_project.py - 为项目初始化 engineering-workflow 工程骨架。
用法：
    python3 init_engineering_project.py --project-root /path/to/project --modules mlist,rmail,cmail,model
    python3 init_engineering_project.py --project-root /path/to/project --modules core,ui --language generic --root-dir Agentic
"""

import argparse
import shutil
import os
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parent.parent
ASSETS_DIR = SKILL_DIR / "assets"

# 语言 -> 常用源码扩展名
LANG_EXTENSIONS = {
    "cpp": [".h", ".hpp", ".cpp", ".cc", ".cxx", ".mm"],
    "c": [".h", ".c"],
    "python": [".py"],
    "javascript": [".js", ".jsx", ".ts", ".tsx"],
    "java": [".java"],
    "go": [".go"],
    "rust": [".rs"],
    "csharp": [".cs"],
    "generic": [".h", ".hpp", ".cpp", ".cc", ".py", ".js", ".ts", ".java", ".go", ".rs", ".cs"],
}


def copy_template(src: Path, dst: Path, mapping: dict):
    text = src.read_text(encoding="utf-8")
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", str(value))
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(text, encoding="utf-8")


def render_build_verify(language: str, project_root: Path) -> str:
    """根据语言生成 build_verify.sh 内容。"""
    if language in ("cpp", "c"):
        return """#!/usr/bin/env bash
# build_verify.sh - CMake/CTest 构建验证脚本
# 成功判据：退出码 0 + build/build_report.txt 包含 BUILD_PASS + build/.build_sentinel 更新

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKFLOW_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${WORKFLOW_ROOT}/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
REPORT_FILE="${BUILD_DIR}/build_report.txt"
SENTINEL_FILE="${BUILD_DIR}/.build_sentinel"
MAX_RETRIES=3
RETRY=0

mkdir -p "${BUILD_DIR}"

echo "[build_verify] Project root: ${PROJECT_ROOT}" | tee "${REPORT_FILE}"
echo "[build_verify] Build dir: ${BUILD_DIR}" | tee -a "${REPORT_FILE}"

while [ ${RETRY} -lt ${MAX_RETRIES} ]; do
    echo "[build_verify] Attempt $((RETRY + 1))/${MAX_RETRIES}" | tee -a "${REPORT_FILE}"

    if [ ! -f "${BUILD_DIR}/CMakeCache.txt" ]; then
        echo "[build_verify] Configuring CMake..." | tee -a "${REPORT_FILE}"
        cmake -S "${PROJECT_ROOT}" -B "${BUILD_DIR}" -DCMAKE_BUILD_TYPE=Release 2>&1 | tee -a "${REPORT_FILE}"
    fi

    echo "[build_verify] Building..." | tee -a "${REPORT_FILE}"
    if cmake --build "${BUILD_DIR}" --parallel 2>&1 | tee -a "${REPORT_FILE}"; then
        echo "[build_verify] Build succeeded." | tee -a "${REPORT_FILE}"

        echo "[build_verify] Running CTest..." | tee -a "${REPORT_FILE}"
        run_ctest() {
            if cmake --version | head -n1 | grep -qE '3\\.([2-9][0-9]|1[0-9][0-9])'; then
                ctest --test-dir "${BUILD_DIR}" --output-on-failure
            else
                (cd "${BUILD_DIR}" && ctest --output-on-failure)
            fi
        }
        if run_ctest 2>&1 | tee -a "${REPORT_FILE}"; then
            echo "BUILD_PASS" >> "${REPORT_FILE}"
            date -u +%Y-%m-%dT%H:%M:%SZ > "${SENTINEL_FILE}"
            echo "[build_verify] All checks passed. Sentinel: ${SENTINEL_FILE}" | tee -a "${REPORT_FILE}"
            exit 0
        else
            echo "[build_verify] CTest failed." | tee -a "${REPORT_FILE}"
            echo "TEST_FAIL" >> "${REPORT_FILE}"
            exit 1
        fi
    else
        echo "[build_verify] Build failed." | tee -a "${REPORT_FILE}"
        RETRY=$((RETRY + 1))
    fi
done

echo "[build_verify] Exceeded max retries (${MAX_RETRIES})." | tee -a "${REPORT_FILE}"
echo "BUILD_FAIL" >> "${REPORT_FILE}"
exit 1
"""
    # 通用/其他语言版本
    return """#!/usr/bin/env bash
# build_verify.sh - 通用构建验证脚本
# 成功判据：退出码 0 + build/build_report.txt 包含 BUILD_PASS + build/.build_sentinel 更新

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKFLOW_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${WORKFLOW_ROOT}/.." && pwd)"
BUILD_DIR="${PROJECT_ROOT}/build"
REPORT_FILE="${BUILD_DIR}/build_report.txt"
SENTINEL_FILE="${BUILD_DIR}/.build_sentinel"
MAX_RETRIES=3
RETRY=0

mkdir -p "${BUILD_DIR}"

echo "[build_verify] Project root: ${PROJECT_ROOT}" | tee "${REPORT_FILE}"
echo "[build_verify] Build dir: ${BUILD_DIR}" | tee -a "${REPORT_FILE}"

detect_build() {
    if [ -f "${PROJECT_ROOT}/CMakeLists.txt" ]; then
        echo "cmake"
    elif [ -f "${PROJECT_ROOT}/Makefile" ]; then
        echo "make"
    elif [ -f "${PROJECT_ROOT}/package.json" ]; then
        echo "npm"
    elif [ -f "${PROJECT_ROOT}/pyproject.toml" ] || [ -f "${PROJECT_ROOT}/setup.py" ]; then
        echo "python"
    else
        echo "unknown"
    fi
}

BUILD_SYSTEM=$(detect_build)
echo "[build_verify] Detected build system: ${BUILD_SYSTEM}" | tee -a "${REPORT_FILE}"

while [ ${RETRY} -lt ${MAX_RETRIES} ]; do
    echo "[build_verify] Attempt $((RETRY + 1))/${MAX_RETRIES}" | tee -a "${REPORT_FILE}"

    case "${BUILD_SYSTEM}" in
        cmake)
            if [ ! -f "${BUILD_DIR}/CMakeCache.txt" ]; then
                cmake -S "${PROJECT_ROOT}" -B "${BUILD_DIR}" -DCMAKE_BUILD_TYPE=Release 2>&1 | tee -a "${REPORT_FILE}"
            fi
            BUILD_CMD=(cmake --build "${BUILD_DIR}" --parallel)
            TEST_CMD=(bash -c 'cd "'"${BUILD_DIR}"'" && ctest --output-on-failure')
            ;;
        make)
            BUILD_CMD=(make -C "${PROJECT_ROOT}")
            TEST_CMD=(make -C "${PROJECT_ROOT}" test)
            ;;
        npm)
            BUILD_CMD=(npm run build --prefix "${PROJECT_ROOT}")
            TEST_CMD=(npm test --prefix "${PROJECT_ROOT}")
            ;;
        python)
            BUILD_CMD=(python -m compileall "${PROJECT_ROOT}")
            # pytest 不可用时回退 unittest，再不可用则跳过测试
            if python -c "import pytest" >/dev/null 2>&1; then
                TEST_CMD=(python -m pytest "${PROJECT_ROOT}")
            elif python -c "import unittest" >/dev/null 2>&1; then
                # unittest 无测试时退出码为 5，接受 0/5 为成功
                TEST_CMD=(bash -c 'python -m unittest discover -s "'"${PROJECT_ROOT}"'" -p "test_*.py"; code=$?; [ $code -eq 0 ] || [ $code -eq 5 ]')
            else
                TEST_CMD=(bash -c 'echo "No test framework available, skip tests" && exit 0')
            fi
            ;;
        *)
            echo "[build_verify] Unknown build system, skipping build." | tee -a "${REPORT_FILE}"
            echo "BUILD_SKIP" >> "${REPORT_FILE}"
            date -u +%Y-%m-%dT%H:%M:%SZ > "${SENTINEL_FILE}"
            exit 0
            ;;
    esac

    echo "[build_verify] Building..." | tee -a "${REPORT_FILE}"
    if "${BUILD_CMD[@]}" 2>&1 | tee -a "${REPORT_FILE}"; then
        echo "[build_verify] Build succeeded." | tee -a "${REPORT_FILE}"
        echo "[build_verify] Running tests..." | tee -a "${REPORT_FILE}"
        if "${TEST_CMD[@]}" 2>&1 | tee -a "${REPORT_FILE}"; then
            echo "BUILD_PASS" >> "${REPORT_FILE}"
            date -u +%Y-%m-%dT%H:%M:%SZ > "${SENTINEL_FILE}"
            echo "[build_verify] All checks passed. Sentinel: ${SENTINEL_FILE}" | tee -a "${REPORT_FILE}"
            exit 0
        else
            echo "[build_verify] Tests failed." | tee -a "${REPORT_FILE}"
            echo "TEST_FAIL" >> "${REPORT_FILE}"
            exit 1
        fi
    else
        echo "[build_verify] Build failed." | tee -a "${REPORT_FILE}"
        RETRY=$((RETRY + 1))
    fi
done

echo "[build_verify] Exceeded max retries (${MAX_RETRIES})." | tee -a "${REPORT_FILE}"
echo "BUILD_FAIL" >> "${REPORT_FILE}"
exit 1
"""


def render_check_stale(extensions: list[str]) -> str:
    """根据扩展名生成 check_project_wiki_stale.py。"""
    ext_tuple = ", ".join(f'"{e}"' for e in extensions)
    return f'''#!/usr/bin/env python3
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

SOURCE_EXTENSIONS = ({ext_tuple})


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def find_module_files(workflow_root: Path, project_root: Path):
    """解析 project_wiki/*.md 顶部元数据，返回登记的文件集合。"""
    wiki_dir = workflow_root / "project_wiki"
    registered = {{}}  # rel_path -> {{"module": str, "sha": str|null}}
    for md_path in wiki_dir.glob("*.md"):
        if md_path.name == "overview.md":
            continue
        text = md_path.read_text(encoding="utf-8")
        m = re.search(r"<!--\\s*root_dirs:\\s*(.*?)-->", text, re.S)
        if not m:
            continue
        dirs_raw = m.group(1)
        root_dirs = re.findall(r"-\\s*(\\S+)", dirs_raw)
        for d in root_dirs:
            full_dir = project_root / d
            if not full_dir.exists():
                continue
            for ext in SOURCE_EXTENSIONS:
                for f in full_dir.rglob(f"*{{ext}}"):
                    rel = f.relative_to(project_root).as_posix()
                    registered[rel] = {{"module": md_path.stem, "sha": None}}
    return registered


def scan_disk(project_root: Path, source_dirs):
    """扫描磁盘上的源码文件。"""
    actual = set()
    for d in source_dirs:
        full_dir = project_root / d
        if not full_dir.exists():
            continue
        for ext in SOURCE_EXTENSIONS:
            for f in full_dir.rglob(f"*{{ext}}"):
                actual.add(f.relative_to(project_root).as_posix())
    return actual


def load_cache(workflow_root: Path):
    cache_path = workflow_root / ".review_cache.json"
    if cache_path.exists():
        return json.loads(cache_path.read_text(encoding="utf-8"))
    return {{}}


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
        print(f"[check_wiki_stale] {{wiki_dir}} not found, skip.")
        sys.exit(0)

    registered = find_module_files(workflow_root, project_root)
    source_dirs = list({{Path(p).parts[0] for p in registered}})

    if not source_dirs:
        # 模板项目或 module.md 未填写 root_dirs 时，扫描常见源码目录
        fallback_dirs = ["src", "source", "app", "lib", "libs"]
        source_dirs = [d for d in fallback_dirs if (project_root / d).exists()]
        if source_dirs:
            print(f"[check_wiki_stale] module.md 中未发现有效 root_dirs，回退扫描：{{source_dirs}}")
        else:
            print("[check_wiki_stale] 未发现任何源码目录，跳过漂移检测。")
            save_cache(workflow_root, {{}})
            sys.exit(0)

    actual = scan_disk(project_root, source_dirs)

    cache = load_cache(workflow_root)
    new_cache = {{}}

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
    print(f"新增文件 ({{len(added)}}):")
    for rel in sorted(added):
        print(f"  + {{rel}}")
    print(f"删除文件 ({{len(deleted)}}):")
    for rel in sorted(deleted):
        print(f"  - {{rel}}")
    print(f"大改文件 ({{len(changed)}}):")
    for rel in sorted(changed):
        print(f"  ~ {{rel}}")

    if args.patch and added:
        # 按目录找到对应 module.md 补登
        by_module = {{}}
        for rel in added:
            module = None
            for reg_rel, info in registered.items():
                if rel.startswith(str(Path(reg_rel).parent)):
                    module = info["module"]
                    break
            if not module:
                module = "overview"
            by_module.setdefault(module, []).append(rel)

        for module, files in by_module.items():
            md_path = wiki_dir / f"{{module}}.md"
            if not md_path.exists():
                md_path = wiki_dir / "overview.md"
            with open(md_path, "a", encoding="utf-8") as f:
                f.write("\\n## 自动补登文件\\n\\n")
                for rel in files:
                    f.write(f"- `{{rel}}`\\n")
        print(f"[check_wiki_stale] --patch: appended {{len(added)}} files to module docs.")

    save_cache(workflow_root, new_cache)

    has_stale = bool(added or deleted or changed)
    if has_stale and not (args.patch and not deleted and not changed):
        print("[check_wiki_stale] FAIL: project_wiki is stale.")
        sys.exit(1)

    print("[check_wiki_stale] PASS.")
    sys.exit(0)


if __name__ == "__main__":
    main()
'''


def init_project(project_root: Path, modules: list[str], root_dir_name: str = "AIRunWorkDocs", language: str = "cpp"):
    project_root = project_root.resolve()
    workflow_root = project_root / root_dir_name
    extensions = LANG_EXTENSIONS.get(language.lower(), LANG_EXTENSIONS["generic"])

    # 创建目录
    for sub in ["docs", "project_wiki/semantic_bridge", "red_lines/red_lines_by_stage",
                "tools", "runtime", "agents"]:
        (workflow_root / sub).mkdir(parents=True, exist_ok=True)

    # 生成语言相关的 tools
    (workflow_root / "tools" / "build_verify.sh").write_text(render_build_verify(language, project_root), encoding="utf-8")
    (workflow_root / "tools" / "build_verify.sh").chmod(0o755)
    (workflow_root / "tools" / "check_project_wiki_stale.py").write_text(render_check_stale(extensions), encoding="utf-8")
    (workflow_root / "tools" / "check_project_wiki_stale.py").chmod(0o755)

    # 复制语言无关的 tools
    for tool in ["new_tech_spec.py", "render_commit_msg.py", "pre-commit.sh"]:
        src = ASSETS_DIR / "tools" / tool
        dst = workflow_root / "tools" / tool
        shutil.copy2(src, dst)
        dst.chmod(0o755)

    # 生成 docs
    doc_titles = {
        "项目背景.md": "# 项目背景\n\n",
        "原始需求.md": "# 原始需求\n\n",
        "产品设计.md": "# 产品设计\n\n",
        "接口协议.md": "# 接口协议\n\n",
        "任务单.md": "# 任务单\n\n",
    }
    for name, content in doc_titles.items():
        (workflow_root / "docs" / name).write_text(content, encoding="utf-8")

    # 生成 project_wiki/overview.md
    overview_rows = []
    for m in modules:
        overview_rows.append(f"| `{m.capitalize()}/` | 待补充 | [{m}.md]({m}.md) |")
    overview_content = (ASSETS_DIR / "project_wiki" / "overview.md.tpl").read_text(encoding="utf-8")
    overview_content = overview_content.replace(
        "| `MList/` | 邮件列表展示、同步、过滤、多选编辑 | [mlist.md](mlist.md) |\n| `RMail/` | 邮件正文渲染、附件预览、AI 总结/翻译 | [rmail.md](rmail.md) |\n| `CMail/` | 邮件撰写、富文本编辑、附件上传、AI 润色 | [cmail.md](cmail.md) |\n| `Model/` | 领域模型 + DB 持久化 + 业务管理器 | [model.md](model.md) |",
        "\n".join(overview_rows)
    )
    overview_content = overview_content.replace("{{model_h_count}}", "0").replace("{{model_cpp_count}}", "0")
    (workflow_root / "project_wiki" / "overview.md").write_text(overview_content, encoding="utf-8")

    # 生成 module.md
    module_tpl = ASSETS_DIR / "project_wiki" / "module.md.tpl"
    for m in modules:
        copy_template(
            module_tpl,
            workflow_root / "project_wiki" / f"{m}.md",
            {
                "module_id": m,
                "root_dir": f"src/{m.capitalize()}",
                "desc": f"{m} 模块职责待补充",
                "module_name": m.capitalize(),
            }
        )

    # 生成语义桥
    semantic_map = {
        "term_mapping.md": "term_mapping.md.tpl" if language in ("cpp", "c") else "generic_term_mapping.md.tpl",
        "ui_mapping.md": "qt_ui_mapping.md.tpl" if language in ("cpp", "c") else "generic_ui_mapping.md.tpl",
        "db_protocol_mapping.md": "db_protocol_mapping.md.tpl" if language in ("cpp", "c") else "generic_db_protocol_mapping.md.tpl",
    }
    for dst_name, src_name in semantic_map.items():
        src = ASSETS_DIR / "project_wiki" / "semantic_bridge" / src_name
        shutil.copy2(src, workflow_root / "project_wiki" / "semantic_bridge" / dst_name)

    # 生成 red_lines
    shutil.copy2(ASSETS_DIR / "red_lines" / "red_lines.yaml.tpl",
                 workflow_root / "red_lines" / "red_lines.yaml")
    derive_red_lines(workflow_root / "red_lines" / "red_lines.yaml")

    # 生成 agents
    (workflow_root / "agents" / "code_style.md").write_text("# 代码风格\n\n待补充。\n", encoding="utf-8")
    (workflow_root / "agents" / "entrypoints.md").write_text("# 入口分流\n\n待补充。\n", encoding="utf-8")
    (workflow_root / "agents" / "pipeline.md").write_text("# 流水线编排\n\n待补充。\n", encoding="utf-8")

    # 生成 runtime 初始文件
    copy_template(
        ASSETS_DIR / "runtime" / "TECH_SPEC.md.tpl",
        workflow_root / "runtime" / "TECH_SPEC.md",
        {"title": "项目初始规范", "id": "INIT-001", "date": "2026-01-01", "do_1": "初始化工程骨架", "dont_1": "不实现具体业务"}
    )
    shutil.copy2(ASSETS_DIR / "runtime" / "subtasks_schema.json",
                 workflow_root / "runtime" / "subtasks_schema.json")
    (workflow_root / "runtime" / "subtasks.json").write_text("[]", encoding="utf-8")
    (workflow_root / "runtime" / "timeline.txt").write_text("# timeline\n\n", encoding="utf-8")

    print(f"[init_engineering_project] Initialized engineering-workflow at {workflow_root}")
    print(f"[init_engineering_project] Modules: {', '.join(modules)}")
    print(f"[init_engineering_project] Language: {language}")
    print(f"[init_engineering_project] Root dir: {root_dir_name}")


def parse_simple_yaml(text: str):
    """Parse the simple red_lines yaml format without external deps."""
    red_lines = []
    current = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped == "red_lines:":
            continue
        if stripped.startswith("- id:"):
            current = {"id": stripped.split(":", 1)[1].strip()}
            red_lines.append(current)
        elif current and ":" in stripped:
            key, val = stripped.split(":", 1)
            key = key.strip().lstrip("-")
            current[key] = val.strip()
    return {"red_lines": red_lines}


def derive_red_lines(yaml_path: Path):
    try:
        data = parse_simple_yaml(yaml_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"[init_engineering_project] yaml parse failed: {e}")
        return

    red_lines = data.get("red_lines", [])
    root = yaml_path.parent

    critical = [rl for rl in red_lines if rl.get("level") == "critical"]
    standard = [rl for rl in red_lines if rl.get("level") == "standard"]

    lines = ["# Critical 红线（启动即加载）\n\n"]
    for rl in critical:
        lines.append(f"## {rl['id']}: {rl['message']}\n")
        lines.append(f"- 触发：{rl['trigger']}\n")
        lines.append(f"- 动作：{rl['action']}\n\n")
    (root / "red_lines_critical.md").write_text("".join(lines), encoding="utf-8")

    by_stage = {}
    for rl in standard:
        stage = rl.get("stage", "global")
        by_stage.setdefault(stage, []).append(rl)

    for stage, items in by_stage.items():
        lines = [f"# {stage} 阶段红线\n\n"]
        for rl in items:
            lines.append(f"## {rl['id']}: {rl['message']}\n")
            lines.append(f"- 触发：{rl['trigger']}\n")
            lines.append(f"- 动作：{rl['action']}\n\n")
        (root / "red_lines_by_stage" / f"{stage}.md").write_text("".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", required=True)
    parser.add_argument("--modules", default="core,ui,model", help="逗号分隔模块名")
    parser.add_argument("--root-dir", default="AIRunWorkDocs", help="工程辅助根目录名，默认 AIRunWorkDocs")
    parser.add_argument("--language", default="cpp", choices=list(LANG_EXTENSIONS.keys()), help="项目语言，默认 cpp")
    args = parser.parse_args()

    modules = [m.strip().lower() for m in args.modules.split(",") if m.strip()]
    init_project(Path(args.project_root), modules, args.root_dir, args.language)


if __name__ == "__main__":
    main()
