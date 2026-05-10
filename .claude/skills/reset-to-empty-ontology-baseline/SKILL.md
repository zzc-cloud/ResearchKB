---
name: reset-to-empty-ontology-baseline
description: 把 ResearchKB 的 ontology 重置到当前 live 结构下的空图状态，用于 cold-start ingest / relation / projection / governance 回归测试。Whenever 用户要求恢复空骨架、清空 ontology 但保留当前导航骨架与 raw PDFs、或为单篇论文测试重置图谱时，都应使用此 skill。
---

# Reset to Empty Ontology Baseline

## Purpose
把 `ontology/` 重置到当前 live 结构下的空图状态：
- 保留对象域 `index.md` 文件本身，但清理其受管导航区块
- 保留 `ontology/entities/raw-sources/index.md`
- 保留 `ontology/entities/raw-sources/files/*.pdf`
- 删除对象实例页
- 将 `ontology/relations/*.md` 清空为当前 live 格式的空账本
- 将 `ontology/log.md` 重写为空日志基线
- 立即运行 `python3 scripts/lint_graph.py` 验证结果

## Safety
- 默认先检查 `git status --short -- ontology`
- 若 `ontology/` 下存在未提交改动，则默认中止
- 只有用户明确允许覆盖时，才可带 `--force` 执行恢复

## Execution
1. 运行 `.claude/skills/reset-to-empty-ontology-baseline/restore_baseline.py`
2. 如用户已确认覆盖当前 ontology，则附加 `--force`
3. 成功后回报 lint 结果与保留项（indexes / raw PDFs）

## Output
```yaml
status: success | blocked | failed
lint: pass | fail
warnings: []
manual_followups: []
```
