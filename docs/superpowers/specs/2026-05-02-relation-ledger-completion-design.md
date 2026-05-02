# ResearchKB 三类关系账本补齐设计

## 日期
2026-05-02

## 背景
当前 [wiki/ontology/graph-standard.md](wiki/ontology/graph-standard.md) 已声明 `proposes`、`evaluated_on`、`sourced_from` 三类关系，但其中 `proposes` 与 `evaluated_on` 仍被标记为“未归属到实例边账本文件”。这导致 ontology 层已承认关系类型，但实例边层没有正式落点；历史 ingest 产物中虽然已有足够语义证据，也没有被稳定转写为正式关系记录。

同时，`sourced_from` 的 provenance 语义已经在 evidence frontmatter 的 `source_pdf` 中存在，但若没有单独账本，来源追溯仍停留在 metadata 层，而不是正式实例边层。

## 目标
一步到位完成最小一致性修复：

1. 为 `proposes`、`evaluated_on`、`sourced_from` 提供正式账本归属。
2. 更新规范，使 `graph-standard.md` 中不再存在“已声明但未归属”的不一致表述。
3. 补齐当前 `raw/` 下两篇已 ingest 论文对应的缺失实例边。
4. 评估 `paper-ingest` 后续处理新论文时是否还会重复漏出同类关系，并加上最小护栏。

## 非目标
- 不重构整个 ontology。
- 不批量回填所有历史论文，只处理当前两篇已 ingest 论文。
- 不把 framework 型 concept 改成 method；保持当前“framework 优先按 concept 落库”的本体策略。
- 不大改 `paper-ingest` skill 本体，除非检查后确认需要最小改动护栏。

## 设计原则
- 规范层、实例边层、检查层一起闭环。
- provenance 与 evidence 支撑分层维护，不混到一个语义层。
- survey / framework 论文保留 benchmark 豁免，不为统一性而伪造 `evaluated_on` 边。
- `proposes` 允许 `Paper -> Method` 与 `Paper -> Concept(framework/taxonomy)` 两种目标类型。

## 文件变更范围
### 1. 规范文件
- `wiki/ontology/graph-standard.md`

### 2. 新增关系账本
- `wiki/relations/paper_method_links.md`：维护 `proposes`
- `wiki/relations/benchmark_links.md`：维护 `evaluated_on`
- `wiki/relations/provenance_links.md`：维护 `sourced_from`

### 3. 现有关系账本同步
- `wiki/relations/evidence_index.md`
  - 改为只维护 `supported_by`
  - 移除其“维护 `sourced_from`”的职责说明

### 4. 导航与检查
- `wiki/index.md`
- `scripts/lint_graph.py`

## 关系归属设计
### `proposes`
归属到 `wiki/relations/paper_method_links.md`

维护范围：
- `[[Paper]] --proposes--> [[Method]]`
- `[[Paper]] --proposes--> [[Concept]]`

这里的 `Concept` 主要用于 framework / taxonomy 型核心知识产物。这样能覆盖：
- PathMind 论文提出 PathMind 方法
- LLM-KG-CPD Survey 提出“复杂产品设计中的LLM-KG协同框架”这一 framework 型 concept

不把 `proposes` 塞进 `method_evolution.md`，因为后者只应维护 `Method -> Method` 的演化谱系。

### `evaluated_on`
归属到 `wiki/relations/benchmark_links.md`

维护范围：
- `[[Paper]] --evaluated_on--> [[Benchmark]]`
- `[[Method]] --evaluated_on--> [[Benchmark]]`

保留豁免：
- survey / framework / taxonomy 论文若无统一 benchmark，不强制补齐该关系。

### `sourced_from`
归属到 `wiki/relations/provenance_links.md`

维护范围：
- `[[Evidence]] --sourced_from--> [[RawSource]]`

不要求：
- `Paper/Method/Concept -> RawSource`

原因：
- `supported_by` 已负责正式知识页到 Evidence 的支撑关系
- `sourced_from` 更适合停留在 provenance 层，表示 Evidence 来源于 raw 文件
- 这样形成清晰链路：正式知识页 -> Evidence -> RawSource

## 本次要补的实例边
### 1. PathMind
#### proposes
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --proposes--> [[PathMind]]`

#### evaluated_on
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[WebQSP]]`
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]] --evaluated_on--> [[CWQ]]`
- `[[PathMind]] --evaluated_on--> [[WebQSP]]`
- `[[PathMind]] --evaluated_on--> [[CWQ]]`

#### sourced_from
- `[[intermediate/papers/PathMind.sections|PathMind.sections]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
- `[[intermediate/papers/PathMind.experiments|PathMind.experiments]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
- `[[intermediate/papers/PathMind.refs|PathMind.refs]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`
- `[[intermediate/papers/PathMind.full|PathMind.full]] --sourced_from--> [[raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf]]`

### 2. LLM-KG-CPD Survey
#### proposes
- `[[A survey of large language model-augmented knowledge graphs for advanced complex product design]] --proposes--> [[复杂产品设计中的LLM-KG协同框架]]`

#### evaluated_on
- 不补
- 原因：该论文为 survey / framework 型论文，无统一 benchmark，按规范豁免

#### sourced_from
- `[[intermediate/papers/LLM-KG-CPD-Survey.sections|LLM-KG-CPD-Survey.sections]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
- `[[intermediate/papers/LLM-KG-CPD-Survey.analysis|LLM-KG-CPD-Survey.analysis]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
- `[[intermediate/papers/LLM-KG-CPD-Survey.refs|LLM-KG-CPD-Survey.refs]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`
- `[[intermediate/papers/LLM-KG-CPD-Survey.full|LLM-KG-CPD-Survey.full]] --sourced_from--> [[raw/A survey of LLM-augmented knowledge graphs for advanced complex product design.pdf]]`

## 对 `paper-ingest` 后续风险的评估
### 当前为什么会漏
根因不是证据不足，而是三层缺口叠加：
1. ontology 已声明关系类型，但未给 `proposes` / `evaluated_on` 分配正式账本。
2. 当前关系入口只有 `citation_graph.md`、`method_evolution.md`、`concept_links.md`、`task_method_map.md`、`evidence_index.md`，没有这两类关系的出口。
3. `scripts/lint_graph.py` 目前不检查这三类关系是否存在，因此 ingest 产物即使缺边也不会暴露。

### 修完后还会不会再漏
如果只补规范和历史实例、**不补检查护栏**，以后 ingest 新论文仍然可能继续漏：
- PathMind 这类 empirical 方法论文仍可能只在正文写“提出某方法、在某 benchmark 上评测”，但不落到正式关系账本。
- survey / framework 论文仍可能只在 concept 页和 evidence frontmatter 中留下 provenance 语义，而不写正式关系边。

### 最小护栏
在 `scripts/lint_graph.py` 中补最小一致性检查：
- 检查新关系账本文件存在。
- 对当前两篇 phase-one 论文增加针对此次新增关系的最小 needle 检查。
- 不做全库强校验，只做当前已 ingest 的两篇论文样例校验，避免范围扩散。

这样做的效果是：
- 不必立即重写 `paper-ingest` skill
- 但任何后续 ingest 若仍沿用现有产物模式，至少在本地 lint 时会暴露缺边

## 测试与验收
完成后应满足：
1. `wiki/ontology/graph-standard.md` 中不再保留“`proposes`、`evaluated_on` 当前未归属”的表述。
2. `wiki/relations/` 下新增 3 个正式账本文件，并写入当前两篇论文的实例边。
3. `evidence_index.md` 只保留 `supported_by`。
4. `wiki/index.md` 能导航到新增关系账本。
5. `python3 scripts/lint_graph.py` 通过。
6. 能明确说明：后续 `paper-ingest` 若不额外改造，单靠 lint 护栏是否足以避免静默漏边。

## 推荐实施顺序
1. 更新 `graph-standard.md` 的关系定义与关系文件分工
2. 新建三个关系账本文件并写入当前实例边
3. 收敛 `evidence_index.md` 职责
4. 更新 `wiki/index.md`
5. 更新 `scripts/lint_graph.py`
6. 运行 lint 验证
