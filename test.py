from nose.tools import assert_equal
from parameterized import parameterized

from safe_cmp import safe_order

test_inputs = [
    (None, 1),
    (1, []),
    (None, []),
    (None, object()),
    (1, object()),
    (1, 2),
]

test_comparisons = [
    ("<", True),
    ("<=", True),
    ("==", False),
    ("!=", True),
    (">", False),
    (">=", False),
]

@parameterized([
    (input, cmp)
    for input in test_inputs
    for cmp in test_comparisons
])
def test_comparisons(input, cmp):
    a, b = input
    a = safe_order(a)
    op, expected = cmp
    res = eval(f"a {op} b")
    assert_equal(res, expected, f"{a} {op} {b} <> {expected}")
