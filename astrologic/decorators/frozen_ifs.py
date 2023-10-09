import ast
from astrologic.decorators.base import BaseDecorator


class FrozenIfs(BaseDecorator):
    def change_tree(self, tree, original_function, function_text, *args, **kwargs):
        self.add_prefix_and_postfix(function_text, original_function)
        index = 0
        class RewriteName(ast.NodeTransformer):
            def visit_If(self, node):
                _nonlocal = ast.Nonlocal(names=['__ast_container'])
                append = Expr(
                    value=Call(
                        func=Attribute(
                            value=Name(
                                id='__ast_container', ctx=Load()
                            ),
                            attr='append',
                            ctx=Load()
                        )
                    ),
                    args=[Constant(value=index)],
                    keywords=[],
                )
                index += 1
                return [_nonlocal, append, node]
        return RewriteName().visit(tree)

    @staticmethod
    def add_prefix_and_postfix(function_text, original_function):
        function_name = original_function.__name__
        prefix = f"""def superfunction(*args, **kwargs):
    is_recursion = False
"""
        postfix = f"""    while True:
        result = {original_function.__name__}(*args, **kwargs)
        if not is_recursion:
            return result
        is_recursion = False
        args, kwargs = result""".replace('\t', function_text.indent_symbols)
        function_text.wrapp_clean_text(prefix=prefix, postfix=postfix, indent=1)


def superfunction(*args, **kwargs):
    __ast_container = []
    __exception = None
    def a():
        if a: b
    try:
        result = a()
    except Exception as e:
        __exception = e
        result = None
    nonlocal __new_call__
    superfunction.__call__ = __new_call__

frozen_ifs = FrozenIfs()
