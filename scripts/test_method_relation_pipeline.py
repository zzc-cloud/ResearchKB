from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class MethodRelationPipelineTests(unittest.TestCase):
    def run_lint(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )

    def replace_file(self, rel: str, old: str, new: str) -> None:
        path = ROOT / rel
        text = path.read_text(encoding='utf-8')
        self.assertIn(old, text)
        path.write_text(text.replace(old, new), encoding='utf-8')

    def test_docs_describe_method_only_evaluated_on_and_no_method_placeholder(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        evaluated_on = (ROOT / 'ontology/relations/evaluated_on.md').read_text(encoding='utf-8')
        references_method = (ROOT / 'ontology/relations/references_method.md').read_text(encoding='utf-8')
        methods_index = (ROOT / 'ontology/entities/methods/index.md').read_text(encoding='utf-8')

        self.assertIn('`[[Method]] --evaluated_on--> [[Benchmark]]`', graph_standard)
        self.assertNotIn('`[[Paper|Method]] --evaluated_on--> [[Benchmark]]`', graph_standard)
        self.assertIn('Method 不再使用 `status: placeholder` 作为正式中间状态', graph_standard)
        self.assertIn('方法演化与参照关系', graph_standard)
        self.assertIn('该关系与 `based_on` 一起构成方法图谱的核心邻接关系', references_method)
        self.assertIn('合法 source：`Method`。', evaluated_on)
        self.assertNotIn('合法 source：`Paper`、`Method`。', evaluated_on)
        self.assertIn('`status: processed` 与 `status: partial` 的 Method 均可进入“导航入口”', methods_index)

    def test_lint_rejects_paper_evaluated_on_edges(self):
        evaluated_on_path = ROOT / 'ontology/relations/evaluated_on.md'
        paper_path = ROOT / 'ontology/entities/papers/Synthetic Paper.md'
        original = evaluated_on_path.read_text(encoding='utf-8')
        original_paper_exists = paper_path.exists()
        original_paper = paper_path.read_text(encoding='utf-8') if original_paper_exists else None

        paper_path.write_text(
            """---
title: Synthetic Paper
authors: []
year: unknown
venue: unknown
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Paper

## 当前定位
- 当前作为 [[Synthetic Benchmark]] 的测试论文。

## 与知识库现有内容的关系
- 无。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        evaluated_on_path.write_text(
            original
            + "\n- [[Synthetic Paper]] --evaluated_on--> [[Synthetic Benchmark]]\n"
            + "  - source_path: ontology/entities/papers/Synthetic Paper.md\n"
            + "  - target_path: ontology/entities/benchmarks/Synthetic Benchmark.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: SyntheticEvidence\n"
            + "  - evidence_link: [[SyntheticEvidence]]\n"
            + "  - evidence_path: ontology/entities/evidence/SyntheticEvidence.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            evaluated_on_path.write_text(original, encoding='utf-8')
            if original_paper_exists and original_paper is not None:
                paper_path.write_text(original_paper, encoding='utf-8')
            else:
                paper_path.unlink()

        self.assertIn('Paper may not appear as evaluated_on source: Synthetic Paper', result.stdout + result.stderr)

    def test_lint_rejects_method_placeholder_status(self):
        method_path = ROOT / 'ontology/entities/methods/Synthetic Method.md'
        original_exists = method_path.exists()
        original = method_path.read_text(encoding='utf-8') if original_exists else None

        method_path.write_text(
            """---
title: Synthetic Method
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning]
method_family: [hybrid]
scenario: [enterprise-qa]
research_task: []
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Method

## 当前定位
- 仅用于测试，参照 [[PathMind]]。

## 与知识库现有内容的关系
- 无。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            if original_exists and original is not None:
                method_path.write_text(original, encoding='utf-8')
            else:
                method_path.unlink()

        self.assertIn('Method placeholder status is no longer allowed: ontology/entities/methods/Synthetic Method.md', result.stdout + result.stderr)

    def test_relation_reconciliation_contract_mentions_partial_method_materialization_and_method_only_evaluated_on(self):
        skill = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        reconciliation_samples = (ROOT / '.claude/skills/relation-reconciliation/evals/regression-samples.json').read_text(encoding='utf-8')
        self.assertIn('若缺失 target Method 页但其 Method 身份已稳定，应直接 materialize 为 `status: partial` 的 Method 页', skill)
        self.assertIn('`evaluated_on` 只接收 `Method -> Benchmark`', skill)
        self.assertIn('严格谱系才进 `based_on`', skill)
        self.assertIn('比较 / 借鉴 / 路线参照进 `references_method`', skill)
        self.assertIn('source_paper_path', skill)
        self.assertIn('target_paper_path', skill)
        self.assertIn('must write references_method ledger child fields in canonical order', reconciliation_samples)

    def test_projection_and_index_contracts_cover_dual_method_sections_and_partial_navigation(self):
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
        index_sync = (ROOT / '.claude/skills/index-sync/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('## 方法演化与参照关系', projection)
        self.assertIn('上游演化方法', projection)
        self.assertIn('关键参照方法', projection)
        self.assertIn('serving-necessary attributes', projection)
        self.assertIn('对象页 `Formal relations` 继续以 `source_paper_path` / `target_paper_path` 形式投影为 path metadata', projection)
        self.assertIn('`references_method` 的首批规则：若 ledger 中存在 `source_paper_path` / `target_paper_path`，则对象页 `Formal relations` 继续以 `source_paper_path` / `target_paper_path` 形式投影为 path metadata', projection)
        self.assertIn('若 formal relation 已完成投影，但正文模板区块未覆盖其主语义面，应输出 `manual_followups`', projection)
        self.assertIn('默认生成 `[[../x]]` 而不是 `[[../x|Name]]`', projection)
        self.assertIn('`partial`：Method 页可进入默认导航入口', index_sync)
        self.assertIn('source_paper_path', projection_checklist)
        self.assertIn('target_paper_path', projection_checklist)
        self.assertIn('摘要覆盖', projection_checklist)
        self.assertIn('`placeholder` Paper 只进入 non-serving block，并作为 `Paper Stub / Anchor` 理解', index_sync)

    def test_pathmind_regression_uses_method_only_benchmarks_and_partial_upstream_methods(self):
        pathmind_paper = (ROOT / 'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md').read_text(encoding='utf-8')
        pathmind_method = (ROOT / 'ontology/entities/methods/PathMind.md').read_text(encoding='utf-8')
        evaluated_on = (ROOT / 'ontology/relations/evaluated_on.md').read_text(encoding='utf-8')
        references_method = (ROOT / 'ontology/relations/references_method.md').read_text(encoding='utf-8')
        cites = (ROOT / 'ontology/relations/cites.md').read_text(encoding='utf-8')
        knowpath_paper = (ROOT / 'ontology/entities/papers/KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs.md').read_text(encoding='utf-8')

        self.assertNotIn('`evaluated_on`：WebQSP', pathmind_paper)
        self.assertIn('显式 relational path reasoning 代表工作', pathmind_paper)
        self.assertIn('retrieval-augmented 图检索代表方法', pathmind_paper)
        self.assertIn('evidence-path enhanced 代表工作', pathmind_paper)
        self.assertIn('## 方法演化与参照关系', pathmind_method)
        self.assertIn('关键参照方法', pathmind_method)
        self.assertIn('对应代表论文路径', pathmind_method)
        self.assertIn('  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md', pathmind_method)
        self.assertIn('  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md', pathmind_method)
        self.assertNotIn('  - target_paper: Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs', pathmind_method)
        self.assertIn('[[PathMind]] --references_method--> [[GCR]]', references_method)
        self.assertIn('source_paper_path', references_method)
        self.assertIn('target_paper_path', references_method)
        self.assertIn(
            '  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md',
            references_method,
        )
        self.assertIn(
            '  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md',
            references_method,
        )
        self.assertIn('[[PathMind]] --evaluated_on--> [[WebQSP]]', evaluated_on)
        self.assertNotIn('[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]', evaluated_on)
        for name in ['RoG', 'GCR', 'EPERM', 'ToG']:
            text = (ROOT / 'ontology/entities/methods' / f'{name}.md').read_text(encoding='utf-8')
            self.assertIn('status: partial', text)
            self.assertIn('## Object semantics', text)
            self.assertIn('## Formal relations', text)
        self.assertIn('[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[KnowPath - Knowledge-enhanced Reasoning via LLM-generated Inference Paths over Knowledge Graphs]]', cites)
        self.assertIn('status: placeholder', knowpath_paper)
    def test_lint_accepts_path_metadata_projection_without_extra_paper_neighbors(self):
        result = self.run_lint()
        output = result.stdout + result.stderr
        self.assertEqual(result.returncode, 0, output)
        self.assertNotIn('body wikilink missing from Formal relations in ontology/entities/methods/PathMind.md', output)
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        reconciliation = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
        reconciliation_samples = (ROOT / '.claude/skills/relation-reconciliation/evals/regression-samples.json').read_text(encoding='utf-8')
        projection_samples = (ROOT / '.claude/skills/page-projection-sync/evals/regression-samples.json').read_text(encoding='utf-8')

        self.assertIn('若该页已经承接 formal relation instance，则必须具备 formal projection 合同', graph_standard)
        self.assertIn('RawSource 文件是 provenance target，不进入普通对象页双侧 projection 合同', graph_standard)
        self.assertIn('serving-necessary attributes', graph_standard)
        self.assertIn('target_paper_path → target_paper_path', graph_standard)
        self.assertIn('正文模板化关系区块必须对 `## Formal relations` 做主题化摘要覆盖', graph_standard)
        self.assertIn('source_paper_path', graph_standard)
        self.assertIn('target_paper_path', graph_standard)
        self.assertIn('`affected_pages` must include both source and target object pages for every reconciled formal relation instance whose corresponding page file exists.', reconciliation)
        self.assertIn('只要对象页存在，且它在 current formal ledger 中作为任一 instance edge 的 source 或 target 出现，就必须生成 formal projection。', projection)
        self.assertIn('RawSource targets are exempt from object-page incoming projection', projection_checklist)
        self.assertIn('source_paper_path', projection_checklist)
        self.assertIn('target_paper_path', projection_checklist)
        self.assertIn('`references_method` 若存在 `source_paper_path` / `target_paper_path`，对象页投影必须保留 path metadata，但不得把它们升级为新的 paper 邻接。', projection_checklist)
        self.assertIn('Paper Stub / Anchor pages may bear formal relations without becoming Formal Paper entries', projection_checklist)
        self.assertIn('must preserve placeholder cited papers as Paper Stub / Anchor targets', reconciliation_samples)
        self.assertIn('must reject references_method provenance when the matching cites edge is missing', reconciliation_samples)
        self.assertIn('cited-placeholder-target-sync', projection_samples)
        self.assertIn('must keep placeholder cited-paper targets non-serving paper stubs', projection_samples)
        self.assertIn('rawsource-target-exemption', projection_samples)

    def test_paper_stub_and_method_anchor_contract_is_documented(self):
        graph_standard = (ROOT / 'ontology/graph-standard.md').read_text(encoding='utf-8')
        reconciliation = (ROOT / '.claude/skills/relation-reconciliation/SKILL.md').read_text(encoding='utf-8')
        projection = (ROOT / '.claude/skills/page-projection-sync/SKILL.md').read_text(encoding='utf-8')
        index_sync = (ROOT / '.claude/skills/index-sync/SKILL.md').read_text(encoding='utf-8')
        serving = (ROOT / '.claude/skills/serving-governance-review/SKILL.md').read_text(encoding='utf-8')
        reconciliation_samples = (ROOT / '.claude/skills/relation-reconciliation/evals/regression-samples.json').read_text(encoding='utf-8')
        projection_checklist = (ROOT / '.claude/skills/page-projection-sync/evals/quality-checklist.md').read_text(encoding='utf-8')
        projection_samples = (ROOT / '.claude/skills/page-projection-sync/evals/regression-samples.json').read_text(encoding='utf-8')

        self.assertIn('Formal Paper 与 Paper Stub / Anchor', graph_standard)
        self.assertIn('每个 formal / partial `Method` 都必须至少能回挂到一个 paper anchor', graph_standard)
        self.assertIn('若一条 `references_method` 实例边同时声明 `source_paper_path` 与 `target_paper_path`，则 formal ledger 中必须存在对应 `cites`', graph_standard)
        self.assertIn('placeholder cited paper target 应保留为 Paper Stub / Anchor，而不是自动升级为 Formal Paper', reconciliation)
        self.assertIn('不得把 `source_paper_path` / `target_paper_path` 投影成新的 paper 邻接', projection)
        self.assertIn('`placeholder` Paper 只进入 non-serving block，并作为 `Paper Stub / Anchor` 理解', index_sync)
        self.assertIn('Paper Stub / Anchor 属于可合法遍历但非 default paper serving surface 的 phase-1 中间态', serving.replace('`', ''))
        self.assertIn('must preserve placeholder cited papers as Paper Stub / Anchor targets', reconciliation_samples)
        self.assertIn('must reject references_method provenance when the matching cites edge is missing', reconciliation_samples)
        self.assertIn('must keep placeholder cited-paper targets non-serving paper stubs', projection_samples)
        self.assertIn('Paper Stub / Anchor pages may bear formal relations without becoming Formal Paper entries', projection_checklist)

    def test_lint_rejects_ledger_edge_when_source_page_lacks_formal_relations(self):
        cites_path = ROOT / 'ontology/relations/cites.md'
        source_path = ROOT / 'ontology/entities/papers/Synthetic Source Paper.md'
        target_path = ROOT / 'ontology/entities/papers/Synthetic Target Paper.md'
        original_cites = cites_path.read_text(encoding='utf-8')
        original_source_exists = source_path.exists()
        original_target_exists = target_path.exists()
        original_source = source_path.read_text(encoding='utf-8') if original_source_exists else None
        original_target = target_path.read_text(encoding='utf-8') if original_target_exists else None

        source_path.write_text(
            """---
title: Synthetic Source Paper
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Source Paper

## 当前定位
- 当前作为 [[Synthetic Target Paper]] 的测试 source 页。

## 与知识库现有内容的关系
- 无。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        target_path.write_text(
            """---
title: Synthetic Target Paper
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Target Paper

## 当前定位
- 当前作为 [[Synthetic Source Paper]] 的测试 target 页。

## 与知识库现有内容的关系
- 被引用于：[[Synthetic Source Paper]]。

## 待补充
- 无。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `cites`：Synthetic Source Paper（文档：`ontology/entities/papers/Synthetic Source Paper.md`）：[[Synthetic Source Paper]]
  - edge_semantics: synthetic source coverage check.
  - evidence: [[../evidence/PathMind.refs]]
""",
            encoding='utf-8',
        )

        cites_path.write_text(
            original_cites
            + "\n- [[Synthetic Source Paper]] --cites--> [[Synthetic Target Paper]]\n"
            + "  - source_path: ontology/entities/papers/Synthetic Source Paper.md\n"
            + "  - target_path: ontology/entities/papers/Synthetic Target Paper.md\n"
            + "  - edge_semantics: synthetic source coverage check.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            cites_path.write_text(original_cites, encoding='utf-8')
            if original_source_exists and original_source is not None:
                source_path.write_text(original_source, encoding='utf-8')
            else:
                source_path.unlink()
            if original_target_exists and original_target is not None:
                target_path.write_text(original_target, encoding='utf-8')
            else:
                target_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'missing Formal relations on source page for ledger edge: ontology/entities/papers/Synthetic Source Paper.md --cites--> ontology/entities/papers/Synthetic Target Paper.md',
            combined_output,
        )

    def test_lint_rejects_formal_bearing_placeholder_target_without_formal_relations(self):
        cites_path = ROOT / 'ontology/relations/cites.md'
        target_path = ROOT / 'ontology/entities/papers/Synthetic Placeholder Target.md'
        original_cites = cites_path.read_text(encoding='utf-8')
        original_target_exists = target_path.exists()
        original_target = target_path.read_text(encoding='utf-8') if original_target_exists else None

        target_path.write_text(
            """---
title: Synthetic Placeholder Target
authors: []
year: 2026
venue: synthetic
problem: [reasoning]
industry: [general]
research_role: [foundational]
status: placeholder
---

# Synthetic Placeholder Target

## 当前定位
- 当前作为 [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] 的测试 target 页。

## 与知识库现有内容的关系
- 被引用于：[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]。

## 待补充
- 无。
""",
            encoding='utf-8',
        )

        cites_path.write_text(
            original_cites
            + "\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Synthetic Placeholder Target]]\n"
            + "  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md\n"
            + "  - target_path: ontology/entities/papers/Synthetic Placeholder Target.md\n"
            + "  - edge_semantics: synthetic placeholder coverage check.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            cites_path.write_text(original_cites, encoding='utf-8')
            if original_target_exists and original_target is not None:
                target_path.write_text(original_target, encoding='utf-8')
            else:
                target_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'formal-bearing placeholder page missing formal relations contract: ontology/entities/papers/Synthetic Placeholder Target.md',
            combined_output,
        )
        self.assertIn(
            'missing Formal relations on target page for ledger edge: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md --cites--> ontology/entities/papers/Synthetic Placeholder Target.md',
            combined_output,
        )

    def test_lint_rejects_references_method_without_matching_cites_edge(self):
        references_method_path = ROOT / 'ontology/relations/references_method.md'
        cites_path = ROOT / 'ontology/relations/cites.md'
        original_references = references_method_path.read_text(encoding='utf-8')
        original_cites = cites_path.read_text(encoding='utf-8')

        references_method_path.write_text(
            original_references
            + "\n- [[Synthetic Source Method]] --references_method--> [[Synthetic Target Method]]\n"
            + "  - source_path: ontology/entities/methods/Synthetic Source Method.md\n"
            + "  - target_path: ontology/entities/methods/Synthetic Target Method.md\n"
            + "  - source_paper_path: ontology/entities/papers/Synthetic Source Paper.md\n"
            + "  - target_paper_path: ontology/entities/papers/Synthetic Target Paper.md\n"
            + "  - edge_semantics: synthetic missing cites backing.\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            references_method_path.write_text(original_references, encoding='utf-8')
            cites_path.write_text(original_cites, encoding='utf-8')

        self.assertIn(
            'references_method paper provenance must be backed by cites: ontology/entities/papers/Synthetic Source Paper.md -> ontology/entities/papers/Synthetic Target Paper.md',
            result.stdout + result.stderr,
        )

    def test_lint_rejects_partial_method_without_any_paper_anchor(self):
        method_path = ROOT / 'ontology/entities/methods/Synthetic Anchorless Method.md'
        original_exists = method_path.exists()
        original_text = method_path.read_text(encoding='utf-8') if original_exists else None

        method_path.write_text(
            """---
title: Synthetic Anchorless Method
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning]
method_family: [hybrid]
scenario: []
research_task: [knowledge-graph-reasoning]
industry: [general]
research_role: [foundational]
status: partial
---

# Synthetic Anchorless Method

## Object semantics
- 一个故意缺少 paper anchor 的测试方法。

## 当前定位
- 测试 partial Method 锚点校验。

## 与知识库现有内容的关系
- 无。

## 最小定义/角色
- 无。

## 待补充
- 无。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- 无

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
""",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            if original_exists and original_text is not None:
                method_path.write_text(original_text, encoding='utf-8')
            else:
                method_path.unlink()

        self.assertIn(
            'formal/partial Method must resolve to at least one paper anchor: ontology/entities/methods/Synthetic Anchorless Method.md',
            result.stdout + result.stderr,
        )

    def test_lint_exempts_rawsource_targets_from_incoming_projection_requirement(self):
        sourced_from_path = ROOT / 'ontology/relations/sourced_from.md'
        evidence_path = ROOT / 'ontology/entities/evidence/SyntheticProjection.sections.md'
        raw_path = ROOT / 'ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf'
        original_ledger = sourced_from_path.read_text(encoding='utf-8')
        original_evidence_exists = evidence_path.exists()
        original_evidence = evidence_path.read_text(encoding='utf-8') if original_evidence_exists else None
        original_raw_exists = raw_path.exists()

        evidence_path.write_text(
            """---
title: SyntheticProjection.sections
short_name: SyntheticProjection
source_file: ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf
cache_type: sections
status: processed
year: 2026
venue: synthetic
---

# SyntheticProjection.sections

## Object semantics
- Synthetic projection coverage evidence page.

## 对应正式知识节点
- [[../tasks/knowledge-graph-reasoning]]

## 本节支撑什么
- Synthetic projection coverage fixture.

## 关键摘录 / 关键实验 / 关键引用 / 关键分析
- Synthetic projection coverage fixture.

## 来源说明
- Synthetic projection coverage fixture.

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `sourced_from`：Synthetic Projection Coverage.pdf（文档：`ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf`）：[[../raw-sources/files/Synthetic Projection Coverage.pdf]]
  - edge_semantics: synthetic rawsource exemption fixture.
  - evidence: [[../evidence/SyntheticProjection.sections]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- 无
""",
            encoding='utf-8',
        )

        if not original_raw_exists:
            raw_path.write_bytes(b'%PDF-1.4\n%synthetic\n')

        sourced_from_path.write_text(
            original_ledger
            + "\n- [[SyntheticProjection.sections]] --sourced_from--> [[ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf]]\n"
            + "  - source_path: ontology/entities/evidence/SyntheticProjection.sections.md\n"
            + "  - target_path: ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf\n"
            + "  - edge_semantics: synthetic rawsource exemption fixture.\n"
            + "  - evidence: SyntheticProjection.sections\n"
            + "  - evidence_link: [[SyntheticProjection.sections]]\n"
            + "  - evidence_path: ontology/entities/evidence/SyntheticProjection.sections.md\n",
            encoding='utf-8',
        )

        try:
            result = self.run_lint()
        finally:
            sourced_from_path.write_text(original_ledger, encoding='utf-8')
            if original_evidence_exists and original_evidence is not None:
                evidence_path.write_text(original_evidence, encoding='utf-8')
            else:
                evidence_path.unlink()
            if not original_raw_exists and raw_path.exists():
                raw_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertNotIn(
            'missing Formal relations on target page for ledger edge: ontology/entities/evidence/SyntheticProjection.sections.md --sourced_from--> ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf',
            combined_output,
        )
        self.assertNotIn(
            'missing incoming projection for ledger edge: ontology/entities/evidence/SyntheticProjection.sections.md --sourced_from--> ontology/entities/raw-sources/files/Synthetic Projection Coverage.pdf',
            combined_output,
        )


if __name__ == '__main__':
    unittest.main()
