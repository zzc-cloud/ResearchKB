## 关系语义说明
- `supported_by` 表示正式知识对象页由 Evidence 对象页支撑。
- 合法 source：`Method`、`Task`、`Scenario`、`Benchmark`。
- 合法 target：`Evidence`。
- `Paper` 不再作为 `supported_by` 的 source；Evidence 与 Paper 之间也不单独建立 formal relation。
- 若同一正式知识对象由多个证据缓存支撑，应拆为多条独立实例边。

## 实例边
- 无
