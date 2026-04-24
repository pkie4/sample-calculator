#!/usr/bin/env python3
"""Simple safe calculator REPL and one-shot evaluator.
Usage:
  python calculator.py           -> interactive REPL
  python calculator.py 2+3*4     -> prints result and exits
"""
import ast
import operator as op
import math
import sys

# allowed operators
_ops = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

# allowed unary ops
_unary = {ast.UAdd: lambda x: x, ast.USub: lambda x: -x}

# allowed math functions (if you want more add here)
_allowed_names = {k: getattr(math, k) for k in (
    "sin",
    "cos",
    "tan",
    "sqrt",
    "log",
    "log10",
    "exp",
    "pow",
)}
_allowed_names.update({"pi": math.pi, "e": math.e})


def _eval(node):
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    if isinstance(node, ast.Num):  # < Py3.8
        return node.n
    if hasattr(ast, "Constant") and isinstance(node, ast.Constant):  # Py3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant")
    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _ops:
            return _ops[op_type](left, right)
        raise ValueError(f"Unsupported binary operator {op_type}")
    if isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        op_type = type(node.op)
        if op_type in _unary:
            return _unary[op_type](operand)
        raise ValueError(f"Unsupported unary operator {op_type}")
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise ValueError("Only simple function calls allowed")
        func_name = node.func.id
        if func_name not in _allowed_names:
            raise ValueError(f"Function '{func_name}' not allowed")
        args = [_eval(a) for a in node.args]
        return _allowed_names[func_name](*args)
    if isinstance(node, ast.Name):
        if node.id in _allowed_names:
            return _allowed_names[node.id]
        raise ValueError(f"Name '{node.id}' is not allowed")
    raise ValueError(f"Unsupported expression: {type(node).__name__}")


def eval_expr(expr: str):
    tree = ast.parse(expr, mode="eval")
    return _eval(tree)


def repl():
    try:
        while True:
            s = input('calc> ').strip()
            if not s:
                continue
            if s.lower() in ('quit', 'exit'):
                break
            try:
                print(eval_expr(s))
            except Exception as e:
                print('Error:', e)
    except (EOFError, KeyboardInterrupt):
        print()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        expr = ' '.join(sys.argv[1:])
        try:
            print(eval_expr(expr))
        except Exception as e:
            print('Error:', e)
            sys.exit(1)
    else:
        repl()
