# LLM Atlas Labs

这里是知识树的可运行部分。实践分为两条轨道：`Atlas-50M/125M` 用于理解从零训练，`Qwen3-0.6B-Base` 用于体验成熟生态中的持续预训练、SFT、DPO、可验证强化学习、量化和服务。

## 快速开始

```bash
cd labs
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
atlas-lab pretrain --config configs/smoke-cpu.yaml --smoke
python -m unittest discover -s tests
```

CPU smoke 只验证数据、模型前向、反向和参数更新，不代表训练质量。正式 `Atlas-125M` 配置面向 24GB CUDA 单卡；八卡配置是 FSDP 扩展基线，必须在目标集群重新测量网络、吞吐和检查点时间。

## 实验纪律

- 所有命令都从配置读取模型、数据、训练和评测参数；运行时保存解析后的配置、Git 提交和环境清单。
- 大数据、模型权重和检查点不进入 Git；`fixtures/` 只存最小测试样本。
- 每次训练必须保留未训练/未适配基线、固定回归集和成本记录。
- 自进化实验只接受可执行验证器通过的样本，并在独立保留集上判断是否提升。

完整教学顺序见 [`knowledge/06-hands-on-practice`](../knowledge/06-hands-on-practice/README.md)。

