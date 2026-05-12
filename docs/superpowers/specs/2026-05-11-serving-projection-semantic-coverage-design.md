# serving projection semantic coverage design

## 背景

当前 ResearchKB 的 serving-layer 设计已经区分了：

- `ontology/relations/*.md`：formal relation ledger truth surface
- `ontology/entities/*/*.md`：对象页 serving surface

但当前对象页投影合同仍偏轻量：

- [page-projection-sync/SKILL.md](.claude/skills/page-projection-sync/SKILL.md) 当前只要求对象页 `## Formal relations` 投影 `relation_type`、邻接对象、`edge_semantics`、`evidence`
- 正文的人类可读区块只要求模板化同步，不要求对 `Formal relations` 做显式语义覆盖

这导致两个问题：

1. 对象页 `Formal relations` 仍可能丢失 relation ledger 中对 serving 有意义的 relation-specific 属性。
2. 正文区块常常只是对象级摘要，而不是对 `Formal relations` 的语义覆盖；用户或 LLM 仍需回读 `Formal relations` 才能理解关键关系成立语义。

用户已明确新的目标是：

- 对象页 `## Formal relations` 的 `Outgoing` / `Incoming` 应覆盖 formal relation ledger 的全部**必要属性**。
- 正文的人类可读区块应对 `Formal relations` 做**摘要覆盖**，且其语义不应弱于 `Formal relations`。
- 正文覆盖采用“摘要覆盖”而不是“逐条 instance 镜像”。

## 目标

把新的 serving 合同落到以下层面：

- [ontology/graph-standard.md](ontology/graph-standard.md)
- [.claude/skills/page-projection-sync/SKILL.md](.claude/skills/page-projection-sync/SKILL.md)
- 相关 projection / serving checklist
- 回归测试合同

并明确：

1. 什么叫“formal relation ledger 的全部必要属性”
2. 哪些属性必须进入对象页 `Formal relations`
3. 哪些属性只需要体现在正文摘要区块
4. 如何判定“正文区块语义不弱于 `Formal relations`”

## 设计决策

### 1. 区分三层语义面

新的合同需要明确区分三层：

1. **Ledger truth surface**
   - 位于 `ontology/relations/*.md`
   - 承担最完整的 relation instance 真源职责
   - 可保留 path-rich、治理型字段

2. **Object-page formal projection surface**
   - 位于对象页 `## Formal relations`
   - 承担默认问答的一跳 formal graph 读取面
   - 必须覆盖 relation instance 的全部**serving-necessary attributes**
   - 不要求无差别复制全部 ledger child fields

3. **Human-readable summary surface**
   - 位于正文模板化关系区块
   - 承担面向人类和默认 LLM 阅读的主题化摘要职责
   - 必须覆盖 formal relations 的主语义面，但不逐条镜像 instance

### 2. 定义“全部必要属性”而不是“全部 child fields 原样搬运”

本设计不采用“把 ledger child fields 一字不差搬进对象页”的策略。

改为定义：对象页 `Formal relations` 必须覆盖 relation ledger 的全部**必要属性**（serving-necessary attributes）。

#### 2.1 基础必要属性
所有 relation type 的对象页投影都必须覆盖：

- `relation_type`
- 邻接对象身份（对象名称 + document path + 可点击 wikilink）
- `edge_semantics`
- `evidence`

这些字段构成对象页 formal traversal 的基础最小语义集。

#### 2.2 relation-specific 必要属性
若某 relation ledger 中存在仅靠 `edge_semantics` / `evidence` 无法稳定恢复的、对默认 serving 有意义的 relation-specific 属性，则这些字段必须进入对象页 `Formal relations`。

例如：

- `references_method`
  - `target_paper_path` 属于 relation-specific 必要属性，因为它表达“该 target method 对应哪篇代表 / 参考论文”，对默认比较与方法谱系理解有直接帮助。
  - `source_paper_path` 一般不需要在对象页 `Formal relations` 中重复展开为独立子项，因为当前对象页自身已经提供 source 上下文，且 source object / source paper 可由页面位置恢复。

因此：
- **不是所有 ledger 字段都必须投影为独立子项**
- **但所有对 serving 有独立语义贡献的属性都必须在对象页可见**

### 3. 对象页 `Formal relations` 的新合同

对象页的每条投影 relation instance 应至少包含：

```md
- `relation_type`：关系语义标签（文档：`path/to/object.md`）：[[relative/path/to/object|Display Name]]
  - edge_semantics: ...
  - evidence: [[relative/path/to/evidence|Evidence Name]]
```

当 relation type 存在 relation-specific 必要属性时，必须追加该属性的对象页友好表达。

以 `references_method` 为首个落地例子：

```md
- `references_method`：GNN-RAG（文档：`ontology/entities/methods/GNN-RAG.md`）：[[../methods/GNN-RAG]]
  - edge_semantics: PathMind 将 GNN-RAG 作为 retrieval-augmented 图检索代表方法进行比较。
  - target_paper: Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs（文档：`ontology/entities/papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs.md`）：[[../papers/Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs]]
  - evidence: [[../evidence/PathMind.refs]]
```

这里的关键点是：

- ledger 保留 `target_paper_path`
- 对象页不暴露原始 path 字段名，而是投影为对象页友好的 `target_paper`
- 对象页 serving surface 追求完整语义，不追求机器字段原样复制

### 4. 正文区块采用“摘要覆盖合同”

正文区块不逐条重复 `Formal relations`，而是按主题做摘要覆盖。

#### 4.1 Method 页
对于 Method 页，以下区块承担 formal relation 摘要覆盖：

- `## 方法演化与参照关系`
  - 必须覆盖全部 `based_on` 与 `references_method` 的主题语义
  - 对 `references_method`，至少应体现：比较 / 借鉴 / 路线参照对象，以及该对象为何重要
  - 当 `references_method` 存在 `target_paper` 级必要属性时，摘要区块应至少能让读者知道“该参照对象对应哪篇代表论文”或“该对象来自哪条代表路线”

- `## 代表论文`
  - 必须覆盖 `proposes` / 关键 incoming `proposes`

- `## 应用场景` / `## 相关机制` / `## 与其他方法的对比`
  - 必须承接 formal relation 的高频主题语义，避免读者只能从 `Formal relations` 才知道该方法与哪些任务、benchmark、基线发生正式关系

#### 4.2 Paper 页
对于 Paper 页，以下区块承担 formal relation 摘要覆盖：

- `## 核心方法`
  - 必须覆盖 outgoing `proposes`

- `## 引用了哪些重要工作`
  - 不能只是 paper 标题列表
  - 必须至少按路线 / 角色摘要 formal `cites` 语义，例如“显式 relational path reasoning 代表工作”“retrieval-augmented 图检索代表工作”等

- `## 与知识库其他内容的关联`
  - 应覆盖关键对象邻接与证据锚点，而不是停留在笼统描述

#### 4.3 覆盖判定标准
正文区块被视为“语义不弱于 `Formal relations`”，需要满足：

1. formal relation 涉及的主要语义面（如提出、参照、评测、支撑、关键引用路线）都在正文有落点
2. 读者不需要逐条回读 `Formal relations` 才知道“这页与哪些对象发生了什么类型的核心正式关系”
3. 正文允许做主题聚合，但不得把 formal relation 的关键区分压扁到不可恢复

### 5. graph-standard 更新方向

[ontology/graph-standard.md](ontology/graph-standard.md) 需要新增或重写以下规范点：

1. **对象页 `Formal relations` 覆盖规则**
   - 不再表述为仅投影 `edge_semantics` + `evidence`
   - 改为：对象页必须覆盖 formal relation instance 的全部 serving-necessary attributes

2. **relation-specific projection rule**
   - graph-standard 允许 relation ledger 中的部分 path-rich 字段通过“对象页友好别名”投影，而不是原样字段名
   - 例如 `target_paper_path` → `target_paper`

3. **正文摘要覆盖合同**
   - 明确对象页正文必须对 `Formal relations` 做主题化摘要覆盖
   - 该覆盖是 serving-ready 的组成部分，而不是可选美化项

### 6. page-projection-sync skill 更新方向

[page-projection-sync/SKILL.md](.claude/skills/page-projection-sync/SKILL.md) 需要从“最小 formal truth 投影器”升级为“serving-necessary formal truth 投影器”。

具体更新：

1. **输入合同更新**
   - 不再只消费 `source`、`target`、`relation`、`edge_semantics`、`evidence`
   - 改为消费 canonical relation ledger record 中的 serving-necessary attributes

2. **投影合同更新**
   - 对 relation-specific 必要属性定义对象页投影规则
   - `references_method` 的首批规则：`target_paper_path` 必须投影为对象页友好 `target_paper`

3. **正文同步合同更新**
   - 模板化人类区块不再只要求“相关方法列表”
   - 改为要求摘要覆盖 formal relation 的主题语义
   - 若 formal relation 已投影但正文模板区块未覆盖其主题语义，应输出 `manual_followups` 或直接视为同步不完整

### 7. checklist 与测试合同更新方向

需要同步更新：

- page-projection-sync quality checklist
- serving-governance-review 关注点（若已有固定 checklist / eval）
- `scripts/test_method_relation_pipeline.py`
- 与 projection / reconciliation 相关的 regression samples

测试重点应覆盖：

1. `Formal relations` 包含 relation-specific 必要属性的对象页友好投影
2. 正文模板区块不再只是对象列表，而是带主题语义摘要
3. `references_method` 的 `target_paper_path` 能稳定出现在对象页投影后的语义层中
4. 论文页“引用了哪些重要工作”必须覆盖 `cites` 的主要路线语义，而不只是标题清单

## 非目标

本次设计不做以下事情：

- 不要求正文逐条镜像每个 formal relation instance
- 不要求对象页原样展示所有 ledger child-field 名称
- 不要求 relation ledger 失去其治理真源角色
- 不把对象页升级成第二份 machine-oriented ledger
- 不扩展到 UI 之外的外部 API 输出格式

## 影响范围

若按本设计落地，受影响的核心面包括：

- graph-standard 的对象页 serving 合同
- page-projection-sync skill 的 formal projection 规则
- Method / Paper 页的人类区块模板
- projection / serving 质量门
- regression tests 与相关 eval fixtures

## 结论

推荐采用以下方向：

- **ledger** 保持最完整的治理真源
- **对象页 `Formal relations`** 覆盖 formal relation 的全部 serving-necessary attributes
- **正文人类区块** 对 `Formal relations` 做主题化摘要覆盖，且语义不弱于 formal projection

这样既不会把对象页污染成 machine ledger，也能避免当前“formal relations 信息强、正文摘要弱”的 serving 断层。