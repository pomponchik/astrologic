import ast
import inspect
import functools
import textwrap
import importlib

import astunparse

from astrologic.function_text import FunctionText


class BaseDecorator:
    def __call__(self, *args, **kwargs):
        def decorator(func):
            text = FunctionText(func)
            tree = self.get_source_tree(text)
            new_args = () if len(args) == 1 and callable(args[0]) else args
            new_tree = self.change_tree(tree, func, text, *new_args, **kwargs)
            new_tree = ast.fix_missing_locations(new_tree)
            namespace = self.get_new_namespace(func)
            self.post_created_fill_for_namespace(namespace)
            new_function = self.convert_tree_to_function(new_tree, func, namespace, kwargs.get('debug_mode_on'))
            new_function = self.edit_result(func, new_function, namespace)
            return new_function
        if not len(args):
            return decorator
        elif len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        return decorator

    def post_created_fill_for_namespace(self, namespace):
        pass

    def change_tree(self, tree, function_text, **kwargs):
        raise NotImplementedError

    def edit_result(self, original_function, new_function, namespace):
        return new_function

    def convert_tree_to_function(self, tree, original_function, namespace, debug_mode_on):
        if debug_mode_on:
            print('---------------------')
            print(f'Function {original_function.__name__} from module {original_function.__module__} changed. Its code is roughly equivalent to the following:')
            print(astunparse.unparse(tree))
            print('---------------------')
        code = compile(tree, filename=inspect.getfile(original_function), mode='exec')
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

    def get_new_namespace(self, function):
        return self.get_globals_by_function(function)

    def get_all_names(self, tree):
        all_original_names = set()
        class Visiter(ast.NodeVisitor):
            def visit(_self, node):
                try:
                    if isinstance(node, ast.Name):
                        all_original_names.add(node.id)
                except:
                    pass
        Visiter().visit(tree)
        return all_original_names
