# Neighbor joining algorithm code from www.github.com/anicksaha/neighbor_joining.


class Node:
    def __init__(self, id: str):
        """
        Initialize a Node with an ID.

        Args:
            id (str): The unique identifier for the node.
        """
        self._id = id
        self._children = {}

    @property
    def id(self) -> str:
        """
        Get the ID of the node.

        Returns:
            str: The unique identifier of the node.
        """
        return self._id

    @property
    def children(self) -> dict:
        """
        Get the children of the node along with their distances.

        Returns:
            dict: A dictionary mapping child nodes to their distances.
        """
        return self._children

    def add_child(self, node: 'Node', distance: float):
        """
        Add a child node with a given distance.

        Args:
            node (Node): The child node to be added.
            distance (float): The distance to the child node.
        """
        self._children[node] = distance

