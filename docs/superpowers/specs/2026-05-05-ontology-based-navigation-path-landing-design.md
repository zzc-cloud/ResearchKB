# Ontology-Based Navigation Path Landing Design

Date: 2026-05-05

## Summary

Land the ontology-based navigation path in ResearchKB as a layered navigation system with clear role separation:
- `CLAUDE.md` defines global navigation principles and default reading order
- `wiki/ontology/index.md` serves as the system-wide routing entry
- each `wiki/<object-domain>/index.md` serves as the instance directory for that object domain
- `wiki/relations/*.md` serves as the formal relation ledger and governance-side navigation surface
- entity pages remain the default serving-ready reading entry, with `Formal relations` as the constrained topology expansion surface
- `intermediate/papers/` remains the evidence drill-down layer

The implementation scope is the user-selected **standard** level:
- update navigation docs
- create all six object-domain index pages
- add navigation headers to relation ledgers
- add lightweight navigation blocks to existing entity pages
- do not rewrite entity-page body content or rework formal relation payloads

## Problem

ResearchKB already has the right conceptual pieces for ontology-driven navigation, but the navigation path is not yet fully materialized as a stable system:
- `CLAUDE.md` describes ontology-first cognition and default reading order, but it does not fully encode the final layered navigation language the user has settled on
- `wiki/ontology/index.md` acts as a global entry page, but it still needs to become a stricter routing page that points cleanly to object domains, relation ledgers, and evidence usage modes
- object domains such as `wiki/concepts/` and `wiki/tasks/` do not yet all have dedicated `index.md` instance directories
- relation ledgers expose formal edges, but do not consistently explain how they relate back to object domains and when they should be read instead of object pages
- entity pages are the de facto serving-ready entry surface, but they do not yet consistently expose a lightweight navigation block linking back to object-domain indexes and relevant ledgers

Without these layers being made explicit, users and agents can still blur:
- global navigation vs. object-domain navigation
- serving entry vs. governance truth source
- instance discovery vs. topology expansion
- object-page reading vs. evidence drill-down

## Goals

- Materialize the agreed ontology-based navigation path as a concrete documentation and page-linking system.
- Keep `CLAUDE.md` focused on ontology cognition, question classification, and default navigation order.
- Keep `wiki/ontology/index.md` as the single system-wide routing entry, not an instance catalog.
- Create all six object-domain index pages:
  - `wiki/papers/index.md`
  - `wiki/methods/index.md`
  - `wiki/concepts/index.md`
  - `wiki/tasks/index.md`
  - `wiki/scenarios/index.md`
  - `wiki/benchmarks/index.md`
- Make object-domain indexes usable as actual instance directories through a mixed layout:
  - domain description
  - core entry points
  - theme/semantic grouping
  - complete instance list
  - related relation ledgers
- Upgrade each `wiki/relations/*.md` page into a governance-aware navigation page by adding a lightweight header that explains:
  - what formal relations it owns
  - which object domains it is most related to
  - when to read object pages first
  - when to return to the ledger for governance or truth-source verification
- Add lightweight navigation blocks to existing entity pages so readers can move between:
  - entity page
  - object-domain index
  - relevant relation ledgers
  - evidence entry points where applicable
- Preserve the existing ontology rule that serving-ready object pages are the default question-answering entry, while relation ledgers remain the formal graph truth source.

## Non-goals

- Rewrite the body structure of all entity pages.
- Rework or regenerate `Formal relations` content across the repository.
- Perform relation reconciliation or ontology semantic review as part of this task.
- Expand this into a full knowledge-content cleanup.
- Change ingest, reconciliation, projection-sync, or governance workflow behavior.
- Turn relation ledgers into the default user-facing reading surface.

## Chosen approach

Adopt a **five-layer navigation chain plus evidence drill-down**:

1. `CLAUDE.md`
   - defines how to classify the user’s question in ontology terms
   - defines the default navigation order
   - explains when to expand topology and when to consult governance truth

2. `wiki/ontology/index.md`
   - defines the global routing surface
   - links to:
     - ontology standard
     - object-domain indexes
     - relation ledgers
     - evidence usage paths

3. `wiki/<object-domain>/index.md`
   - defines the instance-discovery surface inside each object domain
   - points readers to concrete formal objects
   - links onward to related ledgers

4. entity pages
   - remain the serving-ready reading entry
   - expose a lightweight navigation block
   - use `Formal relations` as the constrained expansion surface

5. `wiki/relations/*.md`
   - remain the formal relation ledger / governance truth source
   - gain a small navigation header that reconnects ledger reading with object-domain navigation

6. `intermediate/papers/`
   - remains the evidence verification layer for mechanism, experiment, citations, baselines, and provenance checks

This keeps the user’s agreed semantics intact:
- object pages are the default reading entry
- ledgers are the formal source of truth
- object-domain indexes support instance discovery
- relation ledgers can anchor specific instances in governance-heavy scenarios, but do not replace object-domain navigation

## Alternatives considered

### Option A: Light implementation
Only update `CLAUDE.md`, `wiki/ontology/index.md`, and add object-domain index pages.

Pros:
- smallest scope
- low edit risk

Cons:
- entity pages would still lack consistent back-links
- relation ledgers would still be weak navigation participants
- the navigation chain would remain incomplete in practice

### Option B: Standard implementation
Update global navigation docs, create all object-domain indexes, add relation-ledger headers, and add lightweight entity-page navigation blocks.

Pros:
- completes the navigation loop end to end
- keeps page bodies mostly intact
- matches the user’s requested scope exactly

Cons:
- requires more multi-file edits than the light option

### Option C: Heavy implementation
In addition to Option B, systematically rewrite entity-page narrative structure and relation-facing human sections.

Pros:
- maximum consistency

Cons:
- scope balloons into full repository restructuring
- mixes navigation work with knowledge-content reauthoring
- high churn for limited immediate benefit

Recommendation: **Option B**.

## Navigation role model

### 1. `CLAUDE.md` role

`CLAUDE.md` should explicitly serve as the **global ontology navigation policy layer**.

It should answer:
- what kind of ontology problem is this
- which node types and relation types may be involved
- which information layers should be read first
- when to expand via topology
- when to verify against relation ledgers or evidence

It should not become:
- an instance catalog
- a replacement for `graph-standard.md`
- a page that lists all concrete ontology objects

### 2. `wiki/ontology/index.md` role

`wiki/ontology/index.md` should explicitly serve as the **single system-wide routing page**.

It should include:
- ontology standard entry
- object-domain index entries
- relation-ledger entries
- recommended reading paths for question answering, governance, evidence verification, and review

It should not include:
- long instance lists
- per-object summaries
- duplicated ontology rules from `graph-standard.md`

### 3. `wiki/<object-domain>/index.md` role

Each object-domain index should explicitly serve as the **instance directory** for its domain.

Each page should use a mixed structure:
- what this domain contains
- which ledgers most relate to this domain
- core entry objects
- theme/semantic grouping where useful
- complete instance list

This allows both:
- exploratory browsing
- stable full coverage even as theme grouping evolves

### 4. entity-page role

Entity pages remain the **default serving-ready reading entry**.

Each page should gain a lightweight navigation block that points to:
- its object-domain index
- relevant relation ledgers
- relevant evidence entry points if there is an obvious evidence path

Entity pages should continue to use `Formal relations` as the constrained topology expansion surface.

Entity pages should not become:
- global navigation pages
- relation-ledger truth sources
- heavily duplicated relation explanation pages

### 5. relation-ledger role

Each `wiki/relations/*.md` page remains the **formal relation truth source and governance-side reading surface**.

Each ledger should gain a lightweight header that explains:
- what formal relation types it owns
- which object domains it most commonly anchors
- that serving-ready question answering should read object pages first
- when to use the ledger instead:
  - governance
  - repair
  - audit
  - truth-source verification
  - object-page expansion insufficiency

Relation ledgers may help anchor instances in specific governance scenarios, but they do not replace object-domain indexes as the primary instance discovery path.

### 6. evidence-layer role

`intermediate/papers/` remains the **evidence drill-down layer**.

It is used when readers need:
- mechanism details
- experimental evidence
- citation support
- baseline context
- provenance verification

It is not the primary discovery surface.

## Concrete page-shape decisions

### `wiki/ontology/index.md`

Refactor into four stable sections:

1. **规范入口**
   - link to `graph-standard`

2. **对象域入口**
   - link to all six object-domain indexes

3. **关系域入口**
   - link to all relation ledgers

4. **推荐路径**
   - question-answering path
   - governance path
   - evidence verification path
   - review/synthesis path

This page should remain a router, not a directory.

### object-domain index pages

Create six pages with a shared structural template:
- domain purpose
- core entry points
- thematic grouping
- complete instance list
- related ledgers

The user selected the **mixed** organization model, so each page should combine:
- a curated upper section for navigation value
- a stable lower section for complete coverage

### relation ledgers

Each ledger gets a uniform page-top navigation block with:
- maintained relation types
- related object domains
- when to read object pages first
- when to consult the ledger
- links back to object-domain indexes
- links to evidence/provenance context where relevant

### entity pages

Each existing formal object page gets a lightweight navigation block, likely near the top, with:
- object-domain index link
- relevant ledgers
- relevant evidence entry if obvious
- one-line role statement explaining that this is the default serving-ready object page, while formal graph truth lives in ledgers

The body narrative and `Formal relations` content remain otherwise unchanged.

## File changes

### Files to modify
- `CLAUDE.md`
- `wiki/ontology/index.md`
- all existing `wiki/relations/*.md`
- existing formal object pages under:
  - `wiki/papers/`
  - `wiki/methods/`
  - `wiki/concepts/`
  - `wiki/tasks/`
  - `wiki/scenarios/`
  - `wiki/benchmarks/`

### Files to create
- `wiki/papers/index.md`
- `wiki/methods/index.md`
- `wiki/concepts/index.md`
- `wiki/tasks/index.md`
- `wiki/scenarios/index.md`
- `wiki/benchmarks/index.md`

## Implementation sequence

### Phase 1: establish global navigation backbone
Update:
- `CLAUDE.md`
- `wiki/ontology/index.md`

Purpose:
- make the global navigation model explicit first
- lock in the distinction between object-page serving entry and ledger truth source

### Phase 2: create all object-domain indexes
Create the six `wiki/<object-domain>/index.md` pages.

Purpose:
- make every object domain navigable as an instance directory
- give `wiki/ontology/index.md` concrete landing pages

### Phase 3: add relation-ledger navigation headers
Update all `wiki/relations/*.md` pages.

Purpose:
- let ledgers participate in navigation without displacing object pages as the default reading entry

### Phase 4: add entity-page navigation blocks
Batch-update existing formal entity pages with lightweight navigation blocks.

Purpose:
- complete the navigation loop from instance pages back to object domains and ledgers

### Phase 5: verify navigation closure
Check:
- ontology index routes everywhere it should
- every object-domain index routes to instances and ledgers
- every entity page routes back to object domain and outward to relevant ledgers
- every ledger routes back to related object domains and context

## Verification model

Success should be measured as **navigation closure**, not ontology-content expansion.

### 1. system entry closure
From `wiki/ontology/index.md`, readers can reach:
- `graph-standard`
- all object-domain indexes
- all relation ledgers
- the evidence reading path

### 2. object-domain closure
From each `wiki/<object-domain>/index.md`, readers can reach:
- core objects in that domain
- the full object list
- related ledgers

### 3. entity-page closure
From each entity page, readers can reach:
- the parent object-domain index
- relevant relation ledgers
- evidence entry points where appropriate

### 4. ledger closure
From each ledger, readers can reach:
- related object-domain indexes
- the object context the ledger governs
- evidence/provenance context where relevant

## Key risks and decisions

### Risk: `wiki/ontology/index.md` becomes a second object catalog
Decision:
- keep it strictly as a router
- do not place instance lists there

### Risk: relation ledgers get treated as the normal first-stop reading surface
Decision:
- explicitly state in each ledger that object pages remain the default question-answering entry
- reserve ledger-first reading for governance-heavy use cases

### Risk: object pages and ledgers both start maintaining human-written relation explanations
Decision:
- keep object-page navigation blocks lightweight
- preserve ledgers as the formal edge truth surface
- avoid adding long relation prose to entity pages

### Risk: object-domain indexes become bloated summary pages
Decision:
- keep them directory-like
- use only short domain-level framing and short labels for entries
- avoid per-entry mini-essays

### Risk: navigation work turns into repository-wide content cleanup
Decision:
- do not rewrite page bodies
- do not use this task to repair unrelated ontology content issues
- constrain edits to navigation surfaces and routing clarity

## Hard rules after landing

1. `wiki/ontology/graph-standard.md` remains the only ontology authority.
2. `CLAUDE.md` defines ontology cognition and default reading order, not concrete instance inventory.
3. `wiki/ontology/index.md` is the single global routing page.
4. `wiki/<object-domain>/index.md` pages own instance-directory navigation.
5. `wiki/relations/*.md` pages own formal relation truth.
6. entity pages remain the default serving-ready reading entry.
7. `Formal relations` remains the constrained topology expansion surface on object pages.
8. `intermediate/papers/` remains the evidence drill-down layer.
9. relation ledgers may anchor instances in special cases, but do not replace object-domain indexes for primary navigation.

## Success criteria

- The layered navigation path is explicitly documented and materially present in the repository.
- All six object domains have usable `index.md` instance directories.
- `wiki/ontology/index.md` functions as a strict router rather than a mixed router/catalog page.
- Relation ledgers clearly distinguish governance truth-source usage from serving-ready object-page reading.
- Existing entity pages expose consistent navigation blocks without body rewrites.
- A reader can reliably move through the intended chain:
  - question classification
  - system routing
  - object-domain discovery
  - entity reading
  - constrained topology expansion
  - evidence verification
