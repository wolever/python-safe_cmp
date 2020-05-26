``safe_cmp``: safe comparisons (total ordering) for any object in Python 3
==========================================================================

``safe_cmp`` provides functions for safely sorting and ordering any value in
Python 3. In fancy math terms, ``safe_cmp`` implements a total ordering of all
values in Python 3.

Installation::

    yarn add safe-cmp

    - or -

    pip install safe-cmp

Description
-----------

In Python 2, it was possible to compare any object::

    >>> None > 2
    False
    >>> [] < object()
    True

But this is no longer true in Python 3::

    >>> None > 2
    ...
    TypeError: '>' not supported between instances of 'NoneType' and 'int'
    >>> [] < object()
    ...
    TypeError: '<' not supported between instances of 'list' and 'object'

There are many cases when it can be convenient to safely compare arbitrary
objects. For example:

* Sort heterogeneous lists (ie, lists that contain many types of object)
* Compare objects to ``None`` (for example, to find the ``max(...)`` of a list
  where some items may be ``None``)
* Write generic functions which will have robust, deterministic behaviour on
  arbitrary input

``safe_cmp`` implements Python 2 (mostly; see `Python 2 Compatibility`_)
compatible safe versions of the ordering functions:

* ``safe_cmp``: a Python 2 compatible implementation of ``cmp`` for Python 3
* ``safe_sorted``: a safe version of ``sorted(...)``
* ``safe_min``: a safe version of ``min(...)``
* ``safe_max``: a safe version of ``max(...)``

And provides a wrapper - ``safe_order`` - which defines a total ordering for
any object (for example, ``heterogeneous_list.sort(key=safe_order)``).

Examples
--------

Sorting a heterogeneous list:

.. code-block:: python

    >>> from safe_cmp import safe_sorted, safe_order
    >>> items = [1, None, "foo", {}, object]
    >>> list(safe_sorted(items)) # Using "safe_sorted"
    [None, {}, 1, 'foo', object]
    >>> items.sort(key=safe_order) # Using "safe_order" with key=
    >>> items
    [None, {}, 1, 'foo', object]

Finding the max of a list which includes nulls:

.. code-block:: python

    >>> from safe_cmp import safe_max
    >>> safe_max([1, None, 3, None, 4])
    4

The rare situation where Python 2 style ``cmp`` is useful:

.. code-block:: python

    >>> from safe_cmp import safe_cmp
    >>> safe_cmp(None, 1)
    -1
    >>> safe_cmp(None, None)
    0
    >>> safe_cmp(1, None)
    1

Note: ``safe_cmp`` will produce Python 2 compatible results when called with
``nan``:

.. code-block:: python

    >>> from safe_cmp import safe_cmp
    >>> nan = float("NaN")
    >>> safe_cmp(nan, 1)
    -1
    >>> safe_cmp(1, nan)
    1
    >>> safe_cmp(nan, nan)
    0

As will ``safe_sorted``:

.. code-block:: python

    >>> from safe_cmp import safe_sorted
    >>> list(safe_sorted([nan, 2, nan, 1]))
    [nan, 2, nan, 1]


Values Without A Defined Ordering
---------------------------------

Values without a naturally defined ordering - complex numbers, certain
user-defined types, etc - will be ordered in terms of their type name and
location in memory.

Specifically, the default ordering is defined as::

    def default_ordering(obj):
        return (type(obj).__name__, id(type(obj)), id(obj))

Note: for Python 2 compatibility, ``None`` and ``NaN`` are handled as special
cases. See `the implementation of safe_cmp`_ for details.

.. _the implementation of safe_cmp: https://github.com/wolever/python-safe_cmp/blob/master/safe_cmp/safe_cmp.py#L7

Another special case worth noting is sets, which *implicitly* have no defined
ordering in Python 3:

.. code-block:: python

    >>> a = set([1])
    >>> b = set([2])
    >>> a < b
    False
    >>> b < a
    False

``safe_cmp`` does not attempt to detect or correct this behavior for sets (or
any other type with an implicitly defined lack of ordering):

.. code-block:: python

    >>> from safe_cmp import safe_cmp
    >>> a = set([1])
    >>> b = set([2])
    >>> safe_cmp(a, b)
    1
    >>> safe_cmp(a, b)
    1


Python 2 Compatibility
----------------------

``safe_cmp`` and friends are compatible with their Python 2 counterparts in
their dealings with ``NaN`` and ``None``, but differ in their handling of types
such as sets and complex numbers which are explicitly unorderable in Python 2:

.. code-block:: python

    >>> 1j > 2j
    ...
    TypeError: no ordering relation is defined for complex numbers
    >>> cmp(set(), set())
    TypeError: cannot compare sets using cmp()

Contrast with ``safe_cmp``:

.. code-block:: python

    >>> from safe_cmp import safe_cmp
    >>> safe_cmp(1j, 2j)
    -1
    >>> safe_cmp(set(), set())
    0


Performance
-----------

Currently ``safe_cmp`` methods are currently implemented in Python (in contrast
to their unsafe builtin counterparts, which are implemented in C), so
performance will be worse for large comparisons::

    In [1]: %timeit safe_max(range(10000000))
    2.8 s ± 42 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    In [2]: %timeit max(range(10000000))
    345 ms ± 6.23 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

For smaller comparisons, hoever, the difference is negligible::

    In [1]: %timeit safe_max(1, 2)
    682 ns ± 7.12 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

    In [2]: %timeit max(1, 2)
    218 ns ± 6.87 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

If there is interest in performant implementations they will be straight
forward to implement.

Additionally, where obvious, performance optimizations have been implemented
(for example, caching the result of ``key=`` functions).
