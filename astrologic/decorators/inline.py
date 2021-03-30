import ast
import uuid
import importlib
from astrologic.decorators.base import BaseDecorator
from astrologic.function_text import FunctionText


class Inliner(BaseDecorator):
    def change_tree(self, tree, original_function, function_text, *functions, **kwargs):
        all_original_names = self.get_all_names(tree)
        class VisiterCalls(ast.NodeTransformer):
            def visit_Expr(_self, node):
                try:
                    value = node.value
                    _node = node
                    if isinstance(value, ast.Call):
                        node = value
                        if node.func.id in functions:
                            function_name = node.func.id
                            function_tree = self.get_function_tree(function_name, original_function.__module__)
                            new_block, declarations = self.replace_names(all_original_names, function_tree, node)
                            new_block = new_block.body[0].body
                            return declarations + new_block
                        else:
                            return _node
                except Exception as e:
                    return node
        return VisiterCalls().visit(tree)

    def get_declaration_block(self, function_tree, call, cache):
        result = []
        args = call.args
        for arg in args:
            old_name = arg.id
            if old_name in cache:
                new_node = ast.Assign(
                    targets=[ast.Name(id=cache[old_name], ctx=ast.Store())],
                    value=arg,
                )
                result.append(new_node)
        tr = function_tree
        for arg, new_arg in zip(args, tr.body[0].args.args):
            old_name = arg.id
            if old_name not in cache:
                new_node = ast.Assign(
                    targets=[ast.Name(id=new_arg.arg, ctx=ast.Store())],
                    value=ast.Name(id=old_name, ctx=ast.Load()),
                )
                result.append(new_node)
        return result

    def replace_names(self, all_original_names, tree, call_node):
        cached_names = {}
        allowed = {x.id for x in call_node.args}
        class Visiter(ast.NodeTransformer):
            def visit_Name(_self, node):
                try:
                    name = node.id
                    if name in allowed:
                        new_name = self.new_name(all_original_names, name, cached_names)
                        node.id = new_name
                    return node
                except Exception as e:
                    return node
        tree = ast.fix_missing_locations(Visiter().visit(tree))
        declarations = self.get_declaration_block(tree, call_node, cached_names)
        return tree, declarations

    def new_name(self, all_original_names, name, cache):
        if name in cache:
            return cache[name]
        number = 0
        while True:
            new_name = 'generated_' + uuid.uuid4().hex
            if new_name not in all_original_names:
                cache[name] = new_name
                return new_name

    def get_function_tree(self, function_name, module_name):
        try:
            module = importlib.import_module(module_name)
        except ModuleNotFoundError:
            return []
        function = getattr(module, function_name)
        text = FunctionText(function)
        tree = self.get_source_tree(text)
        return tree


inline = Inliner()
