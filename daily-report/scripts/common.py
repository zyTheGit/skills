#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日报生成技能 - 共享工具函数"""

import re
from datetime import datetime


def categorize_commit(subject: str) -> str:
    """根据提交信息前缀分类"""
    match = re.match(r"^(\w+)(\(.+\))?:\s*", subject)
    if match:
        prefix = match.group(1).lower()
        type_mapping = {
            "feat": "功能开发", "feature": "功能开发",
            "fix": "问题修复", "bugfix": "问题修复",
            "refactor": "代码重构",
            "docs": "文档更新",
            "test": "测试相关",
            "chore": "构建/工具",
            "style": "样式调整",
            "perf": "性能优化",
        }
        return type_mapping.get(prefix, "其他工作")

    keywords = {
        "添加": "功能开发", "完成": "功能开发", "实现": "功能开发", "新增": "功能开发",
        "修复": "问题修复", "解决": "问题修复",
        "优化": "性能优化",
        "重构": "代码重构",
    }
    for keyword, category in keywords.items():
        if keyword in subject:
            return category
    return "其他工作"


def clean_subject(subject: str) -> str:
    """清洗提交信息：移除前缀和技术细节，保留核心描述"""
    # 移除英文前缀 (feat:, fix: 等)
    cleaned = re.sub(
        r"^(feat|feature|fix|bugfix|refactor|docs|test|chore|style|perf)(\(.+?\))?:\s*",
        "", subject, flags=re.IGNORECASE
    )
    # 移除中文冒号前缀
    cleaned = re.sub(
        r"^(feat|feature|fix|bugfix|refactor|docs|test|chore|style|perf)(\(.+?\))?：\s*",
        "", cleaned, flags=re.IGNORECASE
    )
    # 移除 BUG 编号引用（会单独汇总）
    cleaned = re.sub(
        r'\s*(?:BUG|bug|禅道)[#\-\s]*\d+\s*', ' ', cleaned, flags=re.IGNORECASE
    )
    # 移除 ticket/issue 编号
    cleaned = re.sub(r"\s*#\d+\s*", " ", cleaned)
    cleaned = re.sub(r"\s*\[[\w-]+\]\s*", " ", cleaned)
    # 清理残留的分隔符（如 " - " 变成空格）
    cleaned = re.sub(r'\s*[-:：]\s*', ' ', cleaned)
    # 压缩多余空格
    cleaned = re.sub(r'\s+', ' ', cleaned)
    # 跳过无意义提交
    stripped = cleaned.strip()
    if stripped.lower() in ("tongbu", "1", "同步", ".", "..", ""):
        return ""
    # 过滤 "Update xxx" 等纯文件更新提交
    if re.match(r'^Update\s+\S', stripped, re.IGNORECASE):
        return ""
    return stripped


def extract_bug_numbers(subject: str) -> list[str]:
    """从提交信息中提取 BUG 编号列表"""
    numbers = []

    # 原有模式：BUG123, bug123, 禅道123, #123
    for match in re.finditer(
        r'(?:BUG|bug|禅道)[#\-\s]*(\d+)|#(\d+)',
        subject
    ):
        num = match.group(1) or match.group(2)
        if num not in numbers:
            numbers.append(num)

    # 新增：识别 fix: 后跟纯数字的 BUG 编号（如 fix: 3337、3480、3477）
    # 同时支持中英文冒号，排除单数字的无效提交
    fix_match = re.match(
        r'^fix(?:\(.+?\))?[：:]\s*([\d、，,\s\-]+)$',
        subject, re.IGNORECASE
    )
    if fix_match:
        for num in re.findall(r'\d+', fix_match.group(1)):
            if num not in numbers and len(num) >= 2:
                numbers.append(num)

    return numbers


def summarize_commits(commits: list[dict]) -> list[str]:
    """
    汇总提交记录 - 每条提交独立成行，BUG编号单独汇总

    原则：
    - 每条提交对应一行日报条目，不合并、不过度润色
    - BUG编号统一提取，单起一行汇总
    - 仅做简单去重（完全匹配）
    """
    # 过滤 Merge 提交
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]

    all_bug_numbers = []
    items = []

    for commit in filtered:
        subject = commit["subject"]

        # 提取 BUG 编号（从原始 subject 提取）
        bug_nums = extract_bug_numbers(subject)
        all_bug_numbers.extend(bug_nums)

        # 清洗提交信息
        cleaned = clean_subject(subject)
        if cleaned:
            # 清洗后如果只剩下纯数字（如 "3504"、"3337、3480、3477"），归类为 BUG 编号
            # 排除单数字的无效提交（如 fix: 1）
            if re.match(r'^[\d、，,\s\-]+$', cleaned):
                for num in re.findall(r'\d+', cleaned):
                    if num not in all_bug_numbers and len(num) >= 2:
                        all_bug_numbers.append(num)
            else:
                items.append(cleaned)

    # 简单去重（完全匹配），保持顺序
    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    # BUG编号去重，保持发现顺序
    bug_seen = set()
    unique_bugs = []
    for num in all_bug_numbers:
        if num not in bug_seen:
            bug_seen.add(num)
            unique_bugs.append(num)

    # BUG编号单独一行
    if unique_bugs:
        unique_items.append(f"BUG修复：{', '.join(unique_bugs)}")

    return unique_items


def format_report(
    date: str,
    commits: list[dict],
    is_holiday: bool,
    default_content: str = "日常工作",
) -> str:
    """格式化日报内容"""
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.year}年{dt.month}月{dt.day}日"

    if is_holiday and commits:
        date_str += " （加班）"

    summary = summarize_commits(commits)

    if not summary:
        summary = [default_content]

    lines = [date_str]
    for i, item in enumerate(summary, 1):
        lines.append(f"{i}. {item}")

    return "\n".join(lines)
