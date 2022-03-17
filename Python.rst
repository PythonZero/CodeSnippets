General Python Functions
------------------------

Multi level list comprehension (i.e. list flattening)
====================================================

1. Start with writing it with multiple for loops, e.g. 

      .. code-block:: python

       lst_a = [['A'], ['B'], ['C', 'D']]
       for lst in lst_a:
           for item in lst:
               item

2. Just back-space the colons, and put the `item` at the beginning

    .. code-block:: python

        # step 1:
        for lst in lst_a for item in lst: # delete the colons
            item  # put at the beginning
        # step 2:
        flattened_list = [item for lst in lst_a for item in lst]


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

.. code-block::

    # (V) = Variable
    # (f) = Function

    so (module)
      |___ config.py ---> (V) OFFICE365_PATH
      |___ directories 
      |       |____ filestore.py  
      |____ funcs
              |____ folders.py --> (f) make_folders_if_not_exist
              |____ path_formatting.py --> (f) return_path


In ``filestore.py`` if you want to import ``OFFICE_365_PATH, make_folders_if_not_exist, return_path``, to prevent 
circular imports, you *can't* do:

``from .. import OFFICE365_PATH, make_folders_if_not_exist, return_path``

as it imports from the module `so`, so when you import `so`, it imports `filestore` which then imports `so` --> cyclic-import

**Solution**:

.. code-block:: python

    from ..config import OFFICE365_PATH 
    from ..funcs import make_folders_if_not_exist, return_path

