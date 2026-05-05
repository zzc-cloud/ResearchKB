# Ontology Index

> 本页是 ResearchKB 的唯一导航入口。先导航，再判定，再下钻。

## 1. 规范与判定入口
- 唯一规范页：[[graph-standard]]
- 所有节点、关系、字段、证据与豁免规则，一律以 [[graph-standard]] 为准。

## 2. 正式关系入口
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[task_method_map]]
- [[evidence_index]]
- [[paper_method_links]]
- [[benchmark_links]]
- [[provenance_links]]

## 3. 正式知识对象域入口
- Papers：[[../papers/index|wiki/papers/index.md]]
- Methods：[[../methods/index|wiki/methods/index.md]]
- Concepts：[[../concepts/index|wiki/concepts/index.md]]
- Tasks：[[../tasks/index|wiki/tasks/index.md]]
- Scenarios：[[../scenarios/index|wiki/scenarios/index.md]]
- Benchmarks：[[../benchmarks/index|wiki/benchmarks/index.md]]

## 4. 按任务进入
- 想做受约束知识问答 → 先进入对应 `wiki/<对象域>/index.md` 锁定正式对象，再读取 serving-ready 对象页，并按 `Formal relations` 扩展；需要证据细节时再下钻对应 Evidence 页
- 想判断节点或关系是否合法 → [[graph-standard]]
- 想看正式对象知识 → 对应对象域 index → 对象页
- 想看治理用正式关系账本 → 对应 `wiki/relations/*.md`
- 想核验证据 → `intermediate/papers/`
- 想生成综述或趋势分析 → `docs/`

## 5. 推荐阅读路径
### 初次进入系统
[[graph-standard]] → 本页 → 对应对象域 index → 代表对象页 → 必要时 Evidence / relation ledger

### 回答知识问题
对象域 index → serving-ready 对象页 → `Formal relations` → 邻接对象页 / Evidence 页 → 必要时 relation ledger

### 治理知识变更
[[graph-standard]] → relation ledger → 变更对象页 / Evidence 页 → 必要时对象域 index 回链

## 6. 说明
- 本页负责导航，不负责规范定义。
- 若导航与规范存在差异，以 [[graph-standard]] 为准。
