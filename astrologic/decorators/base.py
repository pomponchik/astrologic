import ast
import inspect
import functools
import textwrap
import importlib

from astrologic.function_text import FunctionText


class BaseDecorator:
    def __call__(self, *args, **kwargs):
        def decorator(func):
            text = FunctionText(func)
            tree = self.get_source_tree(text)
            new_tree = self.change_tree(tree, text, **kwargs)
            new_function = self.convert_tree_to_function_function(new_tree, func)
            return new_function
        if not len(args):
            return decorator
        elif len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        raise ValueError('You are using the decorator incorrectly.')

    def change_tree(self, tree, function_text, **kwargs):
        raise NotImplementedError

    def convert_tree_to_function_function(self, tree, original_function):
        code = compile(tree, filename=inspect.getfile(original_function), mode='exec')
        namespace = self.get_globals_by_function(original_function)
        exec(code, namespace)
        result = namespace[original_function.__name__]
        result = functools.wraps(original_function)(result)
        return result

    def get_source_tree(self, text):
        tree = ast.parse(text.clean_text_with_pre_breaks)
        return tree

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
