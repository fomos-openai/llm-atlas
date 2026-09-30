from __future__ import annotations

from dataclasses import asdict


def run_training_smoke(experiment):
    import torch

    from llm_atlas.model import DecoderOnlyTransformer, ModelConfig

    torch.manual_seed(experiment.seed)
    cfg = ModelConfig(
        vocab_size=experiment.vocab_size,
        sequence_length=experiment.sequence_length,
        layers=experiment.layers,
        heads=experiment.heads,
        hidden_size=experiment.hidden_size,
        intermediate_size=experiment.intermediate_size,
    )
    model = DecoderOnlyTransformer(cfg)
    optimizer = torch.optim.AdamW(model.parameters(), lr=experiment.learning_rate)
    losses = []
    for _ in range(experiment.max_steps):
        sample = torch.randint(0, cfg.vocab_size, (experiment.batch_size, cfg.sequence_length + 1))
        _, loss = model(sample[:, :-1], sample[:, 1:])
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        optimizer.step()
        losses.append(float(loss.detach()))
    return {"model": asdict(cfg), "parameter_count": sum(p.numel() for p in model.parameters()), "losses": losses}

