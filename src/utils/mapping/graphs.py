from typing import List, Tuple

import networkx as nx
from networkx import Graph

from src.utils.mapping.arrays import get_city_pairs_distances


def path_total_distance(graph: nx.Graph, path: List[str], start_index: int = 0, end_index: int = -1) -> float:
    """
    Compute the total distance of a given path in a weighted graph.

    :param graph: the graph
    :param path: the path as a list of node labels
    :param start_index: the index of the starting node (default 0)
    :param end_index: the index of the end node (default -1, i.e., the last node in the path)
    :return: the total distance of the path
    """
    if end_index == -1:
        end_index = len(path) - 1

    dist = 0.0
    for i in range(start_index, end_index):
        curr_node = path[i]
        next_node = path[i + 1]
        dist += graph.edges[curr_node, next_node]['weight']

    return dist


def entities_to_graph(entities, pairs=None, with_edges=True) -> Graph:
    graph = nx.Graph()
    pairs = pairs or get_city_pairs_distances(entities)
    for name, *coords in entities:
        graph.add_node(name, pos=tuple(coords))
    if with_edges:
        for pair, dist in pairs.items():
            graph.add_edge(pair[0], pair[1], distance=dist)
    return graph


def extract_graph_features(graph: Graph) -> Tuple[List[List[float]], List[str]]:
    # extract features and labels
    features = []
    labels = []
    for n, node in graph.nodes.items():
        if node.get('type') == "bot":
            # extract features
            dist = node['distance']
            ammo = node['ammo']
            life = node['life']
            fear_factor = node['fear_factor']
            # print(f'{n} => {node}')
            features.append([dist, ammo, life])
            # label as FLEE or ENGAGE based on some criteria
            if fear_factor > .33 or life > 50:
                labels.append('FLEE')
            else:
                labels.append('ENGAGE')

    return features, labels
