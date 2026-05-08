# Page Projection Sync Quality Checklist

## Inputs
- [ ] Reads updated formal ledgers.
- [ ] Reads relation-reconciliation output including `affected_pages`.

## Sync behavior
- [ ] Updates `## Formal relations` consistently.
- [ ] Updates strong-consistency frontmatter fields.
- [ ] Updates templated human-readable relation blocks.
- [ ] Does not rewrite interpretive prose.
- [ ] 能从包含 `source_path` / `target_path` / `evidence` / `evidence_link` / `evidence_path` 的 canonical ledger 记录中读取 formal truth。
- [ ] 不依赖 relation 页顶部导航说明或旧的 `edge_semantics + evidence` 简化记录形态。

## Output quality
- [ ] Emits a structured YAML summary.
- [ ] Lists any manual followups that still require human editing.
- [ ] `### Outgoing` 与 `### Incoming` 后都必须包含固定角色语义句。
- [ ] 每条投影边必须使用 `relation_type` + 语义标签 + 文档路径 + wikilink 的半展开格式。
- [ ] 每条对象页投影项都必须包含 `edge_semantics` 与 `evidence`。
- [ ] 同邻接对象的多条 relation instance 不得被静默合并。
- [ ] 正文中的 wikilink 不得超出 `Formal relations` 已投影邻接。
- [ ] Evidence 页正文不允许直接链接回 Paper。
