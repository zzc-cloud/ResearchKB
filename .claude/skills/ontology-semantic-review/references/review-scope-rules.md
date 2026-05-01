# 审查范围规则
- 只审查本次变更涉及的节点与关系。
- 不要重述整个本体。
- 默认结构有效性已由 `scripts/lint_graph.py` 先行检查。
- 优先关注如下语义问题：
  - survey 被误写成 task
  - framework 被误写成 method
  - 概念 → 论文支撑关系被错误写进 `concept_links.md`
  - 文献支撑关系被错误写进 `method_evolution.md`
  - 节点身份重复或冲突
  - 关系方向与现有约定不一致
  - 节点粒度不匹配（例如把 framework 当原子 concept，或把 scenario 当 task）
  - 同义或近义概念未合并、也未显式区分

## 分类指引
- Paper：论文产物本身
- Method：可复用的技术方法
- Concept：稳定语义单元
- Framework：多层、角色化或阶段化组织结构
- Task：要解决的问题，不是论文类型
- Scenario：行业或应用语境
- Benchmark：数据集或评测目标
- Evidence：证据缓存，不是领域节点

## 判断启发式
- 如果一个节点主要描述的是研究产出形式（survey / benchmark / dataset paper），优先放在 `research_role` 或论文类型里，而不是 `Task`。
- 如果一个节点主要用于组织多个层级、角色或阶段，优先落到 `Framework` / concept 层，而不是 `Method`。
- 如果一条关系表达的是“这篇论文支撑 / 梳理 / 解释了这个概念”，优先放在概念页证据区或 `evidence_index.md`，而不是 `concept_links.md`。
- 如果一条关系表达的是文献借鉴或引用支撑，而不是严格的技术演化谱系，优先放在 `citation_graph.md`，而不是 `method_evolution.md`。
