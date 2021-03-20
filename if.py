import ast
import inspect
from functools import wraps
import textwrap
import importlib
from astrologic import switcher
from astrologic import no_recursion


c = 'ogogo'
class A:
    def a(self):
        return 'kek'

    @switcher(a=True, b=False)
    def func(self, a, b):
        if a:
            print('lol')
        if b:
            v = 'lolkek'
            print(v)
            print(c)
            s = 1 / 0
        print(self.a())


#is_recursion = False


def func():
    is_recursion = False
    def x():
        nonlocal is_recursion
        is_recursion = True
    x()
    return is_recursion

def func2():
    return ((), {})
#for x in inspect.getsourcelines(A().func)[0]:
#    print(x, end='')

counter = 0

@no_recursion
def recursion():
    global counter
    counter += 1
    if counter != 10000000:
        return recursion()
    return counter
#print(ast.dump(ast.parse(inspect.getsource(rec)), indent=4))
print(rec())
#print(counter)

#print(func())
#print(ast.dump(ast.parse(inspect.getsource(func)), indent=4))
#print(ast.dump(ast.parse(inspect.getsource(func2)), indent=4))

#A().func(0, 0)
