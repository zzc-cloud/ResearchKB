# paper-ingest 关系自动落账设计

## 日期
2026-05-02

## 背景
前一阶段已经在 ResearchKB 主图谱中为 `proposes`、`evaluated_on`、`sourced_from` 建立了正式账本与 lint 护栏，但当前 `paper-ingest` skill 仍停留在“会更新若干关系页”的宽泛表述，没有把这三类关系纳入默认输出义务。

这意味着：
- ontology 层已经承认这三类关系
- 实例边层已经有正式落点
- lint 也能在缺失时报错
- 但 ingest 流程本身仍可能继续静默漏写这些边

用户已明确要求：如果论文中存在这三类关系边，就应像其他关系边一样**自动正式写入**，而不是依赖人工确认；只有在规范本身允许豁免时，才不生成，并明确写出豁免原因。

## 目标
在不重构 `paper-ingest` 的前提下，把 `proposes`、`evaluated_on`、`sourced_from` 纳入 skill 的默认关系落账流程，使后续 ingest 新论文时：

1. 能自动把这三类关系写入对应账本
2. 对 survey / framework / taxonomy 且无统一 benchmark 的论文，不伪造 `evaluated_on`，而是在输出中显式写豁免原因
3. 与现有 `cites`、`based_on`、`supported_by` 等关系保持同级义务，而不是“有空再补”
4. 与现有 lint 护栏形成闭环，减少未来静默漏边

## 非目标
- 不改 ResearchKB 的 ontology 结构
- 不重构整个 `paper-ingest` skill 的章节顺序
- 不引入人工确认分支或 placeholder-first 流程
- 不把 framework 型 concept 改成 method
- 不在这一步修改主库 wiki 页面或账本实例；本次只改 skill 本身及其必要 eval/说明

## 设计原则
- **自动落账优先**：存在且可判定的关系，直接正式写入
- **与其他关系一致**：新关系不应比 `cites` / `method_evolution` 有更弱的执行要求
- **豁免显式化**：对无统一 benchmark 的 survey / framework 论文，不写 `evaluated_on`，但必须说明原因
- **最小改动**：优先在现有 skill 文本中增加明确关系步骤，不拆 skill 架构
- **以 Evidence 驱动 provenance**：只要生成了缓存，就同步落 `sourced_from`

## 需要修改的文件
### 1. 主 skill
- `.claude/skills/paper-ingest/SKILL.md`

### 2. 评测素材（如当前 skill 已维护 evals）
- `.claude/skills/paper-ingest/evals/...`

是否修改 evals 取决于当前目录下已有内容的形式；若已有标准 eval 配置，则补充断言/案例；若只有最小占位，则至少补测试提示和预期行为说明。

## 对 `paper-ingest` 的结构性修改

### 一、扩展 Step 5 的关系更新范围
当前 skill 在 Step 5 中只明确列出：
- `citation_graph.md`
- `method_evolution.md`
- 必要时 `concept_links.md`

设计上应将其升级为“关系账本全量判断表”，明确要求在 ingest 时逐类检查是否应更新：
- `wiki/relations/citation_graph.md`
- `wiki/relations/method_evolution.md`
- `wiki/relations/concept_links.md`
- `wiki/relations/task_method_map.md`
- `wiki/relations/evidence_index.md`
- `wiki/relations/paper_method_links.md`
- `wiki/relations/benchmark_links.md`
- `wiki/relations/provenance_links.md`

这一步的重点不是让 skill 每次都机械更新所有文件，而是要求它**逐类判断是否存在应落账的关系**，只要存在就正式写入。

### 二、增加三类关系的明确抽取规则

#### `proposes`
自动抽取并正式写入：
- 方法论文：`[[Paper]] --proposes--> [[Method]]`
- 当论文核心贡献是 framework / taxonomy 型概念时：`[[Paper]] --proposes--> [[Concept]]`

这条规则用于覆盖两种常见情况：
1. 普通方法论文提出一个方法
2. survey / framework 论文提出一个框架型 concept

skill 中应显式说明：
- framework / taxonomy 型核心知识产物按当前本体仍落为 Concept
- 但其“由论文提出”这一事实，仍应使用 `proposes` 正式登记

#### `evaluated_on`
自动抽取并正式写入：
- empirical / method / application 论文：只要 `sections.md`、`experiments.md` 或正式论文页中存在明确 benchmark，即写 `Paper -> Benchmark`
- 若该论文同时为某个核心 Method 建页，且 benchmark 明确服务该方法评测，也写 `Method -> Benchmark`

豁免规则：
- survey / framework / taxonomy / dataset / benchmark 类型论文若无统一 benchmark，则**不写 `evaluated_on`**
- 但 skill 的最终输出必须明确说明：本次未生成 `evaluated_on`，原因是“无统一 benchmark，按规范豁免”

用户已明确选择这一路径，因此设计上不允许“硬从文献统计或阶段分析里凑 benchmark 边”。

#### `sourced_from`
自动抽取并正式写入：
- 只要本次 ingest 生成了任何 Evidence 缓存（`sections.md`、`refs.md`、`experiments.md`、`analysis.md`、`full.md`），就同步写：
  - `[[Evidence]] --sourced_from--> [[RawSource]]`

这里不需要额外判断论文类型；它与缓存生成是直接绑定关系。也就是说：
- 生成缓存 → 必须落 provenance 边

### 三、把三类关系从“可做”提升为“默认义务”
skill 目前的语言更像：
- 会生成页面
- 会更新若干关系页

设计上应改成：
- 在落库完成前，必须检查并更新所有相关正式关系账本
- `proposes`、`evaluated_on`、`sourced_from` 与 `cites`、`based_on`、`supported_by` 同属默认关系义务

这能避免模型把这三类边当作“补充优化项”。

## 对最终输出格式的修改
当前 `paper-ingest` 最终输出已经有：
- `generated_caches`
- `updated_pages`
- `warnings`
- `skill_update_signals`

应在语义上强化两件事：

### 1. `updated_pages` 必须体现关系账本更新
当本次生成了相关关系边时，输出中应明确列出：
- `wiki/relations/paper_method_links.md`
- `wiki/relations/benchmark_links.md`
- `wiki/relations/provenance_links.md`

### 2. `warnings` / `skill_update_signals` 必须区分“豁免”与“漏写”
例如：
- 正确：`未生成 evaluated_on：该论文为 survey / framework 类型且无统一 benchmark，按规范豁免`
- 不正确：`未生成 evaluated_on，待补充`

也就是说，skill 的输出要能让人分辨：
- 这是正常豁免
- 还是 skill 没判断出来 / 漏了

## 对 eval 的影响
如果 `paper-ingest` 目录下已有评测结构，建议同步补两个最小案例：

### Case 1：标准方法论文
例如 PathMind 类输入，预期：
- 生成 `proposes`
- 生成 `evaluated_on`
- 生成 `sourced_from`

### Case 2：survey / framework 论文
例如 LLM-KG-CPD Survey 类输入，预期：
- 生成 `proposes`
- 生成 `sourced_from`
- 不生成 `evaluated_on`
- 在输出中显式写 benchmark 豁免原因

这不是为了把 skill 做成复杂 benchmark 系统，而是为了防止未来改 skill 时把这次补上的规则再退化掉。

## 风险与对应处理
### 风险 1：framework 型 concept 和 method 混淆
处理：
- 在 skill 里明确引用当前 ontology 规则：framework / taxonomy 型核心知识优先落 Concept，不改 Method
- 但 `proposes` 允许 `Paper -> Concept`

### 风险 2：survey 论文被错误写出 `evaluated_on`
处理：
- 在 skill 中显式加入豁免判定，不允许从文献统计、阶段分析、landscape 里强凑 benchmark 边

### 风险 3：生成了缓存但漏 provenance
处理：
- 把 `sourced_from` 写成与 cache 生成同步触发的直接义务，而不是“关系页补充”

### 风险 4：skill 文案改了，但模型仍偶发漏写
处理：
- 保留现有主库 lint 护栏
- 让 skill 输出显式列出更新了哪些关系账本，便于人工快速复核

## 推荐实施顺序
1. 阅读当前 `paper-ingest/SKILL.md` 与 evals 目录
2. 在 SKILL.md 的 Step 5 / 关系规则 / 最终输出格式中补三类关系的自动落账要求
3. 明确 survey / framework 的 `evaluated_on` 豁免语言
4. 如 evals 已存在标准结构，补两个覆盖案例
5. 运行最小验证，确认 skill 文本与当前主库 ontology 一致

## 验收标准
完成后应满足：
1. `paper-ingest` 明确把 `paper_method_links.md`、`benchmark_links.md`、`provenance_links.md` 纳入默认关系更新范围
2. skill 文本中明确规定：
   - 有 `proposes` 就自动写
   - 有 benchmark 就自动写 `evaluated_on`
   - 有缓存就自动写 `sourced_from`
3. survey / framework / taxonomy 且无统一 benchmark 的论文，不写 `evaluated_on`，并显式说明豁免原因
4. 最终输出能区分“正常豁免”与“漏写/待补”
5. 如已有 eval 结构，新增的测试案例能覆盖“方法论文”和“survey 论文”两类行为
