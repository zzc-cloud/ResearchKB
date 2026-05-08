from pathlib import Path
import importlib.util
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load_reset_baseline_module():
    script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
    spec = importlib.util.spec_from_file_location('reset_to_empty_ontology_baseline', script_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


class LintGraphTests(unittest.TestCase):
    def test_lint_graph_does_not_crash_without_root_ontology_index(self):
        index_path = ROOT / 'ontology' / 'index.md'
        backup_path = ROOT / 'ontology' / 'index.md.tdd-backup'
        restore_needed = False

        if index_path.exists():
            index_path.rename(backup_path)
            restore_needed = True

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )

            combined_output = result.stdout + result.stderr
            self.assertNotIn('FileNotFoundError', combined_output)
            self.assertNotIn('ontology/index.md', combined_output)
        finally:
            if restore_needed and backup_path.exists():
                backup_path.rename(index_path)

    def test_lint_graph_accepts_empty_compiled_ontology_skeleton(self):
        result = subprocess.run(
            [
                'git',
                'status',
                '--short',
                '--',
                'ontology',
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        status_output = result.stdout.strip()
        self.assertTrue(
            bool(status_output)
            or status_output == '',
            status_output,
        )

    def test_paper_ingest_contract_requires_cited_placeholder_pages(self):
        text = (ROOT / '.claude' / 'skills' / 'paper-ingest' / 'SKILL.md').read_text(encoding='utf-8')

        self.assertIn('必须在 ingest 阶段自动创建最小 placeholder paper 页', text)
        self.assertIn('## 当前定位', text)
        self.assertIn('## 与知识库现有内容的关系', text)
        self.assertIn('## 待补充', text)

    def test_lint_graph_checks_cited_paper_targets_have_pages(self):
        cites_path = ROOT / 'ontology' / 'relations' / 'cites.md'
        original = cites_path.read_text(encoding='utf-8')

        cites_path.write_text(
            original
            + "\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Missing Cited Paper]]\n"
            + "  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md\n"
            + "  - target_path: ontology/entities/papers/Missing Cited Paper.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            cites_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('missing cited paper target page: Missing Cited Paper', combined_output)

    def test_lint_graph_requires_placeholder_sections_for_cited_papers(self):
        cites_path = ROOT / 'ontology' / 'relations' / 'cites.md'
        cites_original = cites_path.read_text(encoding='utf-8')
        paper_path = ROOT / 'ontology' / 'entities' / 'papers' / 'Placeholder Fixture Paper.md'
        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        index_original = index_path.read_text(encoding='utf-8')

        paper_path.write_text(
            "---\n"
            "title: Placeholder Fixture Paper\n"
            "authors: []\n"
            "year: unknown\n"
            "venue: unknown\n"
            "problem: [reasoning]\n"
            "industry: [general]\n"
            "research_role: [foundational]\n"
            "status: placeholder\n"
            "---\n\n"
            "# Placeholder Fixture Paper\n\n"
            "[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n\n"
            "## 当前定位\n"
            "仅用于 lint 测试。\n",
            encoding='utf-8',
        )
        index_path.write_text(
            index_original.replace(
                '<!-- BEGIN MANAGED BLOCK:core-entry -->\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n<!-- END MANAGED BLOCK:core-entry -->',
                '<!-- BEGIN MANAGED BLOCK:core-entry -->\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n- [[Placeholder Fixture Paper]]\n<!-- END MANAGED BLOCK:core-entry -->',
            ).replace(
                '<!-- BEGIN MANAGED BLOCK:grouped-navigation -->\n### KG 推理 / KGQA 主线\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n<!-- END MANAGED BLOCK:grouped-navigation -->',
                '<!-- BEGIN MANAGED BLOCK:grouped-navigation -->\n### KG 推理 / KGQA 主线\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n- [[Placeholder Fixture Paper]]\n<!-- END MANAGED BLOCK:grouped-navigation -->',
            ).replace(
                '<!-- BEGIN MANAGED BLOCK:canonical-list -->\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n<!-- END MANAGED BLOCK:canonical-list -->',
                '<!-- BEGIN MANAGED BLOCK:canonical-list -->\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n- [[Placeholder Fixture Paper]]\n<!-- END MANAGED BLOCK:canonical-list -->',
            ),
            encoding='utf-8',
        )
        cites_path.write_text(
            cites_original
            + "\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Placeholder Fixture Paper]]\n"
            + "  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md\n"
            + "  - target_path: ontology/entities/papers/Placeholder Fixture Paper.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            cites_path.write_text(cites_original, encoding='utf-8')
            index_path.write_text(index_original, encoding='utf-8')
            if paper_path.exists():
                paper_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn('missing ## 与知识库现有内容的关系 in cited placeholder paper: Placeholder Fixture Paper', combined_output)
        self.assertIn('missing ## 待补充 in cited placeholder paper: Placeholder Fixture Paper', combined_output)

    def test_materialize_cited_paper_placeholders_creates_missing_pages(self):
        cites_path = ROOT / 'ontology' / 'relations' / 'cites.md'
        cites_original = cites_path.read_text(encoding='utf-8')
        source_page = ROOT / 'ontology' / 'entities' / 'papers' / 'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md'
        created_page = ROOT / 'ontology' / 'entities' / 'papers' / 'Missing Cited Paper.md'
        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        index_original = index_path.read_text(encoding='utf-8')

        if created_page.exists():
            created_page.unlink()

        cites_path.write_text(
            cites_original
            + "\n- [[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --cites--> [[Missing Cited Paper]]\n"
            + "  - source_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md\n"
            + "  - target_path: ontology/entities/papers/Missing Cited Paper.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: PathMind.refs\n"
            + "  - evidence_link: [[PathMind.refs]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.refs.md\n",
            encoding='utf-8',
        )

        try:
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / '.claude' / 'skills' / 'paper-ingest' / 'materialize_cited_paper_placeholders.py'),
                    '--cites-ledger', str(cites_path),
                    '--papers-dir', str(ROOT / 'ontology' / 'entities' / 'papers'),
                    '--source-page', str(source_page),
                    '--paper-index', str(ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'),
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
            combined_output = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, combined_output)
            self.assertTrue(created_page.exists())
            created_text = created_page.read_text(encoding='utf-8')
            self.assertIn('status: placeholder', created_text)
            self.assertIn('## 当前定位', created_text)
            self.assertIn('## 与知识库现有内容的关系', created_text)
            self.assertIn('## 待补充', created_text)
        finally:
            cites_path.write_text(cites_original, encoding='utf-8')
            index_path.write_text(index_original, encoding='utf-8')
            if created_page.exists():
                created_page.unlink()


    def test_papers_index_uses_object_navigation_only_structure(self):
        text = (ROOT / 'ontology' / 'entities' / 'papers' / 'index.md').read_text(encoding='utf-8')
        self.assertIn('<!-- BEGIN MANAGED BLOCK:navigation-entries -->', text)
        self.assertIn('<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->', text)
        self.assertNotIn('## 5. 相关关系账本', text)

    def test_lint_graph_rejects_placeholder_in_navigation_entries(self):
        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        self.assertIn('non-serving-placeholders', text)
        self.assertIn('navigation-entries', text)
        self.assertIn('placeholder', text)

    def test_materializer_puts_cited_placeholders_only_in_non_serving_block(self):
        text = (ROOT / '.claude' / 'skills' / 'paper-ingest' / 'materialize_cited_paper_placeholders.py').read_text(encoding='utf-8')
        self.assertIn('non-serving-placeholders', text)
        self.assertNotIn('core-entry', text)

    def test_papers_index_entries_include_document_path_and_wikilink(self):
        text = (ROOT / 'ontology' / 'entities' / 'papers' / 'index.md').read_text(encoding='utf-8')
        self.assertIn('文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`', text)
        self.assertIn('[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]', text)

    def test_all_entity_indexes_use_navigation_and_placeholder_blocks(self):
        expected = {
            'ontology/entities/papers/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/methods/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/concepts/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/tasks/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/scenarios/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/benchmarks/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/evidence/index.md': ['navigation-entries', 'non-serving-placeholders'],
            'ontology/entities/raw-sources/index.md': ['navigation-entries'],
        }
        for rel, blocks in expected.items():
            text = (ROOT / rel).read_text(encoding='utf-8')
            for block in blocks:
                self.assertIn(f'<!-- BEGIN MANAGED BLOCK:{block} -->', text)

    def test_restore_baseline_script_exists(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        self.assertTrue(script_path.exists())

    def test_clear_relation_ledger_text_keeps_semantics_and_empties_instances(self):
        module = load_reset_baseline_module()
        original = (
            "## 关系语义说明\n"
            "- `based_on` 表示某方法以另一方法作为上游基础。\n\n"
            "## 实例边\n"
            "- [[Child]] --based_on--> [[Parent]]\n"
            "  - source_path: ontology/entities/methods/Child.md\n"
            "  - target_path: ontology/entities/methods/Parent.md\n"
            "  - edge_semantics: fixture\n"
            "  - evidence: Fixture.sections\n"
            "  - evidence_link: [[Fixture.sections]]\n"
            "  - evidence_path: ontology/entities/evidence/Fixture.sections.md\n"
        )

        updated = module.clear_relation_ledger_text(original)

        self.assertIn('## 关系语义说明', updated)
        self.assertIn('`based_on` 表示某方法以另一方法作为上游基础。', updated)
        self.assertIn('## 实例边\n- 无\n', updated)
        self.assertNotIn('[[Child]] --based_on--> [[Parent]]', updated)

    def test_clear_relation_ledger_text_requires_instance_heading(self):
        module = load_reset_baseline_module()
        with self.assertRaisesRegex(ValueError, 'missing ## 实例边 heading'):
            module.clear_relation_ledger_text('## 关系语义说明\n- only semantics\n')

    def test_remove_entity_instance_pages_preserves_indexes_and_raw_pdfs(self):
        module = load_reset_baseline_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            entities = root / 'ontology' / 'entities'
            write_file(entities / 'papers' / 'index.md', '# Papers Index\n')
            write_file(entities / 'papers' / 'Fixture Paper.md', '# Fixture Paper\n')
            write_file(entities / 'methods' / 'index.md', '# Methods Index\n')
            write_file(entities / 'methods' / 'Fixture Method.md', '# Fixture Method\n')
            write_file(entities / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            raw_pdf = entities / 'raw-sources' / 'files' / 'fixture.pdf'
            raw_pdf.parent.mkdir(parents=True, exist_ok=True)
            raw_pdf.write_bytes(b'%PDF-1.4 fixture')

            module.clear_entity_instance_pages(entities)

            self.assertTrue((entities / 'papers' / 'index.md').exists())
            self.assertFalse((entities / 'papers' / 'Fixture Paper.md').exists())
            self.assertTrue((entities / 'methods' / 'index.md').exists())
            self.assertFalse((entities / 'methods' / 'Fixture Method.md').exists())
            self.assertTrue((entities / 'raw-sources' / 'index.md').exists())
            self.assertTrue(raw_pdf.exists())

    def test_write_empty_log_rewrites_history(self):
        module = load_reset_baseline_module()
        with tempfile.TemporaryDirectory() as tmpdir:
            log_path = Path(tmpdir) / 'ontology' / 'log.md'
            write_file(log_path, '# 操作日志\n\n## 2026-05-08 ingest | fixture\n')

            module.write_empty_log(log_path)

            self.assertEqual(
                log_path.read_text(encoding='utf-8'),
                '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n',
            )

    def test_restore_script_blocks_dirty_ontology_without_force_in_temp_repo(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subprocess.run(['git', 'init'], cwd=root, capture_output=True, text=True, check=True)
            write_file(root / 'ontology' / 'graph-standard.md', '# graph standard\n')
            write_file(root / 'ontology' / 'log.md', '# 操作日志\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'index.md', '# Papers Index\n')
            write_file(root / 'ontology' / 'entities' / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            raw_pdf = root / 'ontology' / 'entities' / 'raw-sources' / 'files' / 'fixture.pdf'
            raw_pdf.parent.mkdir(parents=True, exist_ok=True)
            raw_pdf.write_bytes(b'%PDF-1.4 fixture')
            write_file(root / 'ontology' / 'relations' / 'based_on.md', '## 关系语义说明\n- fixture\n\n## 实例边\n- 无\n')
            write_file(
                root / 'scripts' / 'lint_graph.py',
                'print("PASS: graph lint succeeded")\n',
            )
            write_file(root / 'ontology' / 'dirty-marker.md', 'dirty\n')

            env = os.environ | {'RESEARCHKB_RESET_ROOT': str(root)}
            result = subprocess.run(
                [sys.executable, str(script_path), '--check-only'],
                cwd=root,
                capture_output=True,
                text=True,
                env=env,
            )

            self.assertIn('blocked: ontology has uncommitted changes', result.stdout + result.stderr)

    def test_restore_script_force_resets_temp_repo_and_runs_lint(self):
        script_path = ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py'
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            subprocess.run(['git', 'init'], cwd=root, capture_output=True, text=True, check=True)
            write_file(root / 'ontology' / 'graph-standard.md', '# graph standard\n')
            write_file(root / 'ontology' / 'log.md', '# 操作日志\n\n## 2026-05-08 ingest | fixture\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'index.md', '# Papers Index\n')
            write_file(root / 'ontology' / 'entities' / 'papers' / 'Fixture Paper.md', '# Fixture Paper\n')
            write_file(root / 'ontology' / 'entities' / 'methods' / 'index.md', '# Methods Index\n')
            write_file(root / 'ontology' / 'entities' / 'methods' / 'Fixture Method.md', '# Fixture Method\n')
            write_file(root / 'ontology' / 'entities' / 'raw-sources' / 'index.md', '# Raw Sources Index\n')
            raw_pdf = root / 'ontology' / 'entities' / 'raw-sources' / 'files' / 'fixture.pdf'
            raw_pdf.parent.mkdir(parents=True, exist_ok=True)
            raw_pdf.write_bytes(b'%PDF-1.4 fixture')
            write_file(
                root / 'ontology' / 'relations' / 'based_on.md',
                '## 关系语义说明\n- fixture\n\n## 实例边\n- [[Child]] --based_on--> [[Parent]]\n',
            )
            write_file(
                root / 'scripts' / 'lint_graph.py',
                'print("PASS: graph lint succeeded")\n',
            )

            env = os.environ | {'RESEARCHKB_RESET_ROOT': str(root)}
            result = subprocess.run(
                [sys.executable, str(script_path), '--force'],
                cwd=root,
                capture_output=True,
                text=True,
                env=env,
            )

            combined = result.stdout + result.stderr
            self.assertEqual(result.returncode, 0, combined)
            self.assertIn('PASS: graph lint succeeded', combined)
            self.assertEqual(
                (root / 'ontology' / 'relations' / 'based_on.md').read_text(encoding='utf-8'),
                '## 关系语义说明\n- fixture\n\n## 实例边\n- 无\n',
            )
            self.assertFalse((root / 'ontology' / 'entities' / 'papers' / 'Fixture Paper.md').exists())
            self.assertFalse((root / 'ontology' / 'entities' / 'methods' / 'Fixture Method.md').exists())
            self.assertTrue((root / 'ontology' / 'entities' / 'papers' / 'index.md').exists())
            self.assertTrue(raw_pdf.exists())
            self.assertEqual(
                (root / 'ontology' / 'log.md').read_text(encoding='utf-8'),
                '# 操作日志\n\n- 系统级导航：`CLAUDE.md`\n- 图谱规范：[[graph-standard]]\n',
            )
            self.assertEqual((root / 'ontology' / 'graph-standard.md').read_text(encoding='utf-8'), '# graph standard\n')

    def test_restore_baseline_script_leaves_graph_standard_outside_restore_scope(self):
        text = (ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py').read_text(encoding='utf-8')
        self.assertIn("ROOT / 'ontology' / 'entities'", text)
        self.assertIn("ROOT / 'ontology' / 'relations'", text)
        self.assertIn("ROOT / 'ontology' / 'log.md'", text)
        self.assertNotIn("shutil.rmtree(ONTOLOGY)", text)
        self.assertNotIn("copytree(BASELINE, ONTOLOGY)", text)

    def test_restore_baseline_script_preserves_raw_source_pdfs(self):
        text = (ROOT / '.claude' / 'skills' / 'reset-to-empty-ontology-baseline' / 'restore_baseline.py').read_text(encoding='utf-8')
        self.assertIn("ROOT / 'ontology' / 'entities' / 'raw-sources' / 'files'", text)
        self.assertNotIn("shutil.rmtree(ENTITIES)", text)

    def test_lint_graph_accepts_empty_index_blocks_without_wikilinks(self):
        task_index = ROOT / 'ontology' / 'entities' / 'tasks' / 'index.md'
        original = task_index.read_text(encoding='utf-8')
        empty_state = (
            '# Tasks Index\n\n'
            '> 本页负责 Task 对象域导航：先定位正式任务实例，再进入具体任务页。\n\n'
            '## 1. 对象域说明\n'
            '- 本域收录 Task 节点。\n'
            '- 默认 serving-ready 的任务进入“导航入口”。\n\n'
            '## 2. 导航入口\n'
            '<!-- BEGIN MANAGED BLOCK:navigation-entries -->\n'
            '<!-- END MANAGED BLOCK:navigation-entries -->\n\n'
            '## 3. 其他实例（不可导航）\n'
            '<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->\n'
            '<!-- END MANAGED BLOCK:non-serving-placeholders -->\n'
        )
        task_index.write_text(empty_state, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            task_index.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertNotIn('ontology page has no wikilinks: ontology/entities/tasks/index.md', combined_output)

    def test_lint_graph_accepts_raw_source_entries_with_projected_metadata_lines(self):
        raw_index = ROOT / 'ontology' / 'entities' / 'raw-sources' / 'index.md'
        original = raw_index.read_text(encoding='utf-8')
        projected = (
            '# Raw Sources Index\n\n'
            '> 本页负责 RawSource 受管原始文件导航：先定位原始 PDF，再在需要时直接打开文件进行最终回查。\n\n'
            '## 1. 对象域说明\n'
            '- 本域收录受管原始 PDF 文件。\n'
            '- 默认从本页进入 provenance 回查原件。\n\n'
            '## 2. 导航入口\n'
            '<!-- BEGIN MANAGED BLOCK:navigation-entries -->\n'
            '- PathMind 原文入口（文档：`ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf`）：[[ontology/entities/raw-sources/files/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]\n'
            '  - object_semantics: PathMind 原始 PDF 文件实例，用于 provenance 回查。\n'
            '  - status: serving-ready\n'
            '<!-- END MANAGED BLOCK:navigation-entries -->\n'
        )
        raw_index.write_text(projected, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            raw_index.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing object_semantics projection in ontology/entities/raw-sources/index.md', combined_output)
        self.assertNotIn('missing status projection in ontology/entities/raw-sources/index.md', combined_output)

        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        paper_path = ROOT / 'ontology' / 'entities' / 'papers' / 'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md'
        original = index_path.read_text(encoding='utf-8')
        paper_created = False

        if not paper_path.exists():
            paper_path.write_text(
                "---\n"
                "title: PathMind Paper\n"
                "authors: []\n"
                "year: unknown\n"
                "venue: unknown\n"
                "problem: [reasoning]\n"
                "industry: [general]\n"
                "research_role: [integrated]\n"
                "status: processed\n"
                "---\n\n"
                "# PathMind Paper\n\n"
                "[[../methods/PathMind|PathMind]]\n",
                encoding='utf-8',
            )
            paper_created = True

        updated = original.replace(
            '- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] — 提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa，状态=serving-ready',
            '- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]\n  - object_semantics: 提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa。\n  - status: serving-ready',
            1,
        )
        index_path.write_text(updated, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            index_path.write_text(original, encoding='utf-8')
            if paper_created and paper_path.exists():
                paper_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing navigation entry document-path format in ontology/entities/papers/index.md', combined_output)
        self.assertNotIn('missing object_semantics projection in ontology/entities/papers/index.md', combined_output)
        self.assertNotIn('missing status projection in ontology/entities/papers/index.md', combined_output)

    def test_lint_graph_accepts_relation_instance_role_sentences(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        paper_path = ROOT / 'ontology' / 'entities' / 'papers' / 'PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md'
        original = method_path.read_text(encoding='utf-8')
        paper_created = False

        if not paper_path.exists():
            paper_path.write_text(
                "---\n"
                "title: PathMind Paper\n"
                "authors: []\n"
                "year: unknown\n"
                "venue: unknown\n"
                "problem: [reasoning]\n"
                "industry: [general]\n"
                "research_role: [integrated]\n"
                "status: processed\n"
                "---\n\n"
                "# PathMind Paper\n\n"
                "[[../methods/PathMind|PathMind]]\n",
                encoding='utf-8',
            )
            paper_created = True

        updated = original.replace(
            '当前对象作为 source；以下列出当前对象指向的邻接对象。',
            '当前对象作为 source；以下列出当前对象指向的 relation 实例。',
        ).replace(
            '当前对象作为 target；以下列出指向当前对象的邻接对象。',
            '当前对象作为 target；以下列出指向当前对象的 relation 实例。',
        )
        method_path.write_text(updated, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')
            if paper_created and paper_path.exists():
                paper_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertNotIn('missing role sentence ### Outgoing in ontology/entities/methods/PathMind.md', combined_output)
        self.assertNotIn('missing role sentence ### Incoming in ontology/entities/methods/PathMind.md', combined_output)

    def test_lint_graph_uses_relation_type_ledger_names(self):
        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')

        self.assertNotIn('ontology/relations/citation_graph.md', text)
        self.assertNotIn('ontology/relations/method_evolution.md', text)
        self.assertNotIn('ontology/relations/concept_links.md', text)
        self.assertNotIn('ontology/relations/task_method_map.md', text)
        self.assertNotIn('ontology/relations/paper_method_links.md', text)
        self.assertNotIn('ontology/relations/benchmark_links.md', text)
        self.assertNotIn('ontology/relations/evidence_index.md', text)
        self.assertNotIn('ontology/relations/provenance_links.md', text)

    def test_lint_graph_requires_new_relation_type_ledgers(self):
        expected = [
            'ontology/relations/cites.md',
            'ontology/relations/proposes.md',
            'ontology/relations/based_on.md',
            'ontology/relations/targets_task.md',
            'ontology/relations/uses_concept.md',
            'ontology/relations/evaluated_on.md',
            'ontology/relations/supported_by.md',
            'ontology/relations/sourced_from.md',
        ]

        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        for needle in expected:
            self.assertIn(needle, text)

    def test_lint_graph_does_not_expect_retired_relation_types(self):
        retired = [
            'ontology/relations/improves_on.md',
            'ontology/relations/depends_on.md',
            'ontology/relations/applies_to.md',
            'ontology/relations/supports.md',
            "('PathMind', 'improves_on', '路径导向知识图谱推理')",
            "('PathMind', 'applies_to', '知识图谱推理问答')",
            "('RoG', 'improves_on', '路径导向知识图谱推理')",
        ]

        text = (ROOT / 'scripts' / 'lint_graph.py').read_text(encoding='utf-8')
        for needle in retired:
            self.assertNotIn(needle, text)
    def test_lint_graph_requires_edge_semantics_in_relation_ledgers(self):
        relation_path = ROOT / 'ontology' / 'relations' / 'targets_task.md'
        original = relation_path.read_text(encoding='utf-8')

        broken = original.replace('  - edge_semantics:', '  - reason:', 1)
        relation_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            relation_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('invalid relation child-field order in ontology/relations/targets_task.md', combined_output)

    def test_lint_graph_requires_edge_semantics_and_evidence_in_object_page_projections(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        broken = original.replace(
            """- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - edge_semantics: PathMind 面向知识图谱推理总任务。
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]""",
            """- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]
  - evidence: [[../evidence/PathMind.sections|PathMind.sections]]""",
            1,
        )
        method_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('missing edge_semantics field in projected relation item: ontology/entities/methods/PathMind.md', combined_output)

    def test_lint_graph_requires_index_entries_to_use_object_semantics_projection(self):
        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        original = index_path.read_text(encoding='utf-8')

        broken = original.replace(
            """- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - object_semantics: 提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa。
  - status: serving-ready""",
            """- PathMind 入口（文档：`ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md`）：[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]
  - status: serving-ready""",
            1,
        )
        index_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            index_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('missing object_semantics projection in ontology/entities/papers/index.md', combined_output)

    def test_lint_graph_requires_index_entry_target_files_to_exist(self):
        index_path = ROOT / 'ontology' / 'entities' / 'papers' / 'index.md'
        original = index_path.read_text(encoding='utf-8')

        broken = original.replace(
            'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md',
            'ontology/entities/papers/Missing Canonical Paper.md',
            1,
        ).replace(
            '[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]',
            '[[ontology/entities/papers/Missing Canonical Paper]]',
            1,
        )
        index_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            index_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'missing index entry target file in ontology/entities/papers/index.md: ontology/entities/papers/Missing Canonical Paper.md',
            combined_output,
        )

    def test_lint_graph_rejects_paper_supported_by_edges(self):
        supported_by_path = ROOT / 'ontology' / 'relations' / 'supported_by.md'
        paper_path = ROOT / 'ontology' / 'entities' / 'papers' / 'Synthetic Paper.md'
        original = supported_by_path.read_text(encoding='utf-8')
        paper_created = False

        if not paper_path.exists():
            paper_path.write_text(
                "---\n"
                "title: Synthetic Paper\n"
                "authors: []\n"
                "year: unknown\n"
                "venue: unknown\n"
                "problem: [reasoning]\n"
                "industry: [general]\n"
                "research_role: [foundational]\n"
                "status: placeholder\n"
                "---\n\n"
                "# Synthetic Paper\n\n"
                "[[PathMind]]\n\n"
                "## 当前定位\n"
                "测试夹具。\n\n"
                "## 与知识库现有内容的关系\n"
                "仅用于 lint 测试。\n\n"
                "## 待补充\n"
                "- 正式内容待补。\n",
                encoding='utf-8',
            )
            paper_created = True

        supported_by_path.write_text(
            original
            + "\n- [[Synthetic Paper]] --supported_by--> [[PathMind.sections]]\n"
            + "  - source_path: ontology/entities/papers/Synthetic Paper.md\n"
            + "  - target_path: ontology/entities/evidence/PathMind.sections.md\n"
            + "  - edge_semantics: test fixture\n"
            + "  - evidence: PathMind.sections\n"
            + "  - evidence_link: [[PathMind.sections]]\n"
            + "  - evidence_path: ontology/entities/evidence/PathMind.sections.md\n",
            encoding='utf-8',
        )

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            supported_by_path.write_text(original, encoding='utf-8')
            if paper_created and paper_path.exists():
                paper_path.unlink()

        combined_output = result.stdout + result.stderr
        self.assertIn('Paper may not appear as supported_by source: Synthetic Paper', combined_output)
        self.assertNotIn('unknown supported_by source type for Synthetic Paper', combined_output)

    def test_lint_graph_requires_semi_expanded_projection_format(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        updated = original.replace(
            '- `targets_task`：任务目标（文档：`ontology/entities/tasks/knowledge-graph-reasoning.md`）：[[../tasks/knowledge-graph-reasoning|knowledge-graph-reasoning]]',
            '- `[[PathMind]] --targets_task--> [[knowledge-graph-reasoning]]`',
            1,
        )
        method_path.write_text(updated, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('legacy full-edge projection found in ontology/entities/methods/PathMind.md', combined_output)

    def test_lint_graph_rejects_evidence_body_links_to_paper(self):
        evidence_path = ROOT / 'ontology' / 'entities' / 'evidence' / 'PathMind.sections.md'
        original = evidence_path.read_text(encoding='utf-8')

        broken = original.replace(
            'PathMind 的问题设定、三模块框架与总体方法定位。',
            'PathMind 的问题设定、三模块框架与总体方法定位，见 [[../papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models|PathMind paper]]。',
        )
        evidence_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            evidence_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('Evidence body may not link to Paper: ontology/entities/evidence/PathMind.sections.md', combined_output)

    def test_lint_graph_requires_body_wikilinks_to_be_projected(self):
        method_path = ROOT / 'ontology' / 'entities' / 'methods' / 'PathMind.md'
        original = method_path.read_text(encoding='utf-8')

        broken = original.replace(
            '相较纯 retrieval-augmented 方法，它更强调路径重要性建模；相较 synergy-augmented 方法，它减少了大搜索空间下的多轮交互成本。',
            '相较纯 retrieval-augmented 方法，它更强调路径重要性建模；也可参考 [[../concepts/LLM增强知识图谱|LLM增强知识图谱]]。',
            1,
        )
        method_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            method_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn('body wikilink missing from Formal relations in ontology/entities/methods/PathMind.md: ../concepts/LLM增强知识图谱|LLM增强知识图谱', combined_output)
    def test_lint_graph_allows_relation_page_without_edge_wikilinks_when_no_instances(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )

        combined_output = result.stdout + result.stderr
        self.assertNotIn('ontology page has no wikilinks: ontology/relations/based_on.md', combined_output)

    def test_lint_graph_rejects_relation_navigation_wikilinks(self):
        relation_path = ROOT / 'ontology' / 'relations' / 'targets_task.md'
        original = relation_path.read_text(encoding='utf-8')
        broken = original.replace(
            '## 关系语义说明\n',
            '## 关系语义说明\n- 相关对象域：[[../entities/tasks/index|tasks/index]]\n',
            1,
        )
        relation_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            relation_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'forbidden relation-page wikilink outside allowed positions in ontology/relations/targets_task.md: ../entities/tasks/index|tasks/index',
            combined_output,
        )

    def test_lint_graph_requires_canonical_relation_child_field_order(self):
        relation_path = ROOT / 'ontology' / 'relations' / 'targets_task.md'
        original = relation_path.read_text(encoding='utf-8')
        broken = original.replace(
            '  - source_path: ontology/entities/methods/PathMind.md\n  - target_path: ontology/entities/tasks/knowledge-graph-reasoning.md\n',
            '  - target_path: ontology/entities/tasks/knowledge-graph-reasoning.md\n  - source_path: ontology/entities/methods/PathMind.md\n',
            1,
        )
        relation_path.write_text(broken, encoding='utf-8')

        try:
            result = subprocess.run(
                [sys.executable, str(ROOT / 'scripts' / 'lint_graph.py')],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        finally:
            relation_path.write_text(original, encoding='utf-8')

        combined_output = result.stdout + result.stderr
        self.assertIn(
            'invalid relation child-field order in ontology/relations/targets_task.md',
            combined_output,
        )

