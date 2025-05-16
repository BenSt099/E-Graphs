"""This module implements rewrite rules.

Classes:
    RewriteRule: Represents a rewrite rule with a left and a right side.
"""

import AbstractSyntaxTree


class RewriteRule:
    """Class that represents a rewrite rule.

    Attributes:
        - name: String
        - expr_lhs: String in prefix-notation
        - expr_rhs: String in prefix-notation
    """

    def __init__(self, name, expr_lhs, expr_rhs):
        """Initialises class. Takes three arguments.

        :param name: Name of that rewrite rule.
        :param expr_lhs: Left side of the rewrite rule.
        :param expr_rhs: Right side of the rewrite rule.
        :returns: None.
        """
        self.name = name
        self.expr_lhs = AbstractSyntaxTree.AbstractSyntaxTree(expr_lhs)
        self.expr_rhs = AbstractSyntaxTree.AbstractSyntaxTree(expr_rhs)

    def __str__(self):
        """Returns a string representation of this rule."""
        return f"[{self.name}: {self.expr_lhs} => {self.expr_rhs}]"
