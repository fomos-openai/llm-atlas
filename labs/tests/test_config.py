import tempfile
import unittest
from pathlib import Path

from llm_atlas.config import ExperimentConfig


class ConfigTest(unittest.TestCase):
    def test_smoke_config(self):
        root = Path(__file__).resolve().parents[1]
        config = ExperimentConfig.from_file(root / "configs/smoke-cpu.yaml")
        self.assertEqual(config.strategy, "single")
        self.assertEqual(config.world_size, 1)

    def test_unknown_key_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.yaml"
            path.write_text("run_name: x\nmodel_family: x\ndataset: x\noutput_dir: x\nwrong: 1\n")
            with self.assertRaises(ValueError):
                ExperimentConfig.from_file(path)


if __name__ == "__main__":
    unittest.main()

