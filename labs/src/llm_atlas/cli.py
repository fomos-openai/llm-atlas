from __future__ import annotations

import argparse
import json
from dataclasses import asdict

from llm_atlas.config import ExperimentConfig
from llm_atlas.self_evolution import build_verified_curriculum


COMMANDS = ("data", "pretrain", "sft", "dpo", "rl", "evolve", "eval", "serve")


def parser() -> argparse.ArgumentParser:
    root = argparse.ArgumentParser(prog="atlas-lab")
    subcommands = root.add_subparsers(dest="command", required=True)
    for name in COMMANDS:
        command = subcommands.add_parser(name)
        command.add_argument("--config", required=True)
        command.add_argument("--smoke", action="store_true")
    return root


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    config = ExperimentConfig.from_file(args.config)
    result = {"command": args.command, "config": asdict(config), "mode": "validated-plan"}
    if args.command == "pretrain" and args.smoke:
        from llm_atlas.training import run_training_smoke

        result = run_training_smoke(config)
    elif args.command == "evolve" and args.smoke:
        result = build_verified_curriculum(lambda expression: str(eval(expression, {"__builtins__": {}}, {})), samples=16)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

