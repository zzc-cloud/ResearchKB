---
name: process-paper
description: 作为 ResearchKB 单篇论文处理的默认统一入口，编排 `paper-ingest` → `relation-reconciliation` → `page-projection-sync` → `index-sync` → `python3 scripts/lint_graph.py` → `ontology-semantic-review` → `serving-governance-review`。Whenever 用户说“处理论文：...”或给出单篇 PDF 路径并希望完成完整落库时，都应优先使用本 skill；若用户明确要求只做某一局部阶段，则让对应阶段 skill 直接处理。
---

# Process Paper

你是 ResearchKB 的单篇论文编译链编排入口。你的任务不是重做各阶段的领域逻辑，而是为“处理论文”意图提供稳定的默认入口、阶段顺序控制、交接验收与失败停止规则。

## 何时使用
- “处理论文：...”
- “摄入论文：...”且语义上是在请求完整单篇论文编译链
- 给出单篇 PDF 路径并希望完成完整落库，而不是只做某一阶段

## 不应抢夺的情形
- 用户明确要求只做 `paper-ingest`
- 用户明确要求只做 `relation-reconciliation`
- 用户明确要求只做 `page-projection-sync`
- 用户明确要求只跑 `index-sync`
- 用户明确要求只做 `ontology-semantic-review`
- 用户明确要求只做 `serving-governance-review`

## 你的职责
1. 识别“处理单篇论文”的完整编译意图
2. 依次调用现有阶段 skill / 命令
3. 检查仓库正式产物与结构化阶段摘要，决定是否可进入下一阶段
4. 在阻塞态出现时停止流程，并明确报告停在哪一阶段

## 阶段顺序
1. `paper-ingest`
2. `relation-reconciliation`
3. `page-projection-sync`
4. `index-sync`
5. `python3 scripts/lint_graph.py`
6. `ontology-semantic-review`
7. `serving-governance-review`

## 阶段交接合同
### ingest → reconciliation
进入下一阶段前，必须同时满足：
- `paper-ingest` 的结构化摘要中存在：`status`、`generated_caches`、`updated_pages`、`relation_candidates`
- `status` 不是阻塞态
- `generated_caches` 对应的最小 Evidence cache 文件已实际写入仓库
- `updated_pages` 中至少包含当前 Paper 页，或存在等价的 paper object 写入结果

若任一项缺失，不进入 `relation-reconciliation`。

### reconciliation → projection
进入下一阶段前，必须同时满足：
- `relation-reconciliation` 的结构化摘要中存在：`status`、`already_present`、`added`、`exempt`、`needs_human_review`、`affected_pages`
- `status` 允许继续
- `affected_pages` 已明确列出需要同步 projection 的对象页
- 若摘要声明新增 formal relation，则对应 ledger 文件已实际写入仓库

若缺少 `affected_pages`，或 formal relation 只停留在口头总结而未写入 ledger，不进入 `page-projection-sync`。

### projection → index
进入下一阶段前，必须同时满足：
- `page-projection-sync` 的结构化摘要中存在：`status`、`projected_pages`、`manual_followups`
- `status` 允许继续
- `projected_pages` 已明确列出本轮完成 projection 的页面
- `projected_pages` 是 projection 阶段页面清单的标准主交接字段；不得以旧字段名 `synced_pages` 替代

若 projection 结果只有模糊说明、没有结构化页面清单，不进入 `index-sync`。

### index → lint/reviews
进入下一阶段前，必须同时满足：
- `index-sync` 的结构化摘要中存在：`status`、`synced_indexes`、`skipped_pages`、`manual_followups`
- `status` 允许继续
- `synced_indexes` 或 `skipped_pages` 至少其一非空，能够说明 index 阶段实际处理了什么

若 index 阶段没有结构化结果清单，不进入 lint / review。

## 治理推进规则
- lint 必须通过，才能继续 `ontology-semantic-review`
- `ontology-semantic-review` 必须按其固定报告模板输出；`总体结论` 为 `fail` 或 `最终建议` 为 `reject` 时，视为阻塞
- `ontology-semantic-review` 的 `总体结论` 为 `pass-with-issues`，或 `最终建议` 为 `revise-then-accept` 时，不进入“正式入图完成”状态
- `serving-governance-review` 的输出状态为 `needs_fixes` 时，整条链只能汇报为 `partial`
- `serving-governance-review` 的输出状态为 `blocked` 时，整条链汇报为 `blocked`
- 只有 lint 通过、ontology semantic review 非阻塞、serving governance 为 `pass` 时，才能汇报 `success`

## 失败处理
- 任一步若返回阻塞态，则停止后续阶段
- 不允许跳过 relation / projection / index / governance 后仍宣称完成
- 若 `paper-ingest` 输出 `partial` 或 `needs-skill-update`，必须明确说明当前处理链停在 ingest
- 若 `ontology-semantic-review` 输出 `pass-with-issues` / `revise-then-accept`，必须明确说明当前处理链停在语义治理整改态
- 若 `serving-governance-review` 输出 `needs_fixes`，必须说明已写入产物与待修复项

## 阶段交接读取面
- `paper-ingest`：读取新写入的 Evidence 缓存、对象页候选、`ontology/log.md` 更新，以及结构化摘要中的 `generated_caches`、`updated_pages`、`relation_candidates`、`relation_exemptions`。
- `relation-reconciliation`：读取正式 relation ledger、必要时 materialize 的 partial Method / paper stub，以及结构化摘要中的 `already_present`、`added`、`exempt`、`needs_human_review`、`affected_pages`。
- `page-projection-sync`：读取已更新对象页 / Evidence 页，以及结构化摘要中的 `projected_pages`、`manual_followups`。
- `index-sync`：读取 `ontology/entities/*/index.md` 与其他受管导航页，以及结构化摘要中的 `synced_indexes`、`skipped_pages`、`manual_followups`。
- `ontology-semantic-review`：读取固定报告模板中的 `总体结论` 与 `最终建议`。
- `serving-governance-review`：读取其明确给出的 serving verdict：`pass` / `needs_fixes` / `blocked`。

## 停止条件
- 缺少下一阶段所需的正式产物时停止，并报告缺失项。
- 任一阶段返回 `blocked`、`needs-skill-update`、无法继续 reconciliation / projection / governance 的状态时停止。
- lint 未通过时，不进入 `ontology-semantic-review`。
- `ontology-semantic-review` 出现 `fail` / `reject` 时，不进入 serving completion；出现 `pass-with-issues` / `revise-then-accept` 时，仅保留整改态，不宣称正式入图完成。
- `serving-governance-review` 为 `needs_fixes` 时，整条链最多汇报为 `partial`。
- `serving-governance-review` 不通过时，整条链只能汇报为未完成。

## 汇报格式
```yaml
status: success | partial | blocked
stopped_stage: none | paper-ingest | relation-reconciliation | page-projection-sync | index-sync | lint | ontology-semantic-review | serving-governance-review
completed_stages: []
written_artifacts: []
next_required_action: none | fix-and-rerun | human-review
notes: []
```

## 结果语义
- `success`：七个阶段全部完成，且 lint、本体语义审查、serving 治理全部通过。
- `partial`：已经完成前若干阶段并写入部分正式产物，但在某个允许保留中间状态的阶段停止，尚不能宣称正式入图完成。
- `blocked`：出现阻塞条件，无法继续推进当前处理链。

## 边界
- 不重新解析 PDF 细节，不替代 `paper-ingest`。
- 不直接改写 formal relation 语义判断，不替代 `relation-reconciliation`。
- 不直接决定对象页投影内容，不替代 `page-projection-sync`。
- 不直接决定 index 收录，不替代 `index-sync`。
- 不重复做 lint、ontology semantic review 或 serving governance review 的领域判断；它只负责编排、交接检查与状态汇报。
