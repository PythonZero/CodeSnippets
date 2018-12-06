 
#### `cyth.pyx`

    from __future__ import print_function
    import cython
    
    def calc_factorial(n: cython.int):
        """Calculates the factorial, n!"""
        out: longlong =  1  # cdef long double out = 1
        for i in range(1, n+1):
            out *= i
        print(out)
        return out

### `file1.py`

    import pyximport; pyximport.install()
    import cyth # the file name is cyth.pyx
    cyth.calc_factorial(1000)
    
    
Notes:

  * use cython.types [full list of types can be found in cython.Shadow (e.g. int_types = ['char', 'short', ...]
  * cython.int can't do as big calculations as normal python int, so should use `out: int = 1` (python's int)
