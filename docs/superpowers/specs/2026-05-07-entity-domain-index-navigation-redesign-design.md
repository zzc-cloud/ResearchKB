# Entity Domain Index Navigation Redesign

## 背景
当前 `ontology/entities/*/index.md` 同时承担了对象域导航、重复枚举实例与 relation 入口提示三类职责，导致以下问题：
- `core-entry` / `grouped-navigation` / `canonical-list` 三段在小规模知识库中高度重复。
- placeholder / cited stub 容易与默认 serving-ready 页面混在同一层导航中。
- 对象域 index 与 relation 层入口混杂，不符合 `CLAUDE.md` 中对象层与关系层分离的本体入口设计。
- 裸 `[[wikilink]]` 缺乏实例语义，不利于人类与 LLM 在进入对象页前完成候选定位。

## 目标
重构 `ontology/entities/*/index.md`，使其只承担**对象域内导航**职责，并保证在自动化论文处理链路中持续符合规范。

## 设计原则
1. **对象层与关系层分离**
   - `ontology/entities/*/index.md` 只负责对象域导航。
   - relation 真源继续保留在 `ontology/relations/*.md` 与 `CLAUDE.md` 的正式关系入口中。
   - 对象域 index 不再包含“相关关系账本 / 正式关系入口”段落。

2. **默认导航与占位实例分层**
   - 默认可 serving 的实例进入导航入口。
   - `status: placeholder` 等不可默认 serving 的实例进入“其他实例（不可导航）”。
   - placeholder 不得混入默认导航入口。

3. **实例必须带语义定位**
   - index 中的实例条目不能只是裸链接。
   - 每个实例后都要附最小语义说明，以支撑对象定位。
   - 语义说明按对象域定制，不使用统一机械字段串。

4. **自动化链路保障一致性**
   - `index-sync` 是唯一负责写 `entities/*/index.md` 受管区块的阶段。
   - `lint_graph.py`、本体语义治理与 serving 治理共同兜底。

## 目标结构
### 通用结构
所有 `ontology/entities/*/index.md` 统一采用：

```md
# <Domain> Index

> 本页负责 <Domain> 对象域导航：先理解本域实例，再进入具体对象页。

## 1. 对象域说明
- ...

## 2. 导航入口
<!-- BEGIN MANAGED BLOCK:navigation-entries -->
...对象域定制语义条目...
<!-- END MANAGED BLOCK:navigation-entries -->

## 3. 其他实例（不可导航）
<!-- BEGIN MANAGED BLOCK:non-serving-placeholders -->
...placeholder / cited stub 条目...
<!-- END MANAGED BLOCK:non-serving-placeholders -->
```

### 特殊域
- `ontology/entities/raw-sources/index.md` 可只保留 `navigation-entries`，因为 raw file 不需要 placeholder 分层。
- 若某对象域当前不存在 placeholder，则 `non-serving-placeholders` 仍保留为空受管区块，以维持结构稳定性。

## 对象域定制语义模板
- **Paper**：核心贡献 / 任务定位 / 当前状态
- **Method**：方法类型 / 解决问题 / 当前状态
- **Concept**：概念内涵 / 作用 / 当前状态
- **Task**：任务定义 / 关注重点 / 当前状态
- **Scenario**：应用语境 / 关键挑战 / 当前状态
- **Benchmark**：评测目标 / 主要任务 / 当前状态
- **Evidence**：证据类型 / 服务对象 / 当前状态
- **RawSource**：文件身份 / provenance 用途

## `papers/index.md` 的具体目标
### 导航入口
仅收录默认 serving-ready 的正式论文实例，例如：
- `[[PathMind - A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models]]`：提出 PathMind 方法，面向 knowledge-graph-reasoning / kgqa / multi-hop-qa，状态=serving-ready

### 其他实例（不可导航）
仅收录 placeholder / cited stub，例如：
- `[[Reasoning on Graphs - Faithful and Interpretable Large Language Model Reasoning]]`：PathMind 引用的 retrieval-augmented 上游论文，占位节点，状态=placeholder
- `[[Graph-constrained reasoning - Faithful reasoning on knowledge graphs with language models]]`：PathMind 引用的 grounded reasoning 上游论文，占位节点，状态=placeholder

## 自动化链路中的职责分工
### 1. `paper-ingest`
- 生成对象页候选，并标定页面状态：`processed / placeholder`
- 在 `cites` target 缺失时，自动补齐 placeholder paper 页
- 为 `index-sync` 提供足够的对象语义来源（对象页正文 / frontmatter / placeholder 模板）

### 2. `relation-reconciliation`
- 只负责 formal relation ledger 对齐
- 不直接改写对象域 index

### 3. `page-projection-sync`
- 只负责把 formal truth 投影回对象页
- 不直接改写对象域 index

### 4. `index-sync`
- 作为唯一的 index 受管区块写入者
- 读取页面状态与对象域模板，生成：
  - `navigation-entries`
  - `non-serving-placeholders`
- 为每个条目补齐对象域定制语义说明

### 5. `lint_graph.py`
新增或调整以下检查：
- `entities/*/index.md` 不得再包含旧的 `core-entry` / `grouped-navigation` / `canonical-list` 结构要求
- 每个 index 必须包含新的受管块
- 需要 placeholder 分层的域中，placeholder 不得进入 `navigation-entries`
- 条目不得是裸 `[[wikilink]]`，必须包含最小语义说明文本
- 对象域 index 不得再包含 relation 层入口段落

### 6. `ontology-semantic-review`
- 检查实例是否被放在正确对象域
- 检查 serving-ready 与 placeholder 分层是否语义合理
- 检查对象描述是否与节点实际身份一致

### 7. `serving-governance-review`
- 检查默认导航入口是否只包含适合默认 serving 的页面
- 检查 placeholder 是否被错误提升到默认入口
- 检查导航文案是否会误导 reader / LLM

## 迁移顺序
1. 先改 `ontology/entities/papers/index.md`
2. 再改 `index-sync` 的受管块与生成逻辑
3. 再改 `scripts/lint_graph.py` 与测试
4. 再推广到 methods / concepts / tasks / scenarios / benchmarks / evidence / raw-sources

## 兼容性判断
这是一次正确的收敛：
- index 职责更纯
- 更符合知识库当前规模与人工使用方式
- 更符合 `CLAUDE.md` 中对象层与关系层分离的本体入口模型
- 更适合人类与 LLM 在导航时做候选定位
