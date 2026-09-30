import unittest

from llm_atlas.evaluation import exact_match
from llm_atlas.self_evolution import build_verified_curriculum
from llm_atlas.verification import ArithmeticVerifier, safe_eval


class VerificationTest(unittest.TestCase):
    def test_safe_eval(self):
        self.assertEqual(safe_eval("(17+5)*3"), 66)
        with self.assertRaises(ValueError):
            safe_eval("__import__('os').system('echo unsafe')")

    def test_verifier_and_curriculum(self):
        verifier = ArithmeticVerifier()
        self.assertTrue(verifier.verify("12+30", "42"))
        self.assertFalse(verifier.verify("12+30", "41"))
        result = build_verified_curriculum(lambda expression: str(safe_eval(expression)), samples=10)
        self.assertEqual(result["acceptance_rate"], 1.0)

    def test_exact_match(self):
        self.assertEqual(exact_match([" a ", "b"], ["a", "c"]), 0.5)


if __name__ == "__main__":
    unittest.main()

