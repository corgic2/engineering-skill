# TECH_SPEC.md 模板

每个需求必须产出一份 git-tracked 的 `runtime/TECH_SPEC.md`，结构如下：

```markdown
# TECH_SPEC: <一句话目标>

## §0 AI 自检清单

- [ ] 已读 §1 功能边界，确认不做范围外改动。
- [ ] 已读 §3 模块地图，知道关键文件与方法。
- [ ] 已读 §5 不变式，承诺不碰清单内命名/文件。
- [ ] 已读 §7 演进事件，了解历史改动与踩坑点。

## §1 功能边界

- **做**：<明确包含>
- **不做**：<明确排除>

## §3 模块地图

| 文件 | 关键方法/类 | 职责 | 调用链 |
|------|------------|------|--------|
| `src/MList/XYZTipsView.cpp` | `setTipsType()` | 显示顶部提示条 | ViewModel → setTipsType → updateUI |

## §5 不变式

- 禁止改名：`XYZMListTipsType_*` 前缀保留。
- 禁止移动文件：`XYZTipsView.h/.cpp` 位置固定。
- 禁止绕过 `ui_mapping.md` 硬编码字号/颜色。

## §7 演进事件

### ITER-1 初始实现
- 日期：2026-07-21
- 变更：新增 M1 顶部小红条
- Commit：abc1234

### BUG-1 修复点击无响应
- 日期：2026-07-22
- 根因：信号槽未连接
- Commit：def5678

## §8 产物清单

| 子需求 | 产出文件 | Commit |
|--------|---------|--------|
| M1 | `XYZTipsView.h/.cpp` | abc1234 |

## §9 版本

- v1.0 初始实现
- v1.1 修复 BUG-1
```
