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

    def test_paper_ingest_contract_mentions_references_method_and_method_only_evaluated_on(self):
        skill = (ROOT / '.claude/skills/paper-ingest/SKILL.md').read_text(encoding='utf-8')
        self.assertIn('`references_method` 使用规则：', skill)
        self.assertIn('若仅存在论文级引用事实而缺少稳定方法对象语义，不得从 `cites` 升格为 `references_method`。', skill)
        self.assertNotIn('必须登记 `[[Paper]] --evaluated_on--> [[Benchmark]]`', skill)
        self.assertIn('只要存在明确 benchmark，应登记 `[[Method]] --evaluated_on--> [[Benchmark]]`', skill)


if __name__ == '__main__':
    unittest.main()
