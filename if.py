import ast
import inspect
from functools import wraps
import textwrap
import importlib
from astrologic import switcher, inline
import time





def a(v):
    d = v
    print(d)

@inline('a')
def b():
    print('lol')
    c = 'kek'
    a(c)

b()



#print(time.time() - start_time)
#print(ast.dump(ast.parse(inspect.getsource(a)), indent=4))
#print(rec())
#print(counter)


#print(func())
#print(ast.dump(ast.parse(inspect.getsource(func)), indent=4))
#print(ast.dump(ast.parse(inspect.getsource(func2)), indent=4))

#A().func(0, 0)
