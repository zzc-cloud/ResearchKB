# Reset to Empty Ontology Baseline Redesign

## Goal
把 `reset-to-empty-ontology-baseline` skill 重构为一个**以当前 live ontology 结构为准**的 reset 工具，用于把 ResearchKB 恢复到可重复执行 cold-start ingest / relation / projection / governance 回归测试的空图状态，同时避免 baseline 快照随着对象页与 relation ledger 格式演化而失效。

## Confirmed reset semantics
本次重构确认的 reset 目标如下：

- 保留 `ontology/graph-standard.md` 原样不动
- 保留各对象域当前 live 的 `index.md`
- 保留 `ontology/entities/raw-sources/index.md`
- 保留 `ontology/entities/raw-sources/files/*.pdf`
- 删除所有具体对象实例页：`papers`、`methods`、`concepts`、`tasks`、`scenarios`、`benchmarks`、`evidence` 下除 `index.md` 之外的 `.md` 文件
- relation ledger 不再从静态 baseline 覆盖，而是以**当前 live relation 文件**为准，保留说明结构，清空“实例边”内容
- `ontology/log.md` 重置为空日志基线
- reset 完成后必须立即通过 `python3 scripts/lint_graph.py`

这里的关键语义是：

- reset 后**目录里不保留任何具体对象页实例文件**
- 对象页的当前结构契约由后续 ingest / projection 流程负责重新生成，而不是由 reset 写回静态空模板
- relation ledger 的结构契约由当前 live 文件定义，reset 只负责把知识实例内容归零

## Why the current skill is not sufficient
当前 skill 失败的根因不是“不会删文件”，而是它依赖了会老化的静态 baseline：

1. `baseline/ontology/entities/` 只有 index 快照，不再代表当前对象页体系
2. `baseline/ontology/relations/*.md` 的 ledger 文案格式已经落后于当前 live 版本
3. `restore_baseline.py` 直接复制 baseline 文件，会把 reset 结果固定在历史结构，而不是当前系统真实形态

因此，只要对象页结构或 relation ledger 格式继续演化，当前 skill 就会继续失真。

## Chosen approach
采用 **live-derived reset**：

### 1. 对象域处理
- 不再从 baseline 恢复 `papers/`、`methods/`、`concepts/`、`tasks/`、`scenarios/`、`benchmarks/`、`evidence/` 目录内容
- 这些目录保留当前 live 的 `index.md`
- 删除目录内其他所有 `.md` 实例页
- `raw-sources/` 是例外：保留当前 live 的 `index.md` 与 `files/` 中的 PDF，不清空 provenance 原件

### 2. Relation ledger 处理
- 不再使用 `baseline/ontology/relations/*.md` 作为真源
- 对每个当前 live relation ledger：
  - 读取当前文件
  - 保留现有标题、关系语义说明、合法 source/target 文案等结构
  - 定位 `## 实例边` 区块
  - 将该区块内容清空为当前空账本表示（默认 `- 无`）
- 这样 reset 后 relation 文件仍然符合当前 live 格式，但 formal relation truth 被清零

### 3. Log 处理
- `ontology/log.md` 不再简单复制旧 baseline 内容
- 改为写入一个固定的空日志基线，至少保留：
  - 标题 `# 操作日志`
  - 系统级导航
  - 图谱规范入口
- 不保留既有 ingest / cache / optimize 等历史条目

### 4. 规范文件处理
- `ontology/graph-standard.md` 完全不动
- skill 只作用于知识状态层，而不改动全局规范真源

## Design trade-offs
### Approach A — live-derived reset（chosen）
- **优点**：总是对齐当前 live 格式，不再受 baseline 老化影响；最符合“reset 到当前系统空图状态”的目标
- **缺点**：需要在脚本里实现 relation ledger 的结构化清空逻辑，而不是简单复制目录

### Approach B — hybrid reset
- relations 用 live-derived；index / log 仍从 baseline 恢复
- **优点**：实现更小
- **缺点**：baseline 仍可能在 index / log 上继续老化，不能彻底解决 drift

### Approach C — hardcoded templates
- 由脚本维护 relation / log / index 空模板
- **优点**：行为可控
- **缺点**：只是把老化位置从 baseline 挪到脚本，仍不符合“以当前 live 为准”

## File-level implementation plan
### Existing files to modify
- `.claude/skills/reset-to-empty-ontology-baseline/SKILL.md`
- `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
- `scripts/test_lint_graph.py`

### Existing files likely no longer authoritative
- `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/relations/*.md`
- `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/entities/*/index.md`
- `.claude/skills/reset-to-empty-ontology-baseline/baseline/ontology/log.md`

这些 baseline 文件可以先保留，但不再作为 reset 真源；后续可视需要精简或删除。

## Restore script behavior
`restore_baseline.py` 应调整为以下行为：

1. 运行 `git status --short -- ontology` 检查 ontology 是否 dirty
2. 若 dirty 且没有 `--force`，返回 `blocked`
3. 若允许继续：
   - 对各对象域目录删除除 `index.md` 之外的 `.md` 文件
   - 确保 `raw-sources/files/` 不受影响
   - 对 `ontology/relations/*.md` 逐个做 live-derived 清空
   - 写入空日志基线到 `ontology/log.md`
4. 运行 `python3 scripts/lint_graph.py`
5. 仅当 lint 通过时返回 success

## Relation ledger clearing contract
relation 清空逻辑必须面向**当前 ledger 结构**，而不是旧格式假设。最低要求：

- 找到 `## 实例边` 标题
- 保留该标题之前的全部内容
- 将标题之后内容替换为：

```md
## 实例边
- 无
```

这意味着 reset 默认假设当前 live ledger 以 `## 实例边` 作为实例区块锚点。若未来该锚点命名变更，测试应先失败，再显式更新 skill。

## Safety model
reset 仍然是覆盖性操作，因此保留现有安全模型：

- 默认检查 `ontology/` 未提交修改
- 若存在未提交修改且未显式授权覆盖，则中止
- 只有用户明确允许覆盖时才可用 `--force`

这样可以防止误删当前知识维护成果。

## Testing strategy
本次重构应以测试先行验证语义，至少覆盖以下场景：

1. **check-only on dirty ontology**
   - 当前 `ontology/` 有改动时，`--check-only` 仍返回 blocked
2. **relation ledger clearing**
   - 给定一个带实例边的 relation 文件，运行清空逻辑后保留说明结构，仅把 `## 实例边` 归零为 `- 无`
3. **entity instance cleanup**
   - 对象域目录中的非 `index.md` 页面被删除；`index.md` 保留
4. **raw source preservation**
   - `raw-sources/files/` 中的 PDF 不被删除
5. **log reset**
   - `ontology/log.md` 被重写为空日志基线
6. **lint after reset**
   - reset 完成后 `python3 scripts/lint_graph.py` 通过

## Success criteria
当 skill 重构完成后，应满足：

1. reset 后 ontology 中不再保留任何知识对象实例页
2. raw source PDFs 仍然可用于后续单篇论文 ingest
3. relation ledgers 仍然使用当前 live 格式，但 formal relation truth 清零
4. `ontology/log.md` 为空日志基线
5. `ontology/graph-standard.md` 未被改动
6. `python3 scripts/lint_graph.py` 立即通过
7. 紧接着可以对任意单篇 PDF 执行 cold-start 编译链测试

## Open implementation note
本设计明确选择“不保留任何具体对象页空骨架文件”。对象页结构契约由后续 `paper-ingest` / `page-projection-sync` 生成流程保证，而不是由 reset skill 维护静态模板。这样可以避免对象页格式再次因为 baseline 快照老化而漂移。
