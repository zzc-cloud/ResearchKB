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

### wiki/relations/citation_graph.md
记录所有已知的论文引用关系，格式：
```markdown
## 引用关系列表
- [[论文A]] → [[论文B]]：A引用B，原因：[方法借鉴/对比实验/理论基础]
```

### wiki/relations/method_evolution.md
记录方法演化树，格式：
```markdown
## 方法演化树
- [[基础方法A]]
  - └─ [[衍生方法B]]（改进点：xxx，来自论文[[论文X]]）
      - └─ [[衍生方法C]]（改进点：xxx）
- [[基础方法D]]
  - └─ [[衍生方法E]]
```

### wiki/relations/concept_links.md
记录概念之间的关系网络。

---

## 核心工作流程

### 📥 工作流 A：摄入单篇论文

当我说 **"处理论文：[文件路径或论文标题]"** 时，执行：

**Step 1 — 阅读与讨论**
- 阅读论文全文
- 向我汇报：核心问题、主要方法、关键结论（3-5条）
- 询问我：是否有特别关注的方向？

**Step 1.5 — 生成论文中间缓存**
- 从 `raw/` 中的 PDF 提取结构化文本
- 存入 `intermediate/papers/`
- 文件命名优先使用论文短名或稳定方法名，避免过长文件名；推荐：`PathMind.sections.md`
- 默认至少生成：
  - `[论文短名].sections.md`：按章节组织的结构化文本缓存
  - `[论文短名].refs.md`：参考文献与关键基线缓存
- 第三个缓存按论文类型分流：
  - 方法 / 应用 / empirical 论文：`[论文短名].experiments.md`
  - survey / framework / benchmark / taxonomy / dataset 论文：`[论文短名].analysis.md`
- 按需生成：
  - `[论文短名].full.md`：高保真工作底稿，用于跨章节深挖
- 后续二次分析优先读取中间缓存，仅在需要版面、图表、公式排版或解析校验时回看 PDF

**中间缓存模板规范**

1. **`[论文短名].sections.md`**（默认必建）
   - 用途：作为后续分析的默认入口
   - 必含内容：
     - frontmatter：`title` / `short_name` / `source_pdf` / `cache_type` / `status` / `venue` / `year`
     - 论文元数据
     - 章节结构
     - Abstract / Introduction / Related Work / Methodology / Experiments / Conclusion 的结构化摘要
     - “适合后续复用的重点”小节

2. **`[论文短名].refs.md`**（默认必建）
   - 用途：服务 citation graph、方法演化和基线梳理
   - 必含内容：
     - 论文自身元数据
     - 关键基线方法列表
     - 与知识库最相关的上游工作定位
     - 可直接复用到 `citation_graph.md` 的引用条目
     - 后续待补节点清单

3. **`[论文短名].experiments.md`**（方法 / 应用 / empirical 论文推荐）
   - 用途：面向实验比较场景，减少读取全文缓存的需要
   - 适用场景：要写实验综述、比指标、看消融、看效率、看泛化
   - 建议内容：
     - 数据集与指标
     - 实现设置
     - 总体结果表
     - 强基线对比
     - 消融实验
     - 路径策略比较
     - 效率结果
     - 可直接复用的结论

4. **`[论文短名].analysis.md`**（survey / framework / benchmark / taxonomy / dataset 论文推荐）
   - 用途：作为非 empirical 论文的第三类证据缓存，承载统计、landscape、阶段分析、software-gap 分析、framework 支撑证据
   - 适用场景：要写综述、做路线归纳、抽 framework / taxonomy、分析 research gaps、总结 benchmark 设计
   - 建议内容：
     - 文献筛选与统计结论
     - 研究路线 / 角色划分
     - 分阶段或分层结构分析
     - software-gap / capability-gap 分析
     - 优势、局限与未来方向
     - 可直接复用的综述结论

5. **`[论文短名].full.md`**（推荐高复用论文建）
   - 用途：作为高保真工作底稿，保留跨章节叙事脉络
   - 说明：不是逐字 OCR 转录，而是面向后续分析复用的高保真重写版
   - 适用场景：要做深度综述、长篇比较、跨章节追踪论证逻辑

**本体化图谱缓存要求**
- 每个 `intermediate/papers/[论文短名].*.md` 页面都必须在顶部包含“对应正式知识节点”区块，至少回链：论文页、核心方法、核心概念、任务节点、benchmark 节点。
- 缓存正文中凡是高频出现且已存在正式节点或占位节点的对象，应优先写成 `[[wikilink]]`。
- 关键章节应通过一句“本节支撑 ...”明确说明该缓存片段支撑哪个正式知识结论。

**缓存使用优先级**
- 默认先读：`sections.md`
- 只看引用/基线：`refs.md`
- 方法 / 应用 / empirical 论文优先看：`experiments.md`
- survey / framework / benchmark / taxonomy / dataset 论文优先看：`analysis.md`
- 需要跨章节深挖：`full.md`
- 仍有歧义时：回看原始 PDF


**Step 2 — 创建论文摘要页**
- 按模板创建 `wiki/papers/[论文名].md`
- 识别所有涉及的方法、概念、场景
- 同步识别研究任务节点（如 `kgqa`、`multi-hop-qa`）与 benchmark 节点（如 `WebQSP`、`CWQ`）

**Step 3 — 更新/创建方法页**
- 对论文中每个核心方法：
  - 如果方法页不存在 → 创建新页
  - 如果方法页已存在 → 更新，添加这篇论文的贡献
  - 判断该方法是基础方法还是衍生方法，更新演化关系

**Step 4 — 更新/创建概念页**
- 对论文中的核心概念做同样处理

**Step 5 — 更新/创建任务 / 场景 / 基准页**
- 对论文涉及的研究任务节点、应用场景节点、benchmark 节点做同样处理

**Step 6 — 更新关联关系文件**
- 更新 `citation_graph.md`（添加引用关系）
- 更新 `method_evolution.md`（如有新的演化关系）
- 更新 `task_method_map.md`（登记任务到方法或高频上游工作的关系）
- 更新 `evidence_index.md`（登记正式知识页与 `intermediate/` 证据层的对应关系）

**Step 7 — 运行 graph lint 并更新导航**
- 运行 `python3 scripts/lint_graph.py` 检查图谱最低约束
- index.md 添加所有新建/更新的页面
- log.md 追加：`## [日期] ingest | 论文标题`

---

### 📥 工作流 B：批量摄入论文

当我说 **"批量处理 raw/ 目录下的所有论文"** 时：
- 先列出所有论文，按主题/年份分组，给我看
- 询问处理顺序（建议：先处理基础/经典论文，再处理衍生论文）
- 逐篇处理，每处理完一篇汇报进度
- 每篇论文在落库前都先生成对应的 `intermediate/papers/` 缓存
- 完成后生成批量摄入报告

---

### 🔍 工作流 C：查询与分析

当我提问时：
1. 读取 `index.md` 定位相关页面
2. 优先读取相关 `wiki/` 页面；如果问题需要回到论文细节，则优先读取 `intermediate/papers/` 缓存，而不是直接读取 PDF
3. 标注引用来源
4. 询问是否存入 `synthesis/qa_archive.md`

**特殊查询指令：**
- `"画出方法演化树"` → 读取 method_evolution.md，用 Markdown 树形图输出
- `"分析[场景]的研究现状"` → 综合 scenarios/ 和相关 papers/ 输出分析报告
- `"[方法A] vs [方法B]"` → 对比两个方法页，生成对比表格
- `"研究空白在哪里"` → 综合 synthesis/research_gaps.md 输出

---

### 🔧 工作流 D：健康检查（Lint）

当我说 **"检查知识库"** 时：
1. 运行 `python3 scripts/lint_graph.py`
2. 扫描所有页面，检查：
   - 孤立页面（无入链）
   - 方法页缺少演化关系标注
   - 论文页缺少引用关系
   - 论文页是否缺少 Method / Concept / Task / Evidence 最小链接义务
   - 重要概念被多次提及但无独立页面
   - 场景页缺少对应方法链接
   - 高价值悬空节点是否需要升级为占位页或正式页
3. 输出检查报告，按优先级排列问题
4. 逐项询问是否修复

---

### 📊 工作流 E：生成综合分析

当我说 **"生成研究综述"** 时：
- 综合所有 papers/、methods/、scenarios/
- 输出结构化综述，包含：
  - 研究演化时间线
  - 核心方法体系
  - 主要应用场景矩阵
  - 研究趋势与空白
- 存入 `synthesis/` 目录

---

## 重要原则

1. **关联优先**：每次处理论文，必须主动寻找与已有内容的关联，不孤立处理
2. **演化意识**：时刻判断方法是基础还是衍生，维护好演化树
3. **引用追踪**：论文引用的重要工作，即使尚未处理，也要在 citation_graph.md 中预登记
4. **场景落地**：每个方法都要追问"在什么场景下用？效果如何？"
5. **增量更新**：新论文的知识要整合进已有页面，不是孤立新建

---

## 初始化指令

**现在请执行以下操作：**

1. 在 `/Users/yyzz/Desktop/MyClaudeCode/ResearchKB/` 下创建完整目录结构
2. 创建初始 `CLAUDE.md`（本文件）
3. 创建空的 `wiki/index.md`（含分类框架）
4. 创建空的 `wiki/log.md`（记录初始化条目）
5. 创建空的 `wiki/overview.md`（含领域描述占位符）
6. 创建空的各关联关系文件
7. 扫描 `raw/` 目录，列出所有论文，按主题分组展示给我
8. 询问我：优先处理哪些论文？有无特别关注的研究问题？
