---
title: PathMind: A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models
short_name: PathMind
source_pdf: /Users/yyzz/Desktop/MyClaudeCode/ResearchKB/raw/A Retrieve-Prioritize-Reason Framework for Knowledge Graph Reasoning with Large Language Models.pdf
cache_type: experiments
status: parsed
---

# PathMind 实验缓存

> 本文件面向“只看实验”的后续复用场景。若只需比较指标、消融、效率与泛化表现，优先读本文件，而不是整篇缓存或 PDF。

## 1. 数据集与指标
### 数据集
- WebQSP
- CWQ (Complex WebQuestions)

### 指标
- Hits@1
- F1

## 2. 实现设置
- LLM backbone：Llama3.1-8B
- 子图构造：3-hop 邻域
- GNN 用于学习节点和关系表示
- 每轮保留 top-3 节点
- 最大迭代数：WebQSP = 2，CWQ = 4
- 框架：PyTorch
- 训练硬件：2× NVIDIA A800 GPU

## 3. 总体结果（RQ1）
### PathMind 结果
| Dataset | Hits@1 | F1 |
|---|---:|---:|
| WebQSP | 0.895 | 0.728 |
| CWQ | 0.707 | 0.614 |

### 论文中可直接引用的强基线对比
| Method | WebQSP Hits@1 | WebQSP F1 | CWQ Hits@1 | CWQ F1 |
|---|---:|---:|---:|---:|
| EPERM | 0.888 | 0.724 | 0.662 | 0.589 |
| GCR | 0.883 | 0.654 | 0.686 | 0.532 |
| GNN-RAG | 0.864 | 0.690 | 0.679 | 0.591 |
| RoG | 0.857 | 0.708 | 0.626 | 0.562 |
| ToG | 0.826 | - | 0.685 | - |
| PathMind | 0.895 | 0.728 | 0.707 | 0.614 |

### 可直接复用的结论
- WebQSP 上，PathMind 优于 EPERM 和 GCR。
- CWQ 上，PathMind 相比 GNN-RAG 提升更明显，说明在复杂多跳任务上优势更突出。
- 相比纯 LLM backbone（如 Llama3.1-8B、Qwen2-7B），PathMind 的结构化路径利用显著提升性能。

## 4. 消融实验（RQ2）
| Variant | WebQSP Hits@1 | WebQSP F1 | CWQ Hits@1 | CWQ F1 |
|---|---:|---:|---:|---:|
| PathMind | 0.895 | 0.728 | 0.707 | 0.614 |
| w/o Prioritization | 0.840 | 0.662 | 0.643 | 0.561 |
| w/o Alignment | 0.871 | 0.695 | 0.672 | 0.586 |
| w/o Training | 0.668 | 0.480 | 0.413 | 0.274 |

### 可直接复用的结论
- Path prioritization 是核心模块，移除后性能下降最明显之一。
- Alignment 不是装饰步骤，而是帮助模型更稳定利用高价值路径的重要训练环节。
- 若没有训练阶段，模型很难有效解释并利用图结构知识。

## 5. 路径选择策略比较
| Strategy | WebQSP Hits@1 | WebQSP F1 | CWQ Hits@1 | CWQ F1 |
|---|---:|---:|---:|---:|
| Random Paths | 0.356 | 0.104 | 0.268 | 0.079 |
| Shortest Paths | 0.854 | 0.681 | 0.662 | 0.578 |
| Important Paths | 0.895 | 0.728 | 0.707 | 0.614 |

### 可直接复用的结论
- 重要路径显著优于随机路径与最短路径。
- “最短路径 = 最优推理路径”并不成立，语义相关性比纯长度更关键。

## 6. 泛化与可扩展性（RQ3）
### 跨 backbone 泛化
| Backbone | WebQSP Hits@1 | WebQSP F1 | CWQ Hits@1 | CWQ F1 |
|---|---:|---:|---:|---:|
| Llama2-7B | 0.864 | 0.687 | 0.652 | 0.573 |
| Qwen2-7B | 0.872 | 0.693 | 0.665 | 0.580 |
| Llama3.1-8B | 0.895 | 0.728 | 0.707 | 0.614 |

### 可直接复用的结论
- 框架能迁移到不同 LLM backbone。
- 更强 backbone 会进一步放大 PathMind 的收益。

## 7. 效率结果
| Method | Hit | Time (s) | # Calls | # Tokens |
|---|---:|---:|---:|---:|
| ToG | 0.751 | 16.14 | 11.6 | 7069 |
| EffiQA | 0.829 | - | 7.3 | - |
| PoG | 0.873 | 16.80 | 9.0 | 5518 |
| RoG | 0.857 | 2.60 | 2 | 521 |
| GNN-RAG | 0.864 | 1.52 | 1 | 414 |
| GCR | 0.883 | 3.60 | 2 | 231 |
| PathMind | 0.895 | 2.23 | 1 | 216 |

### 可直接复用的结论
- 相比 synergy-augmented 方法，PathMind 显著减少调用次数与 token 消耗。
- 相比 retrieval-augmented 基线，PathMind 在保持低成本的同时获得更高准确率。
- 它不是绝对最快，但属于性能/效率折中非常优的一类。

## 8. 适合未来复用的问题入口
- 只想写实验综述：读第 3、4、5、7 节
- 只想写消融分析：读第 4、5 节
- 只想比较效率：读第 7 节
- 只想解释为什么复杂多跳任务更受益：读第 3、5、6 节
