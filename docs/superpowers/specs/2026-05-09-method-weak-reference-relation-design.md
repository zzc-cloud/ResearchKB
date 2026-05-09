# Method Weak-Reference Relation Design

日期：2026-05-09

## 1. 目标

为 ResearchKB 新增一种 **Method ↔ Method 的弱语义 formal relation**，用于承接“比较 / 借鉴 / 路线参照”这类方法级关系，从而解决像 PathMind 与 GCR / EPERM 之间这样的问题：

- 论文中已经存在稳定的方法级关联语义
- 这种关系强于单纯 `cites`
- 但又弱于严格谱系继承，不适合落为 `based_on`

本设计的目标是补齐 Method 层 formal graph 的一个真实缺口，而不是放宽 `based_on`。

## 2. 当前问题

当前本体中，Method ↔ Method 之间只有一种正式关系：

- `based_on`

而 `based_on` 在当前规范中承担的是 **方法演化谱系** 的强语义：

- 上游基础
- 谱系继承
- 直接借鉴来源
- 可驱动 `parent_methods` / `child_methods`

这导致两个问题：

1. 如果像 PathMind → GCR / EPERM 这样的方法级比较 / 借鉴 / 路线参照语义不存在 formal relation 槽位，那么它只能：
   - 退回 prose
   - 或错误挤进 `based_on`

2. 如果把 `based_on` 放宽，虽然短期能容纳更多关系，但会破坏它作为谱系边的纯度，使 `parent_methods` / `child_methods` 失真。

因此，当前问题不是“based_on 太严格”，而是：

> **Method 层缺少一种弱关联但正式存在的关系类型。**

## 3. 设计结论

采用并列新增关系，而不是上提 `based_on` 为抽象父类。

### 推荐新关系名
- **`references_method`**（推荐）

备选但不推荐：
- `compares_with`
- `draws_on`
- `relates_to_method`

### 为什么推荐 `references_method`

- 比 `compares_with` 更宽，可覆盖比较、借鉴、路线参照
- 比 `draws_on` 更中性，不默认带“吸收/利用”的方向性
- 比 `relates_to_method` 更具体，不容易变成垃圾桶关系

## 4. 关系语义定义

`references_method` 表示：

- 一个 **Method** 将另一个 **Method** 作为关键比较对象、借鉴路线、方法参照或同类技术坐标
- 但**不声明**它们之间存在严格的方法演化继承

它是 Method 层的正式关系，强于纯 paper citation，弱于谱系继承。

## 5. 与现有关系的边界

### 5.1 与 `based_on` 的边界

- `based_on`：强语义，表示方法谱系、继承、上游基础
- `references_method`：弱语义，表示比较、借鉴、参照，不进入父方法链

因此：

- `PathMind --based_on--> RoG`
- `PathMind --references_method--> GCR`
- `PathMind --references_method--> EPERM`

这套表达更符合当前论文证据与方法语义层次。

### 5.2 与 `cites` 的边界

- `cites`：Paper → Paper 的论文引用事实
- `references_method`：Method → Method 的对象级方法关联

两者可以并存：

- Paper 层保留引用事实
- Method 层保留方法级比较 / 借鉴语义

### 5.3 与 `uses_concept` 的边界

- 若被引用对象的主语义是概念、框架、taxonomy，而不是方法，则不应使用 `references_method`
- 这类情况应优先落在 `uses_concept`

## 6. 对现有本体结构的影响

### 6.1 `graph-standard.md`
需要新增关系类型定义：

- `references_method`：`[[Method]] --references_method--> [[Method]]`

并明确：
- 用于方法级比较、借鉴、路线参照
- 不表示方法谱系继承
- 不驱动 `parent_methods` / `child_methods`

### 6.2 relation ledger
新增 ledger 文件：

- `ontology/relations/references_method.md`

它与以下文件并列：
- `ontology/relations/based_on.md`
- `ontology/relations/cites.md`

职责区分：
- `cites`：论文引用
- `based_on`：方法谱系
- `references_method`：方法级比较 / 借鉴 / 路线参照

### 6.3 Method 页投影
Method 页 `Formal relations` 应允许投影 `references_method`。

但：
- `parent_methods`
- `child_methods`

仍然**只**从 `based_on` 派生，不从 `references_method` 派生。

这保证：
- 弱关联关系能正式入图
- 强一致 frontmatter 继续只表达谱系信息

### 6.4 `page-projection-sync`
需要增加一条投影规则：

- `based_on` → formal relation + strong frontmatter
- `references_method` → formal relation only

### 6.5 `ontology-semantic-review`
新增后，语义审查不必再在：
- “硬塞进 based_on”
- “退回 prose”

之间二选一，而是可以明确裁决：
- 是否应作为 `references_method`
- 是否其实应是 `based_on`
- 是否仅应保留在 `cites`

### 6.6 `serving-governance-review`
新增后，serving 层能把这类关系当作正式可遍历邻接，而不是只在正文里隐式存在。

## 7. 使用门槛

### 应使用 `references_method` 的情况
当论文或方法页中存在较稳定的 Method → Method 语义，并且至少满足以下之一时：

- 明确把对方方法作为关键比较对象
- 明确把对方方法作为借鉴路线或技术参照
- 在 related work / method comparison / baseline discussion 中反复以方法对象身份出现
- 如果不建这条边，会导致方法级 formal graph 丢失重要邻接信息

### 不应使用的情况
以下情况不应使用 `references_method`：

1. **只是论文引用，没有稳定方法对象语义**
   - 保留在 `cites`

2. **只是提到一个名字，但没有足够证据表明它在当前语境中是方法级邻居**
   - 保留在 prose 或 placeholder note

3. **其实是严格继承 / 上游基础**
   - 使用 `based_on`

4. **其实是在引用概念、框架、任务，而不是方法**
   - 应落在 `uses_concept` 或其他现有对象路径

## 8. 防滥用原则

为避免 `references_method` 变成垃圾桶关系，规范中应明确：

> `references_method` 只用于承接方法级比较、借鉴与路线参照语义；若一个关系仅能说明“论文提到过另一篇论文”，不得从 `cites` 升格为 `references_method`。

同时还应明确：

- 不得把所有 baseline 都自动升格为 `references_method`
- 只有在当前论文中确实承担稳定方法级语义角色时，才允许进入 formal graph

## 9. PathMind 案例中的直接应用

本设计下，PathMind 相关关系可表达为：

- `PathMind --based_on--> RoG`
- `PathMind --references_method--> GCR`
- `PathMind --references_method--> EPERM`

这样：

- RoG 保留谱系地位
- GCR / EPERM 获得正式方法级关系位置
- `based_on` 不再被迫承接弱比较 / 借鉴语义

## 10. 非目标

本设计不做以下事情：

- 不把 `based_on` 上提为所有方法关系的抽象父类
- 不把 `references_method` 扩展到 Paper ↔ Paper、Paper ↔ Method、Concept ↔ Method
- 不在本次设计中同步引入更多 sibling relation type
- 不自动要求所有已存在方法页补全该关系

## 11. 验收标准

完成后至少应满足：

1. 本体中存在正式的 `references_method` relation type
2. `references_method` 与 `based_on`、`cites` 边界清晰
3. Method 页可正式投影该关系
4. `parent_methods` / `child_methods` 不受其污染
5. PathMind ↔ GCR / EPERM 这类关系不再被迫退回 prose 或误挂到 `based_on`

## 12. 推荐落地顺序

1. 先更新 `ontology/graph-standard.md` 中的关系类型定义与使用边界
2. 新增 `ontology/relations/references_method.md`
3. 再更新 `page-projection-sync` / `ontology-semantic-review` / `serving-governance-review` 的关系识别规则
4. 最后把 PathMind / GCR / EPERM 作为首个案例回填验证
