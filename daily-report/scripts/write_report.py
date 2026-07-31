#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""直接写入日报到工作内容文件（解决编码问题）"""

import argparse
import sys
import re
from pathlib import Path


def check_date_exists(date_str: str, output_path: str) -> bool:
    """
    检查文件中是否已存在指定日期的日报
    
    Args:
        date_str: 日期字符串（如 2026年04月20日）
        output_path: 输出文件路径
    
    Returns:
        bool: 是否已存在
    """
    output_file = Path(output_path)
    if not output_file.exists():
        return False
    
    try:
        content = output_file.read_text(encoding="utf-8")
        return date_str in content
    except:
        return False


def remove_existing_date_report(date_str: str, output_path: str) -> str:
    """
    移除文件中已存在的指定日期的日报
    
    Args:
        date_str: 日期字符串（如 2026年04月20日）
        output_path: 输出文件路径
    
    Returns:
        str: 移除后的内容
    """
    output_file = Path(output_path)
    try:
        content = output_file.read_text(encoding="utf-8")
        
        # 使用正则表达式匹配该日期下的所有内容
        # 匹配格式：日期行 + 后续的编号行（直到下一个日期或文件结尾）
        pattern = rf'{re.escape(date_str)}.*?(?=\n\d{{4}}年\d{{2}}月\d{{2}}日|$)'
        new_content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 清理多余的空行
        new_content = re.sub(r'\n{3,}', '\n\n', new_content)
        
        return new_content.strip()
    except:
        return ""


def normalize_newlines(content: str) -> str:
    """
    统一换行符处理，兼容不同 agent 传入方式

    不同 agent 传入 \n 的方式不同：
    - Claude Code 通过 --summary 参数传，\\n 是字面量
    - OpenCode 可能通过 stdin 传，\\n 是真正的换行符
    - Codex/Pi 可能又是另一种方式

    策略：先统一为真正的换行符，再清理多余空行
    """
    # 如果内容中包含字面量 \\n（两个字符），替换为真正的换行符
    # 但要避免把已经是真正换行符的内容搞乱
    # 检测策略：如果字符串中包含 \\n 但不包含真正的换行符，说明是字面量传入
    if r"\n" in content and "\n" not in content:
        content = content.replace(r"\n", "\n")
    # 如果同时包含真正的换行符和字面量 \\n，只替换字面量
    elif r"\n" in content:
        content = content.replace(r"\n", "\n")

    # 清理多余空行（3个以上连续换行压缩为2个）
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content


def write_report(content: str, output_path: str, mode: str = "append", overwrite_date: str = None) -> None:
    """
    写入日报到输出文件
    
    Args:
        content: 日报内容
        output_path: 输出文件路径
        mode: 写入模式 (append/overwrite)
        overwrite_date: 要覆盖的日期（如果 mode 是 overwrite）
    """
    output_file = Path(output_path)

    # 统一换行符处理
    content = normalize_newlines(content)

    # 确保目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)

    if mode == "append" and output_file.exists():
        # 读取现有内容
        try:
            existing_content = output_file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            # 如果文件编码有问题，尝试其他编码
            try:
                existing_content = output_file.read_text(encoding="gbk")
            except:
                existing_content = ""
        
        # 添加空行分隔
        new_content = existing_content.rstrip() + "\n\n" + content
    elif mode == "overwrite":
        if not overwrite_date:
            # 禁止不带日期参数的全文覆写，保护历史内容
            print("错误: --mode overwrite 需要同时指定 --overwrite-date，防止误删历史日报")
            sys.exit(1)
        # 覆盖指定日期的日报
        # 保留该日期之外的历史内容，仅覆盖指定日期的日报
        existing_content = remove_existing_date_report(overwrite_date, output_path)
        if existing_content:
            new_content = existing_content + "\n\n" + content
        else:
            new_content = content

    # 写入文件（UTF-8编码，不带BOM）
    output_file.write_text(new_content, encoding="utf-8")

    print(f"日报已写入: {output_file}")


def main():
    parser = argparse.ArgumentParser(description="写入日报到工作内容文件")
    parser.add_argument("--output", required=True, help="输出文件路径")
    parser.add_argument("--content", required=False, help="日报内容（直接传入）")
    parser.add_argument("--file", required=False, help="日报文件路径")
    parser.add_argument("--mode", default="append", choices=["append", "overwrite"], help="写入模式")
    parser.add_argument("--overwrite-date", required=False, help="要覆盖的日期（如 2026年04月20日）")
    parser.add_argument("--check-date", required=False, help="检查指定日期是否已存在（只检查不写入）")

    args = parser.parse_args()
    
    # 只检查日期是否存在
    if args.check_date:
        exists = check_date_exists(args.check_date, args.output)
        print(f"日期 {args.check_date} 已存在: {exists}")
        sys.exit(0 if exists else 1)

    if args.content:
        # 换行符由 normalize_newlines 统一处理，此处直接传入
        content = args.content
    elif args.file:
        content = Path(args.file).read_text(encoding="utf-8")
    else:
        # 从标准输入读取
        content = sys.stdin.read()

    write_report(content, args.output, args.mode, args.overwrite_date)


if __name__ == "__main__":
    main()