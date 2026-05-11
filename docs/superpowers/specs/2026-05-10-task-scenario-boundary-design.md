# Task/Scenario ontology boundary and Method→Scenario relation design

## Context
ResearchKB currently models `Task` and `Scenario` as separate entity types, but the boundary is under-specified in practice. This has allowed at least one mixed case: the current Scenario page `知识图谱推理问答` is semantically too close to the task cluster `knowledge-graph-reasoning` / `kgqa` / `multi-hop-qa`, which weakens ontology consistency and makes future ingest prone to repeating the same classification error.

At the same time, several formal relation families still allow `Paper` to act as a semantic source where the reusable knowledge unit should really be the `Method`. In particular, the current contracts for `uses_concept` and `targets_task` are too broad for the user's intended ontology boundary. Together, these issues make it easier for future ingest to over-project paper-level statements into formal graph truth.

`Scenario` is also currently underpowered in the formal graph. `Task` participates in `targets_task`, `Concept` participates in `uses_concept`, and `Benchmark` participates in `evaluated_on`, but `Scenario` is mostly represented through frontmatter, prose, and `supported_by`. That leaves Scenario as an independent entity type without a stable primary formal adjacency pattern.

The user approved a medium-scope fix: update the ontology contract, fix the known mixed example, and update the relevant skills so future paper-processing work classifies `Task` vs `Scenario` correctly. The user also approved introducing exactly one new Scenario formal relation, with a strict constraint: the new main relation must be `Method -> Scenario`, and `Paper -> Scenario` must remain disallowed. The user then added a further constraint: `uses_concept` and `targets_task` should also accept only `Method` as formal source, not `Paper`.

## Goals
- Preserve `Task` and `Scenario` as distinct entity types.
- Make their semantic boundary explicit enough to guide future ingest and review work.
- Give `Scenario` a real formal-graph role.
- Restrict `uses_concept` and `targets_task` so their legal formal source is only `Method`.
- Fix the existing mixed example so the live ontology reflects the intended boundary.
- Update skill guidance so later paper-processing sessions apply the same rule consistently.

## Non-goals
- Do not add `Paper -> Scenario` as a formal relation.
- Do not keep `Paper` as a legal source for `uses_concept` or `targets_task`.
- Do not add `Scenario -> Task` as a formal relation in this change.
- Do not add lint-script enforcement in this task.
- Do not perform a whole-repo migration beyond the known mixed example and the prompt/rule sources that influence future processing.

## Design decisions

### 1. Keep `Task` and `Scenario` separate
`Task` and `Scenario` serve different ontology roles and should not be merged.

- `Task` answers: what research problem, reasoning pattern, or question-answering objective is being solved?
- `Scenario` answers: in what application, business, or deployment context is the method used?

This preserves a clean split between problem semantics and application-context semantics.

### 2. Introduce one new formal relation: `applied_in`
Add a new formal relation:

- `[[Method]] --applied_in--> [[Scenario]]`

Meaning:
- The method is explicitly applied, positioned, or validated in a concrete application scenario.
- This is the primary formal adjacency for Scenario.

Hard constraints:
- Valid source: `Method`
- Valid target: `Scenario`
- `Paper -> Scenario` is not allowed
- `Scenario -> Task` is not introduced

Rationale:
- A method-to-scenario edge is closer to the reusable ontology unit than a paper-to-scenario edge.
- It keeps `targets_task` focused on research-problem semantics while letting `applied_in` carry application-context semantics.
- It avoids turning Scenario into a mere task container.

### 3. Narrow existing relation families to Method-only sources
Update the ontology contract for these formal relations:

- `[[Method]] --uses_concept--> [[Concept]]`
- `[[Method]] --targets_task--> [[Task]]`

Meaning:
- Formal graph truth about concept usage and task targeting should be attached to reusable methods, not directly to papers.
- Paper pages may still describe concepts, tasks, and application context in frontmatter, prose, and evidence-backed explanation, but these are not formal ledger edges.

Hard constraints:
- `Paper -> Concept` via `uses_concept` is not allowed
- `Paper -> Task` via `targets_task` is not allowed
- Scenario remains connected formally only through `Method -> Scenario`

Rationale:
- This keeps the formal graph centered on reusable knowledge units instead of publication containers.
- It reduces duplication where the same semantics would otherwise be asserted by both a paper and its proposed method.
- It sharpens the distinction between descriptive paper content and formal ontology truth.

### 4. Clarify boundary rules for future classification
The ontology contract and skill guidance should include explicit classification heuristics.

#### Task classification
Use `Task` for items that primarily denote:
- research problems
- reasoning objectives
- QA paradigms
- inference forms
- alignment/completion/query objectives

Examples:
- `knowledge-graph-reasoning`
- `kgqa`
- `multi-hop-qa`

#### Scenario classification
Use `Scenario` for items that primarily denote:
- business or application context
- deployment environment
- end-use setting
- domain workflow context

Examples:
- `enterprise-qa`
- `financial-risk`
- `compliance`

#### Ambiguity rule
When a candidate could be interpreted either way:
1. Ask whether it describes a research problem or an application context.
2. If it names a reasoning / QA / alignment / completion objective, classify as `Task`.
3. If it names an industry / business / deployment setting, classify as `Scenario`.
4. If still ambiguous, default to `Task` unless there is clear application-context evidence.

This default intentionally biases away from over-creating Scenario nodes.

### 5. Keep Scenario↔Task association out of the formal ledger
Scenario pages may still list relevant tasks through frontmatter and prose, but that association is not formal-graph truth in this change.

Concretely:
- Scenario pages may use `research_task` to summarize the task family commonly carried by the scenario.
- Scenario prose may explain which tasks are typical within that scenario.
- This does not produce a `Scenario -> Task` relation ledger entry.

Rationale:
- It keeps the formal graph compact.
- It avoids prematurely promoting editorial context into a new relation family.
- It still allows Scenario pages to remain useful as navigation and serving surfaces.

### 6. Fix the known mixed example
The current Scenario page `ontology/entities/scenarios/知识图谱推理问答.md` should be rewritten into a true application-context page, converging toward an expression like `企业知识图谱问答`.

Expected shape after the fix:
- The page becomes a genuine Scenario node with application-context semantics.
- Its `research_task` field may still mention `knowledge-graph-reasoning`, `kgqa`, and `multi-hop-qa`.
- Its formal relations should rely on `supported_by` and incoming `applied_in`, not a new Scenario→Task relation.
- Related methods such as `PathMind` should connect to it via `applied_in`.

## Files to update

### Ontology contract
- `ontology/graph-standard.md`
  - add `applied_in` to the formal relation list
  - redefine `uses_concept` and `targets_task` as Method-only source relations
  - define source/target legality and semantic scope for all three relation families
  - update Scenario guidance so Scenario is no longer “formal-edge absent” except for `supported_by`
  - add explicit Task vs Scenario classification rules
  - clarify that Scenario may mention tasks in frontmatter/prose without creating formal Scenario→Task truth
  - clarify that Paper-level concept/task/scenario descriptions stay in prose, frontmatter, and evidence-backed explanation rather than formal edges

### Relation ledger
- `ontology/relations/applied_in.md`
  - new relation ledger file
  - include semantic explanation section and canonical instance format
  - legal source: `Method`
  - legal target: `Scenario`

### Existing pages
- `ontology/entities/scenarios/知识图谱推理问答.md`
  - rename or rewrite into a true application-context scenario
- `ontology/entities/scenarios/index.md`
  - update managed navigation entry to match the corrected scenario node
- affected method pages such as `ontology/entities/methods/PathMind.md`
  - project the new `applied_in` relation
- any affected evidence or projection surfaces if the scenario rename changes links

### Skill guidance
At minimum update:
- `.claude/skills/ontology-semantic-review/...`

The skill guidance should explicitly state:
- `Task` = research problem / reasoning objective
- `Scenario` = application context / deployment setting
- ambiguous cases default to `Task`
- `Method -> Scenario` is allowed via `applied_in`
- `Method -> Concept` is the only legal `uses_concept` source
- `Method -> Task` is the only legal `targets_task` source
- `Paper -> Scenario`, `Paper -> Concept`, and `Paper -> Task` are not allowed as formal relations
- Scenario/task association in prose/frontmatter must not be mistaken for a Scenario formal edge family

If other paper-processing skills contain Task/Scenario classification heuristics or relation-family assumptions, update them to the same contract.

## Data flow impact
After this change, future compiled ontology output should prefer this pattern:
- `[[PathMind]] --uses_concept--> [[路径优先化]]`
- `[[PathMind]] --targets_task--> [[kgqa]]`
- `[[PathMind]] --targets_task--> [[multi-hop-qa]]`
- `[[PathMind]] --applied_in--> [[企业知识图谱问答]]`

This keeps:
- concept-usage truth on methods only
- research-problem truth on methods only via `targets_task`
- application-context truth in `applied_in`
- scenario-level task summarization in page fields/prose only

## Error handling and governance implications
- If a candidate node names a research objective, it should not be upgraded to Scenario simply because it is commonly used in an application setting.
- If a paper mentions an application context but the method is the real reusable unit, the formal edge should land on the method, not on the paper.
- If a paper discusses concepts or tasks, that may support method-level `uses_concept` / `targets_task` edges, but should not be projected as paper-level formal edges.
- If evidence only supports “this paper studies task X” but not “method Y targets task X,” then `targets_task` should not be fabricated.
- If evidence only supports “this paper mentions scenario Z” but not “method Y is applied in scenario Z,” then `applied_in` should not be fabricated.
- Semantic review should flag `Paper -> Scenario`, `Paper -> Concept`, and `Paper -> Task` attempts as ontology errors.

## Testing and verification
This task does not add programmatic lint checks, but implementation should still verify:
- the new relation contract is represented consistently in `graph-standard.md` and `ontology/relations/applied_in.md`
- `uses_concept.md` and `targets_task.md` are updated to Method-only source legality
- the corrected Scenario page no longer reads like a task cluster
- the updated method page(s) use `applied_in` consistently
- no paper page still projects `uses_concept` or `targets_task` formal edges
- skill prompts encode the same classification rule as the ontology contract

## Open choices already resolved
- Add Scenario formal relation? Yes.
- Which relation? `Method -> Scenario` only.
- Allow `Paper -> Scenario`? No.
- Keep `Paper` as `uses_concept` source? No.
- Keep `Paper` as `targets_task` source? No.
- Add `Scenario -> Task` now? No.
- Add lint enforcement now? No.
