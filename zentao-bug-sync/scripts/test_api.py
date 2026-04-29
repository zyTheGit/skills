#!/usr/bin/env python3
"""测试禅道 API"""

import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
base_url = os.getenv("ZENTAO_URL", "").rstrip("/")
account = os.getenv("ZENTAO_ACCOUNT", "")
password = os.getenv("ZENTAO_PASSWORD", "")

session = requests.Session()

resp1 = session.post(
    f"{base_url}/user-login.html",
    data={"account": account, "password": password},
    headers={"Content-Type": "application/x-www-form-urlencoded"},
)
print(f"Login successful")

# 尝试使用 PATH_INFO 格式的 URL
# 禅道的 URL 格式可能是: bug-browse-{product_id}-{module_id}-{browse_type}-{param}-{orderBy}-{recTotal}-{recPerPage}-{pageID}.json
test_urls = [
    f"{base_url}/bug-browse-1-0-all-0-id_desc-732-20-1.json",
    f"{base_url}/bug-browse-1-0-all-0-id_desc-732-20-2.json",
    f"{base_url}/bug-browse-1--id_desc-732-20-2.json",
]

for i, url in enumerate(test_urls, 1):
    try:
        resp = session.get(url)
        print(f"\nTest {i}: {url}")
        print(f"Status: {resp.status_code}")
        print(f"Response length: {len(resp.text)}")
        if resp.status_code == 200 and len(resp.text) > 300:
            try:
                data = resp.json()
                if "data" in data:
                    inner = json.loads(data["data"])
                    bugs = inner.get("bugs", [])
                    print(f"Bugs count: {len(bugs)}")
                    if bugs:
                        print(f"First bug ID: {bugs[0].get('id')}")
                        print(f"Last bug ID: {bugs[-1].get('id')}")
            except Exception as e:
                print(f"JSON parse error: {e}")
                print(f"Response first 100: {resp.text[:100]}")
    except Exception as e:
        print(f"Request error: {e}")
