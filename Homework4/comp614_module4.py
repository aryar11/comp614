"""
COMP 614
Provided code for homework 4: directed graph class.
"""


class DiGraph:
    """
    A representation of a directed graph.
    """

    def __init__(self):
        """
        Constructs a new empty graph.
        """
        self._graph = {}

    def nodes(self):
        """
        Returns a set containing all of the nodes in the graph.
        """
        return set(self._graph.keys())

    def get_neighbors(self, node):
        """
        Given a particular node, returns a set containing all neighbors of that
        node in the graph. This will only include neighbors that are connected
        to one of node's *outbound* edges.
        """
        return self._graph[node]

    def add_node(self, node):
        """
        Adds the given node to the graph.
        """
        if node not in self._graph:
            self._graph[node] = set([])

    def add_edge(self, node1, node2):
        """
        Adds an edge from node1 to node2.
        """
        self.add_node(node1)
        self.add_node(node2)
        self._graph[node1].add(node2)

    def copy(self):
        """
        Returns a deep copy of this graph.
        """
        new_graph = DiGraph()

        # Copy all edges, which will also copy the nodes
        for node, nbrs in self._graph.items():
            for nbr in nbrs:
                new_graph.add_edge(node, nbr)

        return new_graph

    def __eq__(self, other):
        """
        Returns True if self and other are equivalent DiGraph objects; returns 
        False otherwise.
        """
        # Check that other has the correct type
        if type(other) != DiGraph:
            return False

        # Check that other has the same nodes as self
        elif other.nodes() != self.nodes():
            return False

        # Check that other has the same edges as self
        for node, nbrs in self._graph.items():
            if other.get_neighbors(node) != nbrs:
                return False

        # Passed all equivalence checks
        return True
