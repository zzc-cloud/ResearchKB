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


if __name__ == '__main__':
    unittest.main()
