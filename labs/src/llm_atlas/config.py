from __future__ import annotations

from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any


def _scalar(value: str) -> Any:
    value = value.strip()
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if value.lower() in {"null", "none"}:
        return None
    try:
        return float(value) if "." in value or "e" in value.lower() else int(value)
    except ValueError:
        return value.strip('"\'')


def load_flat_yaml(path: str | Path) -> dict[str, Any]:
    """Load the deliberately flat lab configs without requiring PyYAML."""
    result: dict[str, Any] = {}
    for raw in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        if ":" not in line:
            raise ValueError(f"invalid config line: {raw}")
        key, value = line.split(":", 1)
        result[key.strip()] = _scalar(value)
    return result


@dataclass(frozen=True)
class ExperimentConfig:
    run_name: str
    model_family: str
    dataset: str
    output_dir: str
    seed: int = 42
    vocab_size: int = 256
    sequence_length: int = 64
    layers: int = 2
    heads: int = 2
    hidden_size: int = 64
    intermediate_size: int = 192
    batch_size: int = 2
    gradient_accumulation: int = 1
    learning_rate: float = 0.0003
    max_steps: int = 2
    precision: str = "fp32"
    strategy: str = "single"
    world_size: int = 1

    @classmethod
    def from_file(cls, path: str | Path) -> "ExperimentConfig":
        raw = load_flat_yaml(path)
        allowed = {field.name for field in fields(cls)}
        unknown = sorted(set(raw) - allowed)
        if unknown:
            raise ValueError(f"unknown config keys: {', '.join(unknown)}")
        config = cls(**raw)
        config.validate()
        return config

    def validate(self) -> None:
        if self.hidden_size % self.heads:
            raise ValueError("hidden_size must be divisible by heads")
        if self.sequence_length < 8 or self.vocab_size < 32:
            raise ValueError("sequence_length and vocab_size are too small")
        if self.strategy not in {"single", "fsdp", "tensor_parallel"}:
            raise ValueError(f"unsupported strategy: {self.strategy}")
        if self.strategy == "single" and self.world_size != 1:
            raise ValueError("single strategy requires world_size=1")
        if self.strategy != "single" and self.world_size < 2:
            raise ValueError("distributed strategy requires world_size>=2")

