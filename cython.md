 
#### `cyth.pyx`

Can use type annotations (for python 3.x support)

    from __future__ import print_function
    import cython
    
    def calc_factorial(n: cython.int):
        """Calculates the factorial, n!"""
        out: longlong =  1  # cdef long double out = 1
        for i in range(1, n+1):
            out *= i
        print(out)
        return out
        
_Alternate way_ - faster as it uses `cdef` (but cdef can only be called from cython (the .pyx) files). 

So must write a `def` function that calls the `cdef` function.

    cdef int in_c_calc_sum_nums(int n):
        """Calculates the factorial
        >>> calc_sum_nums(5)
        120
        """
        cdef int out = 1
        for i in range(1, n+1):
            out += i
        return out

    def calc_sum_nums(n):
        return in_c_calc_sum_nums(n)  # calls the cdef
    

### `file1.py`

    import pyximport; pyximport.install()
    import cyth # the file name is cyth.pyx
    cyth.calc_factorial(1000)
    
    
Notes:

  * use cython.types [full list of types can be found in cython.Shadow (e.g. `int_types = ['char', 'short', ...]`)]
     - e.g. `cython.char`, `cython.short`
  * `cython.int` can't do as big calculations as normal python `int`, so should use `out: int = 1` (python's `int`)
    - otherwise you get `inf`
