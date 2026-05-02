# ResearchKB 核心架构

## 一句话定位
> ResearchKB 是一个以本体为骨架、以知识编译为生产方式、以治理为入库门禁、以问答与发现为应用出口的 repo-native 研究知识操作系统。

## 四层结构

### 本体骨架层
- 权威源：[[graph-standard]]
- 作用：定义节点类型、关系类型、字段约束、证据要求与最小链接义务

### 本体实例编译层
- 入口：论文摄入与知识编译流程（由 `paper-ingest` skill 承担）
- 作用：把原始论文编译成 `intermediate/papers/`、`wiki/` 与 `wiki/relations/` 的候选知识变更

### 本体治理层
- 结构治理：`python3 scripts/lint_graph.py`
- 语义治理：`ontology-semantic-review`
- 作用：阻止错误知识进入正式图谱

### 本体应用层
- 正式消费：受约束的知识问答
- 探索消费：受控的探索发现
- 作用：消费治理通过后的正式知识，并发现新的候选知识

## 最小闭环
1. [[graph-standard]] 定义合法边界
2. 编译层生成知识变更
3. 治理层裁决是否允许入库
4. 应用层消费正式知识
5. 发现新的候选知识后进入下一轮闭环

## 核心原则
- 本体先于抽取
- 正式知识必须经过治理
- 证据先于结论
- 应用层只消费治理后的正式知识
- 系统持续演化，但演化必须受控

## 相关入口
- [[graph-standard]]
- [[task_method_map]]
- [[evidence_index]]
- [[citation_graph]]
- [[method_evolution]]
- [[concept_links]]
- [[overview]]
- [[ontology/index|ontology-index]]

## 应用层契约

### 正式问答
- 默认基于 `wiki/` 与 `wiki/relations/` 回答问题。
- 必要时回看 `intermediate/papers/` 作为证据补充。
- 回答时区分：正式知识结论、关系账本结论、证据缓存结论、待核验推断。

### 探索发现
- 可以提出可能的新概念、新关系与知识空白。
- 这些发现不能直接写入正式图谱。
- 所有候选发现都必须回到下一轮编译与治理闭环。
