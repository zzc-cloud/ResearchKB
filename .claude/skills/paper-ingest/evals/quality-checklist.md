# Paper Ingest Quality Checklist

## Trigger layer
- The skill should trigger when the user asks to process / ingest / parse /落库 a paper or PDF into ResearchKB.
- The skill should not trigger for plain Q&A, explanation, comparison, or graph queries that do not request persistence.

## Type classification layer
- Determine whether the paper is method / application / survey / benchmark / dataset / taxonomy / framework / mixed.
- The classification must drive cache naming and node placement.

## Cache contract layer
- All papers should create `sections.md`, `refs.md`, and `full.md`.
- Method / application / empirical papers should create `experiments.md`.
- Survey / framework / benchmark / taxonomy / dataset papers should create `analysis.md`.

## Node placement layer
- Method papers should prioritize paper + method + concept + benchmark/scene nodes.
- Survey/framework papers should prioritize paper + concept/framework + scenario + evidence/relations.
- Survey papers should not be forced into a single-method template.

## Evidence layer
- Every cache must backlink the formal paper node.
- Caches should include `对应正式知识节点` and `本节支撑 ...` where applicable.
- Evidence references in wiki pages must point to the correct third cache type (`experiments` or `analysis`).

## Relation layer
- Citation graph should reflect important upstream works.
- Method evolution is required for method papers; concept links and evidence index are especially important for survey/framework papers.
- Task/task-map updates must not misclassify survey as a technical task.

## Final status layer
- `success` only when the structure fits and the main assets are complete.
- `partial` when most assets are built but some mapping remains uncertain.
- `needs-skill-update` when the paper type or structure exceeds stable support.
