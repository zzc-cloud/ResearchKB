## 关系语义说明
- `evaluated_on` 表示某个正式 Method 在某个正式 benchmark 上进行了评测。
- 合法 source：`Method`。
- 合法 target：`Benchmark`。
- 该关系不再用于 `Paper -> Benchmark`；论文页中的 benchmark 讨论应保留在 prose、Evidence 与 Method 的 formal relation 投影中。

## 实例边
- [[PathMind]] --evaluated_on--> [[WebQSP]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/benchmarks/WebQSP.md
  - edge_semantics: PathMind 在 WebQSP 上进行主要性能、效率与可扩展性评测。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
- [[PathMind]] --evaluated_on--> [[CWQ]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/benchmarks/CWQ.md
  - edge_semantics: PathMind 在 CWQ 上验证复杂多跳推理表现，并展示对复杂问题的优势。
  - evidence: PathMind.experiments
  - evidence_link: [[PathMind.experiments]]
  - evidence_path: ontology/entities/evidence/PathMind.experiments.md
