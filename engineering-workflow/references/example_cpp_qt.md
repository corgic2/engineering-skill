# C++ 使用案例：Qt 邮件客户端新增"域名过期提示条"

## 背景

项目：`QtMailClient`（C++17 + Qt6 + CMake）。
需求：邮件列表顶部出现红色提示条，提示用户域名即将过期，点击跳转域名管理页。

## 步骤 1：初始化工程骨架（首次）

用户说：

```
为我的 QtMailClient 项目初始化工程工作流，模块有 MList、RMail、CMail、Model，语言是 C++。
```

Kimi 执行：

```bash
python3 ~/.kimi/skills/engineering-workflow/scripts/init_engineering_project.py \
  --project-root /path/to/QtMailClient \
  --modules mlist,rmail,cmail,model \
  --language cpp

# 或自定义根目录名
python3 ~/.kimi/skills/engineering-workflow/scripts/init_engineering_project.py \
  --project-root /path/to/QtMailClient \
  --modules mlist,rmail,cmail,model \
  --language cpp \
  --root-dir Agentic
```

生成：

```
QtMailClient/
├── AIRunWorkDocs/           # AI/工程辅助根目录
│   ├── docs/                # 业务文档
│   ├── project_wiki/        # 代码侧地图
│   │   ├── overview.md
│   │   ├── mlist.md
│   │   ├── rmail.md
│   │   ├── cmail.md
│   │   ├── model.md
│   │   └── semantic_bridge/
│   │       ├── term_mapping.md
│   │       ├── ui_mapping.md
│   │       └── db_protocol_mapping.md
│   ├── red_lines/
│   │   ├── red_lines.yaml
│   │   ├── red_lines_critical.md
│   │   └── red_lines_by_stage/
│   ├── tools/
│   │   ├── build_verify.sh
│   │   ├── check_project_wiki_stale.py
│   │   ├── new_tech_spec.py
│   │   ├── render_commit_msg.py
│   │   └── pre-commit.sh
│   ├── runtime/
│   │   ├── TECH_SPEC.md
│   │   ├── subtasks.json
│   │   ├── subtasks_schema.json
│   │   └── timeline.txt
│   └── agents/
│       ├── code_style.md
│       ├── entrypoints.md
│       └── pipeline.md
├── src/                     # 项目源码
└── CMakeLists.txt
```

## 步骤 2：开发新需求

用户说：

```
按 PRD 在邮件列表顶部加红色提示条，提示域名即将过期，点击跳转管理页。
```

Kimi 进入 `engineering-workflow` 的"新需求"入口：

### 2.1 设计稿收料

- PRD 在 `AIRunWorkDocs/docs/原始需求.md`。
- CGI 协议字段在 `AIRunWorkDocs/docs/接口协议.md`：新增 `is_show_warning_icon_in_mailtab`。

### 2.2 需求拆解

输出五列表格：

| 序号 | 需求项 | 类型 | 数据来源 | 关联设计稿 |
|------|--------|------|---------|-----------|
| M1 | 邮件列表顶部小红条 | 新增 UI | CGI 字段 is_show_warning_icon_in_mailtab | 153:74513 |
| M2 | 点击小红条跳转管理页 | 新增交互 | TAPD 原文 | 153:74521 |

生成 `AIRunWorkDocs/runtime/subtasks.json`。

**HK-1**：用户确认 subtasks。

### 2.3 代码定位

按五步定位法：

1. 读 `AIRunWorkDocs/project_wiki/overview.md` → 命中 `MList/` 模块。
2. 读 `AIRunWorkDocs/project_wiki/mlist.md` → 命中 `XYZTipsView.h/.cpp`。
3. `rg "XYZTipsView|showWarningTips" src/MList/` → 确认文件与调用方。
4. 读 `XYZTipsView.cpp` 相关片段 → 追踪 `ViewModel::updateTips()` 调用链。
5. 查 `AIRunWorkDocs/project_wiki/semantic_bridge/ui_mapping.md` → 红色小条对应 `XYZStyledLabel::callout()` + `XYZColor::baseRed500()`。

### 2.4 编码实现

自底向上改动：

- `Model/proto/mail_list.proto`：新增字段。
- `Model/MailListSummary.cpp`：解析字段。
- `MList/View/XYZTipsView.h`：新增枚举 `XYZMListTipsType_DomainExpire`。
- `MList/View/XYZTipsView.cpp`：新增显示分支。
- `MList/Controller/XYZMListController.cpp`：绑定点击 → `gotoDomainManagement()`。

### 2.5 编译验证

```bash
./AIRunWorkDocs/tools/build_verify.sh
```

产出 `build/build_report.txt` + `build/.build_sentinel`。

### 2.6 运行验证

启动 Qt 程序，截图核对：

- 邮件列表顶部出现红色提示条。
- 点击后跳转域名管理页。
- 日志命中 `XYZLOG_WARN("show domain expire tips")`。

### 2.7 沉淀归档

更新 `AIRunWorkDocs/runtime/TECH_SPEC.md`：

- §3 模块地图增加 `XYZTipsView` 调用链。
- §7 新增 ITER-1 记录。
- §8 产物清单记录 M1/M2 与 commit。

**HK-2**：用户确认"沉淀 ok"。

### 2.8 提交收尾

```bash
./AIRunWorkDocs/tools/render_commit_msg.py --type feat --scope MList \
  --subject "新增域名过期提示条" \
  --body "M1: 顶部提示条; M2: 点击跳转管理页" \
  --footer "Closes FEAT-2026-001"

./AIRunWorkDocs/tools/check_project_wiki_stale.py
git commit -F .git/COMMIT_EDITMSG_CPP_WORKFLOW
```

**HK-3**：用户确认"提交/go"。

## 步骤 3：新会话接力

一周后新会话，用户说：

```
继续做 FEAT-2026-001 的增量迭代，小红条要支持两种状态。
```

Kimi 自动：

1. 读 `AIRunWorkDocs/runtime/TECH_SPEC.md` §0/§1/§3/§5/§7。
2. 读 `AIRunWorkDocs/runtime/subtasks.json`，看到 M1/M2 为 DONE。
3. 输出现场快报：接下来新增 M3"小红条支持两种状态"，当前阶段 locate。
4. 从代码定位开始继续推进。
