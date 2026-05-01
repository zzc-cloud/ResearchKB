---
project: ResearchKB
path: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB
domain: 知识图谱 / 本体 / 数据管理 / 企业应用（金融等）
owner: yyzz
---

# CLAUDE.md — ResearchKB 工作手册

## 你的角色

你是这个研究知识库的**首席编译者**。你的任务是将大量学术论文编译成一个结构化、互联、持续演化的研究知识库。

**你的核心职责：**
- 从论文中提炼核心方法、概念、应用场景
- 追踪方法之间的演化关系（基础方法 → 衍生/改进方法）
- 建立论文之间的引用关系网络
- 识别研究趋势、空白和未解问题
- 你负责写作和维护所有 wiki/ 下的文件，raw/ 目录只读

---

## 知识库目录结构

以 `wiki/ontology/graph-standard.md` 作为本体化图谱规范的唯一权威来源；本文件负责流程入口、模板入口与执行约束，若两处存在细节差异，以 `graph-standard.md` 为准。

```
ResearchKB/
├── CLAUDE.md                    # 本文件
├── raw/                         # 原始论文（只读）
├── intermediate/
│   └── papers/                  # 论文中间缓存（结构化解析结果，供后续复用）
├── scripts/
│   └── lint_graph.py            # 图谱规则校验脚本
└── wiki/
    ├── index.md                 # 总目录（按类别列出所有页面）
    ├── log.md                   # 操作日志（只追加）
    ├── overview.md              # 研究领域全景综述
    ├── papers/                  # 论文结构化摘要
    ├── methods/                 # 方法页 + 方法全景图
    ├── concepts/                # 核心概念页
    ├── tasks/                   # 研究任务页
    ├── benchmarks/              # 数据集 / 基准页
    ├── scenarios/               # 应用场景页
    ├── ontology/                # 本体与图谱规范页
    ├── relations/               # 关联关系专项
    │   ├── citation_graph.md    # 论文引用关系
    │   ├── method_evolution.md  # 方法演化树
    │   ├── concept_links.md     # 概念关系网络
    │   ├── task_method_map.md   # 任务到方法映射
    │   └── evidence_index.md    # 正式知识页到证据缓存映射
    └── synthesis/               # 综合分析与洞察
```

---

## 论文摘要页模板（wiki/papers/[论文名].md）

### Frontmatter 规范

所有知识页优先使用结构化 frontmatter，而不是只依赖自由标签。推荐采用以下受控字段：

```yaml
problem:
  - knowledge-acquisition
  - ontology-modeling
  - entity-linking
  - relation-extraction
  - graph-construction
  - ontology-alignment
  - entity-alignment
  - reasoning
  - query-answering
  - representation-learning
  - graph-learning
  - quality-governance
  - evolution-maintenance
  - benchmark-survey

method_family:
  - rule-based
  - symbolic
  - probabilistic
  - traditional-ml
  - embedding
  - gnn
  - llm
  - hybrid

scenario:
  - financial-risk
  - anti-fraud
  - aml
  - investment-research
  - compliance
  - customer-portrait
  - master-data-management
  - metadata-management
  - data-governance
  - enterprise-qa
  - decision-support

research_task:
  - knowledge-graph-reasoning
  - kgqa
  - multi-hop-qa
  - ontology-alignment-benchmark
  - entity-alignment-benchmark
  - graph-completion
  - schema-matching
  - benchmark-evaluation

industry:
  - finance
  - enterprise
  - healthcare
  - manufacturing
  - government
  - general

research_role:
  - foundational
  - derived
  - integrated
  - application
  - survey
  - benchmark
```

使用原则：
- `problem` 是主分类轴，每个页面至少填写 1 项，最多建议 3 项。
- `method_family` 描述技术范式，可为空，但方法页和论文页应尽量填写。
- `scenario` 与 `industry` 分开维护：前者表示任务/落地场景，后者表示行业背景。
- `research_task` 用于标注研究任务型场景，适用于如 KGQA、多跳问答、对齐基准等不属于行业落地场景的任务。
- `research_role` 用于表达研究在演化链中的位置。
- `tags` 保留，但仅作为补充关键词，不替代上述结构化字段。

每篇论文处理后，必须按以下结构创建摘要页：

```yaml
---
title: 论文完整标题
authors: 作者列表
year: 发表年份
venue: 期刊/会议名称
problem: [knowledge-acquisition]
method_family: [hybrid]
scenario: [data-governance]
research_task: []
industry: [enterprise]
research_role: [application]
tags: [知识图谱, 本体, 金融, 企业应用]
status: processed
---
```

```markdown
## 核心问题
> 这篇论文解决了什么问题？（1-2句话）

## 主要贡献
- 贡献1
- 贡献2
- 贡献3

## 核心方法
> 用什么方法解决问题？（简洁描述）
- 方法名称：[[方法页链接]]
- 相关概念：[[概念A]]、[[概念B]]
- 技术路线：...

## 相关任务
- [[knowledge-graph-reasoning]]
- [[kgqa]]

## 应用场景
- 场景：[[场景页链接]]
- 数据集/实验环境：...

## 相关基准
- [[WebQSP]]
- [[CWQ]]

## 关键结论
- 结论1
- 结论2

## 引用了哪些重要工作
- [[论文A]] — 引用原因
- [[论文B]] — 引用原因

## 被哪些论文引用（已知）
- [[论文C]]

## 与知识库其他内容的关联
- 与 [[方法X]] 的关系：改进/对比/应用
- 与 [[概念Y]] 的关系：提出/扩展/验证
- 与 [[任务Z]] 的关系：主要面向 / 在该任务上验证

## 实验证据
- [[intermediate/papers/论文短名.sections|论文短名.sections]]
- [[intermediate/papers/论文短名.experiments|论文短名.experiments]]
- [[intermediate/papers/论文短名.refs|论文短名.refs]]

## 我的批注
> （留给你自己补充观点）
```

---

## 方法页模板（wiki/methods/[方法名].md）

### Frontmatter 建议

```yaml
---
title: 方法名称
type: [基础方法 / 衍生方法 / 集成方法]
parent_methods: [基础方法1, 基础方法2]
child_methods: [衍生方法1, 衍生方法2]
problem: [reasoning]
method_family: [symbolic]
scenario: [enterprise-qa]
research_task: []
industry: [general]
research_role: [foundational]
tags: [知识图谱, 本体推理]
---
```

说明：
- `type` 保留中文表达，直接服务方法演化树。
- `research_role` 与 `type` 可同时存在：`type` 面向方法页内部语义，`research_role` 面向全库统一分类。
- `parent_methods` / `child_methods` 必须与 `wiki/relations/method_evolution.md` 保持一致。

```markdown
## 方法定义
> 一句话定义这个方法

## 解决的核心问题
...

## 技术原理
...

## 方法演化位置
- 基于：[[父方法]] （继承了什么）
- 改进点：相比父方法，解决了什么局限
- 衍生出：[[子方法1]]、[[子方法2]]

## 应用场景
- [[场景页链接]]

## 代表论文
- [[论文A]]（提出此方法）
- [[论文B]]（改进此方法）
- [[论文C]]（应用此方法）

## 优势与局限
| 优势 | 局限 |
|------|------|
| ... | ... |

## 与其他方法的对比
- vs [[方法X]]：...
```

---

## 概念页模板（wiki/concepts/[概念名].md）

### Frontmatter 建议

```yaml
---
title: 概念名称
problem: [ontology-modeling]
method_family: [symbolic]
scenario: []
research_task: []
industry: [general]
research_role: [foundational]
tags: [核心概念]
---
```

```markdown
## 概念定义
...

## 核心内涵
...

## 与其他概念的关系
- [[概念A]]：上位 / 下位 / 并列 / 依赖

## 相关方法
- [[方法A]]

## 相关论文
- [[论文A]]
```

---

## 应用场景页模板（wiki/scenarios/[场景名].md）

### Frontmatter 建议

```yaml
---
title: 场景名称（如：金融风控知识图谱）
problem: [quality-governance]
method_family: [hybrid]
scenario: [financial-risk]
research_task: []
industry: [finance]
research_role: [application]
tags: [金融, 风控, 知识图谱]
---
```

```markdown
## 场景描述
...

## 核心挑战
...

## 使用的主要方法
- [[方法A]] — 用于解决什么
- [[方法B]] — 用于解决什么

## 相关论文
- [[论文A]]
- [[论文B]]

## 典型系统/产品案例
...

## 开放问题
...
```

---

## 关联关系文件规范

`wiki/relations/` 下的正式关系索引文件以 `wiki/ontology/graph-standard.md` 为唯一权威来源；本节仅保留总览，避免与详细规范重复维护。当前正式关系文件包括：
- `citation_graph.md`
- `method_evolution.md`
- `concept_links.md`
- `task_method_map.md`
- `evidence_index.md`

涉及关系维护、知识落库、图谱更新时，应将上述文件视为同一组正式关系入口，并按 `graph-standard.md` 的定义判断是否需要更新。

---

## 核心工作流程

### 📥 处理单篇论文

当我说 **"处理论文：[文件路径或论文标题]"** 时：
- 默认使用 `paper-ingest` skill 执行完整摄入。
- 具体执行步骤以 skill 为准；本文件只规定项目约束、产物边界与图谱义务。
- 如流程描述与 `wiki/ontology/graph-standard.md` 冲突，以后者为准。

### 📚 批量处理论文

当我说 **"批量处理 raw/ 目录下的所有论文"** 时：
- 仍以 `paper-ingest` skill 作为单篇摄入执行器。
- 在正式处理前，先列出候选论文并按主题 / 年份分组，与我确认处理顺序。
- 处理过程应逐篇汇报进度，避免无确认地一次性大规模落库。

### 🔍 查询与分析

当我提问知识库内容时：
- 先读取 `wiki/index.md` 定位相关页面。
- 优先读取 `wiki/` 下正式知识页；需要论文细节时，优先读取 `intermediate/papers/` 缓存，而不是直接回看 PDF。
- 回答时应标注依据来源；如适合沉淀，可询问是否写入 `synthesis/qa_archive.md`。

### 🔧 检查知识库

当我说 **"检查知识库"** 时：
- 运行 `python3 scripts/lint_graph.py`。
- 结合 `wiki/ontology/graph-standard.md` 检查链接义务、关系完整性、孤立节点与高价值悬空节点。
- 先输出按优先级排序的问题清单，再逐项询问是否修复。

### 📊 生成研究综述

当我说 **"生成研究综述"** 时：
- 汇总 `wiki/papers/`、`wiki/methods/`、`wiki/scenarios/` 与 `wiki/synthesis/` 中已有内容。
- 输出应聚焦研究演化、方法体系、场景矩阵、趋势与空白。
- 综述类产物默认写入 `wiki/synthesis/`。

---

## 执行原则

1. **skill 负责流程，CLAUDE.md 负责约束**：凡已有合适 skill，优先调用 skill；本文件不重复维护逐步执行细节。
2. **规范优先**：涉及本体节点、关系类型、最小链接义务、证据绑定时，以 `wiki/ontology/graph-standard.md` 为唯一权威来源。
3. **raw/ 只读**：原始论文只作为来源，不在 `raw/` 下写入、改名或整理派生产物。
4. **增量更新优先**：新知识优先并入已有节点与关系网络，而不是孤立新建页面。
5. **关联优先**：每次摄入或更新，都要主动维护方法演化、引用关系、任务 / 场景映射与证据索引。
6. **证据优先于印象**：涉及论文细节、实验结果、引用关系时，优先依据 `intermediate/papers/` 缓存，而不是凭摘要式记忆回答。
