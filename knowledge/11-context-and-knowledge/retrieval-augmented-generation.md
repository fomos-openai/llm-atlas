# Retrieval-Augmented Generation

RAG 在生成前检索外部资料，将动态或私有知识放入上下文。典型链路为解析 → 分块 → 索引 → 查询改写 → 检索 → 重排 → 上下文组装 → 生成 → 引用验证。

失败可能来自索引缺失、查询错误、召回不足、错误重排、上下文冲突或模型忽略证据。应分别评估检索质量和答案质量。

参考：[Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)。

