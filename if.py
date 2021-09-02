import ast
import inspect
from functools import wraps
import textwrap
import importlib
from astrologic import switcher, inline, no_recursion
import time





def a(d):
    c = ' cheburek'
    c = d + c
    print(c)

@inline('a', debug_mode_on=True)
def b():
    print('lol')
    c = 'kek'
    a(c)

b()



#print(c(1))
#b()



#print(time.time() - start_time)
#print(ast.dump(ast.parse(inspect.getsource(f)), indent=4))
#print(rec())
#print(counter)


#print(func())
#print(ast.dump(ast.parse(inspect.getsource(func)), indent=4))
#print(ast.dump(ast.parse(inspect.getsource(func2)), indent=4))

#A().func(0, 0)
