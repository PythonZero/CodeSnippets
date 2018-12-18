General Python Functions
------------------------

Time some code
===============

.. code-block:: python    

    from timeit import timeit

    def a_func(n):
        j = 0
        for i in range(n):
            i += j
        return j

    print(timeit('a_func(100)', globals=globals(), number=1000))
