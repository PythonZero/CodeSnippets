Mypy Static Type Checking 
+++++++++++++++++++++++++

Type of parent (i.e. subclasses parent)
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


Forward Referencing (i.e. will be declared later)
##################################################


.. code-block:: python

    # Wrap the class with speech marks
    def do_something_with_class_tree(arg1: "Tree"): pass
    class Tree: pass


Prevent Cyclical Referencing
#############################

.. code-block:: python

    # file1:
    from file2 import grow_a_plant
   
    class Tree:
        def do_something(self):
            grow_a_plant(self)
    
   # file2: 
     if False:   # will never run, but good enough for type checking.
        from file1 import Tree  
        
     def grow_a_plant(tree: "Tree"): pass  # references the Tree in file1.
        
