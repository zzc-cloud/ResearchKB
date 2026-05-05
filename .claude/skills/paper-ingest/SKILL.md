---
name: paper-ingest
description: 完整摄入单篇学术论文并落库到 ResearchKB。Whenever the user says 处理论文、摄入论文、解析论文、落库论文、为某篇 paper 建缓存/摘要/方法页/关系页，或给出 PDF 路径希望完整提取并写入知识库时，都应使用此 skill，即使用户只明确提到其中一步。它会解析论文、生成全部 intermediate 缓存、按用户当前关注方向强化提取、更新 wiki/relations/index/log，并在遇到异常结构论文时输出 needs-skill-update 告警。
---

# Paper Ingest

你是 ResearchKB 的论文完整摄入器。你的任务不是只“读一篇论文”，而是把单篇论文从原始 PDF 编译成 ResearchKB 可以长期复用的知识资产。

## 何时使用
当用户出现以下意图时，优先使用本 skill：
- “处理论文：...”, “摄入论文：...”, “把这篇 paper 落库”
- 给出 PDF 路径，希望完整解析并写入知识库
- 希望为论文生成缓存、摘要页、方法页、概念页、场景页、引用关系或方法演化关系
- 希望围绕某篇论文建立后续可复用的 intermediate 缓存

不要把它用于：
- 只回答一个简短问题且无需落库
- 仅做跨论文综合分析但不处理新增论文
- 与论文无关的普通写作或编程任务

## 核心原则
1. 把 `CLAUDE.md` 视为最高约束，尤其是 taxonomy、缓存模板、目录结构和工作流要求。
2. 默认按论文类型生成最小缓存集合：
   - empirical / method / application 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].experiments.md`
   - survey / framework / taxonomy / benchmark-landscape 论文：`[short_name].sections.md`、`[short_name].refs.md`、`[short_name].analysis.md`
   - theoretical / position 论文：`[short_name].sections.md`、`[short_name].refs.md`
3. 不生成 `full.md`；若未来需要新增 cache 类型，必须先更新本体规范与 skill 合约，而不是临时加文件

## 架构定位
本 skill 属于 ResearchKB 的**本体实例编译入口**。
它的职责是把原始论文编译成候选知识变更，包括：
- `intermediate/papers/` 证据缓存
- `wiki/` 正式节点页候选变更
- formal relation candidates（供后续 relation reconciliation 使用）

它不直接完成全图 formal relation 闭环，也不裁决语义合法性；生成结果后应先交给 relation reconciliation，再进入本体治理层继续审查。
在日常处理论文流程中，本 skill 默认只负责编译入口；完成后必须显式进入 `relation-reconciliation`，而不是把 ingest 结果直接当作正式入图结果。

## 输入约定
从用户提示中提取以下信息：
- 论文路径或论文标题（必须）
- 当前关注方向（可选）
  - 例如：方法演化、技术细节、实验对比、金融场景、数据治理、benchmark 设计

如果用户没有明确关注方向，默认关注：
- 核心问题
- 主要方法
- 关键实验结论
- 与现有知识库的关系

## 执行流程

### Step 1: 解析任务并确认输入
1. 识别论文路径或标题。
2. 如果用户给出的是标题但未给路径，先在 `raw/` 目录定位文件。
3. 提取当前关注方向；若未提供，使用默认关注方向。
4. 生成稳定短名 `short_name`：优先用论文方法名或公认简称，避免使用超长全文标题直接命名缓存文件。

### Step 2: 首次阅读与结构判断
1. 读取论文 PDF 的首页、方法/实验关键页、参考文献页。
2. 判断论文的大致类型：
   - 方法论文
   - 应用论文
   - survey / benchmark / dataset / taxonomy 论文
   - framework / mixed 论文
3. 判断结构是否标准：
   - 是否存在可映射的 abstract/introduction/method/experiments/conclusion
   - 是否存在明显附录依赖、图表依赖、章节标题异常、关键信息缺失

### Step 3: 生成 intermediate 缓存
在 `intermediate/papers/` 下按论文类型生成最小缓存集合：

1. 所有论文默认生成：
   - `[short_name].sections.md`
   - `[short_name].refs.md`
2. 第三缓存按论文类型分流：
   - empirical / method / application 论文：`[short_name].experiments.md`
   - survey / framework / benchmark / taxonomy / dataset / benchmark-landscape 论文：`[short_name].analysis.md`
3. theoretical / position 论文不生成第三缓存，除非本体规范后续明确扩展

生成要求：
- `sections.md` 是默认分析入口，承担章节结构、核心机制与 formal relation 审计所需的最小章节级摘要
- `refs.md` 服务引用关系、方法演化与上游基线 grounding
- `experiments.md` 仅用于实验、消融、效率、泛化与 benchmark 结果证据
- `analysis.md` 仅用于综述统计、landscape、阶段分析、software-gap 分析、framework 支撑证据或 benchmark 设计分析
- 不生成 `full.md`，也不以长篇高保真重写稿替代 `sections.md`

写缓存时优先遵循 `CLAUDE.md` 中的缓存模板规范。

### Step 4: 输出初读结论
在真正落库前，向用户给出一轮简短初读结论：
- 核心问题
- 主要方法
- 关键结论（3-5 条）
- 结合关注方向补充一段重点观察

如果用户显式要求跳过这一轮汇报并直接落库，可以直接继续。

### Step 5: 创建/更新知识库页面
按 `CLAUDE.md` 的模板和 frontmatter 规范进行落库：

1. 论文页：`wiki/papers/[论文名].md`
2. 方法页：若是方法论文，为核心方法创建或更新 `wiki/methods/`
3. 概念页：为核心概念创建或更新 `wiki/concepts/`
4. 场景页：为核心场景创建或更新 `wiki/scenarios/`
5. 对于 survey / framework / taxonomy 论文：优先把核心知识落到 concept / framework / scenario / synthesis，而不是强行抽取单一方法页
6. 关联关系：在落库完成前，逐类判断是否存在应正式落账的关系；只要存在就写入对应账本，而不是留在正文 prose 中。
   - `wiki/relations/citation_graph.md`
   - `wiki/relations/method_evolution.md`
   - `wiki/relations/concept_links.md`
   - `wiki/relations/task_method_map.md`
   - `wiki/relations/evidence_index.md`
   - `wiki/relations/paper_method_links.md`
   - `wiki/relations/benchmark_links.md`
   - `wiki/relations/provenance_links.md`
7. 更新：
   - `wiki/ontology/index.md`
   - `wiki/log.md`

### Step 5.5: 汇总候选正式关系
在完成页面与缓存候选更新后，必须显式整理本次论文直接支撑的 formal relation candidates，而不是只把关系散落写进正文或关系账本。

输出时至少按以下关系类型归类：
- `proposes`
- `targets_task`
- `evaluated_on`
- `uses_concept`
- `supported_by`
- `cites`
- `applies_to`
- `based_on`
- `improves_on`
- `sourced_from`

并且必须区分三类：
1. direct relations：证据明确、可直接落账
2. high-confidence candidate relations：强支持但仍需 graph-level reconciliation
3. needs-human-review relations：存在方向、粒度或本体归属歧义

## 分类与抽取规则
### 论文页
必须尽量填充这些结构化字段：
- `problem`
- `method_family`
- `scenario`
- `research_task`
- `industry`
- `research_role`

### 方法页
重点判断：
- 这是基础方法、衍生方法还是集成方法？
- 它的父方法是谁？
- 是否应挂到某个“方法族”之下，而不是直接把若干基线都写成 `parent_methods`？

### 场景页
区分：
- `scenario`：行业/落地场景
- `research_task`：研究任务型场景（例如 KGQA、多跳问答、benchmark）

### 关系文件
- 对重要上游论文，即使知识库中尚未有完整页，也可先在 citation graph 中预登记。
- 对高频上游方法，优先建立最小 stub 页，而不是只留下空链接。
- `proposes`：
  - 方法论文若提出核心方法，必须登记 `[[Paper]] --proposes--> [[Method]]`
  - 若论文核心贡献是 framework / taxonomy 型概念，必须登记 `[[Paper]] --proposes--> [[Concept]]`
  - framework / taxonomy 型核心知识产物仍按当前本体优先落为 Concept，不改写为 Method
- `evaluated_on`：
  - empirical / method / application 论文只要存在明确 benchmark，必须登记 `[[Paper]] --evaluated_on--> [[Benchmark]]`
  - 若该 benchmark 同时明确服务某个核心 Method 的正式评测，也应登记 `[[Method]] --evaluated_on--> [[Benchmark]]`
  - survey / framework / taxonomy / dataset / benchmark 类型论文若无统一 benchmark，不生成 `evaluated_on`，并在最终输出中显式写明“按规范豁免”
- `sourced_from`：
  - 只要本次生成了 `sections.md`、`refs.md`、`experiments.md`、`analysis.md` 任一 Evidence 缓存，就必须同步登记 `[[Evidence]] --sourced_from--> [[RawSource]]`

## 异常结构检测
以下情况说明当前论文可能不适合直接套用标准模板：

1. 缺少清晰的方法章节，主要贡献是 survey / benchmark / dataset / taxonomy / framework
2. 实验关键信息大量放在 appendix，中正文无法稳定支撑 empirical `experiments.md`
3. 章节标题高度非标准，难以映射到常规模板
4. 论文没有单一核心方法，更多是评测框架、数据集贡献、角色划分或分层 framework
5. taxonomy 无法稳定归类到现有 `problem / method_family / research_task` 体系
6. 图表、表格或版式对理解贡献过大，文本解析后信息明显残缺

## 降级策略
若发现异常结构，不要硬落库为“普通方法论文”。采用以下策略：

1. 尽可能先完成 intermediate 缓存
2. 根据可确认的信息做部分落库
3. 将不确定部分明确标记为待补
4. 输出结构化告警，提醒当前 skill 需要进一步优化

## 最终输出格式
完成后，必须以一个结构化摘要收尾。使用下面模板：

```yaml
status: success | partial | needs-skill-update
paper_type_guess: method | application | survey | benchmark | dataset | taxonomy | framework | mixed
generated_caches:
  - intermediate/papers/<short_name>.sections.md
  - intermediate/papers/<short_name>.refs.md
  - intermediate/papers/<short_name>.experiments.md | intermediate/papers/<short_name>.analysis.md
updated_pages:
  - wiki/papers/...
  - wiki/methods/...
  - wiki/concepts/...
  - wiki/scenarios/...
  - wiki/relations/...
relation_candidates:
  proposes: []
  targets_task: []
  evaluated_on: []
  uses_concept: []
  supported_by: []
  cites: []
  applies_to: []
  based_on: []
  improves_on: []
  sourced_from: []
relation_exemptions:
  - relation_type: evaluated_on
    reason: no unified benchmark; exempt by graph-standard
warnings:
  - ...
skill_update_signals:
  - ...
```

解释：
- `success`：基础缓存、正式页面与应有关系账本更新都已完成，且结构适配良好。
- `partial`：完成了大部分工作，但某些页面、字段或正式关系账本仍需人工补充。
- `needs-skill-update`：当前论文类型或结构已经超出本 skill 的稳定适配范围。
- `relation_candidates`：必须显式列出本次论文直接支撑或高置信支持的 formal relation 候选，供后续 relation reconciliation 使用。
- `relation_exemptions`：若某类关系按规范豁免（例如 survey / framework 论文无统一 benchmark，因此不生成 `evaluated_on`），必须在此显式说明；不要把正常豁免写成“待补充”。

## 触发 `needs-skill-update` 的典型例子
- “这是一篇 benchmark/survey/framework 论文，当前方法页模板不是最佳落点。”
- “方法章节缺失，无法稳定抽取单一核心方法。”
- “实验细节主要在 appendix，当前 `experiments.md` 只能部分生成。”
- “taxonomy 难以稳定归类，建议为此类论文扩展 frontmatter 或页面模板。”
- “该论文更适合生成 `analysis.md` 而不是 `experiments.md`，当前 skill 若仍硬套实验缓存说明分流规则不足。”

## 质量要求
- 优先保证知识提炼可复用，而不是追求一次性写得很长。
- 不要把 PDF 的解析噪声直接带入 wiki 页面。
- 缓存层保真，知识页抽象。
- 对已存在页面做增量更新，避免重复造页。
- 用户一旦明确了关注方向，相关提取与批注必须优先服务该方向。

## 示例
### 示例 1：标准方法论文
输入：
- `处理论文：raw/PathMind.pdf，重点看方法演化`

预期：
- 生成 3 个缓存（`sections`、`refs`、`experiments`）
- 创建/更新 paper + method + concept + scenario + relation 页面
- 重点输出 PathMind 相对 RoG / GCR / EPERM 的演化关系

### 示例 2：结构异常论文
输入：
- `处理论文：raw/某篇benchmark论文.pdf，重点看评测设计`

预期：
- 尽量生成 4 个缓存
- 不要强行把它当普通方法论文完整落库
- 输出 `needs-skill-update` 或 `partial`
- 指出该类 benchmark 论文可能需要专门模板

## 使用完成后的建议
若输出为 `partial` 或 `needs-skill-update`，应在回复中明确说明：
- 哪些内容已经完成
- 哪些内容仍不稳定
- 当前 skill 该如何升级，才能更好适配这类论文
- 若某类关系因规范豁免未生成，应明确区分“正常豁免”与“skill 漏写”，避免把豁免项误报为待补。

## Ingest 完成后的后续治理要求
当本次摄入已经完成缓存、wiki 页面与候选关系输出后：
1. 必须先交给 `relation-reconciliation` 补齐 formal relation ledger
2. relation ledger 更新后，必须交给 `page-projection-sync` 回写对象页投影
3. 然后运行 `python3 scripts/lint_graph.py`
4. lint 通过后，必须调用 `ontology-semantic-review` skill 审查语义合理性
5. 如本次改动涉及 serving-ready 页面，还必须调用 `serving-governance-review`
6. 只有结构、语义与 serving 都合理时，才建议接受本次变更并进入 git 提交
