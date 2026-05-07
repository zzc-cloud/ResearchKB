> 本页是正式关系账本：维护 `sourced_from` provenance 实例边。默认问答不以本页作为首入口；只有在 Evidence 来源回溯、治理、修复或真源核对时优先读取本页。
>
> 相关对象域：[[../papers/index|papers/index]]
> 相关证据入口：[[evidence_index]]

## `sourced_from` 实例边
- `[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: sections 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] frontmatter `source_pdf`
- `[[intermediate/papers/PathMind.experiments|PathMind.experiments]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: experiments 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.experiments|PathMind.experiments]] frontmatter `source_pdf`
- `[[intermediate/papers/PathMind.refs|PathMind.refs]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
  - reason: refs 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: sections 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: analysis 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] frontmatter `source_pdf`
- `[[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
  - reason: refs 缓存直接由原始 PDF 解析生成。
  - evidence: [[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] frontmatter `source_pdf`

## 说明
- 本页是 `sourced_from` 实例边的正式账本。
- `sourced_from` 默认记录 Evidence 到 RawSource 的 provenance 关系。
- 正式知识页应优先通过 `supported_by` 连接到 Evidence，而不是直接连接原始 PDF。
