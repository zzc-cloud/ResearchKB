---
title: Paper stub and method anchor design
tags:
  - design
  - ontology
  - paper
  - method
  - references_method
  - cites
---

# Paper stub and method anchor design

日期：2026-05-12

## 1. 背景

当前 ResearchKB 已经允许从 source paper 的 related-work / reference evidence 中，抽取：

- `Paper --cites--> Paper`
- `Method --references_method--> Method`
- 以及由此派生的一批 partial `Method` 与 placeholder `Paper`

以 PathMind 为例，当前已经存在：

- [ontology/relations/references_method.md](../../ontology/relations/references_method.md) 中的 `PathMind -> RoG/GNN-RAG/GCR/EPERM/ToG` 方法参照边
- [ontology/relations/cites.md](../../ontology/relations/cites.md) 中的对应 paper citation 边
- [ontology/entities/methods/](../../ontology/entities/methods/) 下由这些关系支撑的 partial method 页面
- [ontology/entities/papers/](../../ontology/entities/papers/) 下被创建出来的 cited-work placeholder paper 页面

这套结构已经能支持方法层的弱参照建模，但还存在一个本体分层问题：

1. `Method` 与 `Paper` 不必一一对应，这一点已确认。
2. `references_method` 与 `cites` 也不必一一对应，这一点也已确认。
3. 但它们至少必须存在可审计的对应关系，否则：
   - `Method` 可能成为无来源锚点的漂浮节点；
   - `Paper` 可能只是为了凑 relation target 而无约束膨胀。
4. 如果进一步要求“正式 Paper 必须有独立 ontology 产出”，那么当前这些仅由 citation 触发生成的 placeholder paper 不能再与 Formal Paper 混为一谈。

因此，本设计要解决的核心问题不是“要不要保留这些节点”，而是：

> **如何在不要求一一对应的前提下，让 Method 与 Paper、references_method 与 cites 之间保持最小但硬性的回挂关系，同时避免 Paper 层冗余膨胀。**

## 2. 设计目标

本设计收敛以下目标：

1. `Method` 不要求和 `Paper` 一一对应，但每个 `Method` 必须至少能回挂到某个 paper anchor。
2. `references_method` 不要求和 `cites` 一一对应，但凡 `references_method` 声明了 paper path provenance，就必须能回挂到对应 `cites`。
3. `Paper` 不再只有一种语义状态，而要区分：
   - 正式对象层中的 Formal Paper
   - 仅用于 relation/provenance 锚定的 Paper Stub / Anchor
4. 仅因被引用而创建出来的 cited-work paper，不应自动视为正式 Paper。
5. 现有由 PathMind 等 source paper 抽取出来的 partial `Method` 必须仍然能够合法成立，而不因为提高 Formal Paper 门槛而整体失效。

## 3. 核心设计

## 3.1 Paper 分层

### A. Formal Paper

Formal Paper 指正式对象层中的 `Paper` 节点，满足：

- 该 paper 自身产出至少一种稳定 ontology payload；
- 可以作为默认对象层 serving surface 的正式入口；
- 可以进入默认问答入口与对象域 index 的正式主链。

稳定 ontology payload 的例子包括但不限于：

- `[[Paper]] --proposes--> [[Method]]`
- `[[Paper]] --surveys_method--> [[Method]]`
- 稳定产出可治理的 Evidence 对象页，或稳定支撑 phase-legal formal object extraction

仅有 citation target 身份，不足以让某篇 paper 成为 Formal Paper。

### B. Paper Stub / Anchor

Paper Stub / Anchor 指仅用于 relation 与 provenance 锚定的 paper 页面，满足：

- 可以由 `cites`、`references_method.target_paper_path` 等需求触发生成；
- 其主要职责是作为：
  - `cites` target
  - `references_method` 的 paper-level provenance 锚点
  - future ingest 的稳定升级落点
- 不算正式 `Paper`；
- 不进入默认 serving surface；
- 不作为默认问答首入口。

这类页面可以继续使用最小骨架，但在本体语义上应重新理解为 **Paper Stub / Anchor**，而不是“已经正式入图的 Paper”。

## 3.2 Method 的最低锚点规则

`Method` 不要求和 `Paper` 一一对应，但每个 formal / partial `Method` 都必须至少能回挂到一个 paper anchor。

允许的锚点来源包括：

- incoming `proposes`
- `references_method` 中的 `source_paper_path` / `target_paper_path`
- `surveys_method` 或其他稳定 coverage provenance

因此：

- `Method` 不必一定有“独立提出它的 source paper”才成立；
- 但不能成为无 paper provenance 的孤立方法节点。

## 3.3 `references_method` 与 `cites` 的最小硬约束

### `references_method`

- formal 语义仍然是 `Method -> Method`
- `source_paper_path` / `target_paper_path` 只是 paper-level provenance
- 这两个字段不改变其 formal relation 类型，不把它变成 `Paper -> Paper`

### `cites`

- formal 语义仍然是 `Paper -> Paper`
- 不新增 `references_method_path` 或类似镜像字段
- `cites` 保持 paper-level truth 的独立 relation 身份

### 二者之间的硬回挂规则

若一条 `references_method` 实例边同时声明：

- `source_paper_path = P1`
- `target_paper_path = P2`

则 formal ledger 中必须存在：

- `[[P1]] --cites--> [[P2]]`

否则：

- 该 `references_method` 不应视为 fully valid formal edge；
- 至少应进入 `needs-human-review`；
- 不允许把没有 paper citation 回挂的 method reference 直接当作正式稳定 truth。

反向不成立：

- 有 `cites`，不等于必须存在 `references_method`
- `cites` 与 `references_method` 不是镜像账本

## 3.4 抽取状态机

### A. 允许抽出 Paper Stub

当 source paper 中存在稳定 `cites`，且 target paper 被 formal relation provenance 所需要时，可以生成 target paper stub。

典型场景：

- source paper 引用了某 target paper
- 同时 source paper 还把该 target paper 对应的方法稳定提炼为 `references_method` target
- 此时 target paper 需要有一个可解析、可复用、未来可升级的 paper anchor

### B. 允许抽出 partial Method

当 target method 同时满足：

- 具有可命名、可复用的稳定方法语义
- 存在 method-level formal relation（如 `references_method`）
- 且能回挂到 target paper stub / anchor

则允许从 source paper 中把它 materialize 为 partial `Method`。

这解释了为什么当前由 PathMind 抽取出来的：

- RoG
- GNN-RAG
- GCR
- EPERM
- ToG

仍然可以合法成立：

- 它们有稳定方法语义
- 有 `references_method`
- 有对应 `cites`
- 有 target paper anchor

### C. 升级为 Formal Paper

只有当 target paper 自身产出稳定 ontology payload 时，才从 Paper Stub 升级为 Formal Paper。

升级后应满足：

- 仍保留同一页面路径
- 不改已有 `cites` / `references_method` 的锚点路径
- 不创建重复的第二个 paper 页面

### D. 不允许的情况

若只是普通 related-work mention：

- 可以保留在 `cites`
- 必要时可以建 paper stub
- 但不得自动 materialize 为 partial `Method`
- 也不得自动升级为 Formal Paper

换言之：

- citation relevance 不等于 method-level stable identity
- citation presence 也不等于 formal-paper-worthiness

## 4. 治理与 serving 规则

## 4.1 治理规则

### A. `references_method` 的 paper 回挂一致性

对每条带有：

- `source_paper_path`
- `target_paper_path`

的 `references_method` 实例边，治理时必须检查：

1. 两个 path 都可解析到 paper 页面；
2. `cites` ledger 中存在 `P1 --cites--> P2`；
3. 若任一条件不成立，则该 relation 至少进入 `needs-human-review`。

### B. partial Method 的合法依赖

partial `Method` 可以依赖：

- source paper 的 evidence
- `references_method`
- `cites`
- target paper stub

也就是说：

- partial `Method` 的成立不要求 target paper 已升级为 Formal Paper
- 只要求它有足够稳定的 method identity 与 provenance 回挂

### C. Stub 的升级路径

未来若目标论文被单独 ingest，且其自身满足 Formal Paper 条件，则：

- 该 stub 应在原路径上升级；
- 已有 relation ledger、projection、method anchor 都继续复用；
- 不应另建重复页面。

## 4.2 serving 规则

### Paper Stub / Anchor

- 不进入默认 `papers/index` 的正式主 serving 列表
- 不作为默认问答首入口
- 可以被 relation、evidence、对象页 formal projection 引用

### Formal Paper

- 才能进入默认对象层 serving surface
- 才能作为正式知识入口参与默认问答导航

这意味着：

- 当前很多 `status: placeholder` cited-work 页面仍可以保留；
- 但它们的语义要从“尚未补完的正式 Paper”改判为“Paper Stub / Anchor”。

## 5. 对当前 PathMind 相关页面的影响

### 5.1 现有 partial Method 继续成立

当前这些 partial Method：

- [RoG](../../ontology/entities/methods/RoG.md)
- [GNN-RAG](../../ontology/entities/methods/GNN-RAG.md)
- [GCR](../../ontology/entities/methods/GCR.md)
- [EPERM](../../ontology/entities/methods/EPERM.md)
- [ToG](../../ontology/entities/methods/ToG.md)

在本设计下仍然成立，因为它们满足：

- 稳定方法语义
- `references_method` formal edge
- 对应 `cites`
- target paper anchor

### 5.2 现有 cited-work placeholder paper 的语义重解释

当前这批由 PathMind 引出的 cited-work paper 页面，不应再被当作 Formal Paper，而应重解释为 Paper Stub / Anchor。

这包括但不限于：

- [Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning](../../ontology/entities/papers/Reasoning%20on%20Graphs%20-%20Faithful%20and%20Interpretable%20Large%20Language%20Model%20Reasoning.md)
- [Gnn-rag - Graph neural retrieval for efficient large language model reasoning on knowledge graphs](../../ontology/entities/papers/Gnn-rag%20-%20Graph%20neural%20retrieval%20for%20efficient%20large%20language%20model%20reasoning%20on%20knowledge%20graphs.md)
- [Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models](../../ontology/entities/papers/Graph-constrained%20reasoning%20-%20Faithful%20reasoning%20on%20knowledge%20graphs%20with%20language%20models.md)
- [An Evidence Path Enhanced Reasoning Model for Knowledge Graph Question Answering](../../ontology/entities/papers/An%20Evidence%20Path%20Enhanced%20Reasoning%20Model%20for%20Knowledge%20Graph%20Question%20Answering.md)
- [Think-on-Graph - Deep and responsible reasoning of large language model on knowledge graph](../../ontology/entities/papers/Think-on-Graph%20-%20Deep%20and%20responsible%20reasoning%20of%20large%20language%20model%20on%20knowledge%20graph.md)

其中部分页面未来可能升级为 Formal Paper，但当前不应因为“已存在页面”而默认视为正式对象层节点。

## 6. 规范落点建议

本设计后续若进入实现，应主要落到以下规范点：

1. [ontology/graph-standard.md](../../ontology/graph-standard.md)
   - 明确 Formal Paper 与 Paper Stub / Anchor 的分层语义
   - 明确 `Method` 的最低 paper-anchor 规则
   - 明确 `references_method` 需要可回挂 `cites`

2. [ontology/relations/references_method.md](../../ontology/relations/references_method.md)
   - 保持 `source_paper_path` / `target_paper_path`
   - 后续治理时按新一致性要求校验 `cites`

3. `relation-reconciliation` / `page-projection-sync` / `serving-governance-review`
   - 明确 stub 页面可存在，但不等于 Formal Paper
   - 明确 partial Method 的弱锚点合法性
   - 明确 Formal Paper 的升级门槛

4. `papers/index` 与 serving 层治理
   - 默认主 serving surface 应排除纯 stub 页面
   - 仅把 Formal Paper 作为正式对象入口

## 7. 非目标

本设计不做以下事情：

- 不要求 `Method` 与 `Paper` 一一对应
- 不要求 `references_method` 与 `cites` 一一对应
- 不要求给 `cites` 新增 `references_method_path` 等镜像字段
- 不要求所有 cited paper 立即升级为 Formal Paper
- 不直接重写当前所有 stub 页面模板
- 不扩大到其他 relation type 的 paper-path 设计

## 8. 最终结论

本设计的核心结论是：

1. `Method` 与 `Paper`、`references_method` 与 `cites` 不必一一对应；
2. 但它们必须存在最小、硬性的 provenance 回挂关系；
3. `Paper` 必须分成 Formal Paper 与 Paper Stub / Anchor 两层；
4. 现有由 PathMind 抽出的 partial Method 仍然成立；
5. 现有由 citation 触发创建的 cited-work placeholder paper 应重新理解为 Stub，而不是 Formal Paper；
6. Formal Paper 的门槛应保持更高，只授予真正产出稳定 ontology payload 的 paper。
