from __future__ import annotations

from dataclasses import dataclass

try:
    import torch
    from torch import nn
    from torch.nn import functional as F
except ImportError as exc:  # pragma: no cover - exercised by environment check
    raise RuntimeError("Install labs dependencies with: pip install -e '.[dev]'") from exc


@dataclass(frozen=True)
class ModelConfig:
    vocab_size: int = 256
    sequence_length: int = 128
    layers: int = 4
    heads: int = 4
    hidden_size: int = 256
    intermediate_size: int = 768


class RMSNorm(nn.Module):
    def __init__(self, width: int, eps: float = 1e-5) -> None:
        super().__init__()
        self.weight = nn.Parameter(torch.ones(width))
        self.eps = eps

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        scale = torch.rsqrt(x.float().pow(2).mean(-1, keepdim=True) + self.eps)
        return (x.float() * scale).to(x.dtype) * self.weight


def rotary(x: torch.Tensor) -> torch.Tensor:
    _, _, length, width = x.shape
    half = width // 2
    positions = torch.arange(length, device=x.device, dtype=torch.float32)
    frequencies = 1.0 / (10000 ** (torch.arange(half, device=x.device).float() / half))
    angles = positions[:, None] * frequencies[None, :]
    cos, sin = angles.cos()[None, None], angles.sin()[None, None]
    left, right = x[..., :half], x[..., half:half * 2]
    return torch.cat((left * cos - right * sin, left * sin + right * cos), dim=-1)


class Attention(nn.Module):
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        self.heads = cfg.heads
        self.head_size = cfg.hidden_size // cfg.heads
        self.qkv = nn.Linear(cfg.hidden_size, 3 * cfg.hidden_size, bias=False)
        self.out = nn.Linear(cfg.hidden_size, cfg.hidden_size, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch, length, width = x.shape
        q, k, v = self.qkv(x).chunk(3, dim=-1)
        reshape = lambda item: item.view(batch, length, self.heads, self.head_size).transpose(1, 2)
        q, k, v = rotary(reshape(q)), rotary(reshape(k)), reshape(v)
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.out(y.transpose(1, 2).contiguous().view(batch, length, width))


class Block(nn.Module):
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        self.attn_norm = RMSNorm(cfg.hidden_size)
        self.attn = Attention(cfg)
        self.mlp_norm = RMSNorm(cfg.hidden_size)
        self.gate = nn.Linear(cfg.hidden_size, cfg.intermediate_size, bias=False)
        self.up = nn.Linear(cfg.hidden_size, cfg.intermediate_size, bias=False)
        self.down = nn.Linear(cfg.intermediate_size, cfg.hidden_size, bias=False)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = x + self.attn(self.attn_norm(x))
        h = self.mlp_norm(x)
        return x + self.down(F.silu(self.gate(h)) * self.up(h))


class DecoderOnlyTransformer(nn.Module):
    def __init__(self, cfg: ModelConfig) -> None:
        super().__init__()
        self.cfg = cfg
        self.embedding = nn.Embedding(cfg.vocab_size, cfg.hidden_size)
        self.blocks = nn.ModuleList(Block(cfg) for _ in range(cfg.layers))
        self.norm = RMSNorm(cfg.hidden_size)
        self.lm_head = nn.Linear(cfg.hidden_size, cfg.vocab_size, bias=False)
        self.lm_head.weight = self.embedding.weight

    def forward(self, tokens: torch.Tensor, labels: torch.Tensor | None = None):
        if tokens.shape[1] > self.cfg.sequence_length:
            raise ValueError("input exceeds configured sequence length")
        x = self.embedding(tokens)
        for block in self.blocks:
            x = block(x)
        logits = self.lm_head(self.norm(x))
        loss = None
        if labels is not None:
            loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), labels.reshape(-1))
        return logits, loss

