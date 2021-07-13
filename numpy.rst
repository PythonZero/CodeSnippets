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


Incremental filling of an array
===================================

.. code-block:: python
    
    # Prepare a dataframe
    >>> df = pd.DataFrame(columns=["a", "b", "c", "d", "e", "f"], index=[1,2,3])
    
    # Fill the dataframe with ascending values
    >>> df.loc[:] = np.arange(df.shape[0] * df.shape[1]).reshape(df.shape)
    
    >>> df
            a   b   c   d   e   f
        1   0   1   2   3   4   5
        2   6   7   8   9  10  11
        3  12  13  14  15  16  17
