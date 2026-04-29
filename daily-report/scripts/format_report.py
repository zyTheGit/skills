#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""格式化日报内容 - 独立 CLI 工具"""

import argparse
import json
import sys
from pathlib import Path

from common import format_report

# 确保 Windows 上的 UTF-8 输出
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="格式化日报内容")
    parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--commits", required=True, help="提交记录 JSON 文件路径")
    parser.add_argument(
        "--is-holiday",
        type=lambda x: x.lower() == "true",
        required=True,
        help="是否为节假日 (true/false)",
    )
    parser.add_argument(
        "--default-content", default="日常工作", help="无提交时的默认内容"
    )
    parser.add_argument("--output", help="输出文件路径（可选，默认输出到标准输出）")

    args = parser.parse_args()

    # 读取提交记录
    commits_data = json.loads(Path(args.commits).read_text(encoding="utf-8-sig"))

    # 格式化日报
    report = format_report(
        args.date, commits_data, args.is_holiday, args.default_content
    )

    if args.output:
        Path(args.output).write_text(report, encoding="utf-8")
        print(f"日报已写入: {args.output}")
    else:
        print(report)


if __name__ == "__main__":
    main()
