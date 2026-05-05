# Obsidian Graph Inflation Fix Design

Date: 2026-05-05

## Summary

Fix the mismatch between Obsidian graph density and the formal relation graph by separating two different kinds of page links:

1. **formal-neighbor links** — links that correspond to formal one-hop graph neighbors and therefore may remain `[[wikilink]]`
2. **context links** — links used only for reading, comparison, background routes, or related navigation and therefore should not use `[[wikilink]]`

The central problem is not broken formal relations. It is that human-friendly relation blocks currently mix formal neighbors and navigation/context references in the same link syntax, so Obsidian renders both as graph edges.

## Problem

At the moment, many object pages use `[[wikilink]]` both for:
- formal one-hop neighbors that also exist in `Formal relations`
- non-formal reading/navigation/background references

Obsidian does not understand that distinction. It only sees a wikilink and renders a graph edge.

Therefore the visible Obsidian graph becomes:

> formal graph + navigation/context link graph

This is why Obsidian shows significantly more edges than the `Formal relations` surface.

## Root cause

The root cause is representational, not ontological.

- `Formal relations` may be correct
- relation ledgers may be correct
- but human-friendly relation blocks still use the same `[[wikilink]]` syntax for non-formal navigation references

As a result, the page layer leaks extra edges into the Obsidian graph.

## Goals

- Separate formal-neighbor links from context links at the template level.
- Preserve the readability of pages.
- Reduce Obsidian graph inflation.
- Keep `Formal relations` as the clean formal graph projection.
- Add lint protection so non-formal links do not creep back into the wrong blocks.

## Non-goals

- Remove all human-friendly navigation information.
- Rewrite formal relation semantics.
- Change relation ledgers.
- Eliminate contextual narrative from pages.

## Two-link model

### A. Formal-neighbor links

Definition:
- already present in the page’s `Formal relations`
- consistent with the formal ledger
- represent formal one-hop graph neighbors
- allowed to remain `[[wikilink]]`

These belong to the formal graph projection layer.

### B. Context links

Definition:
- primarily for reading support
- used for background routes, related methods, comparison methods, further reading, or same-theme navigation
- not guaranteed to have a formal graph edge
- should not use `[[wikilink]]`

These belong to the reading-assistance layer.

## Template implications

Human-friendly relation blocks should no longer be a single mixed zone.

### 1. Formal-neighbor block

Example:

```markdown
## 正式相关节点
- [[复杂产品设计中的LLM-KG协同框架]]
- [[A survey of large language model-augmented knowledge graphs for advanced complex product design]]
```

Every link in this block must correspond to a formal edge present in the page’s `Formal relations` and in the ledgers.

### 2. Context / Background block

Example:

```markdown
## 相关方法 / 路线
- PathMind
- RoG
- GCR
- ToG
```

or

```markdown
## 背景路线
- PathMind（方法论文主线）
- RoG（显式路径推理路线）
- GCR（graph-constrained reasoning 路线）
- ToG（协同增强路线）
```

These keep the information but remove the graph edge side effect.

## Why this is the minimal correct fix

This approach preserves both core goals:

### 1. Formal graph cleanliness
Obsidian graph becomes much closer to the formal graph, instead of being inflated by navigation-only links.

### 2. Human readability
The information stays on the page. Only its edge-generating representation changes.

This is better than deleting related-information blocks entirely, and better than simply accepting the inflated graph forever.

## Required changes

### 1. `wiki/ontology/graph-standard.md`
Add a rule stating:
- human-friendly relation links are split into formal-neighbor links and context links
- only formal-neighbor links may use `[[wikilink]]`
- context links default to plain text

### 2. `.claude/skills/page-projection-sync/SKILL.md`
Update sync behavior so that:
- formal neighbors are emitted as `[[wikilink]]`
- background/comparison/further-reading items are emitted as plain text
- the skill no longer assumes all human-friendly relation blocks should be linked

### 3. `scripts/lint_graph.py`
Add protection so that:
- some human-friendly blocks are allowed to contain formal-neighbor wikilinks
- some blocks (e.g. background routes, comparison blocks, context-only reading lists) should not contain wikilinks
- future regressions are caught automatically

### 4. Already migrated pages
Prioritize cleanup in:

#### PathMind / high-frequency mainline
- concept pages with related method/route blocks
- task pages with broad related-method blocks
- scenario pages with broad method lists
- benchmark pages with contextual task/scenario links

#### Survey / framework mainline
- framework concept pages
- scenario pages
- task pages
- survey paper pages with mixed related-object/reference lists

## Initial examples of the problem

### Likely context-only
- `PathMind`
- `RoG`
- `GCR`
- `ToG`
inside broad concept-page `相关方法 / 路线` blocks where no formal one-hop edge exists.

### Likely formal-neighbor links
- survey paper → framework concept
- survey paper → core concept
- survey paper → task
- framework concept → scenario

## Success criteria

After this fix:
1. Obsidian graph edge count drops noticeably.
2. Obsidian graph is much closer to the `Formal relations` graph.
3. Human-friendly pages still retain useful background information.
4. lint prevents non-formal links from creeping back into formal-neighbor-only blocks.
5. serving-governance remains stable.

## Recommendation

Adopt the two-link model:
- `Formal-neighbor links` stay as `[[wikilink]]`
- `Context links` become plain text

This is the smallest change that preserves page readability while restoring a clean separation between the formal graph and the reading-support layer.
