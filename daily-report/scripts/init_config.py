#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化日报生成配置"""

import json
from pathlib import Path


def get_default_config_dir() -> Path:
    """获取默认配置目录（固定路径：~/.config/daily-report/）"""
    return Path.home() / ".config" / "daily-report"


def get_default_config() -> dict:
    """获取默认配置"""
    output_file = Path.home() / "Desktop" / "工作内容.txt"

    return {
        "repos": [],
        "output_file": str(output_file),
        "author": None,
        "holiday_api": "https://timor.tech/api/holiday/info/",
        "default_content": "日常工作",
    }


def init_config(config_dir: Path | None = None) -> Path:
    """初始化配置文件"""
    if config_dir is None:
        config_dir = get_default_config_dir()

    config_path = config_dir / "config.json"

    # 创建配置目录
    config_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        default_config = get_default_config()
        config_path.write_text(
            json.dumps(default_config, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"已创建默认配置文件: {config_path}")
        print("请编辑配置文件，设置仓库路径（repos）和作者名称（author）")
        _print_permission_hint(config_dir, default_config["output_file"])
    else:
        print(f"配置文件已存在: {config_path}")

    return config_path


def _print_permission_hint(config_dir: Path, output_file: str) -> None:
    """输出配置提示"""
    config_str = str(config_dir).replace("\\", "/")
    output_parent = str(Path(output_file).parent).replace("\\", "/")

    hint = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
配置文件已创建，请编辑设置仓库路径（repos）和作者名称（author）。

配置目录: {config_str}
输出目录: {output_parent}

如需授权访问，请在对应 agent 的配置中添加目录权限。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    print(hint)


def load_config(config_dir: Path | None = None) -> dict:
    """加载配置文件"""
    if config_dir is None:
        config_dir = get_default_config_dir()

    config_path = config_dir / "config.json"

    if not config_path.exists():
        init_config(config_dir)

    return json.loads(config_path.read_text(encoding="utf-8"))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="初始化日报生成配置")
    parser.add_argument("--config-dir", help="配置目录路径（可选）")
    parser.add_argument("--show", action="store_true", help="显示当前配置")

    args = parser.parse_args()

    config_dir = Path(args.config_dir) if args.config_dir else None

    if args.show:
        config = load_config(config_dir)
        print(json.dumps(config, ensure_ascii=False, indent=2))
    else:
        init_config(config_dir)


if __name__ == "__main__":
    main()
