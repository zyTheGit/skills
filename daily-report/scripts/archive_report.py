# -*- coding: utf-8 -*-
"""按年归档日报文件（方案A）
- 2025 及更早的日报归档到 工作内容_2025.txt（保持原顺序）
- 2026 年保留在主文件 工作内容.txt
用法:
  uv run python archive_report.py            # 执行归档
  uv run python archive_report.py --dry-run  # 预览，不实际写入
"""
import argparse
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

MAIN = pathlib.Path.home() / "Desktop" / "工作内容.txt"
ARCHIVE = MAIN.with_name("工作内容_2025.txt")


def is_date_line(s: str):
    """判断是否日期行（YYYY/MM/DD 或 YYYY年M月D日）"""
    return bool(
        re.match(r"^\d{4}/\d{2}/\d{2}$", s.strip())
        or re.match(r"^\d{4}年\d{1,2}月\d{1,2}日", s.strip())
    )


def date_year(s: str):
    m = re.match(r"^(\d{4})", s.strip())
    return int(m.group(1)) if m else None


def split_entries(lines):
    """按日期行切分为 (年份, 段落行列表) 列表"""
    entries = []
    cur_year = None
    cur = []
    for line in lines:
        if is_date_line(line):
            if cur:
                entries.append((cur_year, cur))
            cur_year = date_year(line)
            cur = [line]
        else:
            cur.append(line)
    if cur:
        entries.append((cur_year, cur))
    return entries


def main():
    parser = argparse.ArgumentParser(description="按年归档日报文件")
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不写入")
    args = parser.parse_args()

    if not MAIN.exists():
        print(f"错误: 主文件不存在 {MAIN}")
        sys.exit(1)

    content = MAIN.read_text(encoding="utf-8")
    entries = split_entries(content.split("\n"))

    keep = [e for y, e in entries if y == 2026]
    archive = [e for y, e in entries if y is not None and y < 2026]
    unknown = [e for y, e in entries if y is None]

    def join(es):
        return "\n\n".join("\n".join(e).rstrip() for e in es if e)

    keep_text = join(keep).strip() + ("\n" if keep else "")
    archive_text = join(archive).strip() + ("\n" if archive else "")

    if unknown:
        print(f"警告: {len(unknown)} 段无法识别年份，将保留在主文件")
        if unknown:
            extra = join(unknown)
            keep_text = (keep_text + "\n\n" + extra).strip() + "\n"

    print(f"主文件({MAIN.name}): 保留 {len(keep)} 天 (2026)")
    print(f"归档文件({ARCHIVE.name}): {len(archive)} 天 (2025及更早)")

    if args.dry_run:
        print("\n[预览模式] 未写入任何文件")
        print(f"  主文件将变为 {len(keep_text)} 字符 ({len(keep_text.splitlines())} 行)")
        print(f"  归档文件将变为 {len(archive_text)} 字符 ({len(archive_text.splitlines())} 行)")
        return

    if archive:
        # 归档文件存在则合并（防止重复归档后重复执行）
        if ARCHIVE.exists():
            old = ARCHIVE.read_text(encoding="utf-8")
            if old.strip():
                archive_text = (old.rstrip() + "\n\n" + archive_text).strip() + "\n"
        ARCHIVE.write_text(archive_text, encoding="utf-8")
        print(f"已写入归档文件: {ARCHIVE}")

    # 备份后写回主文件
    bak = MAIN.with_name("工作内容_bak.txt")
    bak.write_text(content, encoding="utf-8")
    MAIN.write_text(keep_text, encoding="utf-8")
    print(f"主文件已更新: {MAIN} (备份在 {bak.name})")


if __name__ == "__main__":
    main()
