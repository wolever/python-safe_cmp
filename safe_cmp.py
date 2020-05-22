"""
Python 2-style total ordering for Python 3.
"""

Undefined = object()

def safe_cmp(a, b, _nan_is_eq=False):
    """ Python 2 compatible ``cmp`` function.

        See also: https://github.com/python/cpython/blob/2.7/Objects/object.c#L768

        Note: the ``_nan_is_eq`` argument is required to ensure that sorting is
        consistent (ie, where ``nan`` does not move)::

            sorted([1, nan]) == sorted([nan, 1])

        But ``safe_cmp`` should _not_ return ``0`` when called directly (ie,
        because ``safe_cmp(nan, 1)`` should not return ``0``).
    """

    try:
        res = (
            -1 if a < b else
            0 if a == b else
            1 if a > b else
            0 if _nan_is_eq else
            None
        )
        if res is not None:
            return res
        a_is_nan = a != a
        b_is_nan = b != b
        return (
            0 if a_is_nan and b_is_nan else
            -1 if a_is_nan else
            1
        )
    except TypeError:
        pass

    if a is None:
        if b is None:
            return 0

        return -1

    if b is None:
        return 1

    typ_a = type(a)
    typ_b = type(b)
    return safe_cmp(
        (typ_a.__name__, id(typ_a)),
        (typ_b.__name__, id(typ_b)),
    )

def _build_comperator(name, op, lt, eq, gt):
    ns = {"safe_cmp": safe_cmp}
    exec(f"""
def comperator(self, b, __safe_cmp=safe_cmp):
    res = __safe_cmp(self._obj, b, _nan_is_eq=True)
    return (
        {lt} if res == -1 else
        {eq} if res == 0 else
        {gt}
    )""", ns, ns)
    res = ns["comperator"]
    res.__name__ = name
    return res


class safe_order:
    def __init__(self, obj):
        self._obj = obj

    __lt__ = _build_comperator("__lt__", "<", "True", "False", "False")
    __le__ = _build_comperator("__le__", "<=", "True", "True", "False")
    __gt__ = _build_comperator("__gt__", ">", "False", "False", "True")
    __ge__ = _build_comperator("__ge__", ">=", "False", "True", "True")

    def __repr__(self):
        return f"safe_order({self._obj!r})"

    def __str__(self):
        return f"safe_order({self._obj})"


def safe_max(a, *rest, default=Undefined, key=None):
    """ safe_max(iterable, *[, default=obj, key=func]) -> value
        safe_max(arg1, arg2, *args, *[, key=func]) -> value

        With a single iterable argument, return its biggest item. The
        default keyword-only argument specifies an object to return if
        the provided iterable is empty.
        With two or more arguments, return the largest argument.
    """
    items = a if not rest else (a, ) + rest
    res = default
    res_cmp = Undefined
    for item in items:
        if res is Undefined:
            res = item
            continue
        if res_cmp is Undefined:
            res_cmp = res if key is None else key(res)
        item_cmp = item if key is None else key(item)
        cmp_res = safe_cmp(res_cmp, item_cmp)
        if cmp_res < 0:
            res = item
            res_cmp = item_cmp

    if res is Undefined:
        raise ValueError("safe_max() arg is an empty sequence")
    return res

def safe_min(a, *rest, default=Undefined, key=None):
    """ safe_min(iterable, *[, default=obj, key=func]) -> value
        safe_min(arg1, arg2, *args, *[, key=func]) -> value

        With a single iterable argument, return its biggest item. The
        default keyword-only argument specifies an object to return if
        the provided iterable is empty.
        With two or more arguments, return the largest argument.
    """
    items = a if not rest else (a, ) + rest
    res = default
    res_cmp = Undefined
    for item in items:
        if res is Undefined:
            res = item
            continue
        if res_cmp is Undefined:
            res_cmp = res if key is None else key(res)
        item_cmp = item if key is None else key(item)
        cmp_res = safe_cmp(res_cmp, item_cmp)
        if cmp_res > 0:
            res = item
            res_cmp = item_cmp

    if res is Undefined:
        raise ValueError("safe_min() arg is an empty sequence")
    return res

def safe_sorted(iter, *, key=None, reverse=False):
    if key is None:
        use_key = safe_order
    else:
        use_key = lambda x: safe_order(key(x))
    return sorted(iter, key=use_key, reverse=reverse)
