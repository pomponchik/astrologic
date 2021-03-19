import ast
import inspect
from functools import wraps
import textwrap
import importlib
from astrologic.decorators.if_switcher import switcher


c = 'ogogo'
class A:
    def a(self):
        return 'kek'

    @switcher(a=True, b=True)
    def func(self, a, b):
        if a:
            print('lol')
        if b:
            v = 'lolkek'
            print(v)
            print(c)
            s = 1 / 0
        print(self.a())


def f():
    pass

print(inspect.getsourcelines(f))


#print(ast.dump(ast.parse(inspect.getsource(func)), indent=4))

A().func(0, 0)
