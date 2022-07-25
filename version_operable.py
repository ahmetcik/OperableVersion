__authour__ = "Emre Ahmetcik"
__date__ = "07/2022"

import operator
from packaging import version
from functools import total_ordering
import numpy as np

operators_dict = {'+': operator.add,
                  '-': operator.sub,
                  '*': operator.mul,
                  '/': operator.floordiv
                 }

def try_convert_dtype(x, dtype=float, except_fill=-np.inf):
    try:
        return dtype(x)
    except:
        return except_fill

@total_ordering
class VersionComparable(object):
    def __init__(self, x):
        x = str(x)
        self.x_comparable = version.parse(x)

    def __le__(self, y):
        return self.x_comparable <= version.parse(str(y))

    def __eq__(self, y):
        return self.x_comparable == version.parse(str(y))
    
class VersionAddable(object):
    def __init__(self, x):
        self.x_split, self.n_x = self._get_relevant_attr(x)
    
    def _get_relevant_attr(self, x):
        x_split = [try_convert_dtype(xi, dtype=int) for xi in str(x).split('.')]
        return x_split, len(x_split)
        
    def _apply_op(self, y, op):
        # operator string to operator function using operators_dict
        op_func = operators_dict[op]
        
        # Get relevant attributes needed for elementwise operation
        # For this, assume first that argument y is VersionAddable object.
        # If not such object, apply function _get_relevant_attr.
        try:
            y_split, n_y = y.x_split, y.n_x
        except:
            y_split, n_y = self._get_relevant_attr(y)
        
        # If x and y are not of same lenght (i.e. number of elements split by '.'),
        # then apply elementwise operation to min length among x and y. Next,
        # add tail of the one with max lenght.
        if self.n_x < n_y:
            n_min = self.n_x
            tail_split = y_split[n_min:]
        else:
            n_min = n_y
            tail_split = self.x_split[n_min:]
        
        z = [op_func(self.x_split[i], y_split[i]) for i in range(n_min)]
        z += tail_split
        z = [str(zi) for zi in z]
        z = '.'.join(z)
        return z

    def __add__(self, y):
        return self._apply_op(y, '+')
    
    def __sub__(self, y):
        return self._apply_op(y, '-')

    def __mul__(self, y):
        return self._apply_op(y, '*')
    
    def __div__(self, y):
        return self._apply_op(y, '/')
    
class VersionOperable(VersionAddable, VersionComparable):
    """Class to make a variables of type version (e.g. '1.2.1') comparable 
    with each other as well as allow arithmetic operations on them. For 
    example, we want that '1.4.' < '2.1.2.7' = True, 
    and '1.4 + '2.1.2.7' = '3.5.2.7', where add was applied elementwise."""

    def __init__(self, x):
        self.x = x
        VersionAddable.__init__(self, x)
        VersionComparable.__init__(self, x)

    def __str__(self):
        return str(self.x)

if __name__ == '__main__':
    a2 = VersionOperable('7.2')
    a3 = '4.1.2.4'
    print(a2 + a3)
    print(a2 >= a3)
