# 04 · Tokenization 与表示

模型不直接读取文字、图像或声音，而是读取离散或连续表示。表示方式影响序列长度、计算成本、跨语言公平、数字/代码能力和长上下文行为。

- [Tokenization](./tokenization.md)
- [Embeddings](./embeddings.md)
- [位置编码](./positional-encoding.md)
- [上下文表示](./context-representation.md)

表示层的核心权衡是压缩与可分辨性：更粗的单位缩短序列，却可能损失组合性；更细的单位覆盖开放词汇，却增加计算和长依赖。

