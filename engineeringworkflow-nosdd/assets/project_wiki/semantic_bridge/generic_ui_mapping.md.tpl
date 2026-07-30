# UI 映射：设计 Token ↔ 框架封装

## 文字样式

| 设计 Token | 框架封装 API | 说明 |
|-----------|------------|------|
| <token_name> | `<StyledComponent>::<variant>()` | <说明> |

## 颜色

| 设计 Token | 框架封装 API | 说明 |
|-----------|------------|------|
| <token_name> | `<Color>::<name>()` | <说明，如自动响应 Dark Mode> |

## 按钮/组件

| 设计 Token | 框架封装 API | 说明 |
|-----------|------------|------|
| <token_name> | `<StyledButton>::<variant>()` | <说明> |

## 禁止硬编码

```<language>
// ❌ 错误
<硬编码示例>

// ✅ 正确
<按映射规则翻译示例>
```
