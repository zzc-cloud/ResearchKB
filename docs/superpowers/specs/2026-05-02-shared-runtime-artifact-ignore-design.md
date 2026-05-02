# Shared runtime artifact ignore design

## Goal
Add a repository-shared ignore strategy for local runtime artifacts so they stop polluting `git status`, while preserving local files on disk and avoiding broad ignore rules that could hide intentionally versioned project content.

## Why this change
The repository currently shows recurring local-only artifacts in `git status`:
- `.claude/worktrees/`
- `.smart-env/multi/`
- `.obsidian/workspace.json`
- `.smart-env/event_logs/event_logs.ajson`

Two of these are untracked runtime directories. Two are already tracked files that behave like machine-local state or logs. Without a shared ignore strategy, these artifacts keep reappearing and create noise around real content changes.

## Scope
Included:
- Create or update a shared `.gitignore`
- Add targeted ignore rules for the four runtime-artifact paths above
- Stop tracking `.obsidian/workspace.json` and `.smart-env/event_logs/event_logs.ajson` while keeping the files locally
- Verify the ignore rules and final `git status`

Excluded:
- No ignoring of entire `.obsidian/` or `.smart-env/` trees
- No deletion of local runtime files
- No cleanup of unrelated tracked files
- No changes to project logic, ontology content, or skills

## Proposed design

### 1. Use repository-shared `.gitignore`
The ignore rules should live in `.gitignore`, not `.git/info/exclude`, because the user explicitly wants repository-shared behavior.

This makes the runtime-artifact policy visible and consistent across collaborators.

### 2. Add only narrow ignore rules
The ignore file should include exactly the targeted runtime paths:
- `.claude/worktrees/`
- `.smart-env/multi/`
- `.obsidian/workspace.json`
- `.smart-env/event_logs/event_logs.ajson`

This avoids overreaching rules like ignoring the entire `.obsidian/` or `.smart-env/` tree.

### 3. Remove tracked runtime files from the index only
Because `.obsidian/workspace.json` and `.smart-env/event_logs/event_logs.ajson` are already tracked, adding them to `.gitignore` is not sufficient.

The implementation should remove them from git’s index while preserving the local files on disk. After that, the new `.gitignore` rules will prevent them from reappearing in normal status output.

## File-level changes
- Create or modify: `.gitignore`
- Update index tracking for:
  - `.obsidian/workspace.json`
  - `.smart-env/event_logs/event_logs.ajson`

## Verification
1. Confirm `.gitignore` contains the four targeted rules
2. Run `git check-ignore -v` against all four paths
3. Confirm the two tracked runtime files still exist locally
4. Confirm those two files are no longer tracked by git
5. Run `git status --short` and confirm the runtime artifacts no longer appear

## Risks
- If these files were intentionally meant to be shared, removing them from the index would stop that behavior
- If ignore rules are too broad, future legitimate files under `.obsidian/` or `.smart-env/` could be hidden by accident

This design minimizes those risks by targeting only the exact runtime paths rather than whole directories.

## Success criteria
- `.claude/worktrees/` no longer appears as untracked
- `.smart-env/multi/` no longer appears as untracked
- `.obsidian/workspace.json` no longer appears as modified
- `.smart-env/event_logs/event_logs.ajson` no longer appears as modified
- Local runtime files remain present on disk
- Ignore policy is shared through the repository
