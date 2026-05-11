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
- Method papers should prioritize paper + method + benchmark/scene nodes.
- Survey/framework papers should prioritize paper + method/framework + scenario + evidence/relations.
- Survey papers should not be forced into a single-method template.

## Evidence layer
- Every cache must backlink the formal paper node.
- Caches should include `对应正式知识节点` and `本节支撑 ...` where applicable.
- Evidence references in wiki pages must point to the correct third cache type (`experiments` or `analysis`).

## Relation layer
- Citation graph should reflect important upstream works.
- Method evolution is required for method papers; evidence index and task/scenario coverage are especially important for survey/framework papers.
- Task/task-map updates must not misclassify survey as a technical task.

## Relation autowrite checks
- [ ] 如果论文提出核心方法，输出与落库结果必须包含 `proposes` 正式关系，而不是只在正文里写“提出了某方法”。
- [ ] 如果论文核心贡献是可复用方法框架或面向任务的可复用解决方案，输出与落库结果必须包含 `Paper -> Method` 的 `proposes` 关系。
- [ ] 若论文只提供 taxonomy、术语组织或解释框架而不形成可复用方法，不得在 phase 1 强行创建独立实体。
- [ ] 如果论文是 survey / landscape / taxonomy 角色，并且系统梳理了既有方法，则输出与落库结果必须包含 `surveys_method`，而不是只保留 `cites`。
- [ ] `surveys_method` 不得替代 `proposes`；只有首次提出或正式定义的方法才使用 `proposes`。
- [ ] 普通相关工作提及或单条引用事实，不得被误升格为 `surveys_method`。
- [ ] 如果 empirical / method / application 论文存在明确 benchmark，输出与落库结果必须包含 `evaluated_on` 正式关系。
- [ ] 如果 survey / framework / taxonomy 论文没有统一 benchmark，不能伪造 `evaluated_on`；必须在输出中明确说明“按规范豁免”。
- [ ] 只要生成了任一 Evidence 缓存，就必须同步登记 `sourced_from` provenance 关系。
- [ ] 最终结构化输出必须显式包含 `relation_candidates`，而不是只在正文或关系账本中隐含关系。
- [ ] `relation_candidates` 至少应覆盖：`proposes`、`targets_task`、`evaluated_on`、`applied_in`、`supported_by`、`cites`、`sourced_from`。
- [ ] 若某类关系按规范豁免，最终结构化输出必须显式包含 `relation_exemptions`。
- [ ] 若存在方向、粒度或本体归属歧义，最终结构化输出必须将对应关系放入 `needs-human-review` 语义，而不是静默忽略。
