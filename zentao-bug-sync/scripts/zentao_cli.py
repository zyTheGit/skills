#!/usr/bin/env python3
"""禅道 BUG 同步智能入口 - 自动检测意图、初始化检查、默认路径"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

from init_config import get_config_dir_from_env, get_env_path, get_credentials

SKILL_DIR = Path(__file__).parent.parent
DEFAULT_OUTPUT_DIR = Path.home() / "Desktop" / "zentao-bugs"


def check_dependencies():
    """检查依赖是否安装"""
    required = ["requests", "openpyxl", "dotenv"]
    package_names = {"dotenv": "python-dotenv"}
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            install_name = package_names.get(pkg, pkg)
            missing.append(install_name)
    return missing


def check_config():
    """检查配置文件"""
    env_path = get_env_path()

    if not env_path.exists():
        return False, f"凭据文件不存在: {env_path}"

    credentials = get_credentials()

    if not credentials["url"]:
        return False, "禅道 URL 未配置"
    if not credentials["account"]:
        return False, "账号未配置"
    if not credentials["password"]:
        return False, "密码未配置"

    return True, "配置正常"


def init_check():
    """初始化检查"""
    issues = []

    deps_missing = check_dependencies()
    if deps_missing:
        issues.append(f"缺少依赖: {', '.join(deps_missing)}")

    config_ok, config_msg = check_config()
    if not config_ok:
        issues.append(f"配置问题: {config_msg}")

    return issues


def install_dependencies():
    """安装缺失的依赖"""
    missing = check_dependencies()
    if missing:
        print(f"正在安装缺失依赖: {', '.join(missing)}")
        subprocess.run(["uv", "pip", "install", *missing], check=True)
        print("依赖安装完成")
    else:
        print("所有依赖已安装")


def get_default_excel():
    """获取默认 Excel 文件路径"""
    DEFAULT_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today = datetime.now().strftime("%Y%m%d")
    return DEFAULT_OUTPUT_DIR / f"zentao_bugs_{today}.xlsx"


def find_latest_excel():
    """查找最新的 Excel 文件"""
    if not DEFAULT_OUTPUT_DIR.exists():
        return None
    xlsx_files = list(DEFAULT_OUTPUT_DIR.glob("zentao_bugs_*.xlsx"))
    if not xlsx_files:
        return None
    return max(xlsx_files, key=lambda f: f.stat().st_mtime)


def detect_intent(args):
    """根据参数检测用户意图"""
    if args.fetch:
        return "fetch"
    if args.push:
        return "push"
    if args.sync:
        return "sync"
    if args.prompt:
        return "prompt"
    if args.analyze:
        return "analyze"
    if args.init:
        return "init"

    excel_file = args.input or find_latest_excel()
    if excel_file and excel_file.exists():
        if args.status or args.severity or args.assigned or args.solution:
            return "push"
        return "sync"

    return "fetch"


def run_command(cmd, args_list):
    """运行脚本命令"""
    full_cmd = ["uv", "run", str(SKILL_DIR / "scripts" / cmd)] + args_list
    print(f"执行: {' '.join(full_cmd)}")
    subprocess.run(full_cmd, check=True)


def main():
    parser = argparse.ArgumentParser(
        description="禅道 BUG 同步智能入口 - 自动检测意图并执行相应操作",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  zentao_cli.py                    # 自动检测：无文件则 fetch，有文件则 sync
  zentao_cli.py --fetch            # 拉取自己的 BUG（默认）
  zentao_cli.py --fetch --all      # 拉取所有 BUG
  zentao_cli.py --push             # 推送修改到禅道
  zentao_cli.py --sync             # 增量同步
  zentao_cli.py --prompt           # 生成 AI 提示语
  zentao_cli.py --init             # 初始化配置
  zentao_cli.py --input bugs.xlsx  # 指定 Excel 文件
        """,
    )

    parser.add_argument("--fetch", action="store_true", help="拉取 BUG 到 Excel")
    parser.add_argument("--push", action="store_true", help="推送 Excel 更新到禅道")
    parser.add_argument("--sync", action="store_true", help="增量同步")
    parser.add_argument("--prompt", action="store_true", help="生成 AI 提示语")
    parser.add_argument("--analyze", action="store_true", help="本地结构化解析步骤内容")
    parser.add_argument("--init", action="store_true", help="初始化配置")

    parser.add_argument("--input", type=str, help="Excel 文件路径（默认使用最新文件）")
    parser.add_argument("--output", type=str, help="输出文件路径（fetch 时）")
    parser.add_argument("--status", type=str, help="状态过滤或更新")
    parser.add_argument("--bug-id", type=str, help="指定 BUG ID")
    parser.add_argument(
        "--all", action="store_true", help="获取所有 BUG（默认只获取自己的）"
    )
    parser.add_argument("--dry-run", action="store_true", help="预览模式")

    args = parser.parse_args()

    issues = init_check()
    if issues and not args.init:
        print("初始化检查发现问题:")
        for issue in issues:
            print(f"  - {issue}")
        print("\n请先运行: uv run scripts/zentao_cli.py --init")
        return 1

    if args.init:
        install_dependencies()
        subprocess.run(
            ["uv", "run", str(SKILL_DIR / "scripts" / "init_config.py")], check=True
        )
        print()
        config_ok, config_msg = check_config()
        print(f"配置检查: {config_msg}")
        if config_ok:
            print(f"配置目录: {get_config_dir_from_env()}")
            print(f"凭据文件: {get_env_path()}")
        return 0

    intent = detect_intent(args)
    if args.input:
        excel_file = Path(args.input).expanduser()
    else:
        excel_file = find_latest_excel() or get_default_excel()

    print(f"检测意图: {intent}")
    print(f"Excel 文件: {excel_file}")

    if intent == "fetch":
        cmd_args = []
        if args.output:
            cmd_args.extend(["--output", args.output])
        else:
            cmd_args.extend(["--output", str(excel_file)])
        if args.status:
            cmd_args.extend(["--status", args.status])
        if args.all:
            cmd_args.append("--all")
        run_command("fetch_bugs.py", cmd_args)

    elif intent == "push":
        if not excel_file.exists():
            print(f"Excel 文件不存在: {excel_file}")
            print("请先运行 fetch 拉取 BUG")
            return 1
        cmd_args = ["--input", str(excel_file)]
        if args.dry_run:
            cmd_args.append("--dry-run")
        run_command("push_bugs.py", cmd_args)

    elif intent == "sync":
        if not excel_file.exists():
            print(f"Excel 文件不存在: {excel_file}")
            print("请先运行 fetch 拉取 BUG")
            return 1
        cmd_args = ["--input", str(excel_file)]
        run_command("sync_bugs.py", cmd_args)

    elif intent == "prompt":
        if not excel_file.exists():
            print(f"Excel 文件不存在: {excel_file}")
            print("请先运行 fetch 拉取 BUG")
            return 1
        cmd_args = ["--input", str(excel_file)]
        if args.bug_id:
            cmd_args.extend(["--bug-id", args.bug_id])
        if args.all:
            cmd_args.append("--all")
        run_command("generate_prompt.py", cmd_args)

    elif intent == "analyze":
        if not excel_file.exists():
            print(f"Excel 文件不存在: {excel_file}")
            print("请先运行 fetch 拉取 BUG")
            return 1
        cmd_args = ["--input", str(excel_file)]
        if args.bug_id:
            cmd_args.extend(["--bug-id", args.bug_id])
        if args.all:
            cmd_args.append("--all")
        run_command("analyze_steps.py", cmd_args)

    return 0


if __name__ == "__main__":
    sys.exit(main())
