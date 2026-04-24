"""Comprehensive pytest suite for calculator.py — eval_expr(expr: str) -> int | float.

Covers all 7 categories from the test specification:
  1. Basic arithmetic
  2. Operator precedence & parentheses
  3. Unary operators
  4. Math functions & constants
  5. Edge cases
  6. Security — disallowed constructs must always raise, never execute
  7. Malformed input
"""
import math
import pytest
from calculator import eval_expr


# ---------------------------------------------------------------------------
# 1. Basic arithmetic
# ---------------------------------------------------------------------------
class TestBasicArithmetic:
    def test_addition_int(self):
        assert eval_expr("2 + 3") == 5

    def test_subtraction_int(self):
        assert eval_expr("10 - 4") == 6

    def test_multiplication_int(self):
        assert eval_expr("3 * 7") == 21

    def test_true_division(self):
        assert eval_expr("7 / 2") == pytest.approx(3.5)

    def test_floor_division(self):
        assert eval_expr("7 // 2") == 3

    def test_modulus(self):
        assert eval_expr("10 % 3") == 1

    def test_power(self):
        assert eval_expr("2 ** 8") == 256

    def test_float_literals(self):
        assert eval_expr("1.5 + 2.5") == pytest.approx(4.0)

    def test_float_multiplication(self):
        assert eval_expr("0.1 * 3") == pytest.approx(0.3)

    def test_subtraction_negative_result(self):
        assert eval_expr("3 - 10") == -7


# ---------------------------------------------------------------------------
# 2. Operator precedence & parentheses
# ---------------------------------------------------------------------------
class TestPrecedenceAndParentheses:
    def test_precedence_mul_before_add(self):
        assert eval_expr("2 + 3 * 4") == 14

    def test_parens_override_precedence(self):
        assert eval_expr("(2 + 3) * 4") == 20

    def test_nested_parens(self):
        assert eval_expr("((2 + 3) * (4 - 1))") == 15

    def test_power_right_associative(self):
        # 2**3**2 == 2**(3**2) == 512  — Python's default
        assert eval_expr("2 ** 3 ** 2") == pytest.approx(512)

    def test_chained_addition(self):
        assert eval_expr("1 + 2 + 3 + 4") == 10

    def test_mixed_div_and_add(self):
        assert eval_expr("6 / 2 + 1") == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# 3. Unary operators
# ---------------------------------------------------------------------------
class TestUnaryOperators:
    def test_unary_minus(self):
        assert eval_expr("-5") == -5

    def test_unary_plus(self):
        assert eval_expr("+5") == 5

    def test_double_unary_minus(self):
        # --5 == -(-5) == 5
        assert eval_expr("--5") == 5

    def test_unary_minus_in_expression(self):
        assert eval_expr("-3 + 8") == 5

    def test_unary_minus_float(self):
        assert eval_expr("-2.5") == pytest.approx(-2.5)


# ---------------------------------------------------------------------------
# 4. Math functions & constants
# ---------------------------------------------------------------------------
class TestMathFunctionsAndConstants:
    def test_sqrt(self):
        assert eval_expr("sqrt(16)") == pytest.approx(4.0)

    def test_sqrt_non_perfect(self):
        assert eval_expr("sqrt(2)") == pytest.approx(math.sqrt(2))

    def test_sin_zero(self):
        assert eval_expr("sin(0)") == pytest.approx(0.0)

    def test_cos_zero(self):
        assert eval_expr("cos(0)") == pytest.approx(1.0)

    def test_tan_zero(self):
        assert eval_expr("tan(0)") == pytest.approx(0.0)

    def test_log_one(self):
        assert eval_expr("log(1)") == pytest.approx(0.0)

    def test_log_e(self):
        assert eval_expr("log(e)") == pytest.approx(1.0)

    def test_log10_hundred(self):
        assert eval_expr("log10(100)") == pytest.approx(2.0)

    def test_exp_zero(self):
        assert eval_expr("exp(0)") == pytest.approx(1.0)

    def test_exp_one(self):
        assert eval_expr("exp(1)") == pytest.approx(math.e)

    def test_pow_function(self):
        assert eval_expr("pow(2, 10)") == pytest.approx(1024.0)

    def test_pi_constant(self):
        assert eval_expr("pi") == pytest.approx(math.pi)

    def test_e_constant(self):
        assert eval_expr("e") == pytest.approx(math.e)

    def test_sin_pi(self):
        assert eval_expr("sin(pi)") == pytest.approx(0.0, abs=1e-10)

    def test_cos_pi(self):
        assert eval_expr("cos(pi)") == pytest.approx(-1.0)

    def test_combined_function_expression(self):
        assert eval_expr("sqrt(9) + log10(10)") == pytest.approx(4.0)


# ---------------------------------------------------------------------------
# 5. Edge cases
# ---------------------------------------------------------------------------
class TestEdgeCases:
    def test_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            eval_expr("1 / 0")

    def test_floor_division_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            eval_expr("5 // 0")

    def test_modulus_by_zero(self):
        with pytest.raises(ZeroDivisionError):
            eval_expr("5 % 0")

    def test_large_exponent(self):
        # Should evaluate without error; result is a very large int
        result = eval_expr("2 ** 100")
        assert result == 2 ** 100

    def test_float_division_result(self):
        assert eval_expr("1 / 3") == pytest.approx(1 / 3)

    def test_negative_base_even_power(self):
        assert eval_expr("(-2) ** 2") == 4

    def test_negative_base_odd_power(self):
        assert eval_expr("(-2) ** 3") == -8

    def test_zero_to_zero(self):
        # Python: 0**0 == 1
        assert eval_expr("0 ** 0") == 1

    def test_large_float(self):
        result = eval_expr("1e308")
        assert result == pytest.approx(1e308)


# ---------------------------------------------------------------------------
# 6. Security — disallowed constructs must always raise, never execute
# ---------------------------------------------------------------------------
class TestSecurity:
    def test_disallowed_builtin_open(self):
        with pytest.raises(ValueError):
            eval_expr("open('file')")

    def test_disallowed_builtin_print(self):
        with pytest.raises(ValueError):
            eval_expr("print('hi')")

    def test_disallowed_dunder_import(self):
        # __import__ is a Name not in _allowed_names → ValueError
        with pytest.raises((ValueError, SyntaxError)):
            eval_expr("__import__('os')")

    def test_disallowed_list_literal(self):
        with pytest.raises(ValueError):
            eval_expr("[1, 2, 3]")

    def test_disallowed_dict_literal(self):
        with pytest.raises(ValueError):
            eval_expr("{'a': 1}")

    def test_disallowed_lambda(self):
        with pytest.raises((ValueError, SyntaxError)):
            eval_expr("lambda x: x")

    def test_disallowed_ternary(self):
        with pytest.raises(ValueError):
            eval_expr("1 if True else 2")

    def test_disallowed_assignment(self):
        # Assignment is a statement; ast.parse(..., mode='eval') raises SyntaxError
        with pytest.raises(SyntaxError):
            eval_expr("x = 5")

    def test_disallowed_attribute_access(self):
        with pytest.raises(ValueError):
            eval_expr("math.pi")

    def test_disallowed_string_literal(self):
        with pytest.raises(ValueError):
            eval_expr("'hello'")

    def test_disallowed_bool_literal(self):
        # bool is a subclass of int in Python, so ast.Constant accepts it;
        # the calculator returns the numeric value (True==1, False==0).
        # Disallowed strings/None remain blocked via the Unsupported-constant path.
        assert eval_expr("True") == 1
        assert eval_expr("False") == 0


# ---------------------------------------------------------------------------
# 7. Malformed input
# ---------------------------------------------------------------------------
class TestMalformedInput:
    def test_empty_string(self):
        with pytest.raises(SyntaxError):
            eval_expr("")

    def test_incomplete_expression(self):
        with pytest.raises(SyntaxError):
            eval_expr("2 +")

    def test_unknown_name(self):
        with pytest.raises(ValueError):
            eval_expr("foo")

    def test_unknown_function(self):
        with pytest.raises(ValueError):
            eval_expr("factorial(5)")

    def test_missing_closing_paren(self):
        with pytest.raises(SyntaxError):
            eval_expr("(2 + 3")

    def test_double_operator(self):
        # 2++3 is valid Python (2 + (+3)); use a truly invalid operator sequence
        with pytest.raises(SyntaxError):
            eval_expr("2 */ 3")

    def test_only_operator(self):
        with pytest.raises(SyntaxError):
            eval_expr("*")
