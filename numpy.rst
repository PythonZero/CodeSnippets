Numpy Stuff
-------------------------

Repeating data
==================================

.. code-block:: python    

    >>> np.tile([1, 2, 3,], 5)
    array([1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3])
    
    
    >>> arr = np.array([1, 2, 3])
    >>> np.repeat(arr[None, :], 3, axis=0)
    array([[1, 2, 3],
           [1, 2, 3],
           [1, 2, 3]])
