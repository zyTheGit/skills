#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化禅道 BUG 同步配置"""

import json
import os
from pathlib import Path
from dotenv import load_dotenv


def get_skill_dir() -> Path:
    """获取技能目录"""
    return Path(__file__).parent.parent


def get_opencode_config_dir() -> Path:
    """获取 opencode 默认配置目录"""
    return Path.home() / ".config" / "opencode"


def get_config_dir_from_env() -> Path:
    """
    从 .env 文件获取配置目录

    优先级：
    1. 技能目录下的 .env 文件中的 ZENTAO_BUG_SYNC_CONFIG_DIR
    2. 系统环境变量 ZENTAO_BUG_SYNC_CONFIG_DIR
    3. 默认 opencode 配置目录下的 skill-config/zentao-bug-sync
    """
    skill_dir = get_skill_dir()
    env_path = skill_dir / ".env"

    if env_path.exists():
        load_dotenv(env_path)

    config_dir = os.environ.get("ZENTAO_BUG_SYNC_CONFIG_DIR")

    if config_dir:
        return Path(config_dir)

    return get_opencode_config_dir() / "skill-config" / "zentao-bug-sync"


def get_config_path() -> Path:
    """获取配置文件路径"""
    return get_config_dir_from_env() / "config.json"


def get_env_path() -> Path:
    """获取配置目录下的 .env 文件路径（存放敏感信息）"""
    return get_config_dir_from_env() / ".env"


def get_default_config() -> dict:
    """获取默认配置"""
    return {
        "zentao_url": "",
        "zentao_account": "",
        "zentao_password": "",
        "default_output_dir": str(Path.home() / "Desktop" / "zentao-bugs"),
        "default_filename_format": "zentao_bugs_{date}.xlsx",
    }


def init_config() -> Path:
    """
    初始化配置文件

    Returns:
        配置文件路径
    """
    config_dir = get_config_dir_from_env()
    config_path = config_dir / "config.json"
    env_path = config_dir / ".env"

    config_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists():
        default_config = get_default_config()
        config_path.write_text(
            json.dumps(default_config, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"已创建默认配置文件: {config_path}")
        print("请修改配置文件中的 zentao_url、zentao_account、zentao_password")

    if not env_path.exists():
        env_content = """# 禅道连接配置（敏感信息）
# 请填写实际的连接信息
ZENTAO_URL=
ZENTAO_ACCOUNT=
ZENTAO_PASSWORD=
"""
        env_path.write_text(env_content, encoding="utf-8")
        print(f"已创建环境配置文件: {env_path}")
        print("请在 .env 文件中填写禅道连接信息")

    return config_path


def load_config() -> dict:
    """
    加载配置文件

    Returns:
        配置字典
    """
    config_path = get_config_path()

    if not config_path.exists():
        init_config()

    config_text = config_path.read_text(encoding="utf-8")
    return json.loads(config_text)


def load_env_credentials() -> dict:
    """
    从配置目录下的 .env 文件加载敏感凭据

    Returns:
        凭据字典 {url, account, password}
    """
    env_path = get_env_path()

    if env_path.exists():
        load_dotenv(env_path)

    return {
        "url": os.environ.get("ZENTAO_URL", ""),
        "account": os.environ.get("ZENTAO_ACCOUNT", ""),
        "password": os.environ.get("ZENTAO_PASSWORD", ""),
    }


def get_credentials() -> dict:
    """
    获取禅道连接凭据

    优先级：
    1. 配置目录下的 .env 文件（推荐）
    2. 技能目录下的 .env 文件（兼容旧版）
    3. config.json 文件（不推荐存放密码）

    Returns:
        凭据字典 {url, account, password}
    """
    credentials = load_env_credentials()

    if credentials["url"] and credentials["account"] and credentials["password"]:
        return credentials

    skill_env_path = get_skill_dir() / ".env"
    if skill_env_path.exists():
        load_dotenv(skill_env_path)
        credentials = {
            "url": os.environ.get("ZENTAO_URL", ""),
            "account": os.environ.get("ZENTAO_ACCOUNT", ""),
            "password": os.environ.get("ZENTAO_PASSWORD", ""),
        }
        if credentials["url"] and credentials["account"] and credentials["password"]:
            return credentials

    config = load_config()
    return {
        "url": config.get("zentao_url", ""),
        "account": config.get("zentao_account", ""),
        "password": config.get("zentao_password", ""),
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="初始化禅道 BUG 同步配置")
    parser.add_argument("--show", action="store_true", help="显示当前配置")
    parser.add_argument(
        "--show-credentials", action="store_true", help="显示连接凭据（含敏感信息）"
    )

    args = parser.parse_args()

    if args.show_credentials:
        credentials = get_credentials()
        print("连接凭据:")
        print(f"  URL: {credentials['url']}")
        print(f"  Account: {credentials['account']}")
        print(f"  Password: {'*' * len(credentials['password'])}")
        print(f"  配置目录: {get_config_dir_from_env()}")
    elif args.show:
        config = load_config()
        print("当前配置:")
        print(json.dumps(config, ensure_ascii=False, indent=2))
        print(f"\n配置目录: {get_config_dir_from_env()}")
        print(f"配置文件: {get_config_path()}")
        print(f"凭据文件: {get_env_path()}")
    else:
        config_path = init_config()
        print(f"\n配置已初始化完成")
        print(f"配置目录: {get_config_dir_from_env()}")
        print(f"\n下一步:")
        print(f"1. 编辑 {get_env_path()} 填写禅道连接信息")
        print(f"2. 运行 uv run scripts/zentao_cli.py --init 检查配置")


if __name__ == "__main__":
    main()
