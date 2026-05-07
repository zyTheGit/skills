#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""日报生成技能 - 共享工具函数"""

import re
from datetime import datetime


def _longest_common_substring(a: str, b: str) -> str:
    """返回两个字符串的最长公共子串"""
    n, m = len(a), len(b)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    max_len = 0
    end_pos = 0
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                if dp[i][j] > max_len:
                    max_len = dp[i][j]
                    end_pos = i
    return a[end_pos - max_len:end_pos]


def _merge_similar_items(items: list[str]) -> list[str]:
    """
    合并同类项：检测共享公共子串的条目，合并为一条
    如 "暂停令典表调整使用全局预览组件" 和 "开工令典表调整使用全局预览组件"
    → "暂停令、开工令等典表调整使用全局预览组件"
    """
    if len(items) <= 1:
        return items

    n = len(items)
    used = set()
    result = []

    for i in range(n):
        if i in used:
            continue

        group = [i]
        for j in range(i + 1, n):
            if j in used:
                continue
            common = _longest_common_substring(items[i], items[j])
            # 公共子串需 >= 6 且包含中文，避免 "等loading" 这种不通顺合并
            if len(common) >= 6 and re.search(r'[一-龥]', common):
                group.append(j)
                used.add(j)

        if len(group) == 1:
            result.append(items[group[0]])
        else:
            group_items = [items[idx] for idx in group]
            # 找组内所有条目的最长公共子串
            common = group_items[0]
            for gi in range(1, len(group_items)):
                common = _longest_common_substring(common, group_items[gi])

            if common and len(common) >= 4:
                parts = []
                for s in group_items:
                    idx = s.index(common)
                    prefix = s[:idx].strip()
                    # 如果公共部分在开头，取后缀作为区分
                    suffix = s[idx + len(common):].strip()
                    if prefix:
                        parts.append(prefix)
                    elif suffix:
                        parts.append(suffix)
                    else:
                        parts.append(s)
                unique = "、".join(p for p in parts if p)
                if unique:
                    result.append(f"{unique}等{common}")
                else:
                    result.append(common)
            else:
                result.extend(group_items)

    return result


def categorize_commit(subject: str) -> str:
    """根据提交信息前缀分类（支持中英文冒号）"""
    match = re.match(r"^(\w+)(\(.+\))?[：:]\s*", subject)
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
    汇总提交记录（简易版） - 每条提交独立成行，BUG编号单独汇总
    保留用于兼容，推荐使用 summarize_commits_grouped
    """
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]

    all_bug_numbers = []
    items = []

    for commit in filtered:
        subject = commit["subject"]
        bug_nums = extract_bug_numbers(subject)
        all_bug_numbers.extend(bug_nums)

        cleaned = clean_subject(subject)
        if cleaned:
            if re.match(r'^[\d、，,\s\-]+$', cleaned):
                for num in re.findall(r'\d+', cleaned):
                    if num not in all_bug_numbers and len(num) >= 2:
                        all_bug_numbers.append(num)
            else:
                items.append(cleaned)

    seen = set()
    unique_items = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)

    bug_seen = set()
    unique_bugs = []
    for num in all_bug_numbers:
        if num not in bug_seen:
            bug_seen.add(num)
            unique_bugs.append(num)

    if unique_bugs:
        unique_items.append(f"BUG修复：{', '.join(unique_bugs)}")

    return unique_items


def summarize_commits_grouped(commits: list[dict]) -> tuple[dict[str, dict[str, list[str]]], list[str]]:
    """
    分组汇总提交记录 - 按项目分组，再按类型分组，BUG编号统一收集

    返回: (grouped, bug_numbers)
    grouped = {
        "进度管理": {"功能开发": [...], "问题修复": [...]},
        "策划管理": {"功能开发": [...]},
    }
    bug_numbers = ["3638", "3640"]
    """
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]

    all_bug_numbers = []
    grouped: dict[str, dict[str, list[str]]] = {}

    for commit in filtered:
        repo = commit["repo"]
        subject = commit["subject"]

        # 提取 BUG 编号
        bug_nums = extract_bug_numbers(subject)
        all_bug_numbers.extend(bug_nums)

        # 清洗提交信息
        cleaned = clean_subject(subject)
        if not cleaned:
            continue

        # 清洗后只剩纯数字，归类为 BUG 编号
        if re.match(r'^[\d、，,\s\-]+$', cleaned):
            for num in re.findall(r'\d+', cleaned):
                if num not in all_bug_numbers and len(num) >= 2:
                    all_bug_numbers.append(num)
            continue

        # 判断类型
        category = categorize_commit(subject)

        if repo not in grouped:
            grouped[repo] = {}
        if category not in grouped[repo]:
            grouped[repo][category] = []

        if cleaned not in grouped[repo][category]:
            grouped[repo][category].append(cleaned)

    # 合并同类项：每个项目每个类别内相似的条目合并
    for repo in grouped:
        for cat in grouped[repo]:
            grouped[repo][cat] = _merge_similar_items(grouped[repo][cat])

    # BUG编号去重，保持发现顺序
    bug_seen = set()
    unique_bugs = []
    for num in all_bug_numbers:
        if num not in bug_seen:
            bug_seen.add(num)
            unique_bugs.append(num)

    return grouped, unique_bugs


def format_report(
    date: str,
    commits: list[dict],
    is_holiday: bool,
    default_content: str = "日常工作",
) -> str:
    """
    格式化日报内容
    按项目分类 → 相同类型合并 → BUG修复统一汇总
    """
    dt = datetime.strptime(date, "%Y-%m-%d")
    date_str = f"{dt.year}年{dt.month}月{dt.day}日"

    if is_holiday and commits:
        date_str += " （加班）"

    # 检查是否有非 Merge 的有效提交
    filtered = [c for c in commits if not c["subject"].lower().startswith("merge")]
    if not filtered:
        return f"{date_str}\n1. {default_content}"

    grouped, bug_numbers = summarize_commits_grouped(commits)

    lines = [date_str]

    # 类别显示顺序
    category_order = [
        "功能开发", "样式调整", "性能优化", "代码重构",
        "问题修复", "文档更新", "测试相关", "构建/工具", "其他工作",
    ]

    cn_numerals = ["一", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

    for idx, (repo_name, categories) in enumerate(grouped.items()):
        numeral = cn_numerals[idx] if idx < len(cn_numerals) else str(idx + 1)
        lines.append(f"{numeral}、{repo_name}")

        # 按优先级排序类别
        sorted_cats = sorted(
            categories.keys(),
            key=lambda c: category_order.index(c) if c in category_order else 99,
        )

        for cat in sorted_cats:
            items = categories[cat]
            lines.append(f"  {cat}：")
            for i, item in enumerate(items, 1):
                lines.append(f"  {i}. {item}")
            lines.append("")

    # 统一 BUG 修复汇总
    if bug_numbers:
        lines.append(f"BUG修复：{', '.join(bug_numbers)}")

    return "\n".join(lines).strip()
