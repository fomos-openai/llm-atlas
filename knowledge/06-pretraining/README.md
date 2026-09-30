# 06 · 预训练

预训练用大规模自监督目标学习语言、代码与多模态分布。它建立广泛先验与表示能力，但不直接保证遵循指令、事实可靠或安全。

## 主流程

[目标函数](./objectives.md) → [优化与稳定性](./optimization-and-stability.md) → [规模与计算](./scaling-and-compute.md) → [分布式训练](./distributed-training.md) → [检查点](./checkpointing.md) → [失败模式](./training-failure-modes.md)

## 关键观测

训练损失是必要但不充分的信号。应同步跟踪数据组成、梯度/激活统计、关键能力、记忆与污染、安全代理指标、吞吐和硬件故障。

