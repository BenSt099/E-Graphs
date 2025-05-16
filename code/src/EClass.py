"""This module implements an EGraph class.

Classes:
    EClass: Represents an EClass together with its unique EClass-ID.
"""

import uuid


class EClass:
    """Class that represents an EClass.

    Attributes:
        - id: Unique identifier for this class (EClass-ID).
        - nodes: A set of ENodes
        - parents: A Set of tuples with: tuple(ENode, EClass-ID).
    """

    def __init__(self):
        """Initialises class. Takes no arguments."""
        self.id = str(uuid.uuid4())
        self.nodes = set()
        self.parents = set()
