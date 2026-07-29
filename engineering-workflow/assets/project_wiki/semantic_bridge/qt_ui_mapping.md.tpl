# Qt UI 映射：设计 Token ↔ Qt 封装

## 文字样式

| 设计 Token | Qt 封装 API | 说明 |
|-----------|------------|------|
| Mobile/title_1 | `XYZStyledLabel::title1()` | 大标题 |
| Mobile/callout | `XYZStyledLabel::callout()` | 提示条正文 |
| Mobile/caption_2 | `XYZStyledLabel::caption2()` | 辅助说明 |

## 颜色

| 设计 Token | Qt 封装 API | 说明 |
|-----------|------------|------|
| Base/base_gray_100 | `XYZColor::baseGray100()` | 主文本色，自动响应 Dark Mode |
| Base/base_blue_500 | `XYZColor::baseBlue500()` | 主按钮色 |

## 按钮/组件

| 设计 Token | Qt 封装 API | 说明 |
|-----------|------------|------|
| button_blue_large | `XYZStyledButton::blueLarge()` | 大号主按钮 |

## 禁止硬编码

```cpp
// ❌ 错误
label->setFont(QFont("Arial", 15));
label->setTextColor(QColor("#1a1a1a"));

// ✅ 正确
label = XYZStyledLabel::callout();        // Mobile/callout
label->setTextColor(XYZColor::baseGray100());
```
