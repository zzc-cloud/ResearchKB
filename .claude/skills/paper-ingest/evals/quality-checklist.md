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

## Relation autowrite checks
- [ ] 如果论文提出核心方法，输出与落库结果必须包含 `proposes` 正式关系，而不是只在正文里写“提出了某方法”。
- [ ] 如果论文核心贡献是 framework / taxonomy 型概念，输出与落库结果必须包含 `Paper -> Concept` 的 `proposes` 关系。
- [ ] 如果 empirical / method / application 论文存在明确 benchmark，输出与落库结果必须包含 `evaluated_on` 正式关系。
- [ ] 如果 survey / framework / taxonomy 论文没有统一 benchmark，不能伪造 `evaluated_on`；必须在输出中明确说明“按规范豁免”。
- [ ] 只要生成了任一 Evidence 缓存，就必须同步登记 `sourced_from` provenance 关系。
