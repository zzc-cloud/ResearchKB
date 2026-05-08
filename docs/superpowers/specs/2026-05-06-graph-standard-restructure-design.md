# ResearchKB Graph Standard Restructure Design

Date: 2026-05-06
Status: Draft for review
Target: [ontology/graph-standard.md](ontology/graph-standard.md)

## 1. Goal

Rebuild `ontology/graph-standard.md` into a stable **normative source** for ResearchKB.

The target state is:
- `graph-standard.md` defines **what is valid** in the graph.
- `CLAUDE.md` defines **how work is routed and executed**.
- skills define **how each stage performs its task**.
- `ontology/index.md` and object-domain indexes define **where navigation starts**.

This restructure is intentionally a **boundary cleanup and structural reorganization**, not a semantic rewrite of the ontology.

## 2. Problem Statement

The current `graph-standard.md` contains strong normative content, but also mixes in:
- workflow sequencing
- runtime consumption guidance
- index/navigation maintenance details
- skill-adjacent execution explanations

That blending creates three problems:
1. the document is harder to read because ontology truth, serving rules, and process explanations are interleaved;
2. some sections repeat rules that already exist earlier in the file;
3. some process-oriented content duplicates `CLAUDE.md`, creating dual-maintenance risk.

The restructuring should preserve the file as the **single normative standard** while removing or compressing content that belongs elsewhere.

## 3. Boundary Decision

### 3.1 Keep in `graph-standard.md`

Keep any content that defines one of the following:
- ontology truth
- relation semantics
- page contracts
- evidence contracts
- projection contracts
- serving and governance acceptance criteria
- quality floor and exemption rules
- a small amount of high-level guidance on how to consume the standard

### 3.2 Move out of `graph-standard.md`

Move content out when it primarily describes:
- execution order
- stage sequencing
- skill responsibilities
- operational routing steps
- managed-block maintenance details
- detailed runtime behavior that is better owned by `CLAUDE.md`, `ontology/index.md`, or specific skills

### 3.3 Compress rather than delete

Keep a small amount of principle-level guidance when it helps readers understand how the standard is intended to be consumed.

Examples of acceptable retained guidance:
- `ontology/relations/` is the formal truth source for instance edges.
- object pages and `## Formal relations` are the default serving/read surface after governance.
- evidence pages support mechanism, experiment, citation, and provenance verification.

Examples of guidance that should be removed or reduced:
- step-by-step reading order written like an operating manual
- detailed explanations of which skill owns which maintenance step
- compile-chain sequencing duplicated from `CLAUDE.md`

## 4. Target Document Structure

The recommended structure is:

```md
# ResearchKB Graph Standard

## 1. Document Positioning

## 2. Ontology Foundations
### 2.1 Node Types
### 2.2 Survey / Framework Modeling Axioms
### 2.3 Relation Types

## 3. Entity Page Contracts
### 3.1 Controlled Frontmatter Fields
### 3.2 General Filling Principles
### 3.3 Paper
### 3.4 Method
### 3.5 Concept
### 3.6 Task
### 3.7 Benchmark
### 3.8 Scenario
### 3.9 Evidence

## 4. Relation Ledger and Evidence Contracts
### 4.1 Instance Edge Layer
### 4.2 Instance Edge Record Format
### 4.3 Relation File Ownership
### 4.4 Concept-Network Supplemental Edge Labels
### 4.5 Instance Edge Maintenance Rules
### 4.6 Redundant Cache Retirement Rules
### 4.7 Evidence Requirements

## 5. Serving-Layer and Governance Contracts
### 5.1 Truth Source and Serving Layers
### 5.2 Cross-Type Serving Projection Rules
### 5.3 Formal Relations Block Specification
### 5.4 Serving Migration States
### 5.5 Serving Governance Validation Requirements
### 5.6 Governance Gates

## 6. Quality Floor and Consumption Principles
### 6.1 Node Judgment Rules
### 6.2 Paper-Type and Exemption Rules
### 6.3 Minimum Linking Obligations
### 6.4 Link Quality Requirements
### 6.5 Knowledge Consumption Principles
### 6.6 Index Projection Principles
### 6.7 Relation Index
```

This structure separates:
- ontology definition
- object-page contracts
- formal ledger/evidence contracts
- serving/governance contracts
- quality floor and consumption principles

## 5. Section-by-Section Boundary Mapping

### 5.1 Keep as normative source

These areas should remain in `graph-standard.md` with only minor wording cleanup:
- node types
- survey / framework modeling axioms
- controlled frontmatter fields
- per-type required/recommended fields
- per-type body structure requirements
- evidence cache rules and boundaries
- relation types
- instance edge record format
- relation file ownership
- instance edge maintenance rules
- cross-type serving projection rules
- `## Formal relations` block specification
- serving migration states
- governance validation requirements
- governance gates
- node judgment rules
- paper-type and exemption rules
- minimum linking obligations
- link quality requirements
- evidence requirements

### 5.2 Keep but compress

These areas should stay, but be reduced to principle statements.

#### A. Instance edge / serving read surface guidance
Current content spans multiple sections that repeat the same idea:
- formal truth lives in `ontology/relations/`
- governed object pages are the default read surface
- governance/audit flows may return to the ledger

Target state:
- keep a short statement in the instance-edge area;
- keep a short layer-boundary statement in the serving/governance area;
- keep a short consumption-principles statement for question answering.

#### B. Index projection principles
Keep only:
- indexes are navigation projections, not formal truth sources;
- being indexable and being default-serving are different states.

Move out:
- which tool maintains managed blocks;
- which validator owns which operational responsibility.

#### C. Repeated survey/framework classification language
When later sections need to reference classification logic, they should point back to the earlier modeling axiom instead of restating it in full.

### 5.3 Move to `CLAUDE.md`

The following belongs in `CLAUDE.md` rather than `graph-standard.md`:
- single-paper compile chain sequence
- stage ordering
- interruption conditions
- operational routing between ontology layer / object layer / relation layer / evidence layer / raw layer
- default task-to-skill workflow guidance

### 5.4 Move to skill docs / templates / evals

The following should live in skill contracts, references, or evaluation checklists instead of the normative standard:
- extraction branching logic in `paper-ingest`
- candidate relation bucketing and reporting formats
- `needs-skill-update` triggers
- projection-sync execution detail
- governance-review procedural checklists
- verbose prose template guidance that is execution-oriented rather than contractual

## 6. Identified Redundancy Hotspots

### 6.1 Survey/framework logic repeated in later paper-type rules
`paper-type and exemption` guidance currently repeats classification logic already defined by the earlier modeling axiom.

Target fix:
- keep the exemption logic;
- replace repeated classification prose with a short cross-reference to the modeling axiom.

### 6.2 `supports` / `depends_on` explained twice
The semantics are already defined in relation types, and later repeated again in concept-network supplemental labels.

Target fix:
- keep semantic definitions in relation types;
- keep only usage-scope restrictions in the later section.

### 6.3 Serving/read-surface principles repeated across multiple sections
The same truth-source vs serving-surface idea appears in:
- instance-edge layer
- truth-source / serving-layer section
- knowledge consumption rules

Target fix:
- assign each section one responsibility and shorten all three.

## 7. Recommended Wording Direction

### 7.1 Document positioning
Add a short opening section stating:
- this file is the normative source for graph structure, relation legality, evidence obligations, projection rules, and governance acceptance criteria;
- workflow sequencing lives in `CLAUDE.md`;
- navigation entrypoints live in `ontology/index.md` and object-domain indexes.

### 7.2 Knowledge consumption principles
Rewrite this area so it stays principle-level, for example:
- default knowledge serving reads governed object pages and their `## Formal relations`;
- evidence pages are used for mechanism, experiment, citation, and provenance verification;
- formal relation ledgers are the truth source used primarily in governance, repair, and audit contexts.

### 7.3 Index projection principles
Rewrite this area so it stays principle-level, for example:
- indexes are stable navigation projections rather than truth sources;
- index inclusion and serving exposure are separate decisions.

## 8. Title Recommendation

Rename the document title from:
- `# Graph Standard`

to:
- `# ResearchKB Graph Standard`

Reason:
- clearer when linked from other files;
- stable if additional standards are introduced later;
- consistent with the document’s role as a project-level normative source.

## 9. Execution Plan for the Restructure

Recommended order of edits:
1. add a short `Document Positioning` section;
2. rename the title to `# ResearchKB Graph Standard`;
3. reorder major sections into the six target groups;
4. compress repeated serving/consumption/index principles;
5. replace repeated survey/framework classification prose with cross-references;
6. trim duplicated `supports` / `depends_on` explanations;
7. run a quick read-through for internal consistency after reordering.

This order keeps semantic risk low: structure first, then deduplication.

## 10. Out of Scope

This redesign does not attempt to:
- change ontology semantics;
- add new node or relation types;
- rewrite the ResearchKB compile pipeline;
- rewrite skill prompts as part of the same change;
- redesign object-domain index pages beyond clarifying their boundary relative to the standard.

## 11. Acceptance Criteria

The restructure is successful if all of the following are true:
- `graph-standard.md` reads as a normative standard rather than an execution manual;
- workflow sequencing is no longer duplicated from `CLAUDE.md`;
- navigation ownership is not mixed into truth-source sections except at a principle level;
- repeated survey/framework classification text is reduced;
- repeated serving/read-surface explanations are reduced;
- the resulting structure makes it obvious where to look for ontology rules, page contracts, ledger contracts, and serving/governance requirements.
