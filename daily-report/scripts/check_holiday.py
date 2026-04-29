#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查节假日状态 - 支持 timor.tech API 及周末回退"""

import argparse
import json
from datetime import datetime
from typing import Optional
import urllib.request
import urllib.error

# 默认 API 地址
DEFAULT_API = "https://timor.tech/api/holiday/info/"


def check_holiday(date: str, api_url: Optional[str] = None) -> dict:
    """
    检查指定日期是否为节假日

    Args:
        date: 日期 (YYYY-MM-DD)
        api_url: 节假日 API 地址（可选，默认使用 timor.tech）

    Returns:
        节假日信息字典，含 is_workday (bool)、type (str)、name (str)
    """
    if api_url is None:
        api_url = DEFAULT_API

    try:
        # 构造请求 URL
        url = (
            f"{api_url.rstrip('/')}/{date}"
            if not api_url.rstrip("/").endswith(date)
            else api_url.rstrip("/")
        )
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        return _parse_response(data, date)
    except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
        return _fallback(date, str(e))


def _parse_response(data: dict, date: str) -> dict:
    """
    解析 API 响应，自动适配多种格式

    支持格式：
    1. timor.tech: {"code":0, "type":{"type":0, "name":"周三", "week":3}, "holiday":null}
       type.type: 0=工作日, 1=周末, 2=节假日, 3=补班
    2. 旧格式:     {"type": "workday", "name": "工作日"}
    """
    type_field = data.get("type")

    if isinstance(type_field, dict):
        # timor.tech 格式
        day_type = type_field.get("type", 0)
        day_name = type_field.get("name", "")

        # holiday 字段存在且为非 null 时，获取节假日名称
        holiday_info = data.get("holiday")
        holiday_name = ""
        if isinstance(holiday_info, dict) and holiday_info.get("name"):
            holiday_name = holiday_info["name"]

        # 0=工作日, 3=补班 → 工作日
        # 1=周末, 2=节假日 → 非工作日
        if day_type in (0, 3):
            display_type = "调休" if day_type == 3 else "工作日"
            is_work = True
        else:
            display_type = "节假日" if day_type == 2 else "周末"
            is_work = False

        display_name = holiday_name or day_name
    elif isinstance(type_field, str):
        # 旧格式（dateable.cn 等）
        display_type = type_field
        display_name = data.get("name", "")
        is_work = type_field == "workday"
    else:
        return _fallback(date, f"未知响应格式: {data}")

    return {
        "date": date,
        "type": display_type,
        "name": display_name,
        "is_workday": is_work,
    }


def _fallback(date: str, error: str) -> dict:
    """API 不可用时回退到周末判断"""
    dt = datetime.strptime(date, "%Y-%m-%d")
    is_weekend = dt.weekday() >= 5

    return {
        "date": date,
        "type": "weekend" if is_weekend else "workday",
        "name": "",
        "is_workday": not is_weekend,
        "fallback": True,
        "error": error,
    }


def main():
    parser = argparse.ArgumentParser(description="检查节假日状态")
    parser.add_argument("--date", required=True, help="日期 (YYYY-MM-DD)")
    parser.add_argument("--api-url", help=f"节假日 API 地址（默认 {DEFAULT_API}）")
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
