import ast
from astrologic.decorators.base import BaseDecorator


class IfSwitcher(BaseDecorator):
    def change_tree(self, tree, function_text, **kwargs):
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
        return new_tree


switcher = IfSwitcher()
