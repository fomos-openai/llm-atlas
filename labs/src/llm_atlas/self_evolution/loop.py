from __future__ import annotations

import random
from collections.abc import Callable

from llm_atlas.verification import ArithmeticVerifier


def build_verified_curriculum(
    solve: Callable[[str], str], *, seed: int = 42, samples: int = 100
) -> dict:
    """Create a verified replay set; evaluation data must be held out elsewhere."""
    rng = random.Random(seed)
    verifier = ArithmeticVerifier()
    accepted, rejected = [], []
    for index in range(samples):
        digits = 1 + index * 3 // max(samples, 1)
        ceiling = 10**digits - 1
        left, right = rng.randint(0, ceiling), rng.randint(0, ceiling)
        expression = f"{left}+{right}"
        item = {"prompt": f"计算 {expression}", "expression": expression, "answer": solve(expression), "difficulty": digits}
        (accepted if verifier.verify(expression, item["answer"]) else rejected).append(item)
    return {"accepted": accepted, "rejected": rejected, "acceptance_rate": len(accepted) / max(samples, 1)}

