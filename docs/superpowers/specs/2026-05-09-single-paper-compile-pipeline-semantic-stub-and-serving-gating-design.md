# Single-Paper Compile Pipeline Semantic Stub and Serving Gating Design

日期：2026-05-09

## 1. 目标

优化 ResearchKB 当前单篇论文处理链路：

1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

使其能够正确处理这样一种对象：

- 当前论文已经稳定提取出它们的基础语义
- formal relations 已经可以合法指向它们
- 但这些对象尚不足以直接作为默认 serving surface

典型例子是由一篇论文带出的高频上游方法页，如 RoG / GCR / EPERM。

本设计的目标不是让所有被提及对象都自动变成完整正式页，而是让编译链显式区分：

- 可解析对象
- 具有最小语义骨架的 partial 对象
- 真正可默认服务的 serving-ready 对象

## 2. 当前问题

PathMind 这次 dry run 暴露出的核心问题是：

- 编译链已经能从 refs / related work / method comparison 中稳定抽出 RoG、GCR、EPERM 等对象
- relation ledger 已经可以合法指向这些对象
- 但对象页目前只被物化成空 placeholder
- serving 层因此只能看到“存在的邻居”，看不到“足够可读的邻居”

这说明现在的断层不是抽取失败，而是：

> **抽取成功，但输出契约没有要求把基础语义写回对象页。**

因此当前链路存在两个耦合问题：

1. **语义写回缺口**
   - 高价值上游对象已被识别，但没有最小语义页
2. **serving 判定过粗**
   - 只要 formal neighbor 可解析，就容易误接近 `serving-ready`
   - 但“可做受约束拓扑扩展”不等于“适合作为默认问答入口”

## 3. 已确认的判定原则

本设计明确采用以下判定：

- **仅因为对象页可通过 `Formal relations` 做受约束拓扑扩展，不足以直接提升为 `serving-ready`。**
- 如果某页只有最小基础语义，但 formal relation 已成立，它应被标记为 **`partial`**，而不是 `serving-ready`。
- `partial` 页可以被正式链接、可以被 index 收录、可以参与 formal graph 遍历，但不应被提升为默认 serving 入口。

## 4. 总体方案

采用“**双层闭环增强**”方案，在保留现有 7 步链路的前提下补两类能力：

1. **链路内自动补足最小上游页语义**
2. **链路内自动阻止不合格 semantic stub 提升为 default serving**

不新增新的主阶段，而是在现有阶段中补全职责与契约。

## 5. `paper-ingest` 侧优化

### 5.1 新增 semantic stub candidates 输出

`paper-ingest` 除了继续输出正式主线对象和 relation candidates 外，还应显式输出：

- `semantic_stub_candidates`

它们用于表示：
- 当前论文中已被稳定识别
- 已有基础语义支撑
- 但还不应自动视为完整 serving-ready 对象

### 5.2 每个 semantic stub candidate 最少字段

每个 candidate 至少包含：

- `object_name`
- `object_type`
- `source_evidence`
- `object_semantics`
- `minimal_sections`
  - `当前定位`
  - `与知识库现有内容的关系`
  - `最小定义/角色`
  - `待补充`
- `serving_readiness_hint`
  - `placeholder`
  - `partial`
  - `candidate-serving`

### 5.3 适用对象范围

主要面向：
- 高频上游方法
- 高频 cited paper
- 被 related work 稳定定位的路线性对象
- 已可稳定归类为 Method / Paper / Concept，但当前证据仍不足以升为完整页的对象

### 5.4 为什么不在这一步直接升为正式完整页

因为 `paper-ingest` 的职责仍然是论文编译入口，不应演变为“替所有邻居做完整 ingest”。

它要做的是：
- 把已经确定的最小语义声明为正式产物
- 而不是把所有外溢对象都扩展成 fully served objects

## 6. `relation-reconciliation` 侧优化

`relation-reconciliation` 本身不负责写长 prose，但要把 `semantic_stub_candidates` 纳入 reconcile 输入。

### 新职责
- 校验 semantic stub 与当前 formal relation 的一致性
- 确认这些对象是否：
  - 只需要 placeholder
  - 应升级为 `partial`
  - 仍然需要 `needs-human-review`
- 把涉及的 stub 页加入 `affected_pages`

### 输出增加
除现有 `affected_pages` 外，增加：
- `affected_stub_pages`
- `serving_status_recommendations`

这样 downstream 不需要再从 prose 猜测哪些页面应降级或升级。

## 7. `page-projection-sync` 侧优化

### 7.1 新输入
`page-projection-sync` 在读取 formal ledger 之外，还要读取：

- `semantic_stub_candidates`
- `serving_status_recommendations`

### 7.2 新职责
对于 semantic stub：
- 自动写入最小语义骨架
- 同步 `status: partial` 或 `status: placeholder`
- 保留 formal relation truth
- 但不伪装成 fully served page

### 7.3 自动写回内容
除现有 `Formal relations`、frontmatter、模板化关系区块外，再自动写回：

- `## Object semantics`
- `## 当前定位`
- `## 与知识库现有内容的关系`
- `## 最小定义/角色`
- `## 待补充`

这些区块仅用于 semantic stub / partial 页，不要求所有正式页都走这个降级模板。

### 7.4 关键边界
`page-projection-sync` 仍不自动改写：
- 解释性分析 prose
- 关键结论
- 人工综述判断

它只负责把 ingest 已经产出的最小语义骨架投影落盘。

## 8. `index-sync` 侧优化

### 8.1 新状态模型
index 收录逻辑不再只有“存在 / 不存在”，而是明确区分：

- `placeholder`
- `partial`
- `serving-ready`

### 8.2 收录规则
- `placeholder`
  - 仅进入 non-serving block
- `partial`
  - 可被 index 收录
  - 但不得进入 default entry
- `serving-ready`
  - 进入默认导航入口

### 8.3 这样解决什么问题
- semantic stub 不再被当作空节点
- 但也不会因为“文件存在 + formal relation 可达”就被错误提升为默认入口
- domain index 可以同时表达：
  - 什么对象已可发现
  - 什么对象仍非默认 serving surface

## 9. `ontology-semantic-review` 侧优化

### 新职责边界
它不负责再去“发现这些 stub 应不应该存在”，而是审查：

- semantic stub 的对象分类是否正确
- 它被标记为 `partial` 是否合理
- 其最小定义/角色是否与当前论文证据一致
- 是否有对象被错误地从 partial 升格为 serving-ready

### 输出关注点
语义审查应显式区分：
- formal relation 成立
- semantic stub 成立
- serving-ready 不成立

这样语义治理不会再和 serving 治理混成一层。

## 10. `serving-governance-review` 侧优化

### 10.1 新核心规则
`serving-governance-review` 的判定不再基于：

> “formal neighbor 是否存在？”

而要基于：

> “formal neighbor 是否仍然停留在合格的默认 serving surface 上？”

### 10.2 自动裁决规则
#### 判 `serving-ready`
必须同时满足：
- 当前页自身完整
- 关键 formal neighbors 多数为 `serving-ready`
- 默认遍历不会迅速跌入 semantic stub / partial 页

#### 判 `partial`
当满足：
- 当前页结构完整
- formal relations 完整
- 邻居可解析
- 但关键邻居仍主要是 semantic stub / partial 页

#### 判 `blocked`
当满足：
- formal relation 本身缺失或非法
- 页面依赖不存在节点
- 或 prose / projection 已严重误导 formal truth

### 10.3 关键结论
即使某页已经可以基于 `Formal relations` 做受约束拓扑扩展，**只要它的关键拓扑下一跳仍主要落在 partial stub 上，就不能直接判 `serving-ready`。**

## 11. 优化后的链路效果

当前链路的问题是：

- 抽出对象
- 建 formal relation
- 生成空 placeholder
- 在 serving 阶段才发现这些邻居不可默认服务

优化后应变成：

- 抽出对象
- 生成 semantic stub candidate
- reconcile 中确认其 formal 合法性与状态建议
- projection 中写回最小语义骨架与 `partial` 状态
- index 中收录但不提升为默认入口
- serving-governance-review 稳定裁决整批页面是否真正 serving-ready

## 12. 非目标

本设计不做以下事情：

- 让所有 cited work 自动变成完整正式页
- 把 `paper-ingest` 改造成跨论文批量补全器
- 在一篇论文 ingest 时强制完成所有上游对象的 full ingest
- 用 serving-governance-review 代替 relation / semantic 治理

## 13. 验收标准

优化完成后，至少应满足：

1. 对 RoG / GCR / EPERM 这类对象，不再只生成空 placeholder
2. semantic stub 页具有最小语义骨架与 `status` 标记
3. `index-sync` 能区分 `placeholder` / `partial` / `serving-ready`
4. `serving-governance-review` 不再把“可 formal 遍历”误判为“可默认服务”
5. 单篇论文编译链在面对高频上游对象时，不再把问题拖到最后才暴露

## 14. 推荐落地顺序

1. 先升级 `paper-ingest` 输出 `semantic_stub_candidates`
2. 再升级 `page-projection-sync` 落盘最小语义骨架
3. 再升级 `index-sync` 的状态分层
4. 最后升级 `serving-governance-review` 的状态裁决规则

这个顺序能保证先补产物，再补投影，再补发布裁决，避免反过来只增强审查而没有上游数据来源。
