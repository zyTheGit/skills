# 脚本参考

## generate_report.py（推荐 - 统一入口）

自动化日报生成脚本，整合获取提交、节假日检查、格式化、写入全流程。

```bash
uv run python scripts/generate_report.py [--config-dir <path>] [--date YYYY-MM-DD] [--force]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--config-dir` | 否 | 配置目录路径，默认自动发现（.env > 环境变量 > ~/.config/opencode/skill-config/daily-report） |
| `--date` | 否 | 指定日期，默认今天 |
| `--since` / `--until` | 否 | 日期范围（与 --date 二选一） |
| `--force` | 否 | 强制覆盖已存在的日报 |

**功能**：
- 自动发现配置目录
- 获取所有仓库的提交记录
- 调用节假日 API（含周末回退）
- 逐条汇总提交内容
- 追加写入日报文件

---

## get_commits.py

获取 Git 提交记录。

```bash
uv run python scripts/get_commits.py --since 2026-04-10 --until 2026-04-10 --repo /path/to/repo [--author name]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--since` | 是 | 开始日期 (YYYY-MM-DD) |
| `--until` | 是 | 结束日期 (YYYY-MM-DD) |
| `--repo` | 是 | Git 仓库路径 |
| `--author` | 否 | 按作者过滤 |
| `--output` | 否 | 输出文件路径，默认输出到 stdout |

**输出**：JSON 格式的提交列表

---

## check_holiday.py

检查节假日状态。

```bash
UV run python scripts/check_holiday.py --date 2026-04-10 [--api-url https://...]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 是 | 日期 (YYYY-MM-DD) |
| `--api-url` | 否 | 节假日 API 地址 |
| `--output` | 否 | 输出文件路径 |

**输出**：JSON 格式的节假日信息，含 `is_workday` 字段

---

## format_report.py

格式化日报内容（独立 CL

```bash
uv run python scripts/format_report.py --date 2026-04-10 --commits commits.json --is-holiday false
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--date` | 是 | 日期 (YYYY-MM-DD) |
| `--commits` | 是 | 提交记录 JSON 文件路径 |
| `--is-holiday` | 是 | 是否为节假日 (true/false) |
| `--default-content` | 否 | 无提交时的默认内容（默认"日常工作"） |
| `--output` | 否 | 输出文件路径 |

---

## write_report.py

写入日报到文件，处理编码和覆盖逻辑。

```bash
uv run python scripts/write_report.py --output /path/to/output.txt --content "日报内容"
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--output` | 是 | 输出文件路径 |
| `--content` | 否 | 日报内容（与 --file 二选一） |
| `--file` | 否 | 日报文件路径（与 --content 二选一） |
| `--mode` | 否 | 写入模式：append（默认）/ overwrite |
| `--overwrite-date` | 否 | 覆盖指定日期的日报 |
| `--check-date` | 否 | 仅检查日期是否已存在，不写入 |

---

## init_config.py

初始化配置文件。

```bash
uv run python scripts/init_config.py [--config-dir <path>] [--show]
```

**参数**：

| 参数 | 必需 | 说明 |
|------|------|------|
| `--config-dir` | 否 | 配置目录路径 |
| `--show` | 否 | 显示当前配置（不初始化） |
