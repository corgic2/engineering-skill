#!/usr/bin/env bash
# build_verify.sh - CMake/CTest 构建验证脚本
# 成功判据：退出码 0 + build/build_report.txt 包含 BUILD_PASS + build/.build_sentinel 更新

set -euo pipefail

# 脚本位于 <project>/AIRunWorkDocs/tools/ 下
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
        # CMake >=3.20 支持 --test-dir，否则回退到 cd
        run_ctest() {
            if cmake --version | head -n1 | grep -qE '3\.([2-9][0-9]|1[0-9][0-9])'; then
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
