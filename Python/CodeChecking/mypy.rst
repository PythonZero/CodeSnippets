Must be a type of parent (i.e. subclasses parent)
#################################################

.. code-block:: python
    
    from typing import Type
    
    class A: pass
    class B(A): pass
    class C(A): pass
    
    def add_children_of_a(child1: Type[A], child2: Type[A]) -> None:
        pass
       
    x = add_children_of_a(B(), C()) # okay
    y = add_children_of_a(123, 456) # will error
