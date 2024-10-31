"""
COMP 614
Homework 4: Graphs
"""
from collections import deque
import comp614_module4


def file_to_graph(filename):
    """
    Given the name of a file, reads the contents of that file and uses it to
    build a graph. Assumes that each line will contain the name of a single node.
    If the line does not start with a tab, it contains the name of a new node to
    be added to the graph. If the line starts with a tab, it contains the name of
    a node that is a neighbor of the most recently added node.

    For example, imagine that the file is structured as follows:
    node1
        node2
        node3
    node2
        node1
    node3

    In this case, the graph has three nodes: node1, node2, and node3. node1 has
    outbound edges to node2 and node3. node2 has an outbound edge to node1. node3
    has no outbound edges.
    """
    graph = comp614_module4.DiGraph()
    curr_node = None
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('\t'):
                graph.add_edge(curr_node, line.strip())
            else:
                curr_node = line.strip()
                graph.add_node(curr_node)
    return graph

class Queue:
    """
    A representation of a FIFO queue.
    """

    def __init__(self):
        """
        Constructs a new empty queue.
        """
        self._queue = deque()

    def __len__(self):
        """
        Returns an integer representing the number of items in the queue.
        """
        return len(self._queue)

    def __str__(self):
        """
        Returns a string representation of the queue.
        """
        return "Queue: " + " -> ".join(map(str, self._queue))

    def push(self, item):
        """
        Adds the given item to the queue.
        """
        self._queue.append(item)

    def pop(self):
        """
        Removes and returns the least recently added item from the queue.
        Assumes that there is at least one element in the queue.
        """
        return self._queue.popleft() if self._queue else None

    def clear(self):
        """
        Removes all items from the queue.
        """
        self._queue.clear()


def bfs(graph, start_node):
    """
    Performs a breadth-first search on the given graph starting at the given
    node. Returns a two-element tuple containing a dictionary mapping each
    node to its distance from the start node and a dictionary mapping each
    node to its parent in the search.
    """
    queue = Queue()
    dist = {}
    parent = {}

    for node in graph.nodes():
        dist[node] = float("inf")
        parent[node] = None
    dist[start_node] = 0
    queue.push(start_node)
    while len(queue) != 0:
        curr = queue.pop()
        for neighbor in graph.get_neighbors(curr):
            if dist[neighbor] == float("inf"):  
                dist[neighbor] = dist[curr] + 1 
                parent[neighbor] = curr 
                queue.push(neighbor)  

    return dist, parent


def connected_components(graph):
    """
    Finds all weakly connected components in the graph. Returns these components
    in the form  of a set of components, where each component is represented as a
    frozen set of nodes. Should not mutate the input graph.
    """
    visited = set()  # Keeps track of visited nodes
    components = set()  # Stores each component as a frozenset

    # Helper function to perform BFS and gather nodes in the current component
    def bfs_component(start_node):
        queue = Queue()
        queue.push(start_node)
        component = set()  # To store nodes in the current component
        visited.add(start_node)
        
        while len(queue) > 0:
            node = queue.pop()
            component.add(node)
            
            # Get all neighbors in both directions for weak connectivity
            neigh = graph.get_neighbors(node)
            nodes = {n for n in graph.nodes() if node in graph.get_neighbors(n)}
            neighbors = neigh | nodes
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.push(neighbor)
                    
        return component

    # Go through each node in the graph
    for node in graph.nodes():
        if node not in visited:
            component = bfs_component(node)
            components.add(frozenset(component)) 

    return components