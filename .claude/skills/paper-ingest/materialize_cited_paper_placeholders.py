#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

EDGE_RE = re.compile(r"- \[\[(?P<src>[^\]]+)\]\] --(?P<rel>[^`\n]+)--> \[\[(?P<dst>[^\]]+)\]\]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cites-ledger", required=True)
    parser.add_argument("--papers-dir", required=True)
    parser.add_argument("--source-page", required=True)
    parser.add_argument("--paper-index")
    return parser.parse_args()


def extract_cited_targets(text: str) -> list[str]:
    targets: list[str] = []
    for match in EDGE_RE.finditer(text):
        if match.group("rel") != "cites":
            continue
        target = match.group("dst").split("|", 1)[0].strip()
        targets.append(target)
    return targets


def placeholder_content(title: str, source_page_stem: str) -> str:
    return f"""---
title: {title}
authors: []
year: unknown
venue: unknown
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
tags: [placeholder, cited-work]
---

# {title}

## 当前定位
- 当前作为 [[{source_page_stem}]] 的关键上游工作或对比对象。

## 与知识库现有内容的关系
- 被引用于：[[{source_page_stem}]]

## 待补充
- 正式摘要页、方法贡献、实验设定与证据页。
"""


def add_to_non_serving_placeholder_block(index_path: Path, title: str, source_page_stem: str) -> None:
    text = index_path.read_text(encoding="utf-8")
    label = title
    line = (
        f"- {label} 入口（文档：`ontology/entities/papers/{title}.md`）："
        f"[[ontology/entities/papers/{title}]] — {source_page_stem} 引用的上游论文，占位节点，状态=placeholder"
    )
    start = '<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->'
    end = '<!-- END MANAGED BLOCK:non-serving-placeholders -->'
    if start not in text or end not in text:
        return
    block = text.split(start, 1)[1].split(end, 1)[0]
    if line in block:
        return
    insertion = block.rstrip('\n') + ('\n' if block.strip() else '') + line + '\n'
    text = text.replace(f'{start}{block}{end}', f'{start}{insertion}{end}')
    index_path.write_text(text, encoding="utf-8")


def main() -> int:
    args = parse_args()
    cites_path = Path(args.cites_ledger)
    papers_dir = Path(args.papers_dir)
    source_page = Path(args.source_page)
    index_path = Path(args.paper_index) if args.paper_index else papers_dir / "index.md"

    cites_text = cites_path.read_text(encoding="utf-8")
    source_page_stem = source_page.stem
    created = []

    for target in extract_cited_targets(cites_text):
        target_path = papers_dir / f"{target}.md"
        if index_path.exists():
            add_to_non_serving_placeholder_block(index_path, target, source_page_stem)
        if target_path.exists():
            continue
        target_path.write_text(placeholder_content(target, source_page_stem), encoding="utf-8")
        created.append(target_path.name)

    if created:
        print("CREATED")
        for name in created:
            print(f"- {name}")
    else:
        print("NOOP")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
