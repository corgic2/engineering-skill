# 阶段：需求拆解

## 目标

把产品语言翻译成代码指令，产出结构化 `subtasks.json` 与五列表格。

## 拆解五规则

### 1. 范围识别（硬关键词表）

命中以下任一关键词，强制拆为客户端/移动端/项目端项：

| 类别 | 关键词 |
|------|--------|
| 平台/端 | 手机上、手机端、移动端、iOS、Android、客户端、App、Web、桌面端 |
| 原生控件/交互 | Toast、弹窗、浮层、小红条、红点、Tab 角标、下拉刷新、侧滑、长按、点击、按钮、输入框 |
| 框架/技术栈 | 按项目实际框架补充（如 QWidget/QML、React/Vue、Flask/FastAPI 等） |
| 页面/接口术语 | 输入法、键盘展开、全屏弹窗、actionsheet、导航栏、API、endpoint |

### 2. 设计稿归宿校验

每张设计稿必须归为以下三类之一：

- **载体**：本次需求要实现的独立页面/组件。
- **状态变体**：同一载体的不同状态（如空态、错误态、加载态）。
- **纯参考**：不影响实现，仅用于理解上下文。

禁止用"参考图"当未归类垃圾桶。

### 3. 拦截点清单

任何"X 触发 Y"类交互必须输出可验证清单：

| 触发元素 X | 触发事件 | 响应 Y | 依据来源 |
|-----------|---------|--------|---------|
| 全选按钮 | 点击 | Toast 提示超量 | figma node 153:74513 |
| 小红条 | 点击 | 跳转管理页 | TAPD 原文引用 |

依据来源只接受：设计稿标注/箭头/nodeId、文档原文直接引用、用户原话引用。

### 4. 领域联想（5 维搜索矩阵）

把需求项扩展为代码搜索词：

1. **平台/框架 API**：项目所用框架的核心 API（如 GUI 框架控件、Web 框架路由、ORM 模型等）。
2. **功能语义**：产品意图的英文同义词（小红条 → tips/banner/warning/notice）。
3. **项目命名习惯**：show* / handle* / on* / goto* / setup* / get* / set* 等前缀。
4. **协议/代理**：Delegate、Notification、Callback、Observer、Middleware、Interceptor。
5. **跨模块通信**：Signal、Event、Handler、MessageBus、RPC、WebSocket 等价物。

### 5. 翻译产物

人类可读的五列表格：

| 序号 | 需求项 | 类型 | 数据来源 | 关联设计稿 nodeId |
|------|--------|------|---------|------------------|
| M1 | 邮件列表顶部小红条 | 新增 UI | CGI 字段 is_show_warning_icon | 153:74513 |

机器可读的 `runtime/subtasks.json`：

```json
[
  {
    "id": "M1",
    "title": "邮件列表顶部小红条",
    "type": "新增UI",
    "data_source": "CGI字段is_show_warning_icon",
    "figma_node": "153:74513",
    "depends_on": [],
    "status": "PENDING",
    "current_stage": "locate",
    "related_commit": ""
  }
]
```
