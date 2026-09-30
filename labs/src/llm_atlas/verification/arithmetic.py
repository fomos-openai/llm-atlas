from __future__ import annotations

import ast
import operator
from dataclasses import dataclass


OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.FloorDiv: operator.floordiv}


def safe_eval(expression: str) -> int:
    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)
        if isinstance(node, ast.Constant) and isinstance(node.value, int):
            return node.value
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -visit(node.operand)
        if isinstance(node, ast.BinOp) and type(node.op) in OPS:
            return OPS[type(node.op)](visit(node.left), visit(node.right))
        raise ValueError("expression contains a disallowed operation")

    if len(expression) > 128:
        raise ValueError("expression is too long")
    return visit(ast.parse(expression, mode="eval"))


@dataclass(frozen=True)
class ArithmeticVerifier:
    def verify(self, expression: str, answer: str) -> bool:
        try:
            return safe_eval(expression) == int(answer.strip())
        except (SyntaxError, ValueError, ZeroDivisionError):
            return False

