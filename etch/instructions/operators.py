from operator import *

def e_add(x, y):
    if type(x) == str:
        return add(x, str(y))
    else:
        return add(x, y)
        