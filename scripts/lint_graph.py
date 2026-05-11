from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")

REQUIRED_DIRECTORIES = [
    'ontology/entities/tasks',
    'ontology/entities/benchmarks',
    'ontology/entities/papers',
    'ontology/entities/methods',
    'ontology/entities/scenarios',
    'ontology/relations',
    'ontology/entities/evidence',
    'ontology/entities/raw-sources',
    'scripts',
]

REQUIRED_FILES = [
    'ontology/graph-standard.md',
    'ontology/log.md',
    'ontology/entities/benchmarks/index.md',
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/surveys_method.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
    'scripts/lint_graph.py',
]

CLAUDE_NEEDLES = [
    'ontology/entities/tasks/',
    'ontology/entities/benchmarks/',
    'ontology/graph-standard.md',
    'ontology/relations/',
    'python3 scripts/lint_graph.py',
]

PIPELINE_SKILL_FILES = [
    '.claude/skills/relation-reconciliation/SKILL.md',
    '.claude/skills/page-projection-sync/SKILL.md',
    '.claude/skills/index-sync/SKILL.md',
]

PAPER_INGEST_NEEDLES = [
    'relation_candidates',
    'relation_exemptions',
    'semantic_stub_candidates',
    'relation-reconciliation',
    'page-projection-sync',
    'index-sync',
]

DAILY_INGEST_CHAIN_NEEDLES = [
    'relation-reconciliation',
    'page-projection-sync',
    'index-sync',
    'ontology-semantic-review',
    'serving-governance-review',
]

INDEX_SYNC_NEEDLES = [
    '# Index Sync',
    '受管区块',
    'synced_indexes',
    'skipped_pages',
    'manual_followups',
    '`placeholder`：只进入 non-serving block',
    '`partial`：Method 页可进入默认导航入口；其他类型仍可被 index 收录但不自动等同 serving-ready',
    '`serving-ready`：进入默认导航入口',
]

GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    '`cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`',
    '方法机制优先绑定 `sections.md`。',
    '`ontology/relations/proposes.md`：维护 `proposes`',
    '`ontology/relations/evaluated_on.md`：维护 `evaluated_on`',
    '`ontology/relations/supported_by.md`：维护 `supported_by`',
    '`ontology/relations/sourced_from.md`：维护 `sourced_from`',
    '## Index 导航投影层',
    '`index-sync`',
    '可被 index 收录',
    '默认 serving 入口',
    'semantic stub',
    '## 最小定义/角色',
    '`partial` 表示对象可被正式链接',
    '不构成 serving 治理失败依据',
]
SERVING_GOVERNANCE_NEEDLES = [
    'domain index pages',
    'default navigation/QA entry surfaces',
    'phase-1 合法稳态',
    '而不是自动降为 `needs_fixes`',
]
DOMAIN_INDEX_FILES = [
    'ontology/entities/papers/index.md',
    'ontology/entities/methods/index.md',
    'ontology/entities/tasks/index.md',
    'ontology/entities/scenarios/index.md',
    'ontology/entities/benchmarks/index.md',
    'ontology/entities/evidence/index.md',
    'ontology/entities/raw-sources/index.md',
]

INDEX_MANAGED_BLOCKS = {
    'ontology/entities/papers/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/methods/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/tasks/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/scenarios/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/benchmarks/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/evidence/index.md': ['navigation-entries', 'non-serving-placeholders'],
    'ontology/entities/raw-sources/index.md': ['navigation-entries'],
}

INDEX_ENTRY_PATH_RE = re.compile(r'（文档：`(?P<doc>[^`]+)`）：\[\[(?P<link>[^\]]+)\]\]')
ALLOWED_EVIDENCE_CACHE_TYPES = {'sections', 'refs', 'experiments', 'analysis'}

SERVING_TYPE_RULES = {
    'paper': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {},
    },
    'method_processed': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
    'method_partial': {
        'required_headings': ['## Object semantics', '## 当前定位', '## 与知识库现有内容的关系', '## 最小定义/角色', '## 待补充', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'method_placeholder': {
        'required_headings': ['## 当前定位', '## 与知识库现有内容的关系', '## 待补充'],
        'strong_frontmatter_fields': set(),
    },
    'task': {
        'required_headings': ['## 相关 benchmark', '## 证据来源 / 关系索引', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'scenario': {
        'required_headings': ['## 相关任务', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'benchmark': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
    'evidence': {
        'required_headings': ['## 对应正式知识节点', '## 本节支撑什么', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': set(),
    },
}

FORBIDDEN_FULL_REFERENCE_NEEDLES = (
    '.full|',
    '.full]]',
    'cache_type: full',
    '高保真工作底稿',
)
FULL_REFERENCE_SCAN_PATHS = [
    ROOT / 'ontology',
    ROOT / 'ontology' / 'entities' / 'evidence',
    ROOT / '.claude' / 'skills',
    ROOT / 'CLAUDE.md',
]
FULL_REFERENCE_SCAN_SUFFIXES = {
    ROOT / 'ontology': ('.md',),
    ROOT / 'ontology' / 'entities' / 'evidence': ('.md',),
    ROOT / '.claude' / 'skills': ('.md', '.json'),
}

FORMAL_RELATION_RE = re.compile(r"- \[\[(?P<src>[^\]]+)\]\] --(?P<rel>[^`\n]+)--> \[\[(?P<dst>[^\]]+)\]\]")
LEGACY_FULL_EDGE_RE = re.compile(r"- `\[\[(?P<src>[^\]]+)\]\] --(?P<rel>[^`]+)--> \[\[(?P<dst>[^\]]+)\]\]`")
SEMI_EXPANDED_RELATION_RE = re.compile(
    r"- `(?P<rel>[^`]+)`：(?P<label>[^（]+)（文档：`(?P<doc>[^`]+)`）：\[\[(?P<link_target>[^\]|]+)(?:\|(?P<link_label>[^\]]+))?\]\]"
)
BODY_WIKILINK_RE = re.compile(r"\[\[(?P<link>[^\]]+)\]\]")
BASE_RELATION_CHILD_FIELD_ORDER = [
    'source_path',
    'target_path',
    'edge_semantics',
    'evidence',
    'evidence_link',
    'evidence_path',
]
REFERENCES_METHOD_CHILD_FIELD_ORDER = [
    'source_path',
    'target_path',
    'source_paper_path',
    'target_paper_path',
    'edge_semantics',
    'evidence',
    'evidence_link',
    'evidence_path',
]
RELATION_LEDGER_FILES = [
    'ontology/relations/cites.md',
    'ontology/relations/proposes.md',
    'ontology/relations/surveys_method.md',
    'ontology/relations/based_on.md',
    'ontology/relations/references_method.md',
    'ontology/relations/targets_task.md',
    'ontology/relations/applied_in.md',
    'ontology/relations/evaluated_on.md',
    'ontology/relations/supported_by.md',
    'ontology/relations/sourced_from.md',
]
ROLE_SENTENCE_BY_HEADING = {
    '### Outgoing': [
        '当前对象作为 source；以下列出当前对象指向的邻接对象。',
        '当前对象作为 source；以下列出当前对象指向的 relation 实例。',
    ],
    '### Incoming': [
        '当前对象作为 target；以下列出指向当前对象的邻接对象。',
        '当前对象作为 target；以下列出指向当前对象的 relation 实例。',
    ],
}
SUPPORTED_BY_ALLOWED_SOURCES = {'Method', 'Task', 'Scenario', 'Benchmark'}
EVALUATED_ON_ALLOWED_SOURCES = {'Method'}
ENTITY_TITLE_TO_TYPE = {
    'PathMind': 'Method',
    'knowledge-graph-reasoning': 'Task',
    'kgqa': 'Task',
    'multi-hop-qa': 'Task',
    '企业知识图谱问答': 'Scenario',
    'WebQSP': 'Benchmark',
    'CWQ': 'Benchmark',
    'PathMind.sections': 'Evidence',
    'PathMind.refs': 'Evidence',
    'PathMind.experiments': 'Evidence',
    'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models': 'Paper',
}
ENTITY_DIRS_BY_TYPE = {
    'Paper': ROOT / 'ontology' / 'entities' / 'papers',
    'Method': ROOT / 'ontology' / 'entities' / 'methods',
    'Task': ROOT / 'ontology' / 'entities' / 'tasks',
    'Scenario': ROOT / 'ontology' / 'entities' / 'scenarios',
    'Benchmark': ROOT / 'ontology' / 'entities' / 'benchmarks',
    'Evidence': ROOT / 'ontology' / 'entities' / 'evidence',
}
FRONTMATTER_FIELD_RE = re.compile(r'^(?P<key>[a-z_]+):\s*(?P<value>.+)$', re.MULTILINE)


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8', errors='ignore')


def split_frontmatter(text: str) -> tuple[dict[str, list[str] | str], str]:
    if not text.startswith('---\n'):
        return {}, text
    _, rest = text.split('---\n', 1)
    frontmatter_block, body = rest.split('\n---\n', 1)
    data: dict[str, list[str] | str] = {}
    for match in FRONTMATTER_FIELD_RE.finditer(frontmatter_block):
        key = match.group('key')
        raw = match.group('value').strip()
        if raw.startswith('[') and raw.endswith(']'):
            inner = raw[1:-1].strip()
            data[key] = [] if not inner else [part.strip() for part in inner.split(',')]
        else:
            data[key] = raw
    return data, body


def extract_legacy_full_edge_lines(text: str) -> list[str]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    return [line.strip() for line in formal_block.splitlines() if LEGACY_FULL_EDGE_RE.match(line.strip())]


def extract_projected_links(text: str) -> dict[str, set[str]]:
    if '## Formal relations' not in text:
        return {'Outgoing': set(), 'Incoming': set()}
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    result = {'Outgoing': set(), 'Incoming': set()}
    current = None
    for raw_line in formal_block.splitlines():
        line = raw_line.strip()
        if line == '### Outgoing':
            current = 'Outgoing'
            continue
        if line == '### Incoming':
            current = 'Incoming'
            continue
        if current and (match := SEMI_EXPANDED_RELATION_RE.match(line)):
            link = match.group('link_target')
            if match.group('link_label'):
                link = f"{link}|{match.group('link_label')}"
            result[current].add(link)
    return result


def extract_projected_relation_keys(text: str) -> set[tuple[str, str, str]]:
    keys: set[tuple[str, str, str]] = set()
    for item in parse_projected_relation_items(text):
        main_line = item['main_line']
        match = SEMI_EXPANDED_RELATION_RE.match(main_line)
        if not match:
            continue
        heading = item['heading']
        relation_type = match.group('rel').strip()
        document_path = match.group('doc').strip()
        keys.add((heading, relation_type, document_path))
    return keys


def is_object_page_relpath(rel_path: str) -> bool:
    return (
        rel_path.startswith('ontology/entities/papers/')
        or rel_path.startswith('ontology/entities/methods/')
        or rel_path.startswith('ontology/entities/tasks/')
        or rel_path.startswith('ontology/entities/scenarios/')
        or rel_path.startswith('ontology/entities/benchmarks/')
        or rel_path.startswith('ontology/entities/evidence/')
    )


def is_rawsource_relpath(rel_path: str) -> bool:
    return rel_path.startswith('ontology/entities/raw-sources/files/')


def extract_formal_relations(text: str) -> list[tuple[str, str, str]]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    edges: list[tuple[str, str, str]] = []
    for match in FORMAL_RELATION_RE.finditer(formal_block):
        edges.append((match.group('src'), match.group('rel'), match.group('dst')))
    return edges


def extract_managed_block(text: str, name: str) -> str | None:
    start = f'<!-- BEGIN MANAGED BLOCK:{name} -->'
    end = f'<!-- END MANAGED BLOCK:{name} -->'
    if start not in text or end not in text:
        return None
    return text.split(start, 1)[1].split(end, 1)[0]


def extract_ledger_edges(text: str) -> list[tuple[str, str, str]]:
    edges: list[tuple[str, str, str]] = []
    for match in FORMAL_RELATION_RE.finditer(text):
        edges.append((match.group('src'), match.group('rel'), match.group('dst')))
    return edges


def extract_relation_ledger_blocks(text: str) -> tuple[str, str] | None:
    if '## 关系语义说明' not in text or '## 实例边' not in text:
        return None
    semantic_block = text.split('## 关系语义说明', 1)[1].split('## 实例边', 1)[0]
    ledger_block = text.split('## 实例边', 1)[1]
    return semantic_block, ledger_block


def parse_relation_instance_records(text: str) -> list[dict[str, object]]:
    blocks = extract_relation_ledger_blocks(text)
    if blocks is None:
        return []
    _semantic_block, ledger_block = blocks
    records: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    for raw_line in ledger_block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped == '- 无':
            continue
        if stripped.startswith('- [[') and '--' in stripped:
            match = FORMAL_RELATION_RE.match(stripped)
            if not match:
                continue
            current = {
                'main_line': stripped,
                'src': match.group('src'),
                'rel': match.group('rel'),
                'dst': match.group('dst'),
                'fields': [],
            }
            records.append(current)
            continue
        if current is not None and stripped.startswith('- '):
            field_line = stripped[2:]
            if ': ' not in field_line:
                continue
            key, value = field_line.split(': ', 1)
            current['fields'].append((key, value))
    return records


def extract_relation_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if match := FORMAL_RELATION_RE.match(line.strip()):
            current = {
                'source': match.group('src').strip(),
                'relation_type': match.group('rel').strip(),
                'target': match.group('dst').strip(),
            }
            records.append(current)
            continue
        if current and line.startswith('  - '):
            key, _, value = line[4:].partition(':')
            if _:
                current[key.strip()] = value.strip()
        elif line.strip() and not line.startswith('  - '):
            current = None
    return records


def load_relation_records(rel_path: str) -> list[dict[str, str]]:
    return extract_relation_records(read_text(rel_path))


def collect_relation_page_wikilinks(text: str) -> list[str]:
    return [match.group('link') for match in BODY_WIKILINK_RE.finditer(text)]


def validate_relation_ledger(rel: str, text: str) -> list[str]:
    errors: list[str] = []
    blocks = extract_relation_ledger_blocks(text)
    if blocks is None:
        errors.append(f'missing relation ledger sections in {rel}')
        return errors
    semantic_block, _ledger_block = blocks

    for match in BODY_WIKILINK_RE.finditer(semantic_block):
        errors.append(
            f'forbidden relation-page wikilink outside allowed positions in {rel}: {match.group("link")}'
        )

    records = parse_relation_instance_records(text)
    for record in records:
        field_pairs = record['fields']
        field_names = [key for key, _value in field_pairs]
        expected_field_order = (
            REFERENCES_METHOD_CHILD_FIELD_ORDER
            if record['rel'] == 'references_method'
            else BASE_RELATION_CHILD_FIELD_ORDER
        )
        if field_names != expected_field_order:
            errors.append(f'invalid relation child-field order in {rel}')
            continue
        field_map = dict(field_pairs)
        forbidden_fields = ['source_path', 'target_path', 'edge_semantics', 'evidence', 'evidence_path']
        if record['rel'] == 'references_method':
            forbidden_fields = [
                'source_path',
                'target_path',
                'source_paper_path',
                'target_paper_path',
                'edge_semantics',
                'evidence',
                'evidence_path',
            ]
        for forbidden_field in forbidden_fields:
            if WIKILINK_RE.search(field_map[forbidden_field]):
                errors.append(
                    f'forbidden relation-page wikilink outside allowed positions in {rel}: {field_map[forbidden_field]}'
                )
        if record['rel'] == 'references_method':
            for paper_field in ['source_paper_path', 'target_paper_path']:
                value = field_map[paper_field]
                if not value.startswith('ontology/entities/papers/') or not value.endswith('.md'):
                    errors.append(f'invalid references_method paper path in {rel}: {value}')
                    continue
                if not (ROOT / value).exists():
                    errors.append(f'missing references_method paper path target in {rel}: {value}')
    return errors


def validate_index_pages(errors: list[str]) -> None:
    for rel in DOMAIN_INDEX_FILES:
        path = ROOT / rel
        if not path.exists():
            errors.append(f'missing domain index file: {rel}')
            continue
        text = read_text(rel)
        for block_name in INDEX_MANAGED_BLOCKS[rel]:
            block = extract_managed_block(text, block_name)
            if block is None:
                errors.append(f'missing managed block {block_name} in {rel}')

        if '## 5. 相关关系账本' in text:
            errors.append(f'legacy relation-entry section must be removed from {rel}')

        navigation_block = extract_managed_block(text, 'navigation-entries') or ''
        placeholder_block = extract_managed_block(text, 'non-serving-placeholders') or ''

        for line in [ln.rstrip() for ln in navigation_block.splitlines() if ln.strip()]:
            stripped = line.strip()
            if not stripped.startswith('- '):
                continue
            if line.startswith('  - '):
                continue
            if '（文档：`' not in stripped or '）：[[' not in stripped:
                errors.append(f'missing navigation entry document-path format in {rel}: {stripped}')
                continue
            if '状态=placeholder' in stripped or '占位节点' in stripped:
                errors.append(f'placeholder promoted into navigation entries in {rel}: {stripped}')
            match = INDEX_ENTRY_PATH_RE.search(stripped)
            if match:
                target_path = ROOT / match.group('doc')
                if not target_path.exists():
                    errors.append(f'missing index entry target file in {rel}: {match.group("doc")}')

        validate_index_entry_projection(navigation_block, rel, errors)

        if 'non-serving-placeholders' in text:
            for line in [ln.rstrip() for ln in placeholder_block.splitlines() if ln.strip()]:
                stripped = line.strip()
                if not stripped.startswith('- '):
                    continue
                if line.startswith('  - '):
                    continue
                if '（文档：`' not in stripped or '）：[[' not in stripped:
                    errors.append(f'missing placeholder entry document-path format in {rel}: {stripped}')
                    continue
                match = INDEX_ENTRY_PATH_RE.search(stripped)
                if match:
                    target_path = ROOT / match.group('doc')
                    if not target_path.exists():
                        errors.append(f'missing index entry target file in {rel}: {match.group("doc")}')
            validate_index_entry_projection(placeholder_block, rel, errors)


def check_evidence_cache_types(errors):
    for path in sorted((ROOT / 'intermediate' / 'papers').glob('*.md')):
        text = path.read_text(encoding='utf-8')
        match = re.search(r'^cache_type:\s*([^\n]+)$', text, re.MULTILINE)
        if not match:
            errors.append(f"Missing cache_type in evidence cache: {path.relative_to(ROOT)}")
            continue
        cache_type = match.group(1).strip()
        if cache_type not in ALLOWED_EVIDENCE_CACHE_TYPES:
            errors.append(
                f"Forbidden or undeclared cache_type '{cache_type}' in {path.relative_to(ROOT)}"
            )


def check_forbidden_full_references(errors):
    for scan_path in FULL_REFERENCE_SCAN_PATHS:
        if scan_path.is_file():
            paths = [scan_path]
        else:
            suffixes = FULL_REFERENCE_SCAN_SUFFIXES.get(scan_path, ('.md',))
            paths = sorted(
                p for p in scan_path.rglob('*') if p.is_file() and p.suffix in suffixes
            )
        for path in paths:
            text = path.read_text(encoding='utf-8')
            for needle in FORBIDDEN_FULL_REFERENCE_NEEDLES:
                if needle in text:
                    errors.append(f"Forbidden full-cache reference '{needle}' found in {path.relative_to(ROOT)}")


def classify_serving_page(rel: str) -> str | None:
    if rel.startswith('ontology/entities/papers/'):
        return 'paper'
    if rel.startswith('ontology/entities/methods/'):
        return 'method'
    if rel.startswith('ontology/entities/tasks/'):
        return 'task'
    if rel.startswith('ontology/entities/scenarios/'):
        return 'scenario'
    if rel.startswith('ontology/entities/benchmarks/'):
        return 'benchmark'
    if rel.startswith('ontology/entities/evidence/'):
        return 'evidence'
    return None


def validate_serving_structure(rel: str, text: str, page_type: str) -> list[str]:
    frontmatter, _body = split_frontmatter(text)
    if page_type == 'method':
        status = frontmatter.get('status')
        if status == 'placeholder':
            page_errors = [f'Method placeholder status is no longer allowed: {rel}']
            status = 'partial'
        else:
            page_errors = []
        if status == 'partial':
            rules = SERVING_TYPE_RULES['method_partial']
        else:
            rules = SERVING_TYPE_RULES['method_processed']
    else:
        rules = SERVING_TYPE_RULES[page_type]
        page_errors = []
    for heading in rules['required_headings']:
        if heading not in text:
            page_errors.append(f'missing serving heading {heading} in {rel}')
    return page_errors


def infer_entity_type_from_name(name: str) -> str | None:
    if name in ENTITY_TITLE_TO_TYPE:
        return ENTITY_TITLE_TO_TYPE[name]
    for entity_type, directory in ENTITY_DIRS_BY_TYPE.items():
        candidate = directory / f'{name}.md'
        if candidate.exists():
            return entity_type
    return None


def extract_non_formal_relations_text(text: str) -> str:
    if '## Formal relations' not in text:
        return text
    before, after = text.split('## Formal relations', 1)
    next_heading = after.find('\n## ')
    if next_heading == -1:
        return before
    return before + after[next_heading + 1:]


def validate_no_generated_display_aliases(rel: str, text: str) -> list[str]:
    page_errors: list[str] = []
    if not rel.startswith('ontology/entities/'):
        return page_errors
    for match in BODY_WIKILINK_RE.finditer(text):
        link = match.group('link')
        if not link.startswith('../'):
            continue
        if '|' in link:
            page_errors.append(f'generated object-page link must omit display alias in {rel}: {link}')
    return page_errors


def parse_projected_relation_items(text: str) -> list[dict[str, object]]:
    if '## Formal relations' not in text:
        return []
    _, formal_tail = text.split('## Formal relations', 1)
    next_heading = formal_tail.find('\n## ')
    formal_block = formal_tail if next_heading == -1 else formal_tail[:next_heading]
    items: list[dict[str, object]] = []
    current: dict[str, object] | None = None
    current_heading = None
    for raw_line in formal_block.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if stripped == '### Outgoing':
            current_heading = 'Outgoing'
            continue
        if stripped == '### Incoming':
            current_heading = 'Incoming'
            continue
        if stripped.startswith('- `') and '（文档：`' in stripped and '）：[[' in stripped:
            current = {'heading': current_heading, 'main_line': stripped, 'fields': []}
            items.append(current)
            continue
        if current is not None and stripped.startswith('- '):
            field_line = stripped[2:]
            if ': ' not in field_line:
                continue
            key, value = field_line.split(': ', 1)
            current['fields'].append((key, value))
    return items


def validate_index_entry_projection(block: str, rel: str, errors: list[str]) -> None:
    lines = [ln.rstrip() for ln in block.splitlines() if ln.strip()]
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line.startswith('- '):
            i += 1
            continue
        child_lines = []
        j = i + 1
        while j < len(lines) and lines[j].startswith('  - '):
            child_lines.append(lines[j].strip())
            j += 1
        if not any(cl.startswith('- object_semantics: ') for cl in child_lines):
            errors.append(f'missing object_semantics projection in {rel}')
        if not any(cl.startswith('- status: ') for cl in child_lines):
            errors.append(f'missing status projection in {rel}')
        i = j


def validate_projection_contract(rel: str, text: str) -> list[str]:
    page_errors: list[str] = []
    if '## Formal relations' not in text:
        return page_errors

    formal_block = text.split('## Formal relations', 1)[1]
    for heading, sentences in ROLE_SENTENCE_BY_HEADING.items():
        if heading in formal_block and not any(sentence in formal_block for sentence in sentences):
            page_errors.append(f'missing role sentence {heading} in {rel}')

    if extract_legacy_full_edge_lines(text):
        page_errors.append(f'legacy full-edge projection found in {rel}')

    projected = extract_projected_links(text)
    allowed_links = projected['Outgoing'] | projected['Incoming']
    body = extract_non_formal_relations_text(text)
    for match in BODY_WIKILINK_RE.finditer(body):
        link = match.group('link')
        if link.startswith('#'):
            continue
        if link not in allowed_links:
            page_errors.append(f'body wikilink missing from Formal relations in {rel}: {link}')

    for item in parse_projected_relation_items(text):
        field_map = dict(item['fields'])
        if 'edge_semantics' not in field_map:
            page_errors.append(f'missing edge_semantics field in projected relation item: {rel}')
        if 'evidence' not in field_map:
            page_errors.append(f'missing evidence field in projected relation item: {rel}')

    if rel.startswith('ontology/entities/evidence/'):
        for match in BODY_WIKILINK_RE.finditer(body):
            target = match.group('link')
            if target.startswith('../papers/') or target.startswith('ontology/entities/papers/'):
                page_errors.append(f'Evidence body may not link to Paper: {rel}')
                break

    return page_errors


def validate_supported_by_contract(errors: list[str]) -> None:
    text = read_text('ontology/relations/supported_by.md')
    for src, rel, _dst in extract_ledger_edges(text):
        if rel != 'supported_by':
            continue
        source_name = src.split('|', 1)[0]
        source_type = infer_entity_type_from_name(source_name)
        if source_type == 'Paper':
            errors.append(f'Paper may not appear as supported_by source: {source_name}')
        elif source_type is None:
            errors.append(f'unknown supported_by source type for {source_name}')
        elif source_type not in SUPPORTED_BY_ALLOWED_SOURCES:
            errors.append(f'unsupported supported_by source type for {source_name}: {source_type}')


def validate_evaluated_on_contract(errors: list[str]) -> None:
    text = read_text('ontology/relations/evaluated_on.md')
    for src, rel, _dst in extract_ledger_edges(text):
        if rel != 'evaluated_on':
            continue
        source_name = src.split('|', 1)[0]
        source_type = infer_entity_type_from_name(source_name)
        if source_type == 'Paper':
            errors.append(f'Paper may not appear as evaluated_on source: {source_name}')
        elif source_type is None:
            errors.append(f'unknown evaluated_on source type for {source_name}')
        elif source_type not in EVALUATED_ON_ALLOWED_SOURCES:
            errors.append(f'unsupported evaluated_on source type for {source_name}: {source_type}')


def validate_method_status_contract(errors: list[str]) -> None:
    for path in (ROOT / 'ontology/entities/methods').glob('*.md'):
        frontmatter, _body = split_frontmatter(path.read_text(encoding='utf-8', errors='ignore'))
        if frontmatter.get('status') == 'placeholder':
            errors.append(f'Method placeholder status is no longer allowed: {path.relative_to(ROOT)}')


def check_references_method_cites_backing(errors: list[str]) -> None:
    cites_records = load_relation_records('ontology/relations/cites.md')
    cites_pairs = {
        (record.get('source_path', ''), record.get('target_path', ''))
        for record in cites_records
        if record.get('relation_type') == 'cites'
    }
    for record in load_relation_records('ontology/relations/references_method.md'):
        source_paper_path = record.get('source_paper_path', '')
        target_paper_path = record.get('target_paper_path', '')
        if not source_paper_path or not target_paper_path:
            continue
        if (source_paper_path, target_paper_path) not in cites_pairs:
            errors.append(
                'references_method paper provenance must be backed by cites: '
                f'{source_paper_path} -> {target_paper_path}'
            )


def check_method_paper_anchors(errors: list[str]) -> None:
    anchor_map: dict[str, set[str]] = {}

    for record in load_relation_records('ontology/relations/proposes.md'):
        target_path = record.get('target_path', '')
        source_path = record.get('source_path', '')
        if target_path.startswith('ontology/entities/methods/') and source_path.startswith('ontology/entities/papers/'):
            anchor_map.setdefault(target_path, set()).add(source_path)

    for record in load_relation_records('ontology/relations/references_method.md'):
        for method_key, paper_key in (('source_path', 'source_paper_path'), ('target_path', 'target_paper_path')):
            method_path = record.get(method_key, '')
            paper_path = record.get(paper_key, '')
            if method_path.startswith('ontology/entities/methods/') and paper_path.startswith('ontology/entities/papers/'):
                anchor_map.setdefault(method_path, set()).add(paper_path)

    for method_path in sorted((ROOT / 'ontology/entities/methods').glob('*.md')):
        rel_path = str(method_path.relative_to(ROOT))
        frontmatter, _ = split_frontmatter(method_path.read_text(encoding='utf-8', errors='ignore'))
        status = frontmatter.get('status')
        if status not in {'partial', 'processed'}:
            continue
        if not anchor_map.get(rel_path):
            errors.append(f'formal/partial Method must resolve to at least one paper anchor: {rel_path}')


def validate_cited_paper_targets(errors: list[str]) -> None:
    cites_text = read_text('ontology/relations/cites.md')
    for _src, rel, dst in extract_ledger_edges(cites_text):
        if rel != 'cites':
            continue
        target_name = dst.split('|', 1)[0]
        target_path = ROOT / 'ontology' / 'entities' / 'papers' / f'{target_name}.md'
        if not target_path.exists():
            errors.append(f'missing cited paper target page: {target_name}')
            continue
        target_text = target_path.read_text(encoding='utf-8', errors='ignore')
        if 'status: placeholder' not in target_text and 'status: processed' not in target_text:
            errors.append(f'cited paper target missing status marker: {target_name}')
        if 'status: placeholder' in target_text:
            for needle in ['## 当前定位', '## 与知识库现有内容的关系', '## 待补充']:
                if needle not in target_text:
                    errors.append(f'missing {needle} in cited placeholder paper: {target_name}')


def validate_ledger_projection_coverage(errors: list[str]) -> None:
    for rel_file in RELATION_LEDGER_FILES:
        text = read_text(rel_file)
        for record in parse_relation_instance_records(text):
            field_map = dict(record['fields'])
            source_path = field_map['source_path']
            target_path = field_map['target_path']
            relation_type = record['rel']
            edge_label = f'{source_path} --{relation_type}--> {target_path}'

            if is_object_page_relpath(source_path):
                source_file = ROOT / source_path
                if source_file.exists():
                    source_text = source_file.read_text(encoding='utf-8', errors='ignore')
                    source_frontmatter, _ = split_frontmatter(source_text)
                    if '## Formal relations' not in source_text:
                        errors.append(f'missing Formal relations on source page for ledger edge: {edge_label}')
                    else:
                        source_keys = extract_projected_relation_keys(source_text)
                        expected_source_key = ('Outgoing', relation_type, target_path)
                        if expected_source_key not in source_keys:
                            errors.append(f'missing outgoing projection for ledger edge: {edge_label}')
                    if source_frontmatter.get('status') == 'placeholder' and '## Formal relations' not in source_text:
                        errors.append(f'formal-bearing placeholder page missing formal relations contract: {source_path}')

            if is_object_page_relpath(target_path):
                target_file = ROOT / target_path
                if target_file.exists():
                    target_text = target_file.read_text(encoding='utf-8', errors='ignore')
                    target_frontmatter, _ = split_frontmatter(target_text)
                    if '## Formal relations' not in target_text:
                        errors.append(f'missing Formal relations on target page for ledger edge: {edge_label}')
                    else:
                        target_keys = extract_projected_relation_keys(target_text)
                        expected_target_key = ('Incoming', relation_type, source_path)
                        if expected_target_key not in target_keys:
                            errors.append(f'missing incoming projection for ledger edge: {edge_label}')
                    if target_frontmatter.get('status') == 'placeholder' and '## Formal relations' not in target_text:
                        errors.append(f'formal-bearing placeholder page missing formal relations contract: {target_path}')
            elif is_rawsource_relpath(target_path):
                continue

def validate_sample_projection(rel: str, rules: dict[str, object]) -> list[str]:
    text = read_text(rel)
    frontmatter, _body = split_frontmatter(text)
    page_errors: list[str] = []
    for key, expected in rules['expected_frontmatter'].items():
        actual = frontmatter.get(key)
        if actual != expected:
            page_errors.append(f'frontmatter mismatch for {key} in {rel}: expected {expected!r}, got {actual!r}')
    actual_edges = set(extract_formal_relations(text))
    for edge in rules['required_edges']:
        if edge not in actual_edges:
            page_errors.append(f'missing formal relation {edge} in {rel}')
    return page_errors


errors: list[str] = []

for rel in REQUIRED_DIRECTORIES:
    path = ROOT / rel
    if not path.exists() or not path.is_dir():
        errors.append(f'missing directory: {rel}')

for rel in REQUIRED_FILES:
    if not (ROOT / rel).exists():
        errors.append(f'missing file: {rel}')

claude_text = read_text('CLAUDE.md')
for needle in CLAUDE_NEEDLES:
    if needle not in claude_text:
        errors.append(f'missing {needle} in CLAUDE.md')

paper_ingest_text = read_text('.claude/skills/paper-ingest/SKILL.md')
for needle in PAPER_INGEST_NEEDLES:
    if needle not in paper_ingest_text:
        errors.append(f'missing {needle} in .claude/skills/paper-ingest/SKILL.md')

for needle in DAILY_INGEST_CHAIN_NEEDLES:
    if needle not in read_text('CLAUDE.md'):
        errors.append(f'missing {needle} in CLAUDE.md daily ingest chain')

page_projection_text = read_text('.claude/skills/page-projection-sync/SKILL.md')
for needle in ['index-sync', 'ontology-semantic-review', 'serving-governance-review', 'semantic_stub_candidates', 'serving_status_recommendations', '## 最小定义/角色', 'status: partial']:
    if needle not in page_projection_text:
        errors.append(f'missing {needle} in page-projection-sync handoff')

if 'page-projection-sync' not in read_text('.claude/skills/relation-reconciliation/SKILL.md'):
    errors.append('missing page-projection-sync in relation-reconciliation handoff')
for needle in ['affected_stub_pages', 'serving_status_recommendations']:
    if needle not in read_text('.claude/skills/relation-reconciliation/SKILL.md'):
        errors.append(f'missing {needle} in relation-reconciliation output contract')

index_sync_path = ROOT / '.claude/skills/index-sync/SKILL.md'
if index_sync_path.exists():
    index_sync_text = read_text('.claude/skills/index-sync/SKILL.md')
    for needle in INDEX_SYNC_NEEDLES:
        if needle not in index_sync_text:
            errors.append(f'missing {needle} in .claude/skills/index-sync/SKILL.md')

for rel in PIPELINE_SKILL_FILES:
    if not (ROOT / rel).exists():
        errors.append(f'missing pipeline skill file: {rel}')

graph_standard_text = read_text('ontology/graph-standard.md')
for needle in GRAPH_STANDARD_NEEDLES:
    if needle not in graph_standard_text:
        errors.append(f'missing {needle} in ontology/graph-standard.md')

serving_review_text = read_text('.claude/skills/serving-governance-review/SKILL.md')
for needle in SERVING_GOVERNANCE_NEEDLES:
    if needle not in serving_review_text:
        errors.append(f'missing {needle} in .claude/skills/serving-governance-review/SKILL.md')

check_evidence_cache_types(errors)
check_forbidden_full_references(errors)
validate_index_pages(errors)
validate_cited_paper_targets(errors)
validate_supported_by_contract(errors)
validate_evaluated_on_contract(errors)
validate_method_status_contract(errors)
check_references_method_cites_backing(errors)
check_method_paper_anchors(errors)
validate_ledger_projection_coverage(errors)

for path in (ROOT / 'ontology').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type is None:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))
        errors.extend(validate_projection_contract(rel, text))
    errors.extend(validate_no_generated_display_aliases(rel, text))

for path in (ROOT / 'ontology/entities/evidence').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type != 'evidence':
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))
        errors.extend(validate_projection_contract(rel, text))
    errors.extend(validate_no_generated_display_aliases(rel, text))

for rel in RELATION_LEDGER_FILES:
    text = read_text(rel)
    errors.extend(validate_relation_ledger(rel, text))

if '## `sourced_from` 实例边' in read_text('ontology/relations/supported_by.md'):
    errors.append('sourced_from must live in ontology/relations/sourced_from.md, not ontology/relations/supported_by.md')

knowledge_pages = []
with_wikilinks = 0
for path in (ROOT / 'ontology').rglob('*.md'):
    knowledge_pages.append(path)
    rel = str(path.relative_to(ROOT))
    text = path.read_text(encoding='utf-8', errors='ignore')
    if rel in RELATION_LEDGER_FILES and '## 实例边\n- 无' in text:
        with_wikilinks += 1
        continue
    if rel in DOMAIN_INDEX_FILES:
        navigation_block = extract_managed_block(text, 'navigation-entries') or ''
        placeholder_block = extract_managed_block(text, 'non-serving-placeholders') or ''
        if not navigation_block.strip() and not placeholder_block.strip():
            with_wikilinks += 1
            continue
    if WIKILINK_RE.search(text):
        with_wikilinks += 1
    else:
        if path.relative_to(ROOT).as_posix() != 'ontology/relations/surveys_method.md':
            errors.append(f'ontology page has no wikilinks: {path.relative_to(ROOT)}')

if errors:
    print('FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('PASS: graph lint succeeded')
print({'ontology_pages': len(knowledge_pages), 'with_wikilinks': with_wikilinks})
