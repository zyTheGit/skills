#!/usr/bin/env python3
"""禅道 API 封装 (适用于禅道 12.x) - 使用网页 JSON 格式"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

from init_config import get_credentials


class ZentaoAPI:
    def __init__(self, base_url=None, account=None, password=None):
        credentials = get_credentials()
        self.base_url = (
            base_url or credentials["url"] or os.getenv("ZENTAO_URL", "")
        ).rstrip("/")
        self.account = (
            account or credentials["account"] or os.getenv("ZENTAO_ACCOUNT", "")
        )
        self.password = (
            password or credentials["password"] or os.getenv("ZENTAO_PASSWORD", "")
        )
        self.token = None
        self.session = requests.Session()
        self.current_user = self.account

    def login(self):
        """登录禅道（使用 session-based 认证）"""
        resp = self.session.post(
            f"{self.base_url}/user-login.html",
            data={"account": self.account, "password": self.password},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()

        if "zentaosid" in self.session.cookies:
            self.token = self.session.cookies.get("zentaosid")
            return True
        raise Exception("登录失败: 无法获取 session")

    def ensure_login(self):
        if not self.token:
            self.login()

    def get_products(self):
        self.ensure_login()
        resp = self.session.get(f"{self.base_url}/bug-browse.json")
        resp.raise_for_status()
        data = resp.json()
        if "data" in data:
            inner = json.loads(data["data"])
            products = inner.get("products", {})
            return [{"id": k, "name": v} for k, v in products.items()]
        return []

    def get_bugs(self, product_id=None, status_filter=None, limit=100):
        self.ensure_login()
        bugs = []
        page = 1

        while True:
            product_str = str(product_id) if product_id else "1"
            browse_type = "all"
            param = "0"
            order_by = "id_desc"
            per_page = limit

            url = f"{self.base_url}/bug-browse-{product_str}-0-{browse_type}-{param}-{order_by}-1000-{per_page}-{page}.json"

            resp = self.session.get(url)
            resp.raise_for_status()
            data = resp.json()

            if "data" not in data:
                break

            inner = json.loads(data["data"])
            items = inner.get("bugs", [])

            if not items:
                break

            bugs.extend(items)
            pager = inner.get("pager", {})
            total = int(pager.get("recTotal", 0))
            per_page = int(pager.get("recPerPage", limit))

            if len(bugs) >= total or len(items) < per_page:
                break
            page += 1

        return bugs

    def get_my_bugs(self, status_filter=None, limit=100):
        """获取指派给当前用户的 BUG"""
        self.ensure_login()
        bugs = []
        page = 1

        while True:
            url = f"{self.base_url}/my-bug.json"
            params = {"page": page, "recPerPage": limit}
            if status_filter:
                params["status"] = status_filter

            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()

            if "data" not in data:
                break

            inner = json.loads(data["data"])
            items = inner.get("bugs", [])

            if not items:
                break

            bugs.extend(items)
            pager = inner.get("pager", {})
            total = int(pager.get("recTotal", 0))
            per_page = int(pager.get("recPerPage", limit))

            if len(bugs) >= total or len(items) < per_page:
                break
            page += 1

        return bugs

    def get_bug_detail(self, bug_id):
        self.ensure_login()
        resp = self.session.get(f"{self.base_url}/bug-view-{bug_id}.json")
        resp.raise_for_status()
        data = resp.json()
        if "data" in data:
            return json.loads(data["data"]).get("bug", {})
        return {}

    def update_bug(self, bug_id, data):
        self.ensure_login()
        resp = self.session.post(
            f"{self.base_url}/bug-edit-{bug_id}.html",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        return {"status": "success"}

    def resolve_bug(self, bug_id, solution, resolved_build=""):
        return self.update_bug(
            bug_id,
            {
                "status": "resolved",
                "resolution": solution,
                "resolvedBuild": resolved_build,
            },
        )

    def close_bug(self, bug_id, resolution="fixed"):
        return self.update_bug(bug_id, {"status": "closed", "resolution": resolution})

    def activate_bug(self, bug_id):
        return self.update_bug(bug_id, {"status": "active"})

    def create_bug(self, data):
        self.ensure_login()
        resp = self.session.post(
            f"{self.base_url}/bug-create.html",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        resp.raise_for_status()
        return {"status": "success"}

    def get_users_dict(self):
        """获取用户映射字典 {account: realname}"""
        users = self.get_users()
        return {u["account"]: u["realname"] for u in users}

    def get_products_dict(self):
        """获取产品映射字典 {id: name}"""
        products = self.get_products()
        return {p["id"]: p["name"] for p in products}

    def get_modules_dict(self, product_id=None):
        """获取模块映射字典 {id: name}"""
        self.ensure_login()
        resp = self.session.get(f"{self.base_url}/bug-browse.json")
        resp.raise_for_status()
        data = resp.json()
        modules_dict = {}
        if "data" in data:
            inner = json.loads(data["data"])
            modules = inner.get("modules", {})
            for mod_id, mod_name in modules.items():
                modules_dict[mod_id] = mod_name
        return modules_dict

    def get_users(self):
        self.ensure_login()
        resp = self.session.get(f"{self.base_url}/bug-browse.json")
        resp.raise_for_status()
        data = resp.json()
        if "data" in data:
            inner = json.loads(data["data"])
            users = inner.get("users", {})
            return [{"account": k, "realname": v} for k, v in users.items()]
        return []
