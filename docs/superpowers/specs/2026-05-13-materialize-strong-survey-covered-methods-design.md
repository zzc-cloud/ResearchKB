# Materialize Strong Survey-Covered Methods for LLM-KG-CPD

## Context
The paper [A survey of large language model-augmented knowledge graphs for advanced complex product design](../../ontology/entities/papers/A%20survey%20of%20large%20language%20model-augmented%20knowledge%20graphs%20for%20advanced%20complex%20product%20design.md) is already ingested as a survey-role Paper and already proposes one integrated framework Method. However, the current ingest output collapsed most of the survey’s structured method coverage into theme-level prose inside [LLM-KG-CPD.refs](../../ontology/entities/evidence/LLM-KG-CPD.refs.md), rather than materializing the covered methods as formal graph objects.

This creates a mismatch with the ontology contract. The graph now has a survey paper that clearly acts as a domain-organizing object, but it does not formally expose the methods it systematically covers. As a result, [ontology/relations/surveys_method.md](../../ontology/relations/surveys_method.md) remains empty even though this survey contains structured method coverage strong enough to admit some methods into the graph.

The user has confirmed that the goal is not to ingest every cited work, but to materialize only the strongest and safest subset as partial Method pages with `surveys_method` relations.

## Goal
Materialize the strongest survey-covered methods from the LLM-KG-CPD survey as `status: partial` Method pages, and connect them to the survey paper through formal `surveys_method` relations.

## Non-goals
- Do not perform full independent ingest of the covered method papers.
- Do not create or expand `cites` coverage for the survey paper in this change.
- Do not add `references_method`, `based_on`, `targets_task`, `applied_in`, or `evaluated_on` for the newly materialized methods.
- Do not add new `Task` or `Scenario` nodes for manufacturing design stages.
- Do not expand beyond the strongest confirmed subset.

## Chosen scope
Materialize exactly these eight Method objects:

1. BEAR
2. AutoKG
3. ASKG
4. OLaLa
5. KG-CGT
6. RelMKG
7. StructGPT
8. CausalKGPT

These eight were chosen because they satisfy all of the following:
- stable method-like naming
- survey-role structured coverage rather than casual mention
- enough local evidence to write a minimal `object_semantics`
- low risk of confusing an application topic, general paper title, or system description with a reusable Method object

Items such as SelfX, KRP-DS, and broader application-paper titles are intentionally excluded from this pass because their ontology identity is less stable and would raise review cost.

## Design decisions

### 1. Use `partial` Method pages, not placeholders
Each selected method will be materialized as a `status: partial` Method page under `ontology/entities/methods/`.

Rationale:
- the ontology contract says stable Method identity plus at least one formal relation should materialize as a partial Method rather than a Method placeholder
- these methods are not yet fully ingested, but they are no longer just unresolved mention-level objects
- partial Method pages make the survey’s method coverage traversable without pretending that the methods have already been fully compiled

### 2. Admit the methods through `surveys_method`
The survey paper will gain eight outgoing `surveys_method` edges in [ontology/relations/surveys_method.md](../../ontology/relations/surveys_method.md).

Rationale:
- the survey did not propose these methods
- the survey is not merely citing them in isolated prose
- the ontology already defines `surveys_method` exactly for this situation: Paper → Method structured survey coverage

### 3. Keep supporting evidence minimal and conservative
Each newly materialized Method will receive:
- one incoming `surveys_method` edge from the survey paper
- one outgoing `supported_by` edge to an evidence cache from the same survey

Preferred evidence source:
- first choice: `LLM-KG-CPD.analysis.md`
- second choice: `LLM-KG-CPD.refs.md` when the available support is still structurally grounded but not yet rewritten into method-by-method analysis prose

Rationale:
- the graph standard prefers survey-oriented `analysis.md` or `sections.md` for `surveys_method`
- but the current ingest preserved only coarse-grained summaries, so this pass should not block on perfect evidence wording if the survey’s method coverage is still stable enough to justify partial admission

### 4. Do not infer downstream relations for these methods yet
No new `targets_task`, `applied_in`, `references_method`, `based_on`, or `evaluated_on` edges will be created for these eight methods.

Rationale:
- this pass is about method admission, not full ontology expansion
- even if some methods likely have task or scenario affiliations, the current local evidence was not written in a method-by-method structured way
- adding more relations now would create unnecessary semantic risk and scope creep

### 5. Do not create cited-paper stubs unless strictly needed
This pass will avoid creating Paper Stub / Anchor pages for the eight methods’ source papers unless a page contract or weak-anchor rule strictly forces it.

Rationale:
- `surveys_method` is a Paper → Method relation and does not itself require per-method cited-paper stubs the way some `references_method` cases do
- adding eight new paper stubs would expand the scope from “materialize methods” to “materialize method papers”
- the user asked for method materialization, not citation-graph expansion

## Per-page contract
Each new Method page will follow the partial Method contract from the graph standard.

### Required frontmatter
- `title`
- `type`
- `parent_methods: []`
- `child_methods: []`
- `problem`
- `method_family`
- `scenario: []`
- `research_task: []`
- `industry`
- `research_role`
- `status: partial`

### Required sections
- `## Object semantics`
- `## 当前定位`
- `## 与知识库现有内容的关系`
- `## 最小定义/角色`
- `## 待补充`
- `## Formal relations`
  - `### Outgoing`
  - `### Incoming`

### Content rules
- `Object semantics` should state the minimum stable method identity, not a full literature summary.
- `当前定位` should explicitly say the page is materialized from survey coverage and remains partial pending independent ingest.
- `与知识库现有内容的关系` should anchor the object to this survey and to the broader LLM/KG method graph.
- `最小定义/角色` should only assert what the survey safely supports.
- `待补充` should explicitly defer full method details to future independent ingest.

## Naming rules
Use the shortest stable method identity visible in the survey literature coverage.

Chosen titles:
- `BEAR`
- `AutoKG`
- `ASKG`
- `OLaLa`
- `KG-CGT`
- `RelMKG`
- `StructGPT`
- `CausalKGPT`

Do not use full paper titles as Method titles unless no stable shorter method name exists.

## Relation design

### `surveys_method`
Add eight edges to [ontology/relations/surveys_method.md](../../ontology/relations/surveys_method.md):
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[BEAR]]`
- `...`
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --surveys_method--> [[CausalKGPT]]`

Each edge semantics should say:
- the survey structurally includes the method as part of a grouped or role-based method coverage set
- the relation expresses survey coverage rather than first proposal

### `supported_by`
Add one `supported_by` edge per new Method page.

Default pattern:
- `[[Method]] --supported_by--> [[LLM-KG-CPD.analysis]]`

Fallback pattern when method-level structural support is currently preserved more clearly in refs coverage:
- `[[Method]] --supported_by--> [[LLM-KG-CPD.refs]]`

## Projection expectations
After ledger updates:
- the survey paper should project outgoing `surveys_method` edges
- each new Method page should project incoming `surveys_method`
- each new Method page should project outgoing `supported_by`
- methods index should include the eight new partial Method pages as navigable entries

No other page types need new index entries from this change.

## Validation criteria
This change is correct when all of the following hold:
1. [ontology/relations/surveys_method.md](../../ontology/relations/surveys_method.md) contains the eight new edges.
2. The survey Paper page projects those eight outgoing `surveys_method` relations.
3. Eight new Method pages exist and satisfy the partial Method contract.
4. Each new Method page has at least one incoming `surveys_method` and one outgoing `supported_by` projection.
5. [ontology/entities/methods/index.md](../../ontology/entities/methods/index.md) includes the new partial Methods in navigation.
6. `python3 scripts/lint_graph.py` still passes.

## Risks and mitigations

### Risk 1: method identity is weaker than expected
Mitigation:
- restrict the scope to the strongest eight only
- keep all new pages at `status: partial`
- avoid downstream relation expansion

### Risk 2: evidence is too coarse in current caches
Mitigation:
- prefer `analysis.md` where possible
- allow `refs.md` as support only when the survey coverage is still clearly structural rather than casual
- keep the admission minimal and reviewable

### Risk 3: scope drifts into full survey citation graph ingest
Mitigation:
- do not create `cites` expansions
- do not create paper stubs unless strictly forced
- do not ingest the eight source papers in this pass

## Implementation sequence
1. Create the eight partial Method pages.
2. Add `supported_by` ledger entries for those Method pages.
3. Add eight `surveys_method` ledger entries.
4. Run page projection sync for the survey paper and the eight Methods.
5. Run index sync for the methods index.
6. Run graph lint.
7. Run ontology semantic review and serving governance review.

## Expected outcome
The survey will stop being a weak prose-only domain overview and become a formal method-coverage entry surface. At the same time, the graph remains conservative: the newly admitted methods are traversable and reviewable, but still clearly marked as partial until their source papers are independently ingested.
