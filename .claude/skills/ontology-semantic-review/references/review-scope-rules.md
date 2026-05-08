- 只审查本次变更涉及的节点与关系。
- 不要重述整个本体。
- 默认结构有效性已由 `scripts/lint_graph.py` 先行检查。
- 优先关注如下语义问题：
  - survey 被误写成 task
  - framework 被误写成 method
  - 概念 → 论文支撑关系被错误写进 `uses_concept.md`
  - 文献支撑关系被错误写进 `based_on.md`
  - 本应下沉到 `edge_semantics` / frontmatter / 正文的改进、前提依赖、场景适配或概念性支撑语义，被错误升格为新的 formal relation
  - 节点身份重复或冲突
  - 关系方向与现有约定不一致
  - 节点粒度不匹配（例如把 framework 当原子 concept，或把 scenario 当 task）
  - 同义或近义概念未合并、也未显式区分

## 分类指引
- Paper：论文产物本身
- Method：可复用的技术方法
- Concept：稳定语义单元
- Framework：多层、角色化或阶段化组织结构
- Task：要解决的问题，不是论文类型
- Scenario：行业或应用语境
- Benchmark：数据集或评测目标
- Evidence：证据缓存，不是领域节点

## 判断启发式
- 如果一个节点主要描述的是研究产出形式（survey / benchmark / dataset paper），优先放在 `research_role` 或论文类型里，而不是 `Task`。
- 如果一个节点主要用于组织多个层级、角色或阶段，优先落到 `Framework` / concept 层，而不是 `Method`。
- 如果一条关系表达的是“这篇论文支撑 / 梳理 / 解释了这个概念”，优先放在概念页证据区或 `supported_by.md`，而不是误写进 `uses_concept.md`。
- 如果一条关系表达的是文献借鉴或引用支撑，而不是严格的技术演化谱系，优先放在 `cites.md`，而不是 `based_on.md`。
- 如果一条语义只是说明改进、前提依赖、场景适配或概念性支撑，优先下沉到 `edge_semantics`、frontmatter 或对象页正文，而不是新增 formal relation。

## Formal projection and Evidence serving rules
- `supported_by` 只允许 `Method`、`Concept`、`Task`、`Scenario`、`Benchmark` 作为 source；`Paper` 不得作为 source。
- Evidence 与 Paper 之间不建立 formal relation。
- Evidence 页正文不允许直接链接回 Paper。
- 对象页与 Evidence 页正文中的所有 wikilink，必须已经在该页 `Formal relations` 中出现。

## Relation-ledger semantic explanation rules
- relation semantic explanation must match the relation’s formal ontology contract.
- relation semantic explanation must帮助判断合法 source / target 类型与实例边归属。
- explanation prose may not introduce object-domain navigation expectations.
- semantics that belong in `edge_semantics` must not be promoted into extra formal-edge interpretations.
- relation ledger 的实例语义字段统一为 `edge_semantics`，不得继续使用 `reason` 作为正式实例字段名。
- 对象页 `Formal relations` 必须逐条投影 relation instance 的 `edge_semantics` 与 `evidence`。
- 对象域 index 的入口语义必须来自对象页真源 `object_semantics`，不得回退为自由 prose hook。
