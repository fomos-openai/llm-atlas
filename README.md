# LLM Atlas · 大模型技术知识地图

> 从哪里来、当下处于什么阶段、未来要去往何处。

[打开交互式知识地图](./LLM-ATLAS.html) · [查看高清 SVG](./LLM-ATLAS.svg) · [阅读 PDF 小书](./LLM-ATLAS.pdf) · [进入知识库](./knowledge/00-start-here/README.md)

![LLM Atlas 知识地图](./LLM-ATLAS.svg)

LLM Atlas 是一套面向学习、研究和工程决策的大模型技术知识库。它把大模型放回完整生命周期：历史与理论基础、数据与表示、架构与训练、后训练与推理、评测与部署、上下文与 Agent、多模态、安全、基础设施、产业生态，以及仍未确定的未来。

## 三条阅读路线

- **从哪里来**：从 [历史源流](./knowledge/01-origins/README.md) 和 [数学与机器学习基础](./knowledge/02-foundations/README.md) 开始，理解 Transformer、规模定律与指令化模型如何出现。
- **当下在哪里**：沿 [完整生命周期](./knowledge/00-start-here/lifecycle.md) 阅读数据、预训练、后训练、评测、推理、增强、Agent 与生产系统，再查看 [2026-09 现状快照](./knowledge/18-state-of-the-field/2026-09/model-landscape.md)。
- **未来去哪里**：从 [未来前沿](./knowledge/19-future-frontiers/README.md) 出发，区分已有证据、活跃研究与高不确定推演。

## 知识库原则

1. **生命周期完整**：模型不是孤立权重；知识树覆盖数据、训练、系统、产品、治理与退役更新。
2. **机制优先**：先解释为什么有效、依赖什么、何时失效，再列模型或工具。
3. **事实与推测分离**：当前状态带日期；未来章节使用证据等级，不把预测写成事实。
4. **原始资料优先**：论文、标准、系统卡、官方文档和可复现实验优先于二手总结。
5. **可维护**：易变化的信息进入 `catalogs/` 和带日期快照，稳定知识进入主题页。

## 项目结构

| 路径 | 内容 |
|---|---|
| `knowledge/00–20` | 主知识树，每章都含导航、核心概念、工程含义与开放问题 |
| `catalogs/` | 模型、数据集、基准、工具与论文的机器可读索引 |
| `atlas/` | Archify typed JSON、验证回执与地图历史快照 |
| `book/` | PDF 小书的章节源与构建配置 |
| `references/` | 引用政策、原始资料清单与 BibTeX |
| `scripts/` | 结构、链接、地图与 PDF 构建/校验脚本 |

## 当前版本

- 知识快照：**2026-09-30**
- 内容语言：中文为主，保留英文标准术语
- 地图：Archify architecture / showcase profile
- 许可证：MIT；外部资料版权归原作者或机构所有

## 贡献

请先阅读 [贡献指南](./CONTRIBUTING.md) 与 [资料来源政策](./references/source-policy.md)。新增内容必须说明其稳定性、证据等级和最后核验日期。路线图见 [ROADMAP](./ROADMAP.md)。
