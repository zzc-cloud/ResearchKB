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
- `wiki/ontology/graph-standard.md`
- `wiki/relations/citation_graph.md`
- `wiki/relations/method_evolution.md`
- `wiki/relations/concept_links.md`
- `wiki/relations/task_method_map.md`
- `wiki/relations/evidence_index.md`
- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`

## 输入
使用以下输入做审查：
1. 当前 git diff 或本次修改文件列表
2. 上述本体与关系规则文件
3. 本次新增或修改的 wiki / intermediate 页面

## 审查重点
检查：
- 实体分类是否正确
- 关系放置是否正确
- 本体位置是否正确
- 是否与现有图谱保持一致
- 是否存在重复 / 冲突 / 伪关系
- 是否存在关系方向错误或粒度不匹配

## 判断原则
- 优先给出能恢复本体一致性的最小修正方案。
- 区分“论文支撑关系”和“本体层概念关系”。
- 必须使用 `references/review-output-template.md` 中的报告格式与 verdict 语义，不要临时发明自己的 verdict 规则。

## 输出
不要直接改写本体。必须使用 `references/review-output-template.md` 的固定结构输出一份语义审查报告。
