# Relations Instance-Edge Layer Design

## Goal

Turn `wiki/relations/` into a canonical instance-edge layer for the ontology, using Markdown-maintained, relation-type-specific files. This layer should make explicit which concrete nodes are connected, by which relation type, and on what evidence, without introducing a separate structured graph datastore.

## Context

The current knowledge base has:
- node-type definitions and schema rules in `wiki/ontology/graph-standard.md`
- concrete node pages under `wiki/papers/`, `wiki/methods/`, `wiki/concepts/`, `wiki/scenarios/`, and related folders
- relation index files under `wiki/relations/`

What it lacks is a strict, canonical representation for **instance edges**. Existing relation files contain useful information, but they are not yet governed by a uniform edge-record format, per-relation-file responsibility, evidence requirements, or deduplication rules. That makes them readable by humans but weaker as a topology layer for systematic traversal and analysis.

## Problem

The ontology currently defines:
1. node classes
2. relation classes

But it does not yet fully standardize:
3. concrete edge instances between nodes

Without a canonical instance-edge layer, the repository can support local reading and informal synthesis, but it cannot reliably support topology-first querying, multi-hop exploration, or stable graph-oriented analysis across the whole corpus.

## Scope

This design covers only:
- standardized maintenance of instance edges under `wiki/relations/`
- updates to `wiki/ontology/graph-standard.md` so edge instances become a first-class normative concept
- normalization of existing relation files to the new conventions

This design does **not** cover:
- a query engine
- automatic graph export
- a separate JSON / RDF / graph-database representation
- new ingest automation beyond documentation and file-structure expectations

## Design Principles

1. **Markdown remains the storage format**
   The graph instance layer should remain human-readable and hand-maintainable.

2. **Relation types own files**
   Each relation file should own one primary relation type or one tightly related relation family.

3. **Edge instances must be explicit**
   A relation file should not rely on prose paragraphs when a concrete edge can be written directly.

4. **Evidence is mandatory**
   Every maintained edge should point to the evidence page or relation-appropriate proof source.

5. **Standards and instances are separated**
   `graph-standard.md` defines what valid edges look like; `wiki/relations/*.md` stores concrete edge instances.

6. **Small graph, strict conventions**
   Since edge volume is limited, the best tradeoff is stricter Markdown conventions rather than a separate data format.

## Alternatives Considered

### Option 1 — Relation-type files with unified edge format
Chosen.

Pros:
- Fits the current repository structure
- Preserves readability and editability
- Low migration cost from current files
- Good enough for limited graph size

Cons:
- Cross-relation traversal still requires reading several files
- Machine processing remains lighter-weight than a structured graph store

### Option 2 — Relation-type files with loose prose formatting
Rejected.

Pros:
- Minimal rewrite effort

Cons:
- Does not solve the canonical-instance problem
- Leaves edge parsing ambiguous
- Weak support for topology-first analysis

### Option 3 — Separate structured graph data
Rejected for now.

Pros:
- Strongest machine-readability
- Easier future querying and export

Cons:
- Adds operational complexity not justified by current graph size
- Duplicates graph knowledge across Markdown and data files

## Proposed Architecture

### 1. `graph-standard.md` becomes authoritative for instance-edge rules

Add sections that define:
- what the instance-edge layer is
- the standard edge record format
- required and optional record fields
- relation-type-to-file mapping
- deduplication rules
- evidence requirements
- placeholder / unverified edge rules

This promotes edge instances from an informal documentation habit to a formal ontology maintenance rule.

### 2. `wiki/relations/` becomes the canonical instance-edge layer

Each file becomes a ledger of explicit edge instances.

Recommended ownership:
- `citation_graph.md` → `cites`
- `method_evolution.md` → `improves_on`, `based_on`
- `task_method_map.md` → `targets_task`
- `concept_links.md` → concept-to-concept relations and `uses_concept`
- `evidence_index.md` → `supported_by`

This preserves the current mental model while clarifying responsibility.

### 3. Edge records use a uniform Markdown format

Each edge record should use the same top-level pattern:

```markdown
- `[[Source Node]] --relation_type--> [[Target Node]]`
  - reason: short explanation of why this edge exists
  - evidence: [[intermediate/papers/SomePaper.refs]]
```

Optional fields:

```markdown
  - status: verified | placeholder
  - note: extra context if needed
```

This yields a representation that is:
- explicit enough for consistent reading and lightweight parsing
- compact enough for manual maintenance
- semantically stricter than freeform prose

## File-by-File Design

### `wiki/relations/citation_graph.md`

Purpose:
- maintain concrete `cites` edges between paper nodes

Rules:
- one edge per citation relation
- `reason` is required
- `evidence` should usually point to a `.refs.md` cache
- prose commentary may appear in a short intro or notes section, but not instead of edges

### `wiki/relations/method_evolution.md`

Purpose:
- maintain concrete `improves_on` and `based_on` edges among method nodes

Rules:
- evolution-tree prose can remain as a readability aid if useful
- canonical truth must be recoverable from explicit edge records
- if one paper introduces the improvement, evidence should point to the relevant `sections.md`, `analysis.md`, or `refs.md`

### `wiki/relations/task_method_map.md`

Purpose:
- maintain `targets_task` edges from papers or methods to task nodes

Rules:
- relation entries should distinguish whether the source is a paper or a method when ambiguity is possible
- evidence should point to `sections.md`, `experiments.md`, or `analysis.md` depending on paper type

### `wiki/relations/concept_links.md`

Purpose:
- maintain concept-to-concept edges and `uses_concept` relations from papers or methods to concept nodes

Rules:
- relation names should be standardized rather than described only in prose
- concept hierarchy and dependency relations should use allowed relation labels defined in `graph-standard.md`

### `wiki/relations/evidence_index.md`

Purpose:
- maintain `supported_by` edges from formal knowledge pages to evidence caches

Rules:
- evidence edges should be explicit, not buried inside page prose only
- this file becomes the authoritative crosswalk between formal node pages and evidence pages

## Required Standard Additions to `graph-standard.md`

Add a new section such as `## 实例边层` that defines:
- an instance edge as a concrete relation between two specific nodes
- `wiki/relations/` as the canonical location for maintained instance-edge ledgers

Add a new section such as `## 实例边记录格式` that defines:
- canonical first line syntax
- required subfields: `reason`, `evidence`
- optional subfields: `status`, `note`

Add a new section such as `## 关系文件分工` that maps relation files to owned relation types.

Add a new section such as `## 实例边维护规则` that defines:
- no duplicate edges within one file
- if the same pair has different relation types, they remain separate records
- placeholder edges must be explicitly marked
- an edge without evidence is invalid unless explicitly exempted by paper-type rules

## Data Flow After Adoption

### During ingest
1. create or update node pages
2. identify concrete relations among nodes
3. write corresponding instance edges in the correct `wiki/relations/*.md` file
4. bind each edge to evidence
5. update relation pages incrementally rather than leaving relation facts only inside prose

### During analysis
1. locate relevant node pages
2. traverse the owned relation files for neighboring edges
3. follow evidence links when validating a hop

This does not create a query engine yet, but it creates the graph layer such an analysis flow depends on.

## Migration Strategy

### Phase 1 — Standard definition
- update `graph-standard.md`
- define edge record format and file ownership rules

### Phase 2 — Normalize existing relation files
- convert existing citation entries into standard edge records
- review the other relation files and convert mixed prose structures to explicit edge records

### Phase 3 — Align CLAUDE.md references
- ensure `CLAUDE.md` points to `graph-standard.md` for relation-maintenance norms
- avoid duplicating edge-format instructions outside the graph standard

## Risks and Mitigations

### Risk: files drift back into prose
Mitigation:
- define explicit canonical edge format in `graph-standard.md`
- treat prose as explanatory only, never as the canonical edge record

### Risk: evidence links become inconsistent
Mitigation:
- require `evidence` field on every maintained edge
- document preferred evidence page by relation type

### Risk: relation ownership becomes fuzzy
Mitigation:
- define clear per-file ownership in the standard
- require new relation types to be assigned to a file explicitly

## Testing / Validation Strategy

Success criteria for the documentation and structure change:
- `graph-standard.md` explicitly defines instance-edge maintenance rules
- each relation file has a clear owned relation scope
- existing relation files can be normalized into a uniform format
- a reader can identify concrete neighboring nodes by reading relation ledgers rather than inferring from prose

## Result

After this change, the repository will still be Markdown-first, but it will no longer only have:
- node schemas
- node pages
- relation type definitions

It will also have a canonical, explicit, evidence-backed instance-edge layer suitable for ontology-driven traversal and future graph-oriented analysis.
