import ast
import inspect
from functools import wraps
import textwrap
import importlib

from astrologic.function_text import FunctionText


class BaseDecorator:
    def __call__(self, *args, **kwargs):
        def decorator(func):
            text = FunctionText(func)
            tree = ast.parse(text.clean_text_with_pre_breaks)
            class RewriteName(ast.NodeTransformer):
                def visit_If(self, node):
                    try:
                        variable_name = node.test.id
                        if variable_name in kwargs:
                            if not kwargs[variable_name]:
                                return None
                            else:
                                return node.body
                        return node
                    except:
                        return node
            new_tree = ast.fix_missing_locations(RewriteName().visit(tree))
            code = compile(new_tree, filename=inspect.getfile(func), mode='exec')
            namespace = self.get_globals_by_function(func)
            exec(code, namespace)
            result = namespace[func.__name__]
            result = wraps(func)(result)
            return result
        if not len(args):
            return decorator
        elif len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        raise ValueError('You are using the decorator incorrectly.')

    def get_globals_by_function(self, function):
        module_name = function.__module__
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            return {}
        result = {}
        for object_name in dir(module):
            _object = getattr(module, object_name)
            result[object_name] = _object
        return result
