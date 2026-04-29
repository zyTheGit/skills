#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查节假日状态"""

import argparse
import json
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error


def check_holiday(date: str, api_url: Optional[str] = None) -> dict:
    """
    检查指定日期是否为节假日

    Args:
        date: 日期 (YYYY-MM-DD)
        api_url: 节假日 API 地址（可选）

    Returns:
        节假日信息字典
    """
    if api_url is None:
        api_url = f"https://dateable.cn/holiday/info/{date}"

    try:
        url = f"{api_url.rstrip('/')}/{date}" if not api_url.endswith(date) else api_url
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
            return {
                "date": date,
                "type": data.get("type", "workday"),
                "name": data.get("name", ""),
                "is_workday": data.get("type") == "workday",
            }
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        # API 不可用时，回退到周末判断
        dt = datetime.strptime(date, "%Y-%m-%d")
        is_weekend = dt.weekday() >= 5  # 周六=5, 周日=6

        return {
            "date": date,
            "type": "weekend" if is_weekend else "workday",
            "name": "",
            "is_workday": not is_weekend,
            "fallback": True,
            "error": str(e),
        }


def main():
    parser = argparse.ArgumentParser(description="检查节假日状态")
    parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--api-url", help="节假日 API 地址（可选）")
    parser.add_argument("--output", help="输出文件路径（可选，默认输出到标准输出）")

    args = parser.parse_args()

    result = check_holiday(args.date, args.api_url)

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        from pathlib import Path

        Path(args.output).write_text(output, encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
