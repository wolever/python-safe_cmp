from nose.tools import assert_equal
from parameterized import parameterized

from safe_cmp import safe_order, safe_sorted, safe_min, safe_max, safe_cmp

nan = float("nan")

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
    (a2, b2, cmp)
    for cmp in test_comparisons
    for (a, b) in test_inputs
    for (a2, b2) in [
        (safe_order(a), b),
        (a, safe_order(b)),
        (safe_order(a), safe_order(b))
    ]
])
def test_safe_order(a, b, cmp):
    op, expected = cmp
    res = eval(f"a {op} b")
    assert_equal(res, expected, f"{a} {op} {b} <> {expected}")

@parameterized(test_inputs)
def test_safe_sorted(*inputs):
    assert_equal(list(safe_sorted(inputs)), list(inputs))

@parameterized(test_inputs)
def test_safe_sorted_reversed_input(*inputs):
    assert_equal(list(safe_sorted(reversed(inputs))), list(inputs))

@parameterized(test_inputs)
def test_safe_sorted_reverse_arg(*inputs):
    assert_equal(list(safe_sorted(inputs, reverse=True)), list(reversed(inputs)))

def test_safe_sorted_with_key():
    assert_equal(list(safe_sorted([1, 2], key=lambda x: -x)), [2, 1])

@parameterized(test_inputs)
def test_safe_cmp(*inputs):
    assert_equal(safe_cmp(*inputs), -1)

@parameterized(test_inputs)
def test_safe_cmp_reversed(*inputs):
    assert_equal(safe_cmp(*reversed(inputs)), 1)

@parameterized([
    (safe_min, ),
    (safe_max, ),
])
def test_safe_min_max_default(func):
    assert_equal(func([], default=42), 42)

@parameterized([
    (input, func_exp, splat)
    for input in test_inputs
    for func_exp in [(safe_min, 0), (safe_max, 1)]
    for splat in [True, False]
])
def test_safe_min_max(input, func_exp, splat):
    func, expected = func_exp
    res = func(*input) if splat else func(input)
    assert_equal(res, input[expected])

@parameterized([
    (nan, nan, 0),
    (1, nan, 1),
    (nan, 1, -1),
    (nan, None, 1),
    (None, nan, -1),
])
def test_safe_cmp_nan(a, b, expected):
    # ensure compat with Python 2 cmp
    assert_equal(safe_cmp(a, b), expected)

@parameterized([
    ([nan, 2, nan, 1], [nan, 2, nan, 1]),
    (["foo", None, nan], [None, nan, "foo"]),
])
def test_sorted_nan(input, expected):
    # ensure compat with sorted
    assert_equal(list(safe_sorted(input)), expected)
