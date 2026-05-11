# Survey Paper to Method Relation Design

## Context
ResearchKB has now been intentionally reduced to a phase-1 method graph. The live ontology centers on `Paper`, `Method`, `Task`, `Scenario`, `Benchmark`, `Evidence`, and `RawSource`, with `Method` as the primary reusable technical object. This works well for ordinary method papers, where a paper usually proposes one core method and then the rest of the graph grows outward from that method.

However, survey papers create a different structural need. A survey paper often does not propose the many methods it discusses, yet it still serves as a high-value ontology object because it systematically organizes, compares, or classifies a large set of methods within a domain. If the graph only preserves `cites` edges from the survey paper, the survey remains a weak entry surface: it references many papers, but it does not formally expose which methods it structurally covers as part of the domain-level method map. If the graph instead reuses `proposes`, the ontology becomes semantically wrong, because the survey did not invent the covered methods.

The user’s requirement is explicit: to form a useful ontology for a large field, survey papers need a formal relation to the many methods they systematically cover.

## Goal
Add a dedicated formal relation from survey papers to methods so that survey papers can act as structured method-coverage entry points without overloading `proposes` or collapsing into plain `cites`.

## Non-goals
- Do not redefine `proposes`.
- Do not reuse `cites` to stand in for method coverage.
- Do not add survey-specific formal relations for `Task`, `Scenario`, or `Benchmark` in this change.
- Do not change method-to-method relations such as `based_on` or `references_method`.

## Design decisions

### 1. Add a dedicated relation: `surveys_method`
Introduce a new formal relation:

- `[[Paper]] --surveys_method--> [[Method]]`

Meaning:
- The paper is a survey or survey-like organizing work that systematically covers, classifies, compares, or otherwise structurally includes the method in its domain analysis.

This relation is intentionally specific:
- source: `Paper`
- target: `Method`
- typical source subtype: survey / framework / landscape / taxonomy paper acting in a survey role

### 2. Keep `surveys_method` distinct from existing relations
The new relation must not be treated as a variant of any existing relation family.

#### Not `proposes`
`proposes` remains reserved for papers that first introduce or formally define a method. A survey paper that discusses an existing method does not propose it.

#### Not `cites`
`cites` only records paper-to-paper citation facts. A survey may cite many papers without systematically covering all of their methods, and it may also structurally compare methods in a way stronger than plain citation.

#### Not `references_method`
`references_method` is a Method→Method relation used for comparison, borrowing, or route reference between methods. It does not represent a survey paper’s organizing relation to methods.

### 3. Evidence threshold must be stronger than mention or citation
A survey paper should generate `surveys_method` only when the method is included in the paper’s actual survey structure, not when it is merely mentioned.

Strong evidence examples:
- the method appears in a method taxonomy or survey table
- the paper groups it into a method family
- the paper explicitly compares it as part of a survey coverage set
- the paper allocates a section/subsection to the method or a method cluster it belongs to
- the paper treats it as part of the domain landscape rather than a one-off related-work mention

Weak evidence that is NOT enough by itself:
- a casual mention in background prose
- a standard citation with no survey structuring role
- one sentence in related work without coverage, grouping, or comparison

### 4. Evidence source should prefer survey-oriented cache material
When available, `surveys_method` should preferentially cite:
- `analysis.md`
- or a survey-oriented `sections.md` passage

The relation should not default to `refs.md` unless the reference page is the only place where structured survey coverage is actually captured.

### 5. Scope the new relation to `Paper -> Method` only
This design deliberately limits the new relation family to methods.

Do NOT add now:
- `surveys_task`
- `surveys_scenario`
- `surveys_benchmark`

Rationale:
- the most urgent ontology gap is between survey papers and the method graph
- adding the broader survey-* family now would expand scope and force additional evidence and contract decisions
- method coverage is the core user need for forming a large-field ontology

## Why this relation is necessary
Without `surveys_method`, the system is forced into one of two bad states:

1. **Under-modeling**
   - The survey paper only has `cites`, so the method graph loses a formal “survey coverage” layer.
   - The survey becomes hard to use as a domain entry surface.

2. **Semantic pollution**
   - The survey uses `proposes` to connect to covered methods.
   - This makes the ontology factually wrong by treating covered methods as newly proposed methods.

`surveys_method` avoids both failures.

## Files and system areas affected

### Ontology contract
Update `ontology/graph-standard.md` to:
- add `surveys_method` to the formal relation list
- define legal source/target types
- distinguish it clearly from `proposes`, `cites`, and `references_method`
- document the “systematic survey coverage” evidence threshold

### Relation ledger
Create:
- `ontology/relations/surveys_method.md`

This file should include:
- relation semantic explanation
- legal source/target contract
- canonical instance format

### Survey-paper serving guidance
Update survey-related page guidance so survey Paper pages can project:
- outgoing `surveys_method`

without suggesting that those methods are proposed by the survey.

### Skills
Update ingest, reconciliation, projection, and semantic review skills so they:
- recognize `surveys_method` as a formal candidate
- route it to the correct ledger
- verify that evidence is structural survey coverage rather than casual mention
- distinguish it from `proposes`

## Expected effect on the graph
After this change, a survey paper can become a formal domain entry object such as:
- `[[Some Survey Paper]] --surveys_method--> [[Method A]]`
- `[[Some Survey Paper]] --surveys_method--> [[Method B]]`
- `[[Some Survey Paper]] --surveys_method--> [[Method C]]`

while still also having:
- `[[Some Survey Paper]] --cites--> [[Paper Behind Method A]]`
- `[[Some Survey Paper]] --cites--> [[Paper Behind Method B]]`

and without incorrectly claiming:
- `[[Some Survey Paper]] --proposes--> [[Method A]]`

## Verification expectations
Implementation should verify that:
- `surveys_method` is defined as `Paper -> Method`
- survey papers can project it in their `Formal relations`
- non-survey papers do not start emitting it casually
- `proposes` remains restricted to actual method introduction
- candidate generation and review logic treat mention-only evidence as insufficient

## Scope boundary
This design addresses exactly one ontology gap:
- survey-paper-to-method formal coverage

It does not redesign:
- the rest of the survey-paper ontology model
- task/scenario/benchmark survey coverage relations
- second-phase abstraction layers
