# 阶段：代码定位

## 目标

把需求项转换为"文件 + 行号 + 调用链"，Token 从全项目灌入压到 ~30K。

## 五步定位法

### 1. 意图消歧

- 只读 `project_wiki/overview.md` + 用户原话/需求项标题。
- 形成技术解读；仅当存在多种解读且影响改动范围时，才列出 2-4 种候选请用户确认。
- 禁止在此步骤读任何源码。

### 2. 模块定位

- 根据解读结果，读最可能相关的 1-2 份 `project_wiki/<module>.md`。
- 输出 2-3 个候选文件路径，附带一行职责说明。
- 仍禁止读源码。

### 3. 关键词搜索

- 项目存在 codegraph 索引（`.codegraph/`）时优先 `codegraph query <symbol>`；否则使用 `rg` 或 `ctags` 脚本搜索，**不进 LLM**。
- 输入候选搜索词集合（来自 5 维矩阵），输出命中文件与行号。
- 典型命令：
  ```bash
  codegraph query XYZTipsView   # 有索引时
  rg -n -t cpp "XYZTipsView|showWarningTips" src/MailClient/MList/   # 无索引兑底
  ```

### 4. 调用链追踪

- 有索引时用 `codegraph callers/callees <symbol>`、`codegraph impact <symbol> --depth 2` 取静态调用链与影响面，再读相关文件片段（~10K token）确认。
- 向上追踪调用方，向下追踪被调方，画出关键调用链。
- 标注数据流方向（如 CGI 字段 → 解析 → ViewModel → View）。
- **图谱只覆盖静态结构**：Qt 信号/槽、事件、回调等运行时连接图谱不可见，其链路必须以 wiki/经验库记录为准，不得因图谱无记录而判定不存在。

### 5. 验证确认

- 读函数实现（~5K token）。
- 输出最终改动点：文件路径、函数/类、修改类型（新增/修改/删除）、理由。
- 检查是否触发 UI/DB/协议红线，必要时加载语义桥。

## 输出格式

```markdown
## 定位结果：M1 邮件列表顶部小红条

### 技术解读
1. 在 MList 模块新增提示条组件（概率高）
2. 在 Model 层新增字段后透传到 UI（概率中）

### 候选文件
- `src/MailClient/MList/View/XYZTipsView.h/.cpp`
- `src/MailClient/MList/Controller/XYZMListController.cpp`

### 调用链
CGI(is_show_warning_icon) → MailListViewModel::updateTips() → XYZTipsView::setTipsType()

### 最终改动点
- `XYZTipsView.h`：新增枚举 `XYZMListTipsType_DomainExpire`
- `XYZTipsView.cpp`：新增显示分支
- `XYZMListController.cpp`：绑定点击事件 → `gotoDomainManagement()`
```
