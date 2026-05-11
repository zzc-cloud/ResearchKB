---
name: ontology-semantic-review
description: 在 `paper-ingest` 完成且 `python3 scripts/lint_graph.py` 通过后，对 ResearchKB 新增或修改的知识图谱内容做本体语义审查。只要用户要求检查新摄入论文、概念、框架、任务、场景或关系放置是否合理，或给出 git diff / 改动文件希望判断实体分类、关系归属、全局本体位置是否正确，就应使用本 skill。它用于 ingest 后的知识图谱治理，不用于 PDF 提取，也不用于基础结构 lint。
---

# 本体语义审查

## 目的
在 `paper-ingest` 完成并且 `python3 scripts/lint_graph.py` 通过后，审查本次改动的语义正确性，而不是结构存在性。

## 架构定位
本 skill 属于 ResearchKB 的**本体治理层**。
它不负责抽取论文内容，也不负责基础结构 lint；它负责在 `paper-ingest` 与 `python3 scripts/lint_graph.py` 之后，对候选知识变更做语义审查，判断这些变更是否可以进入正式图谱。

## 先阅读
- `ontology/graph-standard.md`
- `ontology/relations/cites.md`
- `ontology/relations/proposes.md`
- `ontology/relations/based_on.md`
- `ontology/relations/references_method.md`
- `ontology/relations/targets_task.md`
- `ontology/relations/evaluated_on.md`
- `ontology/relations/supported_by.md`
- `ontology/relations/sourced_from.md`
- `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

## 输入
使用以下输入做审查：
1. 当前 git diff 或本次修改文件列表
2. 上述本体与关系规则文件
3. 本次新增或修改的 ontology / intermediate 页面

## 审查重点
检查：
- 实体分类是否正确
- 关系放置是否正确
- 本体位置是否正确
- 是否与现有图谱保持一致
- 是否存在重复 / 冲突 / 伪关系
- 是否存在关系方向错误或粒度不匹配
- `supported_by` 是否被错误用于 `Paper`
- `targets_task` 是否被错误用于 `Paper`
- `applied_in` 是否被错误用于 `Paper`，或是否应由 `Method -> Scenario` 承接
- `Task` 与 `Scenario` 是否被混淆为同一语义层级
- Evidence 是否通过正文或 formal relation 直接连接回 Paper
- 对象页 / Evidence 页正文中的 wikilink 是否超出 formal relation 已投影邻接
- relation 页的“关系语义说明区”是否与 `ontology/graph-standard.md` 一致
- relation 页的“关系语义说明区”是否足以帮助判断 source / target 合法性与实例边归属
- relation 页的“关系语义说明区”是否重新引入了导航型噪声或无关跳转预期
- relation 实例的 `edge_semantics` 是否准确表达边成立语义
- index 入口项投影的 `object_semantics` 是否准确表达对象实例身份

## 判断原则
- 优先给出能恢复本体一致性的最小修正方案。
- 区分“论文支撑关系”和“本体层概念关系”。
- 若方法间关系表达的是比较、借鉴或路线参照，而非严格谱系继承，应优先审查其是否应落为 `references_method`，而不是 `based_on`。
- 必须使用 `.claude/skills/ontology-semantic-review/references/review-output-template.md` 中的报告格式与 verdict 语义，不要临时发明自己的 verdict 规则。

## 输出
不要直接改写本体。必须使用 `.claude/skills/ontology-semantic-review/references/review-output-template.md` 的固定结构输出一份语义审查报告。
