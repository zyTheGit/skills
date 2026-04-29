# 日报生成技能使用指南

## 快速开始

### 1. 初始化配置

首次使用时，skill 会自动创建配置文件：

```bash
uv run python scripts/init_config.py
```

配置文件位置：`~/.daily-report/config.json`

### 2. 修改配置

编辑配置文件，添加你的 Git 仓库路径：

```json
{
  "repos": [
    "/path/to/your/project-a",
    "/path/to/your/project-b"
  ],
  "output_file": "/path/to/your/output.txt",
  "author": "your-name",
  "holiday_api": "https://dateable.cn/holiday/info/"
}
```

**配置项说明**：
- `repos`: Git 仓库路径列表（支持多个仓库）
- `output_file`: 日报输出文件路径
- `author`: Git 作者名称（可选，用于过滤提交）
- `holiday_api`: 节假日 API 地址

### 3. 生成日报

**生成今天的日报**：
```
生成日报
```

**生成指定日期的日报**：
```
生成 2026-04-09 的日报
```

**生成本周的日报**：
```
生成本周的日报
```

## 示例输出

### 工作日示例

```
2026年4月10日
1. 完成用户认证模块开发
2. 修复登录页面样式问题
3. 优化数据库查询性能
```

### 周末加班示例

```
2026年4月12日 （加班）
1. 紧急修复生产环境bug
2. 完成数据迁移脚本
```

## 常见问题

### Q: 如何查看当前配置？

```bash
uv run python scripts/init_config.py --show
```

### Q: 如何添加新的仓库？

直接编辑配置文件，在 `repos` 数组中添加新路径。

### Q: 如何过滤特定作者的提交？

在配置文件中设置 `author` 字段。

### Q: 节假日判断不准确怎么办？

skill 会自动调用节假日 API，如果 API 不可用会回退到周末判断。

## 注意事项

1. 确保 Git 仓库路径正确
2. 确保有权限访问仓库
3. 输出文件目录必须存在
4. 节假日 API 需要网络连接

## 高级用法

### 多仓库汇总

配置多个仓库时，skill 会自动合并所有提交记录并统一汇总。

### 自定义日期范围

```
生成 2026-04-01 到 2026-04-10 的日报
```

### 查看脚本帮助

```bash
uv run python scripts/get_commits.py --help
uv run python scripts/check_holiday.py --help
uv run python scripts/format_report.py --help
```