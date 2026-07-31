# -*- coding: utf-8 -*-
"""日报查询脚本（方案B：脚本化查询，避免 cat 全文占用上下文）

用法:
  uv run python query_report.py --date 2026-04-10           # 查询某天
  uv run python query_report.py --keyword 青赔 --limit 5     # 按关键词搜最近5条
  uv run python query_report.py --since 2026-07-01 --until 2026-07-15  # 范围查询
  uv run python query_report.py --month 2026-07             # 列出某月上班日报日期（含星期）
  uv run python query_report.py --date 2026-04-10 --all-files          # 搜索主文件+归档文件
"""
import argparse
import pathlib
import re
import sys
from datetime import datetime

sys.stdout.reconfigure(encoding="utf-8")

HOME = pathlib.Path.home()
MAIN = HOME / "Desktop" / "工作内容.txt"
ARCHIVES = [
    MAIN.with_name("工作内容_2025.txt"),
    MAIN.with_name("工作内容_bak.txt"),
]

WEEKDAYS = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


def is_date_line(s: str):
    return bool(
        re.match(r"^\d{4}/\d{2}/\d{2}$", s.strip())
        or re.match(r"^\d{4}年\d{1,2}月\d{1,2}日", s.strip())
    )


def split_entries(lines):
    entries = []
    cur = []
    for line in lines:
        if is_date_line(line):
            if cur:
                entries.append(cur)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        entries.append(cur)
    return entries


def norm_date(d: str) -> str:
    """2026-04-10 / 2026/04/10 -> 2026年04月10日"""
    m = re.match(r"^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$", d.strip())
    if not m:
        return d
    y, mo, da = m.groups()
    return f"{y}年{int(mo):02d}月{int(da):02d}日"


def load_entries(all_files: bool):
    files = [MAIN] + (ARCHIVES if all_files else [])
    result = []
    for f in files:
        if f.exists():
            result.extend(split_entries(f.read_text(encoding="utf-8").split("\n")))
    return result


def main():
    parser = argparse.ArgumentParser(description="查询日报内容（不读取整个文件）")
    parser.add_argument("--date", help="查询某天，格式 YYYY-MM-DD")
    parser.add_argument("--keyword", help="按关键词搜索")
    parser.add_argument("--since", help="起始日期 YYYY-MM-DD")
    parser.add_argument("--until", help="结束日期 YYYY-MM-DD")
    parser.add_argument("--limit", type=int, default=5, help="关键词搜索最多返回条数（默认5）")
    parser.add_argument("--month", help="列出某月上班日报日期（格式 YYYY-MM）")
    parser.add_argument("--all-files", action="store_true", help="同时搜索归档文件")
    args = parser.parse_args()

    if not (args.date or args.keyword or args.since or args.until or args.month):
        parser.print_help()
        sys.exit(1)

    entries = load_entries(args.all_files)

    # 按日期降序排序（最近的在前），用于关键词搜索
    def entry_date(e):
        m = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", e[0].strip())
        return m.groups() if m else ("0", "0", "0")

    entries_sorted = sorted(entries, key=entry_date, reverse=True)

    # ---- 按月统计上班日报 ----------------
    if args.month:
        m = re.match(r"^(\d{4})-(\d{1,2})$", args.month.strip())
        if not m:
            print(f"月份格式错误: {args.month}，请使用 YYYY-MM")
            sys.exit(1)
        y, mo = m.groups()
        days = []
        for e in entries:
            dm = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})日?", e[0].strip())
            if dm and dm.group(1) == y and int(dm.group(2)) == int(mo):
                days.append(e[0].strip())
        if not days:
            print(f"{y}年{int(mo):02d}月 没有日报记录")
            sys.exit(0)
        # 按日排序去重（保留原样去重，含加班标记）
        def day_of(s):
            m = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", s)
            return int(m.group(3)) if m else 0

        seen = set()
        uniq = []
        for d in sorted(days, key=day_of):
            key = re.sub(r"\s*（加班）", "", d)
            if key in seen:
                continue
            seen.add(key)
            uniq.append(d)
        print(f"=== {y}年{int(mo):02d}月 上班日报：{len(uniq)} 天 ===")
        for d in uniq:
            dm = re.match(r"^(\d{4})[/年](\d{1,2})[/月](\d{1,2})", d)
            dt = datetime(int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
            wd = WEEKDAYS[dt.weekday()]
            tag = "  （加班）" if "加班" in d else ""
            print(f"  {dt.month:02d}-{dt.day:02d} {wd}{tag}")
        return

    # ---- 按日期查询 ----
    if args.date:
        target = norm_date(args.date)
        found = False
        for e in entries_sorted:
            if e[0].strip().startswith(target):
                print("\n".join(e))
                found = True
                break
        if not found:
            print(f"未找到 {args.date} 的日报")
            sys.exit(1)
        return

    # ---- 范围查询 ----
    if args.since or args.until:
        since = norm_date(args.since) if args.since else "0000年01月01日"
        until = norm_date(args.until) if args.until else "9999年12月31日"
        count = 0
        # 范围查询按正序输出
        for e in sorted(entries, key=entry_date):
            d = e[0].strip()
            if since <= d <= until:
                print("\n".join(e))
                print()
                count += 1
        if count == 0:
            print("该范围内无日报")
        else:
            print(f"共 {count} 天")
        return

    # ---- 关键词搜索 ----
    if args.keyword:
        hits = [e for e in entries_sorted if any(args.keyword in l for l in e)]
        if not hits:
            print(f"未找到包含「{args.keyword}」的日报")
            sys.exit(1)
        for e in hits[: args.limit]:
            print(f"----- {e[0].strip()} -----")
            print("\n".join(e))
            print()
        total = len(hits)
        shown = min(total, args.limit)
        print(f"命中 {total} 天，显示 {shown} 天（可用 --limit 调整）")
        return


if __name__ == "__main__":
    main()
