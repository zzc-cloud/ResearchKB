## 关系语义说明
- `sourced_from` 表示 Evidence 对象页来源于 `ontology/entities/raw-sources/files/` 下的受管原始文件。
- 合法 source：`Evidence`。
- 合法 target：`RawSource`。
- 正式知识页应优先通过 `supported_by` 连接到 Evidence，而不是直接连接原始 PDF。
- 若证据对象页尚未生成而必须临时登记来源，可例外使用 `status: placeholder` 暂存。

## 实例边
- 无
