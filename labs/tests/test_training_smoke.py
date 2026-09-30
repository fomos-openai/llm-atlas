import importlib.util
import unittest
from pathlib import Path

from llm_atlas.config import ExperimentConfig


@unittest.skipUnless(importlib.util.find_spec("torch"), "torch is not installed")
class TrainingSmokeTest(unittest.TestCase):
    def test_forward_backward_update(self):
        from llm_atlas.training import run_training_smoke

        root = Path(__file__).resolve().parents[1]
        result = run_training_smoke(ExperimentConfig.from_file(root / "configs/smoke-cpu.yaml"))
        self.assertGreater(result["parameter_count"], 1000)
        self.assertEqual(len(result["losses"]), 2)
        self.assertTrue(all(loss > 0 for loss in result["losses"]))


if __name__ == "__main__":
    unittest.main()

