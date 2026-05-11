from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
import unittest

SCRIPT = Path('.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py').resolve()


def git(command: list[str], cwd: Path) -> None:
    subprocess.run(['git', *command], cwd=cwd, check=True, capture_output=True, text=True)


class ResetToEmptyOntologyBaselineTests(unittest.TestCase):
    def make_sandbox(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temp_dir = tempfile.TemporaryDirectory()
        sandbox = Path(temp_dir.name) / 'repo'
        shutil.copytree(Path.cwd().resolve(), sandbox, ignore=shutil.ignore_patterns('.git', '__pycache__', '.DS_Store', '.smart-env'))
        git(['init'], sandbox)
        git(['config', 'user.name', 'Test User'], sandbox)
        git(['config', 'user.email', 'test@example.com'], sandbox)
        git(['add', '.'], sandbox)
        git(['commit', '-m', 'sandbox snapshot'], sandbox)
        return temp_dir, sandbox

    def run_reset(self, sandbox: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT), *args],
            cwd=sandbox,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, 'RESEARCHKB_RESET_ROOT': str(sandbox)},
        )

    def test_reset_succeeds_with_live_derived_entity_indexes_and_preserves_raw_sources(self):
        temp_dir, sandbox = self.make_sandbox()
        try:
            result = self.run_reset(sandbox)

            if result.returncode != 0:
                print(result.stdout)
                print(result.stderr)
            self.assertEqual(result.returncode, 0)

            methods_index = (sandbox / 'ontology/entities/methods/index.md').read_text(encoding='utf-8')
            papers_index = (sandbox / 'ontology/entities/papers/index.md').read_text(encoding='utf-8')
            raw_index = (sandbox / 'ontology/entities/raw-sources/index.md').read_text(encoding='utf-8')

            self.assertNotIn('[[ontology/entities/methods/PathMind]]', methods_index)
            self.assertNotIn('[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]', papers_index)
            self.assertIn('[[ontology/entities/raw-sources/files/', raw_index)
            self.assertIn('- 无', (sandbox / 'ontology/relations/references_method.md').read_text(encoding='utf-8'))
            self.assertNotIn('2026-04-30 init', (sandbox / 'ontology/log.md').read_text(encoding='utf-8'))
            self.assertFalse((sandbox / 'ontology/entities/methods/PathMind.md').exists())
            self.assertFalse((sandbox / 'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md').exists())
            self.assertTrue((sandbox / 'ontology/entities/raw-sources/files').exists())
            self.assertTrue(list((sandbox / 'ontology/entities/raw-sources/files').glob('*.pdf')))
        finally:
            temp_dir.cleanup()

    def test_reset_tolerates_orphan_entity_dirs_and_missing_optional_managed_blocks(self):
        temp_dir, sandbox = self.make_sandbox()
        try:
            orphan_dir = sandbox / 'ontology/entities/legacy-concepts'
            orphan_dir.mkdir()
            (orphan_dir / 'Old Concept.md').write_text('# old concept\n', encoding='utf-8')

            tasks_index = sandbox / 'ontology/entities/tasks/index.md'
            tasks_text = tasks_index.read_text(encoding='utf-8')
            tasks_text = tasks_text.replace(
                '## 3. 其他实例（不可导航）\n<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->\n<!-- END MANAGED BLOCK:non-serving-placeholders -->\n',
                '',
            )
            tasks_index.write_text(tasks_text, encoding='utf-8')

            result = self.run_reset(sandbox, '--force')
            self.assertTrue((orphan_dir / 'Old Concept.md').exists())

            updated_tasks_index = tasks_index.read_text(encoding='utf-8')
            self.assertIn('<!-- BEGIN MANAGED BLOCK:navigation-entries -->\n<!-- END MANAGED BLOCK:navigation-entries -->', updated_tasks_index)
        finally:
            temp_dir.cleanup()

    def test_check_only_reports_detected_domains_and_ledgers(self):
        temp_dir, sandbox = self.make_sandbox()
        try:
            result = self.run_reset(sandbox, '--check-only')

            if result.returncode != 0:
                print(result.stdout)
                print(result.stderr)
            self.assertEqual(result.returncode, 0)
            self.assertIn('entity_indexes_detected:', result.stdout)
            self.assertIn('- methods', result.stdout)
            self.assertIn('excluded_domains:', result.stdout)
            self.assertIn('- raw-sources', result.stdout)
            self.assertIn('relation_ledgers_detected:', result.stdout)
            self.assertIn('- references_method', result.stdout)
        finally:
            temp_dir.cleanup()


if __name__ == '__main__':
    unittest.main()

