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


Warnings
=================

.. code-block:: python
    
   import warnings
   
   def suppressed_warning_function():
        with warnings.catch_warnings():  # this alone captures all warnings. Need to delete the simplefilter below to ensure this behavior
            warnings.simplefilter(action='ignore', category=RuntimeWarning)  # this filters to only capture RuntimeWarning, other warnings are still raised
            warnings.warn("A custom warning", category=UserWarning)
            warnings.warn("A runtime warning", category=RuntimeWarning)
  
  
   def test_warning_stuff():
       with pytest.warns(None) as raised_warnings:  # Record warnings
           suppressed_warning_function()

   # Check RuntimeWarnings are suppressed but other warnings are raised
   assert len(raised_warnings.list) == 1
   assert raised_warnings.list[0].category == UserWarning
