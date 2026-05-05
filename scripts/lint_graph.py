from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
WIKILINK_RE = re.compile(r"\[\[[^\]]+\]\]")

REQUIRED_DIRECTORIES = [
    'wiki/tasks',
    'wiki/benchmarks',
    'wiki/ontology',
    'wiki/relations',
    'intermediate/papers',
    'scripts',
]

REQUIRED_FILES = [
    'wiki/ontology/graph-standard.md',
    'wiki/relations/citation_graph.md',
    'wiki/relations/method_evolution.md',
    'wiki/relations/concept_links.md',
    'wiki/relations/task_method_map.md',
    'wiki/relations/evidence_index.md',
    'wiki/relations/paper_method_links.md',
    'wiki/relations/benchmark_links.md',
    'wiki/relations/provenance_links.md',
    'scripts/lint_graph.py',
]

PHASE_ONE_CORE_PAGES = {
    'wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md': {
        'links': [
            '[[PathMind',
            '[[路径优先化]]',
            '[[重要推理路径]]',
            '[[knowledge-graph-reasoning]]',
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[WebQSP]]',
            '[[CWQ]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 与知识库其他内容的关联', '## 证据来源'],
    },
    'wiki/methods/PathMind.md': {
        'links': [
            '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]',
            '[[路径优先化]]',
            '[[重要推理路径]]',
            '[[知识图谱推理问答]]',
            '[[knowledge-graph-reasoning]]',
            '[[WebQSP]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 方法演化位置', '## 证据来源'],
    },
    'wiki/concepts/路径优先化.md': {
        'links': [
            '[[PathMind]]',
            '[[knowledge-graph-reasoning]]',
            '[[知识图谱推理问答]]',
            '[[concept_links]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 证据来源'],
    },
    'wiki/concepts/重要推理路径.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[knowledge-graph-reasoning]]',
            '[[concept_links]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 证据来源'],
    },
    'wiki/scenarios/知识图谱推理问答.md': {
        'links': [
            '[[PathMind]]',
            '[[RoG]]',
            '[[GCR]]',
            '[[knowledge-graph-reasoning]]',
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[WebQSP]]',
            '[[CWQ]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 相关任务', '## 证据来源'],
    },
    'wiki/tasks/knowledge-graph-reasoning.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 证据来源 / 关系索引'],
    },
    'wiki/tasks/kgqa.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 证据来源 / 关系索引'],
    },
    'wiki/tasks/multi-hop-qa.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 证据来源 / 关系索引'],
    },
    'wiki/benchmarks/WebQSP.md': {
        'links': [
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[PathMind]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关任务', '## 证据来源'],
    },
    'wiki/benchmarks/CWQ.md': {
        'links': [
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[PathMind]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关任务', '## 证据来源'],
    },
    'wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[LLM增强知识图谱]]',
            '[[engineering-design-knowledge-management]]',
            '[[复杂产品设计]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.analysis',
        ],
        'sections': ['## 核心方法 / 框架', '## 证据来源'],
    },
    'wiki/scenarios/复杂产品设计.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[LLM增强知识图谱]]',
            '[[engineering-design-knowledge-management]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.analysis',
        ],
        'sections': ['## 使用的主要方法 / 框架 / 概念', '## 证据来源'],
    },
    'wiki/concepts/LLM增强知识图谱.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[复杂产品设计]]',
            '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 证据来源'],
    },
    'wiki/concepts/复杂产品设计中的LLM-KG协同框架.md': {
        'links': [
            '[[LLM增强知识图谱]]',
            '[[复杂产品设计]]',
            '[[engineering-design-knowledge-management]]',
            '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 证据来源'],
    },
    'wiki/tasks/engineering-design-knowledge-management.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[复杂产品设计]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关框架 / 概念', '## 证据来源 / 关系索引'],
    },
}

PHASE_ONE_EVIDENCE_CACHES = {
    'method': [
        'intermediate/papers/PathMind.sections.md',
        'intermediate/papers/PathMind.refs.md',
        'intermediate/papers/PathMind.experiments.md',
    ],
    'survey': [
        'intermediate/papers/LLM-KG-CPD-Survey.sections.md',
        'intermediate/papers/LLM-KG-CPD-Survey.refs.md',
        'intermediate/papers/LLM-KG-CPD-Survey.analysis.md',
    ],
}

FORMAL_PAPER = '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]'
SURVEY_PAPER = '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]'
CLAUDE_NEEDLES = [
    'tasks/',
    'benchmarks/',
    'wiki/ontology/',
    'wiki/relations/',
    'python3 scripts/lint_graph.py',
]
PIPELINE_SKILL_FILES = [
    '.claude/skills/relation-reconciliation/SKILL.md',
    '.claude/skills/page-projection-sync/SKILL.md',
]

PAPER_INGEST_NEEDLES = [
    'relation_candidates',
    'relation_exemptions',
    'relation-reconciliation',
    'page-projection-sync',
]

DAILY_INGEST_CHAIN_NEEDLES = [
    'relation-reconciliation',
    'page-projection-sync',
    'ontology-semantic-review',
    'serving-governance-review',
]
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    '`cache_type` 使用 `sections` / `refs` / `experiments` / `analysis`',
    '方法机制优先绑定 `sections.md`。',
    'paper_method_links.md',
    'benchmark_links.md',
    'provenance_links.md',
    '`wiki/relations/paper_method_links.md`：维护 `proposes`',
    '`wiki/relations/benchmark_links.md`：维护 `evaluated_on`',
    '`wiki/relations/evidence_index.md`：维护 `supported_by`',
    '`wiki/relations/provenance_links.md`：维护 `sourced_from`',
]
INDEX_NEEDLES = [
    '[[graph-standard]]',
    '[[paper_method_links]]',
    '[[benchmark_links]]',
    '[[provenance_links]]',
]
NAVIGATION_ENTRY_PATH = 'wiki/ontology/index.md'
RELATION_LEDGER_NEEDLES = {
    'wiki/relations/paper_method_links.md': [
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]',
        '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]',
    ],
    'wiki/relations/benchmark_links.md': [
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]',
        '[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]',
        '[[PathMind]] --evaluated_on--> [[WebQSP]]',
        '[[PathMind]] --evaluated_on--> [[CWQ]]',
    ],
    'wiki/relations/provenance_links.md': [
        '[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]',
        '[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]',
    ],
}

PLACEHOLDER_PAPERS = {
    'wiki/papers/Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning.md',
    'wiki/papers/Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models.md',
    'wiki/papers/An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering.md',
    'wiki/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md',
    'wiki/papers/Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation.md',
    'wiki/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md',
}

SERVING_TYPE_RULES = {
    'paper': {
        'required_headings': ['## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {},
    },
    'method': {
        'required_headings': ['## 相关概念', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
        'strong_frontmatter_fields': {'parent_methods', 'child_methods'},
    },
    'concept': {
        'required_headings': ['## 相关任务 / 场景', '## 证据来源', '## Formal relations', '### Outgoing', '### Incoming'],
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

SERVING_READY_SAMPLES = {
    'wiki/methods/PathMind.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('PathMind', 'based_on', '路径导向知识图谱推理'),
            ('PathMind', 'improves_on', '路径导向知识图谱推理'),
            ('PathMind', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind', 'targets_task', 'kgqa'),
            ('PathMind', 'targets_task', 'multi-hop-qa'),
            ('PathMind', 'uses_concept', '路径优先化'),
            ('PathMind', 'uses_concept', '重要推理路径'),
            ('PathMind', 'applies_to', '知识图谱推理问答'),
            ('PathMind', 'evaluated_on', 'WebQSP'),
            ('PathMind', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
        ],
    },
    'wiki/methods/RoG.md': {
        'page_type': 'method',
        'expected_frontmatter': {'parent_methods': ['路径导向知识图谱推理'], 'child_methods': []},
        'required_edges': [
            ('RoG', 'based_on', '路径导向知识图谱推理'),
            ('RoG', 'improves_on', '路径导向知识图谱推理'),
            ('RoG', 'targets_task', 'knowledge-graph-reasoning'),
            ('RoG', 'targets_task', 'kgqa'),
            ('RoG', 'targets_task', 'multi-hop-qa'),
        ],
    },
    'wiki/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md': {
        'page_type': 'paper',
        'expected_frontmatter': {},
        'required_edges': [
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'proposes', 'PathMind'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'knowledge-graph-reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'kgqa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'targets_task', 'multi-hop-qa'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '路径优先化'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'uses_concept', '重要推理路径'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'WebQSP'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'evaluated_on', 'CWQ'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'cites', 'KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.sections|PathMind.sections'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.experiments|PathMind.experiments'),
            ('PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models', 'supported_by', 'intermediate/papers/PathMind.refs|PathMind.refs'),
        ],
    },
    'wiki/concepts/路径优先化.md': {'page_type': 'concept', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/tasks/knowledge-graph-reasoning.md': {'page_type': 'task', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/scenarios/知识图谱推理问答.md': {'page_type': 'scenario', 'expected_frontmatter': {}, 'required_edges': []},
    'wiki/benchmarks/WebQSP.md': {'page_type': 'benchmark', 'expected_frontmatter': {}, 'required_edges': []},
    'intermediate/papers/PathMind.sections.md': {'page_type': 'evidence', 'expected_frontmatter': {}, 'required_edges': []},
}

ALLOWED_EVIDENCE_CACHE_TYPES = {'sections', 'refs', 'experiments', 'analysis'}
FORBIDDEN_FULL_REFERENCE_NEEDLES = (
    '.full|',
    '.full]]',
    'cache_type: full',
    '高保真工作底稿',
)
FULL_REFERENCE_SCAN_PATHS = [
    ROOT / 'wiki',
    ROOT / 'intermediate' / 'papers',
    ROOT / '.claude' / 'skills',
    ROOT / 'CLAUDE.md',
]
FULL_REFERENCE_SCAN_SUFFIXES = {
    ROOT / 'wiki': ('.md',),
    ROOT / 'intermediate' / 'papers': ('.md',),
    ROOT / '.claude' / 'skills': ('.md', '.json'),
}

FORMAL_RELATION_RE = re.compile(r"- `\[\[(?P<src>[^\]]+)\]\] --(?P<rel>[^`]+)--> \[\[(?P<dst>[^\]]+)\]\]`")
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
    if rel.startswith('wiki/papers/'):
        return 'paper'
    if rel.startswith('wiki/methods/'):
        return 'method'
    if rel.startswith('wiki/concepts/'):
        return 'concept'
    if rel.startswith('wiki/tasks/'):
        return 'task'
    if rel.startswith('wiki/scenarios/'):
        return 'scenario'
    if rel.startswith('wiki/benchmarks/'):
        return 'benchmark'
    if rel.startswith('intermediate/papers/'):
        return 'evidence'
    return None


def validate_serving_structure(rel: str, text: str, page_type: str) -> list[str]:
    rules = SERVING_TYPE_RULES[page_type]
    page_errors: list[str] = []
    for heading in rules['required_headings']:
        if heading not in text:
            page_errors.append(f'missing serving heading {heading} in {rel}')
    return page_errors


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

for rel, rules in PHASE_ONE_CORE_PAGES.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing phase-one core page: {rel}')
        continue
    text = read_text(rel)
    for needle in rules['links']:
        if needle not in text:
            errors.append(f'missing link {needle} in {rel}')
    for section in rules['sections']:
        if section not in text:
            errors.append(f'missing section {section} in {rel}')

for rel in PHASE_ONE_EVIDENCE_CACHES['method']:
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing evidence cache: {rel}')
        continue
    text = read_text(rel)
    if FORMAL_PAPER not in text:
        errors.append(f'missing formal paper backlink in {rel}')
    if '[[WebQSP]]' not in text and '[[CWQ]]' not in text:
        errors.append(f'missing benchmark backlink in {rel}')
    if '## 对应正式知识节点' not in text:
        errors.append(f'missing node mapping block in {rel}')
    if '本节支撑' not in text:
        errors.append(f'missing evidence intent lines in {rel}')

for rel in PHASE_ONE_EVIDENCE_CACHES['survey']:
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing survey evidence cache: {rel}')
        continue
    text = read_text(rel)
    if SURVEY_PAPER not in text:
        errors.append(f'missing survey paper backlink in {rel}')
    if '## 对应正式知识节点' not in text:
        errors.append(f'missing node mapping block in {rel}')
    if '本节支撑' not in text:
        errors.append(f'missing evidence intent lines in {rel}')

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
    if needle in ['ontology-semantic-review', 'serving-governance-review']:
        if needle not in read_text('.claude/skills/page-projection-sync/SKILL.md'):
            errors.append(f'missing {needle} in page-projection-sync handoff')

if 'page-projection-sync' not in read_text('.claude/skills/relation-reconciliation/SKILL.md'):
    errors.append('missing page-projection-sync in relation-reconciliation handoff')

for rel in PIPELINE_SKILL_FILES:
    if not (ROOT / rel).exists():
        errors.append(f'missing pipeline skill file: {rel}')

graph_standard_text = read_text('wiki/ontology/graph-standard.md')
for needle in GRAPH_STANDARD_NEEDLES:
    if needle not in graph_standard_text:
        errors.append(f'missing {needle} in wiki/ontology/graph-standard.md')

navigation_text = read_text(NAVIGATION_ENTRY_PATH)
for needle in INDEX_NEEDLES:
    if needle not in navigation_text:
        errors.append(f'missing {needle} in {NAVIGATION_ENTRY_PATH}')

for rel, needles in RELATION_LEDGER_NEEDLES.items():
    text = read_text(rel)
    for needle in needles:
        if needle not in text:
            errors.append(f'missing relation edge {needle} in {rel}')

check_evidence_cache_types(errors)
check_forbidden_full_references(errors)

for path in (ROOT / 'wiki').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type is None:
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))

for path in (ROOT / 'intermediate/papers').rglob('*.md'):
    rel = str(path.relative_to(ROOT))
    page_type = classify_serving_page(rel)
    if page_type != 'evidence':
        continue
    text = path.read_text(encoding='utf-8', errors='ignore')
    if '## Formal relations' in text:
        errors.extend(validate_serving_structure(rel, text, page_type))

for rel, rules in SERVING_READY_SAMPLES.items():
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing serving-ready sample page: {rel}')
        continue
    text = read_text(rel)
    errors.extend(validate_serving_structure(rel, text, rules['page_type']))
    errors.extend(validate_sample_projection(rel, rules))

if '## `sourced_from` 实例边' in read_text('wiki/relations/evidence_index.md'):
    errors.append('sourced_from must live in wiki/relations/provenance_links.md, not wiki/relations/evidence_index.md')

for rel in PLACEHOLDER_PAPERS:
    path = ROOT / rel
    if not path.exists():
        errors.append(f'missing placeholder paper: {rel}')
        continue
    text = read_text(rel)
    for needle in ['status: placeholder', '## 当前定位', '## 与知识库现有内容的关系', '## 待补充']:
        if needle not in text:
            errors.append(f'missing {needle} in {rel}')

wiki_pages = []
with_wikilinks = 0
for path in (ROOT / 'wiki').rglob('*.md'):
    wiki_pages.append(path)
    text = path.read_text(encoding='utf-8', errors='ignore')
    if WIKILINK_RE.search(text):
        with_wikilinks += 1
    else:
        errors.append(f'wiki page has no wikilinks: {path.relative_to(ROOT)}')

if errors:
    print('FAIL')
    for error in errors:
        print(f'- {error}')
    sys.exit(1)

print('PASS: graph lint succeeded')
print({'wiki_pages': len(wiki_pages), 'with_wikilinks': with_wikilinks})
