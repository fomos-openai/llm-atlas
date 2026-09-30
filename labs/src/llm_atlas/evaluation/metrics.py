from __future__ import annotations


def exact_match(predictions: list[str], references: list[str]) -> float:
    if len(predictions) != len(references):
        raise ValueError("predictions and references must have equal length")
    if not references:
        return 0.0
    return sum(p.strip() == r.strip() for p, r in zip(predictions, references)) / len(references)

