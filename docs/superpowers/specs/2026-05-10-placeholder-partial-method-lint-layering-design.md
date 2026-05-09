# Placeholder and Partial Method Lint Layering Design

日期：2026-05-10

## 1. 目标

为 `scripts/lint_graph.py` 增加对 Method 页迁移状态的分层校验规则，使其能够区分：

- `status: processed` / fully served Method 页
- `status: partial` 的 semantic-stub Method 页
- `status: placeholder` 的最小占位 Method 页

从而解决当前 `references_method` 首个验证案例中暴露的问题：

- GCR / EPERM 已经作为正式 Method 对象存在
- 它们已能承接 `references_method` formal relation
- 但尚不足以按完整 Method serving 页标准通过 lint

## 2. 当前问题

当前 `scripts/lint_graph.py` 对 Method 页使用统一的 serving 结构合同：

- `## 相关概念`
- `## 证据来源`
- `## Formal relations`
- `### Outgoing`
- `### Incoming`

这隐含了一个前提：

> 所有 Method 页都应被视为完整 serving 面。

但在新的 semantic stub / partial 设计下，这个前提已经不成立。

PathMind → GCR / EPERM 这一案例证明：
- 某些 Method 页在 formal graph 中必须存在
- 它们可能有最小对象语义与正式邻接
- 但它们当前只是 `placeholder` 或 `partial`
- 因此不应被强制满足完整 Method serving 页要求

## 3. 设计结论

`scripts/lint_graph.py` 应对 Method 页按 `status` 分层校验，而不是继续一刀切。

## 4. 分层规则

### 4.1 `status: processed`
仍按完整 Method serving 合同校验。

必需结构保持不变：
- `## 相关概念`
- `## 证据来源`
- `## Formal relations`
- `### Outgoing`
- `### Incoming`

并继续要求：
- `parent_methods` / `child_methods` 强一致
- 正文 wikilink 与 `Formal relations` 对齐
- serving 可遍历性成立

### 4.2 `status: partial`
按最小 semantic-stub Method 合同校验。

最小必需结构：
- `## Object semantics`
- `## 当前定位`
- `## 与知识库现有内容的关系`
- `## 最小定义/角色`
- `## 待补充`
- `## Formal relations`
- `### Outgoing`
- `### Incoming`

说明：
- `partial` 可拥有 formal relation
- 可被 index 收录
- 但不要求完整 Method serving 人类区块

### 4.3 `status: placeholder`
按最小 placeholder Method 合同校验。

最小必需结构：
- `## 当前定位`
- `## 与知识库现有内容的关系`
- `## 待补充`

如果该 placeholder 页已经承接 formal relation，则再要求：
- `## Formal relations`
- `### Outgoing`
- `### Incoming`

说明：
- placeholder 的目标是“可解析”而不是“可服务”
- 不要求它具备完整 Method serving 骨架

## 5. 这与现有设计的关系

这个分层不是新增新体系，而是让 lint 真正落实前面已经确认的设计：

- semantic stub / partial 是合法中间状态
- formal graph 中的可解析对象不等于默认 serving-ready 对象
- serving-ready 必须高于 placeholder / partial

如果 lint 不做这一层分流，那么：
- `partial` / `placeholder` 会在结构层被直接判死
- semantic stub 设计会停留在 skill 文档和治理原则里，无法进入实际运行规则

## 6. 对 `references_method` 案例的直接影响

采用本设计后：
- GCR / EPERM 若保持 `status: placeholder`
- 且承接了 `references_method` formal relation
- 则不再被强制要求提供完整 Method serving 区块

这样它们可以合法处于：
- 正式对象存在
- formal relation 可达
- serving 仍未完成

的中间状态。

## 7. 推荐实现方式

### 7.1 `lint_graph.py`
- 根据 frontmatter 中的 `status` 分支 Method 页校验规则
- 对 `processed` / `partial` / `placeholder` 分别应用不同 required headings

### 7.2 `graph-standard.md`
- 明确 Method 页也适用 placeholder / partial 分层结构合同
- 不只在 general serving 状态中声明，还应落到 Method 对象页契约或 serving 契约中

新增回归测试覆盖：
- `processed` Method 缺少 `## 相关概念` 时应失败
- `partial` Method 不含 `## 相关概念` 但满足 semantic-stub 结构时应通过
- `placeholder` Method 只满足最小占位结构时应通过
- `placeholder` Method 若存在 formal relations，但缺 `### Outgoing/Incoming` 时应失败

## 8. 非目标

本设计不做以下事情：
- 不改变 Paper / Concept / Task / Benchmark / Evidence 的完整 serving 合同
- 不在本次设计中全面重构所有对象类型的 placeholder 规则
- 不强制把现有所有 Method placeholder 立即升级为 `partial`
- 不改变 `references_method` 本身的语义边界

## 9. 验收标准

完成后至少应满足：

1. `processed` Method 页继续按完整 serving 合同校验
2. `partial` Method 页可按 semantic-stub 结构合法通过 lint
3. `placeholder` Method 页可按最小占位结构合法通过 lint
4. GCR / EPERM 这类弱关联 Method 占位页不再因缺少完整 serving 区块而被结构层直接否掉
5. lint 规则与 semantic stub / serving 状态设计保持一致

## 10. 推荐落地顺序

1. 先更新 `graph-standard.md` 中 Method 页的分层契约
2. 再修改 `scripts/lint_graph.py` 的 Method 页状态分支逻辑
4. 最后重新验证 GCR / EPERM 的 PathMind 案例
