# Survey-Derived Method Task/Scenario Relation Design

## Context
ResearchKB now treats `Method` as the central reusable technical object in the phase-1 ontology. A paper may connect to methods through:
- `proposes` when it first introduces a method
- `surveys_method` when it systematically covers an existing method in a survey, landscape, or taxonomy role

Methods already carry the main operational graph semantics:
- `targets_task` for research-task orientation
- `applied_in` for application-scenario orientation

The user’s clarified question is whether a method extracted from a survey paper should retain those same method-level relations, and whether phase 1 should additionally create direct formal relations between `Task` and `Scenario` when both are extracted from the same paper.

## Goal
Clarify phase-1 ontology policy so that survey-derived methods can still formally connect to `Task` and `Scenario`, while deciding whether `Task <-> Scenario` should become a direct formal relation family.

## Non-goals
- Do not redesign the general phase-1 entity model.
- Do not add new direct formal relations between `Task` and `Scenario` in this change unless explicitly justified.
- Do not introduce any second-phase abstraction layer.

## Design decisions

### 1. Survey-derived methods should retain full method-level relation capability
A `Method` extracted from a survey paper should be eligible for the same method-level formal relations as a method extracted from an ordinary method paper.

That means a survey-derived method may still have:
- `[[Method]] --targets_task--> [[Task]]`
- `[[Method]] --applied_in--> [[Scenario]]`

provided that:
- the method identity is stable
- the survey provides structured, auditable evidence for the method’s task or scenario assignment

Rationale:
- Once an object is accepted as a `Method`, its ontology behavior should not depend on whether it was surfaced via `proposes` or `surveys_method`.
- Survey papers often provide more systematic task and scenario grouping than individual method papers.
- Refusing to let survey-derived methods carry these relations would artificially weaken the method graph.

### 2. Paper type should not change Method relation eligibility
Phase 1 should separate two questions:
1. **How did the method enter the graph?**
   - `proposes`
   - `surveys_method`
2. **What formal relations does the method itself support?**
   - `targets_task`
   - `applied_in`
   - `evaluated_on`
   - `based_on`
   - `references_method`
   - `supported_by`

The entry relation determines provenance of graph admission, not downstream relation rights.

Rationale:
- Otherwise the same technical object would behave differently purely because of its source-paper role.
- That would make the ontology internally inconsistent.

### 3. Use stricter evidence thresholds for survey-derived task/scenario edges
Allowing survey-derived methods to connect to tasks and scenarios does not mean every survey mention should generate those edges.

#### `targets_task` from survey coverage
Allow when the survey:
- explicitly groups the method under a task family
- places the method in a task taxonomy/table
- discusses the method as a representative solution for a named task class

Do not allow when:
- the task is only loosely inferred from surrounding prose
- the survey merely cites the original paper without assigning the method to a task grouping

#### `applied_in` from survey coverage
Allow when the survey:
- explicitly classifies the method under an application scenario or domain-use bucket
- uses a structured scenario grouping, comparison table, or scenario subsection
- clearly states the method is applied in that scenario, not merely relevant to it

Do not allow when:
- the scenario is only background context
- the paper’s benchmark domain is mistaken for application scenario
- the survey speculates about possible downstream use without structured coverage

Rationale:
- Survey papers are excellent for structured grouping, but also easy places to over-generalize.
- The right response is stronger evidence gating, not weaker ontology expressivity.

### 4. Do NOT add direct Task↔Scenario formal relations in phase 1
Even if the same paper yields both Task and Scenario nodes, phase 1 should not introduce a direct formal relation family between them.

Examples that should NOT be formalized now:
- `[[Task]] --applied_in--> [[Scenario]]`
- `[[Scenario]] --hosts_task--> [[Task]]`
- `[[Task]] --common_in--> [[Scenario]]`

Rationale:
- `Task` answers “what problem is being solved?”
- `Scenario` answers “in what application context is it used?”
- Their connection is usually mediated by one or more methods, not a universal direct semantic fact
- A direct Task↔Scenario edge would flatten a many-to-many, method-dependent relationship into a static claim
- This would increase relation count rapidly and make the graph more brittle and less precise

### 5. Let Method remain the bridge between Task and Scenario
The intended phase-1 structure should be:
- `Paper --proposes--> Method`
- `Paper --surveys_method--> Method`
- `Method --targets_task--> Task`
- `Method --applied_in--> Scenario`

This preserves a clean mediated structure:
- tasks and scenarios are related because concrete methods connect them
- not because the ontology asserts a generic direct edge between those node types

Rationale:
- This is more faithful to how research knowledge is actually established.
- It also supports constrained traversal: from a task, you can discover relevant scenarios by following shared methods, and vice versa.

## Consequences

### Positive
- Survey papers can enrich the method graph beyond citation structure.
- Methods surfaced from surveys do not become second-class objects.
- Task and scenario semantics remain distinct.
- The graph stays method-centered rather than drifting into coarse task-scenario coupling.

### Accepted trade-off
- Users cannot directly ask the graph for a first-class Task↔Scenario edge family in phase 1.
- Traversal between Task and Scenario will remain mediated through methods.
- This is intentional, because the mediated structure is more semantically faithful.

## Files and system areas affected

### Ontology contract
Update `ontology/graph-standard.md` to explicitly state:
- survey-derived methods may still receive `targets_task` and `applied_in`
- source-paper role does not weaken a Method’s downstream formal relation eligibility
- Task↔Scenario remains non-formal in phase 1

### Survey-method relation spec interaction
Ensure `surveys_method` guidance is consistent with:
- survey-derived methods can still project to tasks and scenarios when evidence is strong
- `surveys_method` is only the admission/coverage relation, not the only relation survey-derived methods are allowed to have

### Ingest and governance skills
Update relevant skills so they:
- allow survey-derived methods to emit `targets_task` and `applied_in`
- use stronger evidence thresholds for those edges in surveys
- explicitly reject direct Task↔Scenario formal-edge creation in phase 1

## Verification expectations
Implementation should verify that:
- survey-derived methods are not artificially blocked from `targets_task` and `applied_in`
- candidate generation distinguishes strong structured survey coverage from weak mention
- no new direct Task↔Scenario formal relation family is introduced
- task/scenario traversal remains mediated by methods

## Scope boundary
This design changes only the interpretation of survey-derived method relations in phase 1.
It does not add a new Task↔Scenario edge family and does not redesign the broader ontology.