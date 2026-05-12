# references_method paper path fields design

## 背景

当前 [ontology/relations/references_method.md](ontology/relations/references_method.md) 的实例边仅记录：

- `source_path`
- `target_path`
- `edge_semantics`
- `evidence`
- `evidence_link`
- `evidence_path`

这足以表达方法到方法的弱参照关系，但还不能显式回答两个 paper 级 provenance 问题：

1. 这条 `references_method` 实例边是从哪篇 source paper 中抽取出来的。
2. 该 `references_method` 的 target method 对应的代表 / 参考论文是哪篇 paper。

用户已确认：不新增 `source_paper` / `target_paper` 文本或 wikilink 字段，而是新增路径字段，以保持 ledger child fields 的可校验路径风格一致性。

## 目标

为 `references_method` 实例边新增两个必填子字段：

- `source_paper_path`
- `target_paper_path`

并同步更新：

- [ontology/relations/references_method.md](ontology/relations/references_method.md) 的实例格式与现有实例边
- [ontology/graph-standard.md](ontology/graph-standard.md) 中对 `references_method` ledger 实例字段的约束说明
- [scripts/lint_graph.py](scripts/lint_graph.py) 中的字段顺序与 path 校验
- [scripts/test_method_relation_pipeline.py](scripts/test_method_relation_pipeline.py) 中的回归测试
- [relation-reconciliation/SKILL.md](.claude/skills/relation-reconciliation/SKILL.md) 及其 eval/regression contract
- 相关 projection / reconciliation 质量清单中对 canonical ledger child fields 的描述

## 设计决策

### 1. 新字段定义

在每条 `references_method` 实例边中新增：

- `source_paper_path`: 该 `references_method` 实例边所抽取自的 source paper 路径
- `target_paper_path`: 该 `references_method` 的 target method 所对应的代表 / 参考论文路径

字段值统一为 `ontology/entities/papers/*.md` 的 vault 相对路径。

示例：

```md
- [[PathMind]] --references_method--> [[GNN-RAG]]
  - source_path: ontology/entities/methods/PathMind.md
  - target_path: ontology/entities/methods/GNN-RAG.md
  - source_paper_path: ontology/entities/papers/PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.md
  - target_paper_path: ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - evidence: PathMind.refs
  - evidence_link: [[PathMind.refs]]
  - evidence_path: ontology/entities/evidence/PathMind.refs.md
```

### 2. 为什么采用 path 字段而不是 paper wikilink 字段

采用 path 字段而不是 `source_paper` / `target_paper`，原因是：

- 与现有 `source_path` / `target_path` / `evidence_path` 风格一致。
- 更适合作为 ledger 真源，便于 lint 做强约束检查。
- 避免同时维护“展示名”和“真实路径”两份信息导致漂移。
- projection 层若未来需要展示 paper wikilink，可由 path 派生，而不必把展示格式写死在 ledger 中。

### 3. 字段顺序

`references_method` 实例边子字段顺序调整为：

1. `source_path`
2. `target_path`
3. `source_paper_path`
4. `target_paper_path`
5. `edge_semantics`
6. `evidence`
7. `evidence_link`
8. `evidence_path`

这样可以保持：对象路径 → 论文路径 → 语义 → 证据 的信息组织顺序。

### 4. 校验规则

`lint_graph.py` 需要对 `references_method` 实例边额外施加以下约束：

- 必须包含 `source_paper_path` 与 `target_paper_path`
- 两个字段都必须以 `ontology/entities/papers/` 开头并以 `.md` 结尾
- 两个路径都必须实际存在
- `source_paper_path` 与 `target_paper_path` 指向的对象页都必须是 Paper 页

本次不要求 lint 在 `references_method` 级别进一步验证：

- `source_paper_path` 是否一定提出 `source_path` 对应的 source method
- `target_paper_path` 是否一定提出 `target_path` 对应的 target method

这些更强的语义一致性可以留待后续单独增强；本次先保证 ledger 字段合同明确、结构可校验。

### 5. graph-standard 与 skill 更新范围

[ontology/graph-standard.md](ontology/graph-standard.md) 需要补充 `references_method` ledger 实例边的字段合同，明确：

- `references_method` 除方法对象路径外，还必须登记抽取来源论文路径与 target method 对应论文路径
- 这两个字段属于 provenance / paper-level anchoring，不改变 `references_method` 仍然是 `Method -> Method` formal relation 的本体语义

同时需要把这次 schema 变更落到 skill 合同中，而不只停留在规范和脚本层：

- [relation-reconciliation/SKILL.md](.claude/skills/relation-reconciliation/SKILL.md) 的 canonical ledger rendering 规则，需要把 `source_paper_path` / `target_paper_path` 纳入 `references_method` 实例边的 canonical child-field contract
- [relation-reconciliation/evals/regression-samples.json](.claude/skills/relation-reconciliation/evals/regression-samples.json) 中关于 canonical child-field 顺序的断言，需要同步更新
- 若 projection 侧质量清单显式描述 canonical ledger child fields，也要同步改成包含这两个新字段，避免 skill 说明与 ledger 真源脱节

本次不要求 [page-projection-sync/SKILL.md](.claude/skills/page-projection-sync/SKILL.md) 消费或展示这两个 paper path；它仍然只消费 formal relation truth 做对象页投影。但如果它的 checklist 或说明显式枚举 canonical ledger child fields，则必须同步改口径。

### 6. 测试策略

[scripts/test_method_relation_pipeline.py](scripts/test_method_relation_pipeline.py) 需要至少覆盖：

- 文档与样例中出现 `source_paper_path` / `target_paper_path`
- PathMind 现有 `references_method` 实例边包含新字段
- lint 在合法数据下继续通过
- relation-reconciliation skill / regression samples 的 canonical child-field contract 已同步更新
- 若后续已有专门的 relation child field 顺序断言，则同步更新期望顺序

本次如果现有测试框架里没有针对缺失 `source_paper_path` / `target_paper_path` 的负例测试入口，可以只先补文档回归与现有正例回归，避免为这次小 schema 变更引入过多额外测试样板。

## 非目标

本次不做以下事项：

- 不新增 `source_paper` / `target_paper` wikilink 字段
- 不修改 `references_method` 的本体方向，仍保持 `Method -> Method`
- 不把 paper 链接展示格式直接写入 relation ledger child fields
- 不扩展到 `based_on`、`evaluated_on` 或其他 relation ledger 的 paper-path 字段
- 不修改 page projection 模板来展示这两个 paper path，除非后续用户单独要求

## 实施影响

这是一次局部 schema 增强，影响面集中在：

- `references_method` ledger 文档与实例数据
- graph standard 文档说明
- relation-reconciliation skill 的 canonical ledger rendering 合同与回归样例
- projection / reconciliation 质量清单里对 canonical child fields 的表述
- lint 的 relation child field 合同
- 方法关系流水线回归测试

它不会改变现有 formal relation 类型集合，也不会改变对象页 `Formal relations` 的拓扑语义，只是为 `references_method` 增加更完整的 paper 级 provenance 锚点。
