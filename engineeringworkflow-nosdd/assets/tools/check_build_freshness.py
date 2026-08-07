#!/usr/bin/env python3
"""Fail when a reused build result is stale.

RL-01 闭环：构建成功以退出码 0、BUILD_PASS 和最新 sentinel 同时成立为准。
本脚本在「引用既有构建结果而非本轮新跑构建」时使用，校验：
1. build/<platform>/.build_sentinel 存在；
2. build/<platform>/build_report.txt 包含 BUILD_PASS；
3. sentinel 的修改时间不早于源码与构建登记文件的最新修改时间。

用法：python check_build_freshness.py <platform>
<platform> 为 build/ 下的子目录名（如 windows-x64 / linux-arm32），由项目自行定义。
"""

from __future__ import print_function

import sys
from pathlib import Path


# AIRunWorkDocs/tools/<本脚本> → AIRunWorkDocs → 项目根
PROJECT_ROOT = Path(__file__).resolve().parents[2]
SOURCE_SUFFIXES = {
    ".h",
    ".hpp",
    ".c",
    ".cc",
    ".cpp",
    ".cxx",
    ".ui",
    ".qrc",
    ".qss",
    ".xml",
    ".ts",
    ".py",
    ".js",
    ".ts",
    ".java",
    ".go",
    ".rs",
}
# 构建登记文件：修改后必须重新构建。按项目技术栈裁剪。
BUILD_MANIFESTS = ("CMakeLists.txt", "Makefile", "package.json", "pom.xml", "build.gradle")
SOURCE_DIRS = ("src", "lib", "include")


def fail(message):
    print("[check_build_freshness] FAIL: {0}".format(message))
    return 1


def newest_input_mtime():
    candidates = []
    for name in SOURCE_DIRS:
        src_root = PROJECT_ROOT / name
        if src_root.is_dir():
            for path in src_root.rglob("*"):
                if path.is_file() and path.suffix.lower() in SOURCE_SUFFIXES:
                    candidates.append(path)
    for name in BUILD_MANIFESTS:
        path = PROJECT_ROOT / name
        if path.is_file():
            candidates.append(path)
    cmake_dir = PROJECT_ROOT / "cmake"
    if cmake_dir.is_dir():
        for path in cmake_dir.rglob("*.cmake"):
            if path.is_file():
                candidates.append(path)
    if not candidates:
        return None, None
    newest = max(candidates, key=lambda p: p.stat().st_mtime)
    return newest.stat().st_mtime, newest


def main(argv):
    build_root = PROJECT_ROOT / "build"
    valid_platforms = (
        sorted(p.name for p in build_root.iterdir() if p.is_dir())
        if build_root.is_dir()
        else []
    )
    if len(argv) != 2 or argv[1] not in valid_platforms:
        print(
            "[check_build_freshness] 用法: python check_build_freshness.py <{0}>".format(
                "|".join(valid_platforms) if valid_platforms else "platform（build/ 下暂无平台目录）"
            )
        )
        return 2

    platform = argv[1]
    build_dir = build_root / platform
    sentinel = build_dir / ".build_sentinel"
    report = build_dir / "build_report.txt"

    if not sentinel.is_file():
        return fail("缺少 sentinel: {0}，请先运行对应平台构建脚本".format(sentinel))
    if not report.is_file():
        return fail("缺少构建报告: {0}".format(report))
    if "BUILD_PASS" not in report.read_text(encoding="utf-8", errors="replace"):
        return fail("构建报告缺少 BUILD_PASS 标记: {0}".format(report))

    src_mtime, src_path = newest_input_mtime()
    if src_mtime is None:
        print("[check_build_freshness] PASS: 尚无源码输入，sentinel 与 BUILD_PASS 成立")
        return 0

    sentinel_mtime = sentinel.stat().st_mtime
    if sentinel_mtime < src_mtime:
        return fail(
            "sentinel 过期：{0} 的修改晚于最近构建，需重新构建 {1}".format(
                src_path.relative_to(PROJECT_ROOT).as_posix(), platform
            )
        )

    print(
        "[check_build_freshness] PASS: {0} sentinel 未过期（最新输入 {1}）".format(
            platform, src_path.relative_to(PROJECT_ROOT).as_posix()
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
