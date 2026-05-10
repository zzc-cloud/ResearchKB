from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path('.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py').resolve()


def git(command: list[str], cwd: Path) -> None:
    subprocess.run(['git', *command], cwd=cwd, check=True, capture_output=True, text=True)


def main() -> int:
    repo_root = Path.cwd().resolve()
    with tempfile.TemporaryDirectory() as tmp:
        sandbox = Path(tmp) / 'repo'
        shutil.copytree(repo_root, sandbox, ignore=shutil.ignore_patterns('.git', '__pycache__', '.DS_Store', '.smart-env'))
        git(['init'], sandbox)
        git(['config', 'user.name', 'Test User'], sandbox)
        git(['config', 'user.email', 'test@example.com'], sandbox)
        git(['add', '.'], sandbox)
        git(['commit', '-m', 'sandbox snapshot'], sandbox)

        result = subprocess.run(
            [sys.executable, str(SCRIPT)],
            cwd=sandbox,
            capture_output=True,
            text=True,
            check=False,
            env={**os.environ, 'RESEARCHKB_RESET_ROOT': str(sandbox)},
        )

        if result.returncode != 0:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError('reset should succeed in sandbox')

        methods_index = (sandbox / 'ontology/entities/methods/index.md').read_text(encoding='utf-8')
        papers_index = (sandbox / 'ontology/entities/papers/index.md').read_text(encoding='utf-8')
        raw_index = (sandbox / 'ontology/entities/raw-sources/index.md').read_text(encoding='utf-8')

        assert '[[ontology/entities/methods/PathMind]]' not in methods_index
        assert '[[ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]' not in papers_index
        assert '[[ontology/entities/raw-sources/files/' in raw_index
        assert '- 无' in (sandbox / 'ontology/relations/references_method.md').read_text(encoding='utf-8')
        assert '2026-04-30 init' not in (sandbox / 'ontology/log.md').read_text(encoding='utf-8')
        assert not (sandbox / 'ontology/entities/methods/PathMind.md').exists()
        assert not (sandbox / 'ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md').exists()
        assert (sandbox / 'ontology/entities/raw-sources/files').exists()
        assert list((sandbox / 'ontology/entities/raw-sources/files').glob('*.pdf'))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
