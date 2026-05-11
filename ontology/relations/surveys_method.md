## 关系语义说明
- `surveys_method` 表示综述论文、landscape 论文、taxonomy 论文或其他 survey-role 论文将某方法纳入其系统梳理、分类、比较或 coverage 范围。
- 合法 source：`Paper`。
- 合法 target：`Method`。
- 该关系不表示方法被首次提出；若论文首次提出或正式定义该方法，应使用 `proposes`。
- 该关系也不等同于普通 `cites`；仅有引用事实、背景 mention 或零散 related-work 提及，不足以生成 `surveys_method`。
- 证据应优先来自 `analysis.md` 或 survey-oriented `sections.md` 中的结构化 coverage 内容，而不是默认从 `refs.md` 升格。

## 实例边
- 无
