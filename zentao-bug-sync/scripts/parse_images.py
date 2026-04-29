#!/usr/bin/env python3
"""解析 BUG Excel 中的图片，使用 Claude Vision API"""

import sys
import argparse
from pathlib import Path
from openpyxl import load_workbook
import requests
import os
from dotenv import load_dotenv


def download_image(url, save_dir):
    """下载图片到本地"""
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()

        filename = url.split("/")[-1]
        filepath = save_dir / filename
        filepath.write_bytes(resp.content)
        return str(filepath)
    except Exception as e:
        print(f"下载失败: {url} - {e}")
        return None


def parse_excel_images(excel_file, limit=10):
    """读取 Excel 并提取需要解析的图片"""
    wb = load_workbook(excel_file)
    ws = wb.active

    bugs_with_images = []
    seen_images = set()

    for row in range(2, ws.max_row + 1):
        bug_id = ws.cell(row=row, column=1).value
        title = ws.cell(row=row, column=2).value
        images = ws.cell(row=row, column=16).value

        if images:
            for img_url in images.split("\n"):
                if img_url and img_url not in seen_images:
                    seen_images.add(img_url)
                    bugs_with_images.append(
                        {
                            "row": row,
                            "bug_id": bug_id,
                            "title": title,
                            "image_url": img_url,
                        }
                    )
                    if len(bugs_with_images) >= limit:
                        return bugs_with_images

    return bugs_with_images


def generate_parse_prompts(bugs_list, output_dir):
    """生成图片解析提示"""
    prompts = []

    for bug in bugs_list:
        prompt = f"""
请解析以下图片，这是 BUG #{bug["bug_id"]} 的截图：

BUG 标题: {bug["title"]}
图片 URL: {bug["image_url"]}

请描述图片中的：
1. 错误信息或提示（如有）
2. 界面状态和关键元素
3. 问题现象分析
4. 可能的根因提示

请使用简洁的中文描述。
"""
        prompts.append(
            {
                "bug_id": bug["bug_id"],
                "row": bug["row"],
                "prompt": prompt,
                "image_url": bug["image_url"],
            }
        )

    return prompts


def main():
    parser = argparse.ArgumentParser(description="解析 BUG 图片")
    parser.add_argument("--input", required=True, help="Excel 文件路径")
    parser.add_argument("--limit", type=int, default=10, help="解析图片数量限制")
    parser.add_argument("--output-prompts", help="输出提示文件")

    args = parser.parse_args()

    excel_path = Path(args.input)
    if not excel_path.exists():
        print(f"文件不存在: {excel_path}")
        return

    print(f"读取 Excel: {excel_path}")
    bugs = parse_excel_images(excel_path, args.limit)

    print(f"发现 {len(bugs)} 个唯一图片需要解析")

    prompts = generate_parse_prompts(bugs, excel_path.parent)

    if args.output_prompts:
        import json

        output_path = Path(args.output_prompts)
        output_path.write_text(json.dumps(prompts, ensure_ascii=False, indent=2))
        print(f"提示已保存到: {output_path}")

    print("\n需要解析的图片:")
    for i, p in enumerate(prompts, 1):
        print(f"{i}. BUG #{p['bug_id']}: {p['image_url']}")

    print("\n请使用 Claude Vision 能力或 @image-analyzer skill 解析以上图片")


if __name__ == "__main__":
    main()
