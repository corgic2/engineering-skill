# 通用使用案例：Web 后端服务新增"健康检查接口"

## 背景

项目：`OrderService`（Python 3.12 + FastAPI + pytest）。
需求：在订单服务中新增健康检查接口，返回数据库连接状态与缓存命中数。

## 步骤 1：初始化工程骨架

```bash
python3 ~/.kimi/skills/engineering-workflow/scripts/init_engineering_project.py \
  --project-root /path/to/OrderService \
  --modules api,service,repository,cache \
  --language python
```

生成：

```
OrderService/
├── AIRunWorkDocs/
│   ├── docs/
│   ├── project_wiki/
│   ├── red_lines/
│   ├── tools/
│   ├── runtime/
│   └── agents/
├── src/
│   ├── api/
│   ├── service/
│   ├── repository/
│   └── cache/
└── pyproject.toml
```

## 步骤 2：开发新需求

用户说：

> 在订单服务中新增健康检查接口，返回数据库连接状态与缓存命中数。

Kimi 进入 `engineering-workflow` 的"新需求"入口：

1. **设计稿收料**：读 `AIRunWorkDocs/docs/原始需求.md` 与接口协议。
2. **需求拆解**：输出五列表格 + `AIRunWorkDocs/runtime/subtasks.json`。
3. **代码定位**：五步定位法命中 `api/health.py` 与 `repository/db.py`。
4. **编码实现**：先看后写，新增 `get_health_status()` 与缓存指标收集。
5. **构建验证**：`./AIRunWorkDocs/tools/build_verify.sh` 按项目构建契约运行 `compileall` + `pytest`。
6. **运行验证**：启动 FastAPI 服务，`curl /health` 返回 200 与 JSON 字段。
7. **沉淀归档**：更新 `TECH_SPEC.md` §3/§7/§8/§9。
8. **提交收尾**：渲染 commit message，跑 `check_project_wiki_stale.py`，提交。

## 与 C++ 案例的差异

| 维度 | C++ 案例 | Python 案例 |
|------|---------|------------|
| 构建工具 | CMake/CTest | pytest/compileall |
| UI 语义桥 | Qt styled API | 无 UI，仅 API 响应格式映射 |
| 文件扩展名 | .h/.cpp | .py |
| 红线侧重 | 硬编码字号/颜色 | 硬编码连接串/密钥 |

核心 8 阶段流水线、project_wiki、red_lines、TECH_SPEC 完全复用，仅语言相关细节不同。
