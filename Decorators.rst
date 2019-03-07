Decorators Snippets
+++++++++++++++++++

Capturing Arguments
==========================

.. code-block:: python

    import inspect
    func_signature = inspect.signature(func)
    func_bound_args = func_signature.bind(*args, **kwargs)
    server = func_bound_args.arguments['server']
    database = func_bound_args.arguments['database']

Example:

.. code-block:: python

    import inspect

    def add(x, y, z):
        return x + y - z


    x = inspect.signature(add)
    b = x.bind(1, **{'z': 3, 'y': 2})
    p = b.arguments   # {x:1, y:2, z:3}
    
