#!/usr/bin/env python3
"""
new_tech_spec.py - 渲染 runtime/TECH_SPEC.md 初始模板。
用法：
    python3 new_tech_spec.py --title "新增域名过期提示条" --id FEAT-2026-001
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime, timezone

# Windows 控制台 UTF-8 输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

TEMPLATE = """# TECH_SPEC: {title}

## §0 AI 自检清单

- [ ] 已读 §1 功能边界，确认不做范围外改动。
- [ ] 已读 §3 模块地图，知道关键文件与方法。
- [ ] 已读 §5 不变式，承诺不碰清单内命名/文件。
- [ ] 已读 §7 演进事件，了解历史改动与踩坑点。

## §1 功能边界

- **做**：
  - 
- **不做**：
  - 

## §3 模块地图

| 文件 | 关键方法/类 | 职责 | 调用链 |
|------|------------|------|--------|
|  |  |  |  |

## §5 不变式

- 禁止改名：
- 禁止移动文件：
- 禁止绕过语义桥硬编码：

## §7 演进事件

### {id} 初始实现
- 日期：{date}
- 变更：
- Commit：

## §8 产物清单

| 子需求 | 产出文件 | Commit |
|--------|---------|--------|
|  |  |  |

## §9 版本

- v1.0 {id} 初始实现
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--title", required=True)
    parser.add_argument("--id", required=True)
    args = parser.parse_args()

    workflow_root = Path(os.environ.get("WORKFLOW_ROOT", Path(__file__).resolve().parent.parent)).resolve()
    runtime_dir = workflow_root / "runtime"
    runtime_dir.mkdir(parents=True, exist_ok=True)

    out_path = runtime_dir / "TECH_SPEC.md"
    date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    content = TEMPLATE.format(title=args.title, id=args.id, date=date)
    out_path.write_text(content, encoding="utf-8")

    sentinel = runtime_dir / ".tech_spec_ready"
    sentinel.write_text(datetime.now(timezone.utc).isoformat(), encoding="utf-8")

    print(f"[new_tech_spec] Created {out_path}")


if __name__ == "__main__":
    main()
