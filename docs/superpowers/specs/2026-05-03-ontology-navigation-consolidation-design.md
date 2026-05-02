# Ontology Navigation Consolidation Design

- 日期：2026-05-03
- 状态：已确认设计，待实现
- 范围：统一 ResearchKB 的导航入口与本体规范入口

## 1. 背景

当前 ResearchKB 同时存在以下入口文档：
- `wiki/index.md`
- `wiki/ontology/index.md`
- `wiki/ontology/graph-standard.md`

其中：
- `graph-standard.md` 已经被 `CLAUDE.md` 设定为本体规范的唯一权威来源。
- `wiki/index.md` 仍承担全库导航职责，但内容逐渐演变为多轴手工穷举页，存在重复、膨胀和维护成本高的问题。
- `wiki/ontology/index.md` 目前内容较薄，尚未真正承担统一导航入口职责。

这导致系统在“入口在哪里”和“规范在哪里”两个问题上仍有职责重叠。

---

## 2. 设计目标

本次重构目标是把导航职责与规范职责彻底分开：

1. `wiki/ontology/index.md` 成为 **唯一导航页**。
2. `wiki/ontology/graph-standard.md` 保持为 **唯一规范页 / 唯一本体判定页**。
3. `wiki/index.md` 直接删除，不保留过渡跳转页。
4. `CLAUDE.md` 中所有默认入口从 `wiki/index.md` 改为 `wiki/ontology/index.md`。

---

## 3. 核心设计决策

### 3.1 保留 `wiki/ontology/graph-standard.md`

`graph-standard.md` 的职责保持不变，并进一步收敛为纯规范职责：
- 节点类型定义
- frontmatter 受控字段
- 关系类型定义
- 实例边格式
- ledger 分工
- 最小链接义务
- 证据要求
- 豁免规则

它不再承担系统总导航职责，也不再被视为实例总目录。

### 3.2 重写 `wiki/ontology/index.md`

`wiki/ontology/index.md` 升级为整个知识系统的唯一导航页。

它只承担以下职责：
- 系统入口说明
- 规范入口
- 正式关系账本入口
- 正式知识对象入口
- 证据层入口说明
- 按任务分流的阅读路径

它不承担以下职责：
- 规范细则定义
- frontmatter 规则说明
- 关系合法性判定
- 大规模手工实例清单

### 3.3 删除 `wiki/index.md`

`wiki/index.md` 直接删除。

删除原因不是它没有价值，而是它原先承担的职责会被重新拆解：
- 导航入口职责 → `wiki/ontology/index.md`
- 规范职责 → `wiki/ontology/graph-standard.md`
- 实例访问职责 → `wiki/` 对象页与 `wiki/relations/`

本次不保留占位页或迁移提示页，以确保入口收敛是明确而彻底的。

---

## 4. 目标信息架构

重构完成后，ResearchKB 的入口关系如下：

- `CLAUDE.md`
  - 提供工作方式与流程约束
  - 默认先导航到 `wiki/ontology/index.md`

- `wiki/ontology/index.md`
  - 唯一导航入口
  - 把用户与 agent 分流到规范页、关系账本、对象页与证据层

- `wiki/ontology/graph-standard.md`
  - 唯一规范页
  - 提供合法性判定规则

- `wiki/relations/*`
  - 正式关系账本层

- `wiki/papers/*` / `wiki/methods/*` / `wiki/concepts/*` / `wiki/tasks/*` / `wiki/scenarios/*` / `wiki/benchmarks/*` / `wiki/synthesis/*`
  - 正式知识对象层

- `intermediate/papers/*`
  - 证据层

---

## 5. 新的 `wiki/ontology/index.md` 内容结构

新的导航页应采用“任务分流式导航”，而不是“多轴穷举式索引”。

推荐结构如下：

### 5.1 页面身份说明
说明本页是唯一导航入口，遵循“先导航，再判定，再下钻”。

### 5.2 规范与判定入口
明确把 `[[graph-standard]]` 标记为唯一规范页和合法性判定中心。

### 5.3 正式关系入口
集中列出：
- `[[citation_graph]]`
- `[[method_evolution]]`
- `[[concept_links]]`
- `[[task_method_map]]`
- `[[evidence_index]]`
- `[[paper_method_links]]`
- `[[benchmark_links]]`
- `[[provenance_links]]`

### 5.4 正式知识对象入口
按对象层列出目录入口，而不是长列表实例：
- Papers
- Methods
- Concepts
- Tasks
- Scenarios
- Benchmarks
- Synthesis

### 5.5 按任务进入
面向使用场景给出入口分流：
- 想判断是否合法 → `graph-standard`
- 想看正式知识 → 对应对象页
- 想看正式关系 → `wiki/relations/`
- 想核验证据 → `intermediate/papers/`
- 想生成分析 → `wiki/synthesis/`

### 5.6 推荐阅读路径
至少覆盖三类：
- 初次进入系统
- 回答知识问题
- 治理知识变更

---

## 6. `CLAUDE.md` 的同步修改范围

本次需要把所有把 `wiki/index.md` 作为默认入口的地方统一改为 `wiki/ontology/index.md`。

重点修改范围：

### 6.1 本体视角判定中的信息层说明
把：
- `wiki/index.md` 定位

改为：
- `wiki/ontology/index.md` 定位导航入口

### 6.2 本体初步探查策略
把可结合的信息层中的 `wiki/index.md` 改为 `wiki/ontology/index.md`。

### 6.3 查询与分析默认顺序
把第一步：
- 读取 `wiki/index.md` 定位

改为：
- 读取 `wiki/ontology/index.md` 定位导航入口

### 6.4 其它任何显式引用旧入口的段落
统一替换为以 `wiki/ontology/index.md` 为入口。

---

## 7. 非目标

本次设计不处理以下内容：
- 不修改 `graph-standard.md` 的本体规则本身
- 不重构 `wiki/relations/` 的账本结构
- 不新建对象级子索引页（如 `wiki/papers/index.md`）
- 不实现导航自动生成
- 不实现问答执行器或探索发现执行器

本次只解决：
- 导航入口统一
- 规范入口统一
- 删除冗余入口页

---

## 8. 设计结果

本次设计落地后，ResearchKB 将形成清晰的双文档协同：

- `wiki/ontology/index.md` = 唯一导航页
- `wiki/ontology/graph-standard.md` = 唯一规范页

并且：
- `wiki/index.md` 被直接删除
- `CLAUDE.md` 中所有默认入口改为 `wiki/ontology/index.md`

这使得整个系统更符合“本体驱动而非目录驱动”的组织方式。

## 9. 实施说明
- 本次实现直接删除 `wiki/index.md`，不保留过渡跳转页。
- 所有默认入口统一改为 `wiki/ontology/index.md`。
- `wiki/ontology/graph-standard.md` 保持为唯一规范页，不承担导航首页职责。
