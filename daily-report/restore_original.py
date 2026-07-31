# -*- coding: utf-8 -*-
"""从会话记录快照恢复原始日报文件（2022/08/18 ～ 2026/07/31）"""
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE = pathlib.Path(__file__).parent
SNAPSHOT = BASE / "full_snapshots.txt"
OUTPUT = pathlib.Path(r"C:\Users\hpee2\Desktop\工作内容.txt")

content = SNAPSHOT.read_text(encoding="utf-8")
lines = content.split("\n")

# ---- 1. 提取 2300b428 的完整快照段 ----
start = None
end = None
for i, line in enumerate(lines):
    if line.startswith("TEXT: 1\t2022/08/18"):
        start = i
    if start is not None and start < i < start + 13000 and "1. 日常工作" in line:
        end = i
        break

assert start is not None and end is not None, f"快照边界未找到: start={start}, end={end}"

snap_lines = []
for line in lines[start : end + 1]:
    # 去掉 TEXT: 前缀和行号前缀
    if line.startswith("TEXT: "):
        line = line[len("TEXT: ") :]
    # 去掉行号 (数字 + tab)
    line = re.sub(r"^\d+\t", "", line)
    snap_lines.append(line)

# 去除尾部多余空行
while snap_lines and snap_lines[-1].strip() == "":
    snap_lines.pop()

part1 = "\n".join(snap_lines)
print(f"快照段: 行 {start}-{end}, 恢复 {len(snap_lines)} 行")

# ---- 2. 07-28 / 07-29 / 07-30 原文（来自写入命令） ----
part2 = """2026年07月28日

一、进度管理
1. 优化青赔管理索赔详情页头部交互，长文本支持展开收起功能并调整按钮格式

2026年07月29日

一、进度管理
1. 优化索赔管理界面，替换自定义文本截断为 el-tooltip 显示完整内容

二、策划管理
1. 修复投资计划弹窗相关多个问题，包括弹窗打开时表单赋值异常、关闭时未清空选项和重置表单项
2. 为长标题添加 tooltip 提示，优化溢出文本显示

三、物资管理
1. 新增物资管理模块，包含施工仓库、到货验收、运单签收功能
2. 重构施工仓库填报页，完善子仓库管理

2026年07月30日
一、进度管理
1. 完成青赔导入区域（ClaimsImportArea）组件支持外部控制操作按钮功能

二、小程序
1. 修复青赔自定义提示接口报错提示问题，优化错误处理逻辑
2. 修复提交审核时前置提交报错弹框显示不完整的问题

三、物资管理
1. 调整施工仓库 API 路径、字段映射与视图配置
2. 将子仓库弹框替换为抽屉组件，优化表单交互体验
3. 重构 src/utils 目录结构，按职责拆分子目录并统一导入路径

2026年07月31日
一、物资管理
1. 完善施工仓库功能，新增仓库查询页面和仓储综合查询页面，支持按条件查询仓库信息
2. 补充 single-select 表格组件传参使用说明文档"""

full = part1.rstrip() + "\n\n" + part2

# 备份当前（重建版）后写入恢复版
if OUTPUT.exists():
    backup = BASE / "working_backup_rebuilt.txt"
    backup.write_text(OUTPUT.read_text(encoding="utf-8"), encoding="utf-8")
    print(f"已备份当前文件 -> {backup}")

OUTPUT.write_text(full, encoding="utf-8")
print(f"已恢复 -> {OUTPUT} ({len(full)} 字符, {len(full.splitlines())} 行)")
