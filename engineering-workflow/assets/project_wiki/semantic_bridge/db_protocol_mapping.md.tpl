# DB/协议映射：Schema/字段 ↔ DAO/序列化结构体

## CGI/协议字段

| 协议字段 | 序列化结构体 | 代码位置 | 说明 |
|---------|------------|---------|------|
| is_show_warning_icon_in_mailtab | `MailListSummary::is_show_warning_icon` | `Model/proto/mail_list.proto:45` | 是否显示顶部提示条 |
| domain_expire_time | `DomainWarning::expire_time` | `Model/proto/domain.proto:12` | 域名过期时间 |

## DB Schema

| 表/字段 | DAO 方法 | 迁移版本 | 说明 |
|--------|---------|---------|------|
| mail_tips.type | `MailTipsDao::insertType()` | v20260721 | 提示条类型 |

## 禁止硬编码

```cpp
// ❌ 错误
bool show = json.value("is_show_warning_icon_in_mailtab").toBool();

// ✅ 正确
auto summary = MailListSummary::fromProto(proto);
bool show = summary.is_show_warning_icon();
```
