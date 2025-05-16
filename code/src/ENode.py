"""This module implements an EGraph node.

Classes:
    ENode: Represents an ENode.
"""


class ENode:
    """Class that represents an ENode.

    Attributes:
        - key: Arithmetic operation or variable.
        - arguments: A list of EClass-IDs.
    """

    def __init__(self, key, arguments):
        """Initialises class. Takes two arguments.

        :param key: Arithmetic operation or variable.
        :param arguments: A list of EClass-IDs.
        :returns: None.
        """
        self.key = key
        self.arguments = arguments
