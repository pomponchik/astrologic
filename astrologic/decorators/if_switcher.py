import ast
from typing import List, Callable, Union, Optional, Any

from astrologic.decorators.base import BaseDecorator
from astrologic.function_text import FunctionText


class IfSwitcher(BaseDecorator):
    def change_tree(self, tree: ast.AST, original_function: Callable[..., Any], function_text: FunctionText, *args: Any, **kwargs: Any) -> Optional[Union[ast.AST, List[ast.AST]]]:
        class RewriteName(ast.NodeTransformer):
            def visit_If(self, node: ast.If) -> Optional[Union[ast.AST, List[ast.AST]]]:
                try:
                    variable_name = node.test.id
                    if variable_name in kwargs:
                        if not kwargs[variable_name]:
                            return None
                        else:
                            return node.body
                    return node

                except Exception:
                    return node

        return RewriteName().visit(tree)  # type: ignore[no-any-return]


switcher = IfSwitcher()
