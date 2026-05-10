#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parents[3]
ROOT = Path(os.environ.get('RESEARCHKB_RESET_ROOT', DEFAULT_ROOT)).resolve()
ONTOLOGY = ROOT / 'ontology'
ENTITIES = ROOT / 'ontology' / 'entities'
RELATIONS = ROOT / 'ontology' / 'relations'
LOG_FILE = ROOT / 'ontology' / 'log.md'
RAW_SOURCES = ROOT / 'ontology' / 'entities' / 'raw-sources'
RAW_SOURCE_FILES = ROOT / 'ontology' / 'entities' / 'raw-sources' / 'files'
RESET_ENTITY_DIRS = [
    'papers',
    'methods',
    'concepts',
    'tasks',
    'scenarios',
    'benchmarks',
    'evidence',
]
EMPTY_LOG = '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n'
INDEX_MANAGED_BLOCK_NAMES = {
    'papers': ['navigation-entries', 'non-serving-placeholders'],
    'methods': ['navigation-entries', 'non-serving-placeholders'],
    'concepts': ['navigation-entries', 'non-serving-placeholders'],
    'tasks': ['navigation-entries', 'non-serving-placeholders'],
    'scenarios': ['navigation-entries', 'non-serving-placeholders'],
    'benchmarks': ['navigation-entries', 'non-serving-placeholders'],
    'evidence': ['navigation-entries', 'non-serving-placeholders'],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    return parser.parse_args()


def ontology_is_dirty() -> bool:
    result = subprocess.run(
        ['git', 'status', '--short', '--', 'ontology'],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    return bool(result.stdout.strip())


def run_lint() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def clear_relation_ledger_text(text: str) -> str:
    marker = '## 实例边'
    if marker not in text:
        raise ValueError('missing ## 实例边 heading in relation ledger')
    prefix = text.split(marker, 1)[0].rstrip()
    return f"{prefix}\n\n{marker}\n- 无\n"


def clear_relation_ledgers(relations_dir: Path) -> None:
    for path in sorted(relations_dir.glob('*.md')):
        cleared = clear_relation_ledger_text(path.read_text(encoding='utf-8'))
        path.write_text(cleared, encoding='utf-8')


def clear_managed_block(text: str, block_name: str) -> str:
    begin = f'<!-- BEGIN MANAGED BLOCK:{block_name} -->'
    end = f'<!-- END MANAGED BLOCK:{block_name} -->'
    if begin not in text or end not in text:
        raise ValueError(f'missing managed block markers for {block_name}')
    before, remainder = text.split(begin, 1)
    _middle, after = remainder.split(end, 1)
    return f'{before}{begin}\n{end}{after}'


def clear_index_managed_blocks(entities_dir: Path) -> None:
    for dirname, block_names in INDEX_MANAGED_BLOCK_NAMES.items():
        index_path = entities_dir / dirname / 'index.md'
        text = index_path.read_text(encoding='utf-8')
        for block_name in block_names:
            text = clear_managed_block(text, block_name)
        index_path.write_text(text, encoding='utf-8')


def clear_entity_instance_pages(entities_dir: Path) -> None:
    for dirname in RESET_ENTITY_DIRS:
        entity_dir = entities_dir / dirname
        entity_dir.mkdir(parents=True, exist_ok=True)
        for path in entity_dir.glob('*.md'):
            if path.name != 'index.md':
                path.unlink()


def write_empty_log(log_path: Path) -> None:
    log_path.write_text(EMPTY_LOG, encoding='utf-8')


def ensure_required_paths() -> None:
    if not ONTOLOGY.exists():
        raise FileNotFoundError(f'missing ontology directory: {ONTOLOGY}')
    if not ENTITIES.exists():
        raise FileNotFoundError(f'missing entities directory: {ENTITIES}')
    if not RELATIONS.exists():
        raise FileNotFoundError(f'missing relations directory: {RELATIONS}')
    if not RAW_SOURCES.exists():
        raise FileNotFoundError(f'missing raw-sources directory: {RAW_SOURCES}')
    if not RAW_SOURCE_FILES.exists():
        raise FileNotFoundError(f'missing raw-source files directory: {RAW_SOURCE_FILES}')


def reset_live_ontology() -> None:
    ensure_required_paths()
    clear_entity_instance_pages(ENTITIES)
    clear_relation_ledgers(RELATIONS)
    write_empty_log(LOG_FILE)
    clear_index_managed_blocks(ENTITIES)


def main() -> int:
    args = parse_args()

    try:
        ensure_required_paths()
    except FileNotFoundError as exc:
        print(f'failed: {exc}')
        return 1

    if ontology_is_dirty() and not args.force:
        print('blocked: ontology has uncommitted changes; rerun with --force to overwrite')
        return 2

    if args.check_only:
        print('success: live-derived reset preconditions satisfied')
        return 0

    try:
        reset_live_ontology()
    except ValueError as exc:
        print(f'failed: {exc}')
        return 1

    lint = run_lint()
    sys.stdout.write(lint.stdout)
    sys.stderr.write(lint.stderr)
    if lint.returncode != 0:
        print('failed: restored baseline did not pass lint')
        return 1

    print('success: ontology restored to empty baseline')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
