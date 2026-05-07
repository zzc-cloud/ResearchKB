> 本页是正式关系账本：维护 `based_on` / `improves_on` 实例边。默认问答优先读取 `wiki/methods/index.md` → 方法页；只有在演化链治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../methods/index|methods/index]]
> 相关证据入口：[[evidence_index]]

## `based_on` / `improves_on` 实例边
- `[[路径导向知识图谱推理]] --based_on--> [[检索增强式知识图谱推理]]`
  - reason: 路径导向路线建立在检索增强式知识图谱推理范式之上。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §2–5
- `[[RoG]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: RoG 采用显式关系推理路径作为核心机制。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[RoG]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过显式生成关系推理路径推进路径导向路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[GCR]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: GCR 采用 grounded reasoning path 路线。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[GCR]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 以 grounded 约束提升推理路径可靠性。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[EPERM]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: EPERM 采用 evidence path 增强路径推理。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §2–4
- `[[EPERM]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过证据路径增强改进路径导向推理。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5
- `[[PathMind]] --based_on--> [[路径导向知识图谱推理]]`
  - reason: PathMind 属于路径导向知识图谱推理路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[PathMind]] --improves_on--> [[路径导向知识图谱推理]]`
  - reason: 通过路径优先化与对齐训练提升路径导向推理质量。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §7.1–7.4
- `[[ToG]] --based_on--> [[协同增强式知识图谱推理]]`
  - reason: ToG 属于协同增强式知识图谱推理路线。
  - evidence: [[intermediate/papers/PathMind.refs|PathMind.refs]] §4
- `[[ToG]] --improves_on--> [[协同增强式知识图谱推理]]`
  - reason: 通过多轮 LLM 交互与迭代搜索推进协同增强路线。
  - evidence: [[intermediate/papers/PathMind.sections|PathMind.sections]] §5

## 说明
- 本页是 `based_on` / `improves_on` 实例边的正式账本。
- 如需保留树形阅读体验，可在实例边之下补充非规范性概览，但不能替代边记录。
