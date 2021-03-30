import ast
from astrologic.decorators.base import BaseDecorator


class IfSwitcher(BaseDecorator):
    def change_tree(self, tree, original_function, function_text, *args, **kwargs):
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
        return RewriteName().visit(tree)


switcher = IfSwitcher()
