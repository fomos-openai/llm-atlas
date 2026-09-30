#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
RECIPES = [
    ("00-environment", "环境、依赖与未训练基线", "smoke-cpu.yaml"),
    ("01-data-tokenizer", "数据清单、去重与 Tokenizer", "atlas-50m-smoke.yaml"),
    ("02-transformer", "从零实现 Decoder-only Transformer", "smoke-cpu.yaml"),
    ("03-pretrain-125m", "单卡预训练 Atlas-125M", "atlas-125m-single-gpu.yaml"),
    ("04-continued-pretraining", "Qwen3-0.6B 持续预训练", "qwen3-0.6b-continued-pretrain.yaml"),
    ("05-sft-lora", "监督微调与 LoRA", "qwen3-0.6b-sft-lora.yaml"),
    ("06-dpo", "离线偏好优化", "qwen3-0.6b-dpo.yaml"),
    ("07-verifiable-rl", "可验证强化学习", "qwen3-0.6b-verifiable-rl.yaml"),
    ("08-synthetic-curriculum", "合成数据与难度课程", "self-evolution.yaml"),
    ("09-self-evolution", "生成—验证—训练—回归闭环", "self-evolution.yaml"),
    ("10-evaluation", "能力、安全与成本回归", "qwen3-0.6b-sft-lora.yaml"),
    ("11-quantize-serve", "量化与 vLLM 服务", "qwen3-0.6b-sft-lora.yaml"),
    ("12-rag-agent", "RAG、工具与 Agent", "qwen3-0.6b-sft-lora.yaml"),
    ("13-scale-out", "从单卡迁移到八卡 FSDP", "eight-gpu-fsdp.yaml"),
]


def recipe(name: str, title: str, config: str) -> str:
    command = name.split("-", 1)[0]
    return f"""# {title}

## 目标

本实验以 `configs/{config}` 为唯一参数入口。开始前先保存 Git 提交、Python/CUDA/PyTorch 版本、设备型号和数据清单；结束后保存解析配置、指标、失败样本与峰值资源。不要把模型权重或大数据提交到仓库。

## 步骤

1. 使用小数据和短步数完成 dry-run，确认输入、标签掩码、张量形状、损失和检查点路径。
2. 记录未训练或未适配基线；一次只改变一个关键变量。
3. 启动正式运行，监控 loss、tokens/s、峰值显存、梯度范数和异常样本。
4. 在从未进入训练或生成闭环的保留集上运行回归，并同时报告质量、时延和成本。

```bash
atlas-lab pretrain --config configs/{config} {"--smoke" if command in {"00", "02"} else ""}
```

## 验收

- 命令、配置和环境可以在新目录复现；中断后能够从明确检查点恢复。
- 指标相对固定基线有解释，不用训练集、生成器评审或单个最好样本代替独立评测。
- 失败被分类为数据、优化、系统、评测或安全问题，并给出下一轮只改变一个变量的实验。
- 对无法在当前硬件实跑的部分明确写成设计或静态验证，不冒充实测结果。
"""


def notebook(title: str, cells: list[str]) -> dict:
    return {
        "cells": [
            {"cell_type": "markdown", "metadata": {}, "source": [f"# {title}\n"]},
            *[{"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [cell]} for cell in cells],
        ],
        "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
        "nbformat": 4,
        "nbformat_minor": 5,
    }


def main() -> None:
    for name, title, config in RECIPES:
        target = ROOT / "labs" / "recipes" / name / "README.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(recipe(name, title, config), encoding="utf-8")
    notebooks = ROOT / "labs" / "notebooks"
    notebooks.mkdir(parents=True, exist_ok=True)
    (notebooks / "quickstart.ipynb").write_text(json.dumps(notebook("LLM Atlas Quickstart", [
        "from llm_atlas.config import ExperimentConfig\nconfig = ExperimentConfig.from_file('../configs/smoke-cpu.yaml')\nconfig",
        "from llm_atlas.training import run_training_smoke\nrun_training_smoke(config)",
    ]), ensure_ascii=False, indent=2), encoding="utf-8")
    (notebooks / "self-evolution.ipynb").write_text(json.dumps(notebook("Verified Self-Evolution", [
        "from llm_atlas.verification import safe_eval\nfrom llm_atlas.self_evolution import build_verified_curriculum",
        "build_verified_curriculum(lambda expression: str(safe_eval(expression)), samples=32)",
    ]), ensure_ascii=False, indent=2), encoding="utf-8")
    print("generated 14 recipes and 2 notebooks")


if __name__ == "__main__":
    main()
