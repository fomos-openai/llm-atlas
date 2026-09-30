#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LABS = ROOT / "labs"
sys.path.insert(0, str(LABS / "src"))

from llm_atlas.config import ExperimentConfig  # noqa: E402


def main() -> None:
    configs = sorted((LABS / "configs").glob("*.yaml"))
    for path in configs:
        ExperimentConfig.from_file(path)
    expected_recipes = {f"{index:02d}" for index in range(14)}
    actual_recipes = {path.name.split("-", 1)[0] for path in (LABS / "recipes").iterdir() if path.is_dir()}
    if actual_recipes != expected_recipes:
        raise SystemExit(f"recipe set differs: {sorted(actual_recipes)}")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"], cwd=LABS,
        env={**__import__("os").environ, "PYTHONPATH": str(LABS / "src")}, check=False,
    )
    if result.returncode:
        raise SystemExit(result.returncode)
    print(f"labs ok: {len(configs)} configs, 14 recipes, unit suite passed")


if __name__ == "__main__":
    main()

