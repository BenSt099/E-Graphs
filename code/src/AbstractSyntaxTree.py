"""This module creates an AbstractSyntaxTree from a given expression.

Classes:
    AbstractSyntaxTree: Class used for generating AST from expression.
    AbstractSyntaxTreeNode: Class used for representing nodes in an AST.
"""

from collections import deque


class AbstractSyntaxTreeNode:
    """Class that represents a node in an AST.

    Please also see class 'AbstractSyntaxTree'.

    Attributes:
        - left: Another ASTNode.
        - key: A string to store information
        - right: Another ASTNode.
    """

    def __init__(self):
        """Initialises class. Takes no arguments."""
        self.left = None
        self.key = str()
        self.right = None


class AbstractSyntaxTree:
    """This class represents an abstract syntax tree by processing an expression
    in prefix-notation in an AST.

    Attributes:
        - root_node: The root ASTNode of the tree.

    Example:

        expr = "(/ (* a 2) 2)"  # in prefix-notation (original: (a*2) / 2)

        ast = AbstractSyntaxTree(expr)

        ast.root_node   # get root node in tree for traversing

        str(ast)        # Returns string representation (equals the input expression)
    """

    def __init__(self, expression):
        """Initializes class. Takes one argument.

        :param expression: A string representing an expression in prefix-notation.
        :returns: None.
        """
        self.root_node = self._process_expression(expression)
        self._string_representation = str()
        self._preorder(self.root_node)
        self._string_representation = self._string_representation.strip()
        if not self._string_representation.startswith("("):
            self._string_representation = "(" + self._string_representation + ")"

    def __str__(self):
        """Returns the string representation of the AST."""
        return self._string_representation

    def _preorder(self, ast_node):
        """Traverses the AST (preorder) and writes result to '_string_representation'.

        :param ast_node: The root ASTNode of the tree.
        :returns: None.
        """
        if ast_node is not None:
            if ast_node.key in ("/", "*", "+", "-", "<<", ">>"):
                self._string_representation += "(" + str(ast_node.key) + " "
            else:
                self._string_representation += str(ast_node.key) + " "
            self._preorder(ast_node.left)
            self._preorder(ast_node.right)
            if ast_node.key in ("/", "*", "+", "-", "<<", ">>"):
                self._string_representation = self._string_representation.strip()
                self._string_representation += ") "

    def _process_expression(self, expression):
        """Turns given expression into AST thereby returning AST's root node.

        Loops over expression, thereby processing one character at a time.
        Character can be: '+', '*', '-', '/', '<<', '>>', '(', ')', ' ' or
        a variable ([a-zA-Z0-9_]+) or a number ([0-9]+).

        :param expression: A string representing an expression in prefix-notation.
        :returns: Instance of ASTNode which servers as root node of created AST.
        """
        root_ast_node = None
        stack = deque()
        word = ""

        for character in expression:
            if character == "(":
                if not stack:
                    ast_node = AbstractSyntaxTreeNode()
                    stack.append(ast_node)
                    root_ast_node = ast_node
                else:
                    last_ast_node = stack[-1]
                    ast_node = AbstractSyntaxTreeNode()
                    if last_ast_node.left is None and last_ast_node.right is None:
                        last_ast_node.left = ast_node
                    elif last_ast_node.left is None:
                        last_ast_node.left = ast_node
                    else:
                        last_ast_node.right = ast_node
                    stack.append(ast_node)
            elif character == ")" and word == "":
                stack.pop()
            elif character in ("/", "*", "+", "-"):
                last_ast_node = stack[-1]
                last_ast_node.key = character
            elif (word == "<" or word == ">") and (character == "<" or character == ">"):
                word += character
                last_ast_node = stack[-1]
                last_ast_node.key = word
                word = ""
            elif (character == " " or character == ')') and word != "":
                last_ast_node = stack[-1]
                if (
                        last_ast_node.left is None
                        and last_ast_node.right is None
                        and not last_ast_node.key == ""
                ):
                    ast_node = AbstractSyntaxTreeNode()
                    ast_node.key = word
                    last_ast_node.left = ast_node
                elif last_ast_node.left is None and last_ast_node.right is None:
                    last_ast_node.key = word
                elif last_ast_node.left is None:
                    ast_node = AbstractSyntaxTreeNode()
                    ast_node.key = word
                    last_ast_node.left = ast_node
                else:
                    ast_node = AbstractSyntaxTreeNode()
                    ast_node.key = word
                    last_ast_node.right = ast_node

                if character == ")":
                    stack.pop()
                word = ""
            elif character == " ":
                pass
            else:
                word += character
        return root_ast_node