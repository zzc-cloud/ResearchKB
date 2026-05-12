# ResearchKB Git History Hard-Block Design

- Date: 2026-05-12
- Scope: ResearchKB project-wide workflow rule
- Status: approved design

## Goal

Prevent Claude from using git history, deleted objects, old commits, or old branch content as knowledge-source reference when working in ResearchKB. The current workspace and current normative files are the only default truth sources.

This design exists because deleted ontology objects may have been removed precisely because they were wrong, obsolete, or structurally invalid. Reusing them as implicit templates can reintroduce rejected graph structure.

## Rule

Add a project-wide hard rule to `CLAUDE.md`:

1. In ResearchKB, git history is **not** a default reference source.
2. Claude must **not** use deleted objects, old commits, old branch content, or historical page structures as content reference.
3. Claude must rely on the **current workspace state only**, especially:
   - `CLAUDE.md`
   - `ontology/graph-standard.md`
   - current `ontology/relations/*.md`
   - current object pages, Evidence pages, and managed indexes
   - current raw-source PDFs and current evidence derived from them
4. If historical information may be useful, Claude must stop and ask for explicit user authorization before accessing git history.
5. Authorization is **single-task and single-purpose only**. It does not carry forward to later tasks.

## Allowed Truth Sources

Default allowed sources:

- Files that currently exist in the workspace
- Current project instructions in `CLAUDE.md`
- Current graph rules in `ontology/graph-standard.md`
- Current relation ledgers
- Current ontology object pages and Evidence pages
- Current raw-source PDFs

## Forbidden Default Sources

Without explicit user authorization, Claude must not use:

- `git show`, `git log`, `git diff`, `git grep` against history for content guidance
- Deleted ontology pages
- Historical templates or frontmatter shapes from prior commits
- Prior branch versions of ontology content
- Historical inference of the form “it used to exist, so it should still guide current modeling”

## Exception Mechanism

Allowed only when the user explicitly authorizes a specific task, for example:

- “For this task, you may inspect git history to explain why X was removed.”
- “You may check old commits, but only to trace the deletion reason.”

Even when authorized:

- access must stay within the explicit purpose
- history still does not outrank current normative files
- the permission expires after that task

## Expected Behavior Changes

For requests such as paper ingest, ontology repair, knowledge-base checks, serving governance, or ontology edits:

- Claude should not inspect git history on its own
- Claude should not search deleted objects for modeling examples
- Claude should not cite old page structures as templates
- Claude should ask first if it believes historical context is necessary

## CLAUDE.md Wording Target

The rule should be written as a project-wide execution rule rather than a paper-ingest-only note, so it governs the whole ResearchKB workflow.

Suggested wording intent:

- current workspace over repository history
- no deleted-object reuse
- explicit per-task authorization for history access
- no carry-over authorization

## Implementation Notes

Only `CLAUDE.md` needs to change for this design.

No skill-specific duplication is required in this change because the user chose `CLAUDE.md` as the single authoritative location.
