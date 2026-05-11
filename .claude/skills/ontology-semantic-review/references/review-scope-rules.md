- 只审查本次变更涉及的节点与关系。
- 不要重述整个本体。
- 默认结构有效性已由 `scripts/lint_graph.py` 先行检查。
- 优先关注如下语义问题：
  - survey 被误写成 task
  - framework 被误写成 method
  - 文献支撑关系被错误写进 `based_on.md`
  - 本应下沉到 `edge_semantics` / frontmatter / 正文的改进、前提依赖、场景适配或解释性语义，被错误升格为新的 formal relation
  - 节点身份重复或冲突
  - 关系方向与现有约定不一致
  - 节点粒度不匹配（例如把 framework 当原子方法，或把 scenario 当 task）

## 分类指引
- Paper：论文产物本身
- Method：可复用的技术方法
- Framework：多层、角色化或阶段化组织结构
- Task：要解决的研究问题、推理范式或问答目标
- Scenario：行业、业务、部署或应用语境
- Benchmark：数据集或评测目标
- Evidence：证据缓存，不是领域节点

## 判断启发式
- 如果一个节点主要描述的是研究产出形式（survey / benchmark / dataset paper），优先放在 `research_role` 或论文类型里，而不是 `Task`。
- 如果一个节点主要用于组织多个层级、角色或阶段，且不形成可复用技术流程，则 phase 1 保留在 prose / Evidence 中，而不是单独实体化。
- 如果一个候选项同时像 Task 又像 Scenario，优先判断其是否命名研究目标；若仍有歧义，默认先判 `Task`。
- 如果一条关系表达的是文献借鉴或引用支撑，而不是严格的技术演化谱系，优先放在 `cites.md`，而不是 `based_on.md`。
- 如果一条语义只是说明改进、前提依赖、场景适配或解释性支撑，优先下沉到 `edge_semantics`、frontmatter 或对象页正文，而不是新增 formal relation。
- `targets_task` 只允许 `Method` 作为 source；若论文描述任务定位，应落到 Method formal edge 或保留在 Paper prose / Evidence。
- `applied_in` 只允许 `Method -> Scenario`；`Paper -> Scenario` 不合法。
- `surveys_method` 只允许 `Paper -> Method`，且 source 应承担综述 / landscape / taxonomy 的 survey-role。
- 如果论文只是引用某方法来源论文，而没有形成结构化 coverage，不应生成 `surveys_method`。
- 如果论文首次提出或正式定义某方法，应使用 `proposes`，而不是 `surveys_method`。
- Method 一旦身份稳定，其可拥有的 formal relations 与来源论文类型无关；通过 `surveys_method` 进入图谱的方法，仍可继续拥有 `targets_task` 与 `applied_in`。
- survey-derived `targets_task` / `applied_in` 必须有结构化、可审计的 coverage 证据；不能仅凭背景 mention 或泛化推断生成。
- phase 1 不直接维护 `Task -> Scenario` 或 `Scenario -> Task` formal relation。

## Formal projection and Evidence serving rules
- `supported_by` 只允许 `Method`、`Task`、`Scenario`、`Benchmark` 作为 source；`Paper` 不得作为 source。
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
