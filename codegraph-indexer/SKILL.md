---
name: codegraph-indexer
description: |
  使用 CodeGraph CLI 对代码库进行预索引，构建本地代码知识图谱（符号、调用关系、继承关系、引用边等），
  并通过图谱进行代码查询、调用链追踪、影响分析，减少 AI 代理的 token 消耗和工具调用次数。
  在以下场景触发：
  (1) 用户要求预索引、初始化索引、构建代码知识图谱或启用 CodeGraph；
  (2) 用户提到 codegraph、代码图谱、代码索引、符号索引；
  (3) 用户要求对项目/代码库进行索引、重新索引、增量同步或检查索引状态；
  (4) 用户要求通过 CodeGraph 查询符号、追踪调用链、分析影响范围或浏览项目结构；
  (5) 用户需要在项目中使用 codegraph 进行代码理解或架构分析。
---

# CodeGraph 代码预索引与查询

## 前置检查

1. 确认 `codegraph` CLI 可用：
   ```
   codegraph --version
   ```
   若不可用，执行全局安装：
   ```
   npm install -g @colbymchenry/codegraph
   ```

2. 确认当前工作目录为目标项目根目录。

## 索引工作流

### 初始化并首次索引

```
codegraph init -i
```

### 重新索引

```
codegraph index --force
```

大型项目索引输出过多时，使用安静模式：
```
codegraph index --force --quiet
```

### 增量同步

```
codegraph sync
```

### 索引完成后汇报

索引完成后必须执行 `codegraph status`，并向用户汇报以下关键数据：
- 索引文件数
- 节点总数 / 边总数
- 数据库大小
- 各语言文件分布

示例汇报格式：
```
索引完成：1,578 个文件，25,145 个节点，45,605 条边，数据库 41.6 MB
```

## 查询工作流

索引完成后，根据用户意图选择查询工具：

| 用户意图 | 命令 |
|---------|------|
| "查找 XXX 在哪里定义" | `codegraph query <symbol>` |
| "谁调用了 XXX" | `codegraph callers <symbol>` |
| "XXX 调用了谁" | `codegraph callees <symbol>` |
| "改 XXX 会影响哪些地方" | `codegraph impact <symbol> --depth 2` |
| "项目的文件结构是什么" | `codegraph files --max-depth 2` |
| "索引状态如何" | `codegraph status` |

复杂分析可组合多条命令，按 query → callers/callees → impact 的顺序递进。

## 大型项目优化

- 第三方库头文件过多导致索引膨胀时，建议将 `build/`、`third_party/`、`_deps/` 等目录加入 `.gitignore`
- C++ 项目若 `Common/` 或 `vendor/` 下包含大量外部库头文件，在 `.gitignore` 中加入对应路径可显著缩减索引体积
- 索引耗时过长时优先使用 `--quiet` 参数

## 故障排查

| 现象 | 处理 |
|------|------|
| `codegraph: command not found` | 执行 `npm install -g @colbymchenry/codegraph` |
| 索引极慢 | 检查大目录是否已排除；使用 `--quiet` |
| `database is locked` | 确认 CodeGraph 版本 >= 0.9；将项目移到本地磁盘（非网络共享） |
| 缺少符号 | 执行 `codegraph sync`；确认文件不在 `.gitignore` 中 |
| 索引已存在想重建 | 使用 `codegraph index --force` |

## 本地安全说明

- **100% 本地**：数据仅存储于项目目录 `.codegraph/codegraph.db`（SQLite）
- **零网络传输**：无外部 API 调用，无需 API Key
- **数据范围**：仅索引代码结构，不采集系统隐私信息
- **可控清除**：执行 `codegraph uninit` 或手动删除 `.codegraph/` 目录

## 参考

完整 CLI 命令列表及组合示例见 [references/cli-reference.md](references/cli-reference.md)。
