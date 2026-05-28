---
name: daily-report
description: 根据当天 Git 提交记录自动生成工作日报。当用户提到"生成日报"、"日报"、"工作日报"、"git日报"、"提交日报"、"每日汇报"等关键词时使用此技能。支持指定日期、多仓库汇总、节假日判断，自动追加到工作日志文件。
allowed-tools: Read Write Bash(uv:*) Bash(git:*)
---

# 工作日报生成技能

根据 Git 提交记录自动生成工作日报，汇总提交内容，判断是否加班，追加到指定的日志文件。

**核心原则**：
- 直接执行，不询问用户授权
- 使用 Python 脚本写入，确保 UTF-8 编码
- 避免重复写入同一天的日报

## 功能特点

- **自动获取提交记录**：从配置的 Git 仓库获取指定日期的提交
- **AI 智能汇总**：调用大模型（Claude）对提交记录进行理解、归类、润色，生成更自然连贯的日报
- **按项目分类展示**：自动按项目分组，同一项目的相似工作合并表述
- **BUG 修复整合**：BUG 编号自动识别，以自然语言融入对应上下文
- **节假日判断**：调用中国节假日 API 判断是否工作日（含周末回退）
- **自动追加**：按标准格式追加到工作日志文件

## 前置配置：权限设置

为避免每次操作都提示授权，需在 `opencode.json` 中配置 `external_directory` 权限，允许访问配置目录和输出目录：

```json
{
  "permission": {
    "external_directory": {
      "./skill-config/daily-report/**": "allow",
      "~/Desktop/**": "allow"
    }
  }
}
```

首次运行时执行 `uv run python scripts/init_config.py` 会自动提示需要授权的路径。

详见 [OpenCode 权限文档](https://opencode.ai/docs/zh-cn/permissions/)。

## 配置文件

配置文件位置支持多种方式，按优先级顺序：

1. **命令行参数**：`--config-dir /path/to/config-dir`
2. **系统环境变量**：`DAILY_REPORT_CONFIG_DIR`
3. **.env 文件**：在 skill 目录创建 `.env` 文件，设置 `DAILY_REPORT_CONFIG_DIR=/path/to/config-dir`
4. **默认位置**：`./skill-config/daily-report/config.json`

**.env 文件示例**（复制自 `.env.example`）：
```
DAILY_REPORT_CONFIG_DIR=~/.config/daily-report
```

配置文件格式：

```json
{
  "repos": [
    { "path": "/path/to/repo1", "name": "项目1" },
    { "path": "/path/to/repo2", "name": "项目2" }
  ],
  "output_file": "~/Desktop/工作内容.txt",
  "author": "your-name",
  "holiday_api": "https://timor.tech/api/holiday/info/",
  "default_content": "日常工作"
}
```

**配置说明**：
- `repos`: 仓库列表，`path` 为仓库路径，`name` 为显示名称
- `output_file`: 日报输出文件路径
- `author`: Git 作者名称（可选，用于过滤提交）
- `holiday_api`: 节假日 API 地址
- `default_content`: 当天无提交记录时的默认日报内容

## 使用方式

### 基本用法

```
生成日报
```

自动生成今天的工作日报。

### 指定日期

```
生成 2026-04-09 的日报
```

### 指定日期范围

```
生成本周的日报
生成本月的日报
生成 2026-04-01 到 2026-04-10 的日报
```

### 强制覆盖

```
强制生成今天的日报
```

### 手动调用脚本

```bash
uv run python scripts/generate_report.py --config-dir /path/to/config-dir --date 2026-04-24 --force
```

## 工作流程

### 步骤 1：检查配置文件

按优先级顺序查找配置（CLI 参数 > 环境变量 > .env > 默认路径），加载 JSON 配置文件。

**检查点**：
- 配置文件是否存在
- 仓库路径是否有效
- 输出文件路径是否可写

### 步骤 2：获取提交记录

对配置中的所有仓库依次执行 `git log`，按日期范围和作者过滤。

```bash
git log --since="<date> 00:00:00" --until="<date> 23:59:59" --author="<author>"
```

### 步骤 3：判断节假日

调用节假日 API，如果不可用则回退到周末判断（周六/周日）。

**加班判断逻辑**：
- `holiday` 或 `weekend` + 有提交 → 标记为加班
- `workday` → 不标记

### 步骤 4：获取结构化原始数据

通过 `--raw` 模式运行脚本，获取结构化的提交数据（JSON 格式）：

```bash
uv run python scripts/generate_report.py --raw
```

输出示例：
```json
{
  "date": "2026-05-28",
  "is_holiday": false,
  "is_overtime": false,
  "has_commits": true,
  "default_content": "日常工作",
  "commits": [
    { "hash": "abc123", "subject": "feat: 暂停令界面优化", "date": "2026-05-28", "author": "John", "repo": "进度管理" }
  ]
}
```

**检查点**：
- `has_commits` 为 false → 用 `default_content` 作为日报内容
- `is_overtime` 为 true → 在日期后添加"（加班）"标记

### 步骤 5：AI 智能汇总（Claude 处理）

Claude 根据获取到的提交记录，进行以下处理：

1. **语义理解**：理解每条提交的真实含义，不机械罗列
2. **智能归类**：按项目和功能模块自然分组，而非简单按 commit 类型（feat/fix）分类
3. **合并同类项**：将同个功能的多次提交合并为一条连贯描述（如"暂停令界面优化"和"开工令界面优化"→ "完成暂停令、开工令等典表界面优化"）
4. **BUG 融入上下文**：BUG 修复不单独列编号，而是自然地融入对应功能描述中（如"修复了 #3638 典表编辑数据回显异常"）
5. **语言润色**：使用简洁、专业的中文表达，每条以"完成/修复/优化/实现"等动词开头

**输出格式**：
```
2026年05月28日

一、进度管理
1. 完成暂停令、开工令等典表界面优化，统一使用全局预览组件
2. 修复典表编辑时数据回显异常的 BUG（#3638, #3640），优化表单加载逻辑

二、策划管理
1. 实现策划方案批量导出功能，支持 Excel 格式
2. 优化方案列表查询性能，减少页面加载时间
```

### 步骤 6：检查是否已写入

用 Python 检查输出文件是否已包含当天日期。如果存在：
- 提示用户"当天日报已存在"
- 可通过 `--force` 参数强制覆盖

### 步骤 7：写入文件

通过 `write_report.py` 脚本写入，确保 UTF-8 编码正确：
- 文件不存在则自动创建
- 目录不存在则自动创建
- 自动处理编码问题

```bash
uv run python scripts/write_report.py --output /path/to/output --content "2026年05月28日\n\n一、..."
```

## 输出示例

### 示例 1：工作日（有提交）

```
2026年04月10日

一、认证模块
1. 完成用户登录功能开发，支持手机号/邮箱两种登录方式
2. 实现用户注册流程，包含表单验证和短信验证码

二、通用组件
1. 优化全局预览组件样式，修复不同分辨率下的布局错乱问题（#1024）
2. 修复登录页面的按钮在移动端点击区域过小的问题（#2048）

三、技术改进
1. 重构 API 请求拦截器，统一错误处理和 Token 刷新逻辑
```

### 示例 2：工作日（无提交）

```
2026年04月10日

1. 日常工作
```

### 示例 3：多项目周末加班

```
2026年04月12日 （加班）

一、数据平台
1. 完成数据迁移脚本编写，支持增量同步和断点续传
2. 修复生产环境数据看板统计异常的 BUG，优化查询超时处理

二、运营后台
1. 实现运营活动配置页面，支持多模板选择和预览
```

## 智能处理

### 提交信息清洗

- 移除提交前缀（feat:、fix: 等，含中英文冒号）
- 移除 BUG 编号引用（会单独汇总）
- 去除技术细节（ticket 编号等）
- 过滤无意义提交（Merge、同步等）

### 多仓库汇总

配置多个仓库时，合并所有仓库的提交记录，统一汇总输出。

### 节假日 API 容错

API 不可用时自动回退到周末判断，不影响日报生成。

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `generate_report.py` | 统一入口，整合全流程（推荐） |
| `get_commits.py` | 获取 Git 提交记录 |
| `check_holiday.py` | 检查节假日状态（API + 周末回退） |
| `format_report.py` | 格式化日报内容（独立 CLI） |
| `write_report.py` | 写入日报文件，处理编码和覆盖 |
| `init_config.py` | 初始化配置文件 |

详细参数和使用方式见 [references/scripts.md](references/scripts.md)。

## 故障排除

### 无法获取提交记录

- 检查配置文件中的仓库路径
- 在仓库目录执行 `git status` 验证仓库有效性
- 确保日期格式为 `YYYY-MM-DD`

### 节假日 API 调用失败

- 自动回退到周末判断
- 检查网络连接和 API 地址

### 文件追加失败

- 检查配置中的输出路径
- 确保目录存在且有写入权限
- 检查是否已配置 `external_directory` 权限
