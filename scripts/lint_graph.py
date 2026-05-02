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
        'sections': ['## 与其他概念的关系', '## 关系索引与证据'],
    },
    'wiki/concepts/重要推理路径.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[knowledge-graph-reasoning]]',
            '[[concept_links]]',
            '[[intermediate/papers/PathMind.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 关系索引与证据'],
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
        'sections': ['## 关联任务', '## 证据来源'],
    },
    'wiki/tasks/knowledge-graph-reasoning.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 关系索引'],
    },
    'wiki/tasks/kgqa.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 关系索引'],
    },
    'wiki/tasks/multi-hop-qa.md': {
        'links': [
            '[[PathMind]]',
            '[[知识图谱推理问答]]',
            '[[task_method_map]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法', '## 关系索引'],
    },
    'wiki/benchmarks/WebQSP.md': {
        'links': [
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[PathMind]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关任务', '## 证据索引'],
    },
    'wiki/benchmarks/CWQ.md': {
        'links': [
            '[[kgqa]]',
            '[[multi-hop-qa]]',
            '[[PathMind]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关任务', '## 证据索引'],
    },
    'wiki/papers/A survey of large language model-augmented knowledge graphs for advanced complex product design.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[LLM增强知识图谱]]',
            '[[engineering-design-knowledge-management]]',
            '[[复杂产品设计]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.analysis',
        ],
        'sections': ['## 核心方法 / 框架', '## 实验证据 / 综述证据'],
    },
    'wiki/scenarios/复杂产品设计.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[LLM增强知识图谱]]',
            '[[engineering-design-knowledge-management]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.analysis',
        ],
        'sections': ['## 使用的主要方法 / 框架', '## 证据来源'],
    },
    'wiki/concepts/LLM增强知识图谱.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[复杂产品设计]]',
            '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.sections',
        ],
        'sections': ['## 与其他概念的关系', '## 关系索引与证据'],
    },
    'wiki/concepts/复杂产品设计中的LLM-KG协同框架.md': {
        'links': [
            '[[LLM增强知识图谱]]',
            '[[复杂产品设计]]',
            '[[engineering-design-knowledge-management]]',
            '[[A survey of large language model-augmented knowledge graphs for advanced complex product design]]',
            '[[intermediate/papers/LLM-KG-CPD-Survey.full',
        ],
        'sections': ['## 与其他概念的关系', '## 证据来源'],
    },
    'wiki/tasks/engineering-design-knowledge-management.md': {
        'links': [
            '[[复杂产品设计中的LLM-KG协同框架]]',
            '[[复杂产品设计]]',
            '[[evidence_index]]',
        ],
        'sections': ['## 相关方法 / 框架', '## 关系索引'],
    },
}

PHASE_ONE_EVIDENCE_CACHES = {
    'method': [
        'intermediate/papers/PathMind.sections.md',
        'intermediate/papers/PathMind.refs.md',
        'intermediate/papers/PathMind.experiments.md',
        'intermediate/papers/PathMind.full.md',
    ],
    'survey': [
        'intermediate/papers/LLM-KG-CPD-Survey.sections.md',
        'intermediate/papers/LLM-KG-CPD-Survey.refs.md',
        'intermediate/papers/LLM-KG-CPD-Survey.analysis.md',
        'intermediate/papers/LLM-KG-CPD-Survey.full.md',
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
GRAPH_STANDARD_NEEDLES = [
    'analysis.md',
    'experiments.md',
    'paper_method_links.md',
    'benchmark_links.md',
    'provenance_links.md',
    '`wiki/relations/paper_method_links.md`：维护 `proposes`',
    '`wiki/relations/benchmark_links.md`：维护 `evaluated_on`',
    '`wiki/relations/evidence_index.md`：维护 `supported_by`',
    '`wiki/relations/provenance_links.md`：维护 `sourced_from`',
]
INDEX_NEEDLES = [
    '[[paper_method_links]]',
    '[[benchmark_links]]',
    '[[provenance_links]]',
]
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


def read_text(rel: str) -> str:
    return (ROOT / rel).read_text(encoding='utf-8', errors='ignore')


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

graph_standard_text = read_text('wiki/ontology/graph-standard.md')
for needle in GRAPH_STANDARD_NEEDLES:
    if needle not in graph_standard_text:
        errors.append(f'missing {needle} in wiki/ontology/graph-standard.md')

index_text = read_text('wiki/index.md')
for needle in INDEX_NEEDLES:
    if needle not in index_text:
        errors.append(f'missing {needle} in wiki/index.md')

for rel, needles in RELATION_LEDGER_NEEDLES.items():
    text = read_text(rel)
    for needle in needles:
        if needle not in text:
            errors.append(f'missing relation edge {needle} in {rel}')

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
