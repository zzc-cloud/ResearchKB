
### wiki/methods/ToG.md
**Human-friendly links examined**
- `协同增强式知识图谱推理`
- `知识图谱推理问答`
- `knowledge-graph-reasoning`
- `multi-hop-qa`
- `CWQ`
- `Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation`
- `intermediate/papers/PathMind.refs|PathMind.refs`
- `intermediate/papers/PathMind.experiments|PathMind.experiments`

**already-formalized**
- `协同增强式知识图谱推理` (`based_on`, `improves_on`)
- `knowledge-graph-reasoning` (`targets_task`)
- `multi-hop-qa` (`targets_task`)
- `CWQ` (`evaluated_on`)
- `Think-on-Graph 2.0 - Deep and Faithful Large Language Model Reasoning with Knowledge-guided Retrieval Augmented Generation` (`proposes` incoming)

**should-be-formalized**
- `知识图谱推理问答` likely should be formalized as `ToG --applies_to--> 知识图谱推理问答` if scenario linkage is intended consistently across the migrated method family.
- `kgqa` appears in frontmatter but not in human-friendly sections or `Formal relations`, so it is a metadata/projection inconsistency rather than a direct human-block expansion case.

**context-only**
- `intermediate/papers/PathMind.refs|PathMind.refs`
- `intermediate/papers/PathMind.experiments|PathMind.experiments`

**Conclusion**
- ToG is mostly aligned, with the main expansion candidate being scenario formalization; there is also a separate frontmatter vs projection inconsistency around `kgqa`.

## Relation-type summary

### already-formalized by relation type
- `proposes`:
  - PathMind paper → PathMind
  - survey paper → 复杂产品设计中的LLM-KG协同框架
  - GCR paper → GCR
  - EPERM paper → EPERM
  - ToG paper → ToG
- `targets_task`:
  - PathMind / RoG / GCR / EPERM / ToG and the two representative papers cover the currently migrated task nodes where formal task modeling already exists.
- `evaluated_on`:
  - PathMind family and migrated benchmark pages are already formalized where benchmark relations are supported.
- `uses_concept`:
  - PathMind and survey mainline concept usage is largely already formalized.
- `applies_to`:
  - PathMind, GCR-family scenario links that were explicitly added, and framework → scenario links in the survey mainline.
- `supports`:
  - 重要推理路径 → task/scenario support edges already formalized.
- `cites`:
  - PathMind paper and survey paper citation blocks already map strongly to formal ledger.
- `supported_by`:
  - PathMind and survey paper evidence bindings are already formalized.

### should-be-formalized by relation type
- `applies_to`:
  - strongest pattern; several migrated method pages still describe a primary scenario in human-friendly blocks without a corresponding formal `applies_to` edge.
  - most evident candidates: `RoG`, `EPERM`, `ToG` → `知识图谱推理问答`
- `proposes`:
  - method pages that still name a representative paper in human-friendly blocks but do not yet expose the matching incoming paper→method edge as a formal neighbor (RoG most clearly)
- `uses_concept`:
  - occasional paper-level concept usage may still be under-projected on concept pages, but this is not yet a dominant gap pattern.

### context-only patterns
- broad “相关方法 / 路线” lists on concept pages often contain method names that serve as background/navigation rather than one-hop formal neighbors.
- benchmark pages routinely link task/scenario pages as reading context even though the ontology does not currently define benchmark→task or benchmark→scenario formal edge types.
- evidence and index links (`concept_links`, `evidence_index`, `intermediate/papers/...`) appear in human-friendly blocks as navigation and should remain non-formal.

## Decision recommendations
- The current formal graph appears systematically narrow mainly in `applies_to` for migrated method pages that already state a primary scenario in their human-friendly blocks.
- A secondary but smaller gap exists around paper→method `proposes` visibility on some migrated method pages that are still less completely projected than their siblings.
- Most concept-page “related methods/routes” links should be downgraded to plain-text context links rather than promoted into the formal graph.
- Benchmark-page task/scenario links should remain context-only unless the ontology is explicitly expanded with new benchmark-neighbor relation types.
- If a follow-up formal-relation expansion pass is created, prioritize `applies_to` on migrated method pages first, then review method-page incoming `proposes` coverage for consistency.
