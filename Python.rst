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


Resolving Circular Imports
==========================

..
    # (V) = Variable
    # (f) = Function

    module
      |___ config.py ---> (V) OFFICE365_PATH
      |___ directories 
      |       |____ filestore.py  
      |____ funcs
              |____ folders.py --> (f) make_folders_if_not_exist
              |____ path_formatting.py --> (f) return_path

