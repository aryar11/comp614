"""
COMP 614
Homework 6: DFS + PageRank
"""

import comp614_module6


def bfs_dfs(graph, start_node, rac_class):
    """
    Performs a breadth-first search on graph starting at the given node.
    Returns a two-element tuple containing a dictionary mapping each visited
    node to its distance from the start node and a dictionary mapping each
    visited node to its parent node.
    """
    rac = rac_class()
    parent = {}

    rac.push(start_node)
    parent[start_node] = None  

    while rac:
        node = rac.pop()

        for neighbor in graph.get_neighbors(node):
            if neighbor not in parent:
                parent[neighbor] = node
                rac.push(neighbor)
    return parent


def recursive_dfs(graph, start_node, parent):
    """
    Recursively performs a depth-first search on the graph.
    Updates the parent mapping in-place as nodes are visited.
    """
    for neighbor in graph.get_neighbors(start_node):
        if neighbor not in parent:
            parent[neighbor] = start_node
            recursive_dfs(graph, neighbor, parent)


def get_inbound_nbrs(graph):
    """
    Given a directed graph, returns a mapping of each node n in the graph to
    the set of nodes that have edges into n.
    """
    inbound_nbrs = {node: set() for node in graph.nodes()}
    for node in graph.nodes():
        neighbors = graph.get_neighbors(node)
        for neigh in neighbors:
            inbound_nbrs[neigh].add(node)
    return inbound_nbrs


def remove_sink_nodes(graph):
    """
    Given a directed graph, returns a new copy of the graph where every node that
    was a sink node in the original graph now has an outbound edge linking it to 
    every other node in the graph (excluding itself).
    """
    graph2 = graph.copy()

    for node in graph2.nodes():
        if len(graph2.get_neighbors(node)) == 0:
            for node2 in graph2.nodes():
                if node2 != node:
                    graph2.add_edge(node, node2)
    return graph2


def page_rank(graph, damping):
    """
    Given a directed graph and a damping factor, implements the PageRank algorithm
    -- continuing until delta is less than 10^-8 -- and returns a dictionary that 
    maps each node in the graph to its page rank.
    """
    graph = remove_sink_nodes(graph)

    nodes = graph.nodes()
    length = len(nodes)
    ranks = {node: 1 / length for node in nodes}  
    inbound_nbrs = get_inbound_nbrs(graph)  
    delta = float("inf")  
    epsilon = 1e-8  

    while delta >= epsilon:
        new_ranks = {}
        for node in nodes:
            rank_sum = sum(
                ranks[neighbor] / len(graph.get_neighbors(neighbor))
                for neighbor in inbound_nbrs[node]
            )
            new_ranks[node] = (1 - damping) / length + damping * rank_sum

        delta = sum(abs(new_ranks[node] - ranks[node]) for node in nodes)
        ranks = new_ranks

    return ranks

graph = comp614_module6.file_to_graph("wikipedia_articles_streamlined.txt")
damping_factor = 0.85

# Run the PageRank algorithm
page_ranks = page_rank(graph, damping_factor)

# Sort the articles by PageRank in descending order and extract the top 10
top_articles = sorted(page_ranks.items(), key=lambda x: x[1], reverse=True)[:10]

print(top_articles)