import ast
import inspect
import functools
import importlib
from typing import Dict, Set, Callable, Union, Optional, Any

import astunparse

from astrologic.function_text import FunctionText


class BaseDecorator:
    def __call__(self, *args: Callable[..., Any], **kwargs: Any) -> Union[Callable[..., Any], Callable[[Callable[..., Any]], Callable[..., Any]]]:
        def decorator(function: Callable[..., Any]) -> Callable[..., Any]:
            text = FunctionText(function)
            tree = self.get_source_tree(text)
            new_args = () if len(args) == 1 and callable(args[0]) else args
            new_tree = self.change_tree(tree, function, text, *new_args, **kwargs)
            new_tree = ast.fix_missing_locations(new_tree)
            namespace = self.get_new_namespace(function)
            new_function = self.convert_tree_to_function(new_tree, function, namespace, kwargs.get('debug_mode_on'))
            new_function = self.edit_result(function, new_function, namespace)
            return new_function

        if not len(args):
            return decorator
        elif len(args) == 1 and callable(args[0]):
            return decorator(args[0])
        return decorator

    def change_tree(self, tree: ast.AST, function_text: FunctionText, **kwargs: Any) -> ast.AST:
        raise NotImplementedError

    def edit_result(self, original_function: Callable[..., Any], new_function: Callable[..., Any], namespace: Dict[str, Any]) -> Callable[..., Any]:
        return new_function

    def convert_tree_to_function(self, tree: ast.AST, original_function: Callable[..., Any], namespace: Dict[str, Any], debug_mode_on: bool):
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

    def get_source_tree(self, text: FunctionText) -> ast.AST:
        tree = ast.parse(text.clean_text_with_pre_breaks)
        return tree

    def get_globals_by_function(self, function: Callable[..., Any]) -> Dict[str, Any]:
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

    def get_new_namespace(self, function: Callable[..., Any]) -> Dict[str, Any]:
        return self.get_globals_by_function(function)

    def get_all_names(self, tree: ast.AST) -> Set[str]:
        all_original_names = set()

        class Visiter(ast.NodeVisitor):
            def visit(_self, node: ast.AST) -> Optional[ast.AST]:
                try:
                    if isinstance(node, ast.Name):
                        all_original_names.add(node.id)
                except Exception:
                    pass

        Visiter().visit(tree)

        return all_original_names
