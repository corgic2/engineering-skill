# CodeGraph CLI 完整命令参考

## 索引管理

| 命令 | 作用 |
|------|------|
| `codegraph init` | 初始化 `.codegraph/` 目录 |
| `codegraph init -i` | 初始化并执行首次索引 |
| `codegraph index` | 完整索引当前项目 |
| `codegraph index --force` | 强制重建索引 |
| `codegraph index --quiet` | 安静模式索引（减少输出） |
| `codegraph sync` | 增量同步变更 |
| `codegraph status` | 显示索引统计信息 |
| `codegraph uninit` | 移除当前项目的 CodeGraph |

## 符号查询

| 命令 | 作用 |
|------|------|
| `codegraph query <name>` | 按名称搜索符号 |
| `codegraph query <name> --kind class` | 限定节点类型搜索 |
| `codegraph query <name> --limit 20` | 限制返回数量 |
| `codegraph query <name> --json` | JSON 格式输出 |

## 调用链分析

| 命令 | 作用 |
|------|------|
| `codegraph callers <symbol>` | 查找调用该符号的位置 |
| `codegraph callees <symbol>` | 查找该符号调用的目标 |
| `codegraph impact <symbol> --depth 2` | 分析修改影响范围 |
| `codegraph affected <files...>` | 查找被变更文件影响的测试文件 |

## 文件浏览

| 命令 | 作用 |
|------|------|
| `codegraph files` | 列出已索引文件结构 |
| `codegraph files --max-depth 3` | 限制目录深度 |
| `codegraph files --filter src` | 过滤特定路径 |

## 常用组合示例

```bash
# 快速了解项目架构
codegraph status
codegraph files --max-depth 2

# 追踪某个类的影响范围
codegraph query MyClass
codegraph callers MyClass --limit 10
codegraph impact MyClass --depth 2

# CI 场景：获取变更影响的测试文件
git diff --name-only | codegraph affected --stdin --quiet
```

## 节点类型（kind）速查

`query --kind` 支持的值：`class`、`method`、`function`、`struct`、`enum`、`enum_member`、`type_alias`、`variable`、`file`、`import`
