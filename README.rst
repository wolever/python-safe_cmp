``safe_cmp`` provides safe comparison operations (a total ordering) for any object in Python 3
==============================================================================================

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

But there are many cases where it is useful to, for example:

* Sort heterogeneous lists (ie, lists that contain many types of object)
* Compare objects to ``None`` (for example, to find the ``max(...)`` of a list
  where some items may be ``None``)
* Write generic functions which will have robust, deterministic behaviour on
  arbitrary input

In fancy math terms, ``safe_cmp`` implements a total ordering of all values in
Python 3[1]_.

.. [1] More precisely, a total ordering *of all values which can be ordered*.
   This excludes ``NaN``, and any other values which are defined as having an
   undefined ordering.

``safe_cmp`` implements safe versions of:

* ``safe_order``: a wrapper which defines a total ordering for any object (for
  example, ``heterogeneous_list.sort(key=safe_order)``)
* ``safe_cmp``: a Python 2 compatible implementation of ``cmp`` for Python 3
* ``safe_sorted``: a safe version of ``sorted(...)``
* ``safe_min``: a safe version of ``min(...)``
* ``safe_max``: a safe version of ``max(...)``

Performance
-----------

Currently ``safe_cmp`` methods are currently implemented in Python (in contrast
to their unsafe builtin counterparts, which are implemented in C), so
performance will notable worse for large comparisons::

    In [1]: %timeit safe_max(range(10000000))
    2.8 s ± 42 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

    In [2]: %timeit max(range(10000000))
    345 ms ± 6.23 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

For smaller comparisons, though, the difference will be negligible::

    In [1]: %timeit safe_max(1, 2)
    682 ns ± 7.12 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

    In [2]: %timeit max(1, 2)
    218 ns ± 6.87 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

If there is interest in performant implementations, however, they will be
straight forward to provide.

Additionally, where obvious, performance optimizations have been implemented
(for example, caching the result of ``key=`` functions).
