# Ontology Semantic Review Reference Path Fix Design

日期：2026-05-09

## 1. 目标

修复 `ontology-semantic-review` 在单篇论文编译链中的断链问题，使其能够在 `python3 scripts/lint_graph.py` 通过后继续正常执行。

本次修复只解决一个明确问题：

- skill 文档声明要读取仓库根目录下的 `references/...`
- 实际 reference 文件位于 `.claude/skills/ontology-semantic-review/references/...`
- 因此第 6 步 `ontology-semantic-review` 会因路径不一致而中断

## 2. 问题定义

当前文件 [`.claude/skills/ontology-semantic-review/SKILL.md`](.claude/skills/ontology-semantic-review/SKILL.md) 在以下位置引用了错误路径：

- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`

但仓库内真实存在的文件是：

- `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

这说明根因不是语义审查逻辑缺失，也不是 reference 文件缺失，而是 **skill 合约与实际文件布局不一致**。

## 3. 修复范围

本次只修改：

- [`.claude/skills/ontology-semantic-review/SKILL.md`](.claude/skills/ontology-semantic-review/SKILL.md)

本次不修改：

- 其他 skill
- 仓库根目录结构
- `ontology-semantic-review` 的 verdict 语义
- 语义审查报告模板内容
- `paper-ingest` / `relation-reconciliation` / `page-projection-sync` / `index-sync` 的行为

## 4. 选定方案

采用最小修复方案：**仅把 `ontology-semantic-review` skill 中所有错误的根路径引用，改为指向 skill 自己目录下真实存在的 reference 文件。**

### 为什么选择这个方案

- 改动最小，直接对准断链根因
- 不引入新的共享目录决策
- 不需要复制 reference 文件
- 不扩大到其他流程或规范迁移
- 能最快恢复单篇论文编译链的第 6 步

## 5. 具体改法

### 5.1 修改“先阅读”列表

将：

- `references/review-output-template.md`
- `references/review-scope-rules.md`
- `references/diff-review-playbook.md`

改为：

- `.claude/skills/ontology-semantic-review/references/review-output-template.md`
- `.claude/skills/ontology-semantic-review/references/review-scope-rules.md`
- `.claude/skills/ontology-semantic-review/references/diff-review-playbook.md`

### 5.2 修改正文中的约束说明

把所有类似下面的表述同步改掉：

- “必须使用 `references/review-output-template.md` 中的报告格式与 verdict 语义”
- “必须使用 `references/review-output-template.md` 的固定结构输出一份语义审查报告”

统一改为指向 skill 本地真实路径，确保：

- 输入依赖路径一致
- 输出约束路径一致
- 执行者不会再被不存在的根目录路径误导

### 5.3 做全文残留检查

修复后需要确认 [`.claude/skills/ontology-semantic-review/SKILL.md`](.claude/skills/ontology-semantic-review/SKILL.md) 中不再残留任何 `references/...` 根路径写法。

## 6. 验证方案

### 6.1 静态验证

验证以下条件成立：

1. skill 文档中不再引用不存在的根目录 `references/...`
2. skill 文档中的 3 个 reference 路径全部存在于磁盘
3. “先阅读”与“输出要求”引用的是同一套真实文件

### 6.2 流程验证

按最小闭环验证：

1. 重新触发 `ontology-semantic-review`
2. 确认不再因缺少 reference 文件而中断
3. 让单篇论文编译链可以继续进入第 6 步与第 7 步

## 7. 风险与回滚

### 风险

风险很低，主要有两类：

1. 漏改某一处旧路径，导致 skill 仍然部分断链
2. “先阅读”与“输出要求”指向不同路径，形成新的不一致

### 回滚

如果修复不合适，只需还原 [`.claude/skills/ontology-semantic-review/SKILL.md`](.claude/skills/ontology-semantic-review/SKILL.md)。

因为本次不涉及：

- ontology 内容页
- relation ledger
- lint 脚本逻辑
- 目录结构调整

所以回滚成本极低。

## 8. 验收标准

修复完成后，必须同时满足：

1. `ontology-semantic-review` 不再引用不存在的 `references/...`
2. 所有相关描述统一指向 `.claude/skills/ontology-semantic-review/references/...`
3. 第 6 步 `ontology-semantic-review` 可被正常执行，不再因 reference 路径错误断链
4. 本次修复不额外引入根目录 `references/`，不扩大为共享规范迁移

## 9. 为什么这是最小正确修复

当前故障根因是 **skill 文档路径声明错误**，而不是 reference 资源缺失。因此最小正确修复应当是：

- 让 skill 合约重新对齐当前真实文件布局

而不是：

- 新增一套根目录 `references/`
- 复制现有 reference 文件
- 顺带重构语义审查体系
- 扩大到其他 skill 的路径治理

这保证修复既正确，又不会因为“顺手做更多”而引入额外变化。
