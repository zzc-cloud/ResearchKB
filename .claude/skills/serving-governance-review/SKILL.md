---
name: serving-governance-review
description: 在 ResearchKB 中，对已经完成结构 lint 与本体语义审查后的对象页、Evidence 页、以及 `ontology/entities/*/index.md` 等受管导航页做 serving 治理审查。Whenever 编排型 skill `process-paper` 已将当前任务推进到 serving governance review 阶段，或用户明确要求只做 serving 治理审查、判断某批迁移页面 / 对象页投影 / 领域 index / default QA surface 是否已经 `serving-ready` 时，都应使用本 skill。默认由 `process-paper` 在结构 lint 与 ontology semantic review 之后调用；它只负责 serving surface 的质量门，不重复做 lint，也不重复做 ontology-semantic-review。
---

# Serving 治理审查

审查已迁移的知识页面与领域 index 页面，判断它们是否已经可以作为默认的受约束问答 serving surface，以及领域级导航 / 问答 serving surface 来提供服务。

## 在以下场景使用
- 一批 Paper / Method / Task / Scenario / Benchmark / Evidence 页面已经迁移到 serving-layer 模型。
- `ontology/entities/*/index.md` 或其他显式受管的 serving / navigation index 页面发生变更，需要判断这些页面是否适合作为 default navigation surface / default QA surface。
- 需要判断页面或 index 当前应标记为 `serving-ready`、`partial` 还是 `legacy`。
- 结构 lint 与本体语义审查已经执行完毕，或其结果已可用。

## 输入
- git diff、文件列表、目录，或某个迁移批次的描述。

## 需要检查的内容
1. **Serving 完整性**
   - 每个已迁移页面是否都包含 `## Formal relations`、`### Outgoing` 与 `### Incoming`？
   - `### Outgoing` 与 `### Incoming` 下，是否都包含适用于当前页面角色的固定角色说明句？
   - 投影条目是否采用 semi-expanded format，包含 relation type、semantic label、文档路径与可点击 wikilink？
   - 该节点类型要求的一跳关系是否已经具备？
   - Evidence 链接是否存在，并且有助于继续下钻核查？

2. **Serving 可读性对齐**
   - 人类可读区块是否与 formal projection 保持一致？
   - 是否存在会让读者或 LLM 相对 formal edges 产生误导的 prose？
   - relation 页可以更偏机器友好，但对象页的 serving projection 不得被 relation ledger 中 path-rich 的子项污染。
   - 投影的 `edge_semantics` 是否完整保留 relation instance 的成立语义，而不是把多个实例压扁成对象级摘要？
   - index 入口项中的 `object_semantics` 是否准确表达对象实例身份，而不是退化回自由 trailing prose？

3. **问答可遍历性**
   - LLM 能否直接从页面识别下一跳节点与关系类型？
   - 每个投影邻居是否都显式暴露其 document path？
   - 页面正文中的 wikilink 是否始终限制在已投影 formal neighbor set 内？
   - 是否缺少关键邻居，导致运行时必须 fallback 到 `ontology/relations/`？
   - formal neighbor 是否仍然停留在合格的默认 serving surface 上，或者虽为 `partial` / `placeholder` 但已被 graph-standard 允许并按 index 状态正确暴露，而不是仅仅“存在即可解析”？
   - `references_method` 属于正式可遍历邻接，但不应被解释为谱系继承或父方法链。
  - `Paper Stub / Anchor` 属于可合法遍历但非 default paper serving surface 的规范允许中间态。
  - 若某 Method / Evidence / Paper 页的关键 formal 邻居是 Paper Stub / Anchor，只要遍历链完整、状态暴露正确且未被错误提升为默认入口，不应仅因其不是 Formal Paper 就判为 serving 失败。

4. **Index 导航质量**
   - `ontology/entities/*/index.md` 与其他显式受管的 serving / navigation index 页面，是否暴露了正确的默认入口层？
   - 是否把 stub / placeholder / 结构不完整的页面错误提升成 default entry？
   - index 的分组与标签是否与页面实际状态一致？
   - 读者或 LLM 是否能够从 domain index pages → object page → Formal relations → adjacent object / Evidence page 顺畅遍历，而不需要 hidden fallback？
   - 如果某个页面只是“已被索引”但尚未适合作为 default navigation/QA entry surfaces / default QA serving surface，是否被明确区分，而不是混入默认 serving 层？
   - 若某些 `partial` / `placeholder` 邻居是当前规范允许的合法稳态，它们是否被准确暴露为中间状态，而不是被误报成默认 serving 缺陷？
   - 必须识别 survey-derived serving path：source survey Paper → partial Method → Evidence，以及 source survey Paper → representative paper stub / anchor。
   - 若该链路的 formal/evidence 遍历完整、paper stub 状态暴露正确且未被误升为默认入口，则应判为合法 serving path，而不是自动降级。
   - 若 survey-derived partial `Method` 已被 default expose，但缺少 representative paper human-readable anchor 或关键 Evidence next-hop，则应至少判为 `needs_fixes`。

5. **Relation ledger 与 serving 的边界**
   - relation 页面是否仍然保持为面向治理的 truth surface，而不是默认 serving 入口页？
   - 对象页是否仍然是主要的人类可读 serving surface？
   - relation-ledger 中偏机器字段的表达，是否避免污染对象页的 serving 可读性？

6. **发布就绪性**
   - 当前页面或批次是否可以安全提升为 default QA serving surface？
   - domain index 页面或其他显式受管导航面，是否可以安全提升为 default navigation / QA serving surface？

## 输出状态
- `pass`：serving-ready
- `needs_fixes`：结构或语义上基本可用，但还不能作为默认 serving surface
- `blocked`：不应被提升为 serving-ready
- 若当前页结构完整、formal relation 完整，而关键邻居虽然主要是 semantic stub / `partial` / `placeholder` 页，但这些邻居本身属于 graph-standard 允许的当前规范中间稳态、index 分层正确、formal/evidence 遍历链完整且不会误导默认问答，则仍可判为 `pass`，而不是自动降为 `needs_fixes`。
- 只有当关键邻居被错误提升为默认入口、缺少该状态所需的最小合同结构、formal/evidence 遍历链断裂，或页面虽然可解析但必须依赖 hidden fallback 才能完成关键下一跳理解时，才应因邻居状态问题降为 `needs_fixes` 或 `blocked`。

## 约束
- 不要重复做结构 lint。
- 不要重复做 ontology-semantic-review。
- 只聚焦于 serving surface 独有的质量门。
- “已索引但非 default-serving” 是合法的中间状态：页面可以被发现，但尚不适合暴露为默认 QA surface。
