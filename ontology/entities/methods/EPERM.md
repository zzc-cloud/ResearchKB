---
title: EPERM
type: 基础方法
parent_methods: []
child_methods: []
problem: [reasoning, query-answering]
method_family: [hybrid, llm]
scenario: []
research_task: [knowledge-graph-reasoning, kgqa]
industry: [general]
research_role: [foundational]
status: partial
---

# EPERM

## Object semantics
- 一种 evidence path enhanced 知识图谱问答方法，代表 evidence-path 增强路线。

## 当前定位
- 当前作为 PathMind 的关键参照方法候选被 materialize。

## 与知识库现有内容的关系
- 被 [[../methods/PathMind]] 作为 evidence-path enhanced 代表方法参照。

## 最小定义/角色
- 论文明确说明 EPERM 通过发现更多 reasoning chains 支持 inference，并在 WebQSP 上是 PathMind 的强对比基线之一。

## 待补充
- 其独立论文页、完整方法定义、独立证据与更多任务邻接仍待后续单篇 ingest 完成。

## Formal relations
### Outgoing
当前对象作为 source；以下列出当前对象指向的 relation 实例。
- `supported_by`：PathMind.refs（文档：`ontology/entities/evidence/PathMind.refs.md`）：[[../evidence/PathMind.refs]]
  - edge_semantics: 引用证据页支撑 EPERM 作为 evidence-path enhanced 代表方法的最小语义。
  - evidence: [[../evidence/PathMind.refs]]

### Incoming
当前对象作为 target；以下列出指向当前对象的 relation 实例。
- `references_method`：PathMind（文档：`ontology/entities/methods/PathMind.md`）：[[../methods/PathMind]]
  - edge_semantics: PathMind 将 EPERM 作为 evidence-path enhanced 代表方法进行比较。
  - evidence: [[../evidence/PathMind.refs]]
