# 10 · 推理与效率

推理系统把权重变成可用服务。核心目标是在质量约束下优化首 token 延迟、每 token 延迟、吞吐、显存、能耗和成本。

[解码](./decoding.md) · [KV cache 与批处理](./kv-cache-and-batching.md) · [投机解码](./speculative-decoding.md) · [量化](./quantization.md) · [剪枝与蒸馏](./pruning-and-distillation.md) · [服务系统](./serving-systems.md) · [延迟/吞吐/成本](./latency-throughput-cost.md)

优化必须基于真实请求长度与并发分布；离线峰值吞吐很可能牺牲交互体验。

