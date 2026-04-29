---
name: zentao-bug-sync
description: 禅道 BUG Excel 双向同步工具。支持智能操作选择、自动初始化检查、默认文件路径。当用户提到禅道、BUG、缺陷、问题跟踪、同步、导出 Excel、批量更新状态、BUG 报表、AI 分析 BUG、步骤解析、根因分析、修复建议等场景时使用此技能。支持本地部署禅道 12.x 版本。默认只获取指派给当前用户的 BUG，字段使用中文显示。配置信息存放在外部目录，不包含敏感信息。获取 BUG 后自动解析步骤中的图片内容。支持本地结构化解析步骤内容，生成关键操作、环境信息、根因分析和修复建议。
---

# 禅道 BUG Excel 同步工具

通过 Python 脚本实现禅道 BUG 与 Excel 的双向同步，**智能检测用户意图**，自动选择合适的操作（fetch/push/sync/prompt）。

## 智能工作流

### 核心特性

1. **智能操作选择**：根据用户意图自动判断应执行 fetch、push、sync、analyze 还是 prompt
2. **默认文件路径**：Excel 文件默认保存在 `~/Desktop/zentao-bugs/`，自动查找最新文件
3. **自动初始化检查**：自动检测依赖安装、配置文件，提示用户完成初始化
4. **只获取自己的 BUG**：默认只获取指派给当前用户的 BUG（使用 `--all` 获取所有）
5. **中文显示**：类型、所属产品、所属模块、指派给、创建人等字段使用中文显示
6. **安全配置**：敏感凭据存放在外部目录，不提交到代码仓库
7. **自动图片解析**：获取 BUG 后自动使用 @image-analyzer 解析步骤中的图片内容
8. **本地结构化解析**：使用 `--analyze` 命令本地解析步骤内容，生成关键操作、环境信息、根因分析、修复建议

### 工作流程

当用户执行 `--fetch` 获取 BUG 后，自动执行以下步骤：

1. **获取 BUG 数据**：从禅道 API 获取 BUG 列表
2. **生成 Excel 文件**：创建包含所有字段的 Excel
3. **检测图片**：扫描每个 BUG 的步骤字段，提取图片链接
4. **自动解析图片**：对于包含图片的 BUG，使用 **@image-analyzer** skill 解析图片内容
5. **填充解析结果**：将图片解析结果写入 Excel 的"步骤解析"列

### 图片解析

当 BUG 步骤中包含图片链接时，根据 AI 的能力自动处理：

**情况 1：AI 有 vision 能力**

自动使用 vision 能力解析图片内容，将分析结果写入 Excel 的"步骤解析"列：

```
【图片分析】
- 错误信息：<识别的错误提示>
- 界面状态：<界面元素描述>
- 问题现象：<具体问题>
- 分析建议：<初步分析>
```

**情况 2：AI 无 vision 能力**

在"步骤解析"列生成解析建议，指导用户手动解析：

```
发现图片，请使用以下方式解析：
1. 在浏览器中打开图片链接查看
2. 使用 @image-analyzer skill 解析（如有安装）
3. 使用 Claude.ai 或其他 vision AI 工具

图片链接: http://192.168.0.205:29100/zentao/file-read-xxxx
```

**用户手动解析方法**：

如果用户需要手动解析图片，可以：
1. 复制 Excel 中的图片链接，在浏览器中打开
2. 使用 `@image-analyzer` skill（需安装）：
   ```
   @image-analyzer http://192.168.0.205:29100/zentao/file-read-xxxx "分析这个 BUG 截图"
   ```
3. 在 Claude.ai 网页版上传图片进行分析

## 配置文件

配置文件位置支持多种方式，按优先级顺序：

1. **技能目录 .env**：设置 `ZENTAO_BUG_SYNC_CONFIG_DIR=/path/to/config-dir`
2. **默认位置**：`~/.config/opencode/skill-config/zentao-bug-sync/`

**配置结构**：
```
~/.config/opencode/skill-config/zentao-bug-sync/
├── config.json      # 通用配置
└── .env             # 敏感凭据（URL、账号、密码）
```

**.env 文件格式**（存放敏感信息）：
```
ZENTAO_URL=http://192.168.0.xxx:xxx/zentao
ZENTAO_ACCOUNT=your_username
ZENTAO_PASSWORD=your_password
```

**config.json 格式**（通用配置）：
```json
{
  "zentao_url": "",
  "zentao_account": "",
  "zentao_password": "",
  "default_output_dir": "~/Desktop/zentao-bugs",
  "default_filename_format": "zentao_bugs_{date}.xlsx"
}
```

凭据优先级：
1. 配置目录下的 `.env` 文件（推荐）
2. 技能目录下的 `.env` 文件（兼容旧版）
3. `config.json` 文件（不推荐存放密码）

### 推荐使用方式（智能入口）

```bash
cd ~/.config/opencode/skills/zentao-bug-sync

# 首次使用：初始化配置
uv run scripts/zentao_cli.py --init

# 自动模式：智能判断操作
uv run scripts/zentao_cli.py              # 无文件 → fetch，有文件 → sync

# 指定操作
uv run scripts/zentao_cli.py --fetch      # 拉取自己的 BUG（默认）
uv run scripts/zentao_cli.py --fetch --all  # 拉取所有 BUG
uv run scripts/zentao_cli.py --push       # 推送更新
uv run scripts/zentao_cli.py --sync       # 增量同步
uv run scripts/zentao_cli.py --analyze    # 本地结构化解析步骤内容
uv run scripts/zentao_cli.py --analyze --all  # 解析所有 BUG
uv run scripts/zentao_cli.py --prompt     # 生成 AI 提示语
uv run scripts/zentao_cli.py --prompt --all  # 为所有 BUG 生成提示语
```

### 默认路径

| 路径 | 说明 |
|------|------|
| `~/Desktop/zentao-bugs/` | Excel 文件默认存放目录 |
| `zentao_bugs_YYYYMMDD.xlsx` | 默认文件名格式 |
| `~/.config/opencode/skill-config/zentao-bug-sync/` | 配置目录（默认） |

## 自动图片解析流程

当执行 `--fetch` 获取 BUG 后，**自动执行**以下步骤解析图片：

### 步骤 1：获取 BUG 并生成 Excel

```bash
uv run scripts/zentao_cli.py --fetch --output <excel_file>
```

Python 脚本自动：
- 从禅道 API 获取 BUG 数据
- 提取步骤中的图片链接
- 生成 Excel 文件，"图片链接"列填充完整 URL

### 步骤 2：读取 Excel 检测图片

读取生成的 Excel 文件，检查"图片链接"列：
- 对于图片链接不为空的 BUG，标记需要解析
- 统计需要解析的 BUG 数量

### 步骤 3：使用 @image-analyzer 解析图片

对于每个包含图片的 BUG，使用 **@image-analyzer** skill 解析：

```
@image-analyzer <图片URL> "请描述这个BUG截图中的：1)具体的错误信息或提示 2)界面状态和操作步骤 3)问题现象分析"
```

**解析要点**：
- 错误提示信息（错误码、错误消息）
- 界面状态（按钮状态、数据展示）
- 问题现象（数据缺失、显示异常）
- 可能原因提示

### 步骤 4：更新 Excel 的"步骤解析"列

将图片解析结果写入 Excel：
- 使用 openpyxl 打开 Excel 文件
- 将解析内容写入对应 BUG 的"步骤解析"列（第 15 列）
- 保存 Excel 文件

**解析内容格式**：
```
【图片分析】
- 错误信息：<从图片中识别的错误提示>
- 界面状态：<界面描述>
- 问题现象：<具体问题>
- 分析建议：<基于图片的初步分析>
```

### 步骤 5：向用户报告结果

解析完成后报告：
- 总共多少个 BUG
- 包含图片的 BUG 数量
- 已完成解析的 BUG 数量
- Excel 文件位置

**示例报告**：
```
获取完成！共 60 个 BUG，其中 45 个包含图片，已全部解析。
文件保存到: ~/Desktop/zentao-bugs/zentao_bugs_20260415.xlsx
```

## 快速开始

### 1. 初始化配置

```bash
uv run scripts/zentao_cli.py --init
```

自动创建配置目录和文件，提示填写禅道连接信息。

### 2. 配置连接信息

编辑配置目录下的 `.env` 文件：

```
ZENTAO_URL=http://192.168.0.xxx:xxx/zentao
ZENTAO_ACCOUNT=your_username
ZENTAO_PASSWORD=your_password
```

**或**使用初始化脚本查看配置：

```bash
uv run python scripts/init_config.py --show          # 显示配置
uv run python scripts/init_config.py --show-credentials  # 显示凭据
```

## 操作说明

### fetch: 拉取 BUG 到 Excel

```bash
uv run scripts/zentao_cli.py --fetch [--output FILE] [--status STATUS]
uv run scripts/zentao_cli.py --fetch --all  # 获取所有 BUG
```

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--output` | 输出文件 | ~/Desktop/zentao-bugs/zentao_bugs_YYYYMMDD.xlsx |
| `--status` | 状态过滤 | 全部 |
| `--all` | 获取所有 BUG | 只获取指派给自己的 |

### push: 推送 Excel 更新到禅道

```bash
uv run scripts/zentao_cli.py --push [--dry-run]
```

| 参数 | 说明 |
|------|------|
| `--dry-run` | 预览变更，不实际提交 |

可更新字段：状态、严重程度、优先级、指派给、解决方案

### sync: 增量同步

```bash
uv run scripts/zentao_cli.py --sync
```

对比 Excel 与禅道差异，仅更新修改过的 BUG。

### prompt: 生成 AI 提示语

```bash
uv run scripts/zentao_cli.py --prompt [--bug-id ID] [--all]
```

为指定 BUG 或所有 BUG 生成 AI 分析提示语，包含根因推测、修复建议、测试覆盖建议。
**自动检测步骤中的图片并提示使用 @image-analyzer 解析。**

### analyze: 本地结构化解析步骤内容

```bash
uv run scripts/zentao_cli.py --analyze [--bug-id ID] [--all]
```

**本地结构化解析** BUG 步骤内容，生成以下详细信息（无需外部 AI API）：

| 输出内容 | 说明 |
|----------|------|
| 关键操作 | 提取步骤中的动词操作（点击、输入、选择等） |
| 环境信息 | 提取环境关键词（浏览器、版本、服务器、数据库等） |
| 根因分析 | 基于关键词匹配推测可能的根本原因（置信度百分比） |
| 修复建议 | 基于 BUG 类型和关键词生成通用修复建议 |

**根因分析类别**：
- 数据问题、接口问题、界面问题、功能问题
- 逻辑问题、性能问题、兼容问题、权限问题、配置问题

**示例输出**：
```
【关键操作】
1. 点击登录按钮
2. 输入用户名和密码
3. 点击提交

【环境信息】
- 浏览器: Chrome 120
- 版本: v1.2.3

【根因分析】
- 接口问题 (置信度: 60%)
  匹配关键词: 接口, 超时
- 权限问题 (置信度: 30%)
  匹配关键词: 权限, 无权

【修复建议】
1. 检查接口请求参数是否正确
2. 验证接口响应数据格式
3. 添加接口异常处理和重试机制
```

## Excel 字段说明（全部中文显示）

| 列名 | 可编辑 | 说明 |
|------|--------|------|
| BUG ID | 否 | 禅道编号 |
| 标题 | 否 | BUG 标题 |
| 状态 | 是 | 激活/已解决/已关闭 |
| 严重程度 | 是 | 1-致命、2-严重、3-一般、4-建议 |
| 优先级 | 是 | 1-4 |
| 类型 | 否 | 代码错误/配置/安装部署/安全相关/性能问题等（中文） |
| 指派给 | 是 | 用户真实姓名（中文） |
| 创建人 | 否 | 用户真实姓名（中文） |
| 所属产品 | 否 | 产品名称（中文） |
| 所属模块 | 否 | 模块名称（中文） |
| 激活日期 | 否 | 只读 |
| 解决方案 | 是 | 设计如此/已修复/外部原因/不予解决等（中文） |
| 解决版本 | 是 | 版本号 |
| 步骤 | 否 | 重现步骤（HTML 格式，包含图片） |
| 步骤解析 | 自动 | 由 analyze 命令生成：关键操作、环境信息、根因分析、修复建议 |
| 图片链接 | 自动 | 从步骤中提取的图片完整 URL（可直接用于 @image-analyzer） |
| 期望结果 | 否 | 只读 |
| 实际结果 | 否 | 只读 |
| AI 提示语 | 自动 | 由 prompt 命令生成 |
| 最后同步时间 | 自动 | 同步时自动更新 |
| 同步状态 | 自动 | synced/pending/conflict |

## 类型映射（中文）

| 英文 | 中文 |
|------|------|
| codeerror | 代码错误 |
| config | 配置 |
| install | 安装部署 |
| security | 安全相关 |
| performance | 性能问题 |
| standard | 标准规范 |
| automation | 自动化测试 |
| trackthings | 跟踪事项 |
| newfeature | 新增需求 |
| designchange | 设计变更 |
| designdefect | 设计缺陷 |
| others | 其他 |

## 解决方案映射（中文）

| 英文 | 中文 |
|------|------|
| bydesign | 设计如此 |
| fixed | 已修复 |
| external | 外部原因 |
| wontfix | 不予解决 |
| postponed | 延期处理 |
| cannotreproduce | 无法重现 |
| tostory | 转为需求 |

## 条件格式

Excel 自动应用：
- 严重程度 1：红色背景
- 严重程度 2：橙色背景
- 状态 = 已关闭：灰色文字
- 状态 = 已解决：蓝色文字

## 状态流转

- 激活 → 已解决（需填写解决方案）
- 已解决 → 已关闭（确认修复）或 激活（问题仍存在）
- 已关闭 → 激活（问题重现）

## 注意事项

1. 确保 API 账号有 BUG 查看/编辑权限
2. 冲突以禅道服务器为准，标记为 conflict
3. 首次使用请运行 `--init` 检查初始化
4. 默认只获取指派给自己的 BUG，使用 `--all` 获取全部
5. 步骤中有图片时，使用 `@image-analyzer` skill 解析图片内容
6. **敏感凭据存放在外部目录**，不提交到代码仓库