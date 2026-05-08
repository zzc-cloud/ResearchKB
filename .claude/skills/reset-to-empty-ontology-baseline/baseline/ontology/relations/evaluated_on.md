> 本页是正式关系账本：维护 `evaluated_on` 实例边。默认问答优先读取 benchmark 页、方法页或论文页；只有在 benchmark 绑定治理、修复、审计或真源核对时优先读取本页。
>
> 相关对象域：[[../entities/benchmarks/index|benchmarks/index]]、[[../entities/methods/index|methods/index]]、[[../entities/papers/index|papers/index]]
> 相关证据入口：[[supported_by]]

## `evaluated_on` 实例边
- `evaluated_on` 表示方法或论文在某个正式 benchmark 上进行了评估。
- 常见 source：`Method`、`Paper`
- 常见 target：`Benchmark`
- empirical / method / application 论文若存在明确 benchmark，默认应在此登记；无统一 benchmark 的 survey / framework / taxonomy 论文可按规范豁免。

## 实例边
