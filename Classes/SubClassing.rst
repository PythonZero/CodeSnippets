Returning from a class
============================

To make a class return something, must call the ``super()'s`` object constructor:
(should always call super anyway):

.. code-block:: python

    class CapitalList(list): 
        def __init__(self, *args): 
            super().__init__([i.upper() for i in args]) 

    >>> CapitalList('dad', 'mum', 'mike')     
        ['DAD', 'MUM', 'MIKE'] 
        

For strings, as they are immutable, must overwrite ``__new__``

``__new__`` must **return** a value

.. code-block:: python

    class SubClassString(str): 
      def __new__(cls): 
          return super().__new__(cls, 'hello') 

 
