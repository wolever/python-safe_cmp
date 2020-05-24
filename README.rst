``safe_cmp``: safe comparisons (total ordering) for any object in Python 3
==========================================================================

``safe_cmp`` provides functions for safely sorting and ordering any value in
Python 3. In fancy math terms, ``safe_cmp`` implements a total ordering of all
values in Python 3 [1]_.

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

``safe_cmp`` implements Python 2 compatible safe versions of the ordering
functions:

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

.. [1] More precisely, a total ordering *of all values which can be ordered*.
   This excludes ``NaN``, and any other values which are defined as having an
   undefined ordering.
