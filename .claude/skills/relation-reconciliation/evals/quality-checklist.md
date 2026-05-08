# Relation Reconciliation Quality Checklist

## Input handling
- [ ] Reads `relation_candidates` and `relation_exemptions` from ingest output.
- [ ] Reads affected object pages, evidence caches, and current relation ledgers.

## Reconciliation logic
- [ ] Distinguishes `already_present`, `add_now`, `exempt`, and `needs_human_review`.
- [ ] Routes each relation type to the correct `ontology/relations/*.md` file.
- [ ] Detects prose-ledger drift when a page implies a relation that is missing from the formal ledger.

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists affected pages for downstream page-projection sync.
- [ ] Does not silently drop ambiguous edges.
- [ ] 不会把 `Paper` 作为 `supported_by` source 落入正式 ledger。
- [ ] 识别 formal relation 实例时以 `relation_type + source + target` 为唯一实例身份。
- [ ] 不会引入 Evidence 与 Paper 之间的新 formal relation。
- [ ] relation 页固定包含“关系语义说明区”和“实例边账本区”。
- [ ] 正式 relation instance 语义字段统一为 `edge_semantics`，不得继续输出 `reason`。
- [ ] 输出的 evidence 仍必须保留，并与 `edge_semantics` 共同构成可投影的实例语义。
- [ ] 实例边子项固定为 `source_path` → `target_path` → `edge_semantics` → `evidence` → `evidence_link` → `evidence_path`。
- [ ] relation 页除主行 `source` / `target` 与 `evidence_link` 外，不出现其他 wikilink。
- [ ] basename 不唯一时，`source` / `target` / `evidence_link` 自动退化为带路径的 wikilink。
