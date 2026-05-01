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
2. 默认执行完整摄入流程：PDF 解析 → 全部缓存 → wiki 多对象落库 → 关系更新 → index/log 更新。
3. 每次都要主动寻找与现有知识库的关联，不孤立处理论文。
4. 优先生成可复用缓存，避免后续重复从 PDF 直接解析。
5. 如果论文结构不适配当前模板，不要硬套；要显式降级并发出 skill 需要升级的信号。

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

### Step 3: 生成全部 intermediate 缓存
在 `intermediate/papers/` 下默认生成以下 4 个文件：

所有论文都生成：
1. `[short_name].sections.md`
2. `[short_name].refs.md`
3. `[short_name].full.md`

第 4 个缓存按论文类型分流：
- 方法 / 应用 / empirical 论文：`[short_name].experiments.md`
- survey / framework / benchmark / taxonomy / dataset 论文：`[short_name].analysis.md`

生成要求：
- `sections.md` 是默认分析入口
- `refs.md` 服务引用关系与方法演化
- `experiments.md` 仅用于实验、消融、效率、泛化信息
- `analysis.md` 用于综述统计、landscape、阶段分析、software-gap 分析、framework 支撑证据或 benchmark 设计分析
- `full.md` 是高保真工作底稿，不是逐字 OCR 转录，而是面向后续分析复用的高保真重写版

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
6. 关联关系：
   - `wiki/relations/citation_graph.md`
   - `wiki/relations/method_evolution.md`
   - 必要时 `wiki/relations/concept_links.md`
6. 更新：
   - `wiki/index.md`
   - `wiki/log.md`

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
  - intermediate/papers/<short_name>.full.md
updated_pages:
  - wiki/papers/...
  - wiki/methods/...
  - wiki/concepts/...
  - wiki/scenarios/...
  - wiki/relations/...
warnings:
  - ...
skill_update_signals:
  - ...
```

解释：
- `success`：完整缓存与落库都已完成，且结构适配良好
- `partial`：完成了大部分工作，但某些页面或字段仍需人工补充
- `needs-skill-update`：当前论文类型或结构已经超出本 skill 的稳定适配范围

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
- 生成 4 个缓存
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
