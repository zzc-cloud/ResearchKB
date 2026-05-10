# Live-Derived Empty Ontology Reset Design

日期：2026-05-10

## 1. 目标

把 `/reset-to-empty-ontology-baseline` 明确重构为 **live-derived reset**，使其在不依赖静态 `baseline/` 快照的前提下，把当前 `ontology/` 重置到“当前 live 结构下的空图状态”。

完成后的 reset 行为应满足：

- 保留对象域 `index.md` 文件本身
- 保留 `ontology/entities/raw-sources/index.md`
- 保留 `ontology/entities/raw-sources/files/*.pdf`
- 删除对象实例页
- 清空 formal relation ledger 的实例边内容
- 重写 `ontology/log.md` 为统一空日志
- 清理对象域 `index.md` 中指向实例页的受管入口块
- 立即运行 `python3 scripts/lint_graph.py`，并以 lint 结果作为成功标准

## 2. 问题与根因

当前 skill 失败的根因不是“缺少 baseline”，而是 reset 实现不完整。

现实现仅做三件事：

1. 删除对象实例页
2. 清空 relation ledger
3. 重写 `ontology/log.md`

但没有同步清理各对象域 `index.md` 中仍然存在的受管实例入口，因此在实例页被删除后，index 继续保留对这些页面的 wikilink，最终触发 `missing index entry target file`。

这说明当前问题本质上是：

> reset 只清除了实例文件，没有清除从 index 指向这些实例文件的受管导航投影。

## 3. 设计结论

本 skill 应采用 **单一真源的 live-derived reset**，而不是维护第二套 `baseline/` 快照。

原因：

- `baseline/` 会形成与 live ontology 并行的第二份结构真源，容易漂移
- relation 类型、index 结构、log 基线都会随着 live 结构演进，静态快照难以长期同步
- reset 的真正语义是“在当前 live schema 上清空图内容”，而不是“从另一份模板恢复”

因此，正确方案应是：

- 基于当前 live 目录与文件格式执行结构化清理
- 仅清空实例内容与 index 中的受管导航块
- 保留 live 结构说明文字与目录骨架

## 4. 推荐方案

### 4.1 总体行为

reset 执行时按以下顺序进行：

1. 检查 `ontology/` 是否存在未提交变更
2. 删除各对象域中的实例页，仅保留 `index.md`
3. 清空 `ontology/relations/*.md` 中的实例边区块
4. 重写 `ontology/log.md` 为空日志
5. 清理对象域 `index.md` 中的受管入口块内容
6. 运行 `python3 scripts/lint_graph.py`
7. 仅当 lint 通过时，报告 reset 成功

### 4.2 对象实例页删除范围

继续使用当前对象域范围：

- `papers`
- `methods`
- `concepts`
- `tasks`
- `scenarios`
- `benchmarks`
- `evidence`

行为要求：

- 删除这些目录下所有非 `index.md` 的 `.md` 文件
- 不删除目录本身
- 不触碰 `raw-sources/`

### 4.3 relation ledger 清空规则

对 `ontology/relations/*.md`：

- 保留 relation 页面顶部说明文字
- 保留 relation type 的语义说明段落
- 保留 `## 实例边` 标题
- 将 `## 实例边` 下的内容统一清空为：
  - `- 无`

这保证 relation 页面仍保持当前 live 格式，但 formal edge 内容被清空。

### 4.4 日志重写规则

`ontology/log.md` 应被重写为统一空日志基线，只保留系统入口说明，不保留历史操作记录。

目标语义是：

- reset 后的日志应表示“当前图为空且尚无后续操作记录”
- 不携带旧实例图历史

### 4.5 index 清理规则

这是本次 redesign 的关键。

对象域 `index.md` 必须执行 **受管块级别清理**，而不是整体替换文件。

原则：

- 保留 index 的标题、域说明、非受管 prose
- 仅清空明确受管的实例导航区块内容
- reset 后不应保留任何指向已删除实例页的 wikilink

当前最小清理范围包括：

- `<!-- BEGIN MANAGED BLOCK:navigation-entries --> ... <!-- END MANAGED BLOCK:navigation-entries -->`
- `<!-- BEGIN MANAGED BLOCK:non-serving-placeholders --> ... <!-- END MANAGED BLOCK:non-serving-placeholders -->`

清理后的结果应为：

- 保留 BEGIN/END 边界注释
- 边界之间内容置空

### 4.6 raw sources 保留规则

以下内容必须原样保留：

- `ontology/entities/raw-sources/index.md`
- `ontology/entities/raw-sources/files/*.pdf`

reset 不负责清理 raw source 目录，不应影响 provenance 原件。

## 5. skill 目录重构

### 5.1 应保留的文件

- `SKILL.md`
- `restore_baseline.py`

### 5.2 应删除的文件/目录

- `baseline/`
- `__pycache__/`

原因：

- `baseline/` 不再符合 live-derived reset 设计
- `__pycache__/` 是运行副产物，不属于 skill 逻辑资产

### 5.3 SKILL.md 语义修正

`SKILL.md` 中关于“保留当前各对象域 `index.md`”的表述需要精确化为：

- 保留对象域 `index.md` 文件本身
- 清理其受管导航区块，使其回到空图状态

避免再次把“保留 index 文件”误实现为“保留 index 原内容不变”。

## 6. 实现约束

### 6.1 不引入新的静态模板真源

实现中不得重新引入 `baseline/` 式模板目录来驱动 reset。

### 6.2 只改受管块，不改 prose

index 清理应只作用于明确受管块，不得改写：

- 标题
- 域说明文字
- 非受管说明段落

### 6.3 relation 清理维持当前 live 格式

relation ledger 的 reset 不应假设固定 relation 名单以外的外部模板；应直接遍历 live `ontology/relations/*.md`。

这保证当 relation type 增减时，reset 自动跟随 live 结构演进。

## 7. 失败与阻塞语义

### 7.1 dirty ontology

如果 `ontology/` 下存在未提交变更，默认中止，并提示只有在用户明确允许覆盖时才可使用 `--force`。

### 7.2 lint fail

如果 reset 后 lint 失败，则整个 reset 视为失败，而不是成功但附带 warning。

原因是：

- reset 的目标就是产出“可 lint 的空图状态”
- lint fail 说明空图状态仍然不自洽

## 8. 非目标

本设计不做以下事情：

- 不修改 `raw-sources/files/*.pdf`
- 不重写对象域 index 的 prose 结构
- 不引入新的对象域模板系统
- 不把 reset 扩展为 ingest、projection 或治理流程
- 不改变 `lint_graph.py` 对 ontology 合法性的总体判定标准

## 9. 验收标准

完成后必须满足：

1. reset 后各对象域实例页被清空，仅剩 `index.md`
2. `raw-sources/index.md` 与 PDF 原件全部保留
3. `ontology/relations/*.md` 仅保留空实例边状态
4. `ontology/log.md` 被重写为空日志基线
5. 各对象域 `index.md` 不再保留指向已删除实例页的受管入口链接
6. `python3 scripts/lint_graph.py` 在 reset 后通过
7. skill 目录中不再保留 `baseline/`

## 10. 推荐落地顺序

1. 先更新 `SKILL.md`，明确 live-derived reset 语义
2. 再修改 `restore_baseline.py`，加入 index 受管块清理逻辑
3. 删除 `baseline/` 与 `__pycache__/`
4. 运行 reset 与 `python3 scripts/lint_graph.py` 验证结果
5. 最后确认 reset 后 ontology 处于可继续 cold-start ingest 的空图状态
