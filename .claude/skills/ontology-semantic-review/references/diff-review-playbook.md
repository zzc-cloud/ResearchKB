# 基于 diff 的语义审查步骤
1. 阅读当前 git diff 或本次修改文件列表。
2. 阅读 `ontology/graph-standard.md` 以及各关系账本文件。
3. 为本次改动涉及的每个节点做分类判断。
4. 对每一条变更关系，依次判断：
   - 这条关系本身是否成立？
   - 它是否放在了正确的关系文件里？
   - 它表达的是局部证据支撑，还是本体层正式关系？
5. 最后按统一模板输出语义审查报告。

## 特别检查项
- 如果 survey 被表示成 task，必须指出。
- 如果 framework 被表示成 method，必须指出。
- 如果 `uses_concept.md` 中出现“概念 → 论文支撑”关系，必须指出，并建议迁移到概念页证据区或 `supported_by.md`。
- 如果 `based_on.md` 中出现文献支撑关系而不是实际技术谱系，必须指出。
- 如果改进、前提依赖、场景适配或概念性支撑语义被单独升格为 formal relation，必须指出，并建议下沉到 `edge_semantics`、frontmatter 或对象页正文。

## Projection-format review prompts
- 若 diff 修改了对象页 `Formal relations`，检查是否仍在使用完整边字符串而不是半展开格式。
- 若 diff 修改了 Evidence 页，检查是否新增了指向 Paper 的正文链接。
- 若 diff 修改了对象页正文，检查新增 wikilink 是否已经在 `Formal relations` 中投影。
- 若 diff 修改了 `supported_by` ledger，检查是否把 `Paper` 放入 source。
- 若 diff 修改了 relation 页，检查“关系语义说明区”是否仍然描述合法 source / target 类型。
- 若 diff 修改了 relation 页，检查其是否清楚区分 formal relation truth 与 context-only semantics。
- 若 diff 修改了 relation 页，检查其是否避免重新引入基于 wikilink 的导航型噪声。
- 若 diff 修改了 relation ledger，检查 `reason` 是否已统一迁为 `edge_semantics`。
- 若 diff 修改了对象页 `Formal relations`，检查每条实例投影是否同时保留 `edge_semantics` 与 `evidence`。
- 若 diff 修改了对象域 index，检查入口项是否投影 `object_semantics` 而不是自由 trailing prose。
