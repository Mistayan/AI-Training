import re
from typing import List, Tuple

import networkx as nx
import numpy as np
from networkx import Graph

from src.utils.mapping.arrays import distances_between_entities
from src.utils.metrics import measure_perf


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
        dist += graph.edges[curr_node, next_node]['distance']

    return dist


@measure_perf
def entities_to_graph(entities, pairs=None, with_edges=True) -> Graph:
    if not entities:
        raise ValueError("entities must not be empty")
    graph = nx.Graph()
    pairs = pairs or distances_between_entities(entities) if with_edges else None
    for name, *coords in entities:
        if not name:
            continue
        type = re.findall("[A-Za-z0-9]+", name.lower())[0]
        graph.add_node(name, pos=tuple(coords), type=type)

    if with_edges:
        for pair, dist in pairs.items():
            graph.add_edge(pair[0], pair[1], distance=dist)
    return graph


def on_same_axis(me_pos, other_pos):
    return me_pos[0] == other_pos[0] or \
        me_pos[1] == other_pos[1]


@measure_perf
def extract_graph_features(graph: Graph, compare_to_me=True) -> Tuple[List[List[float]], List[str]]:
    # extract features and labels
    features = []
    labels = []
    if compare_to_me:
        me = graph.nodes["ME1"]
        me_pos = np.array(me['pos'])
    for n, node in graph.nodes.items():
        if node.get('type') == "bot":
            # extract features
            dist = node['distance']
            ammo = node['ammo']
            life = node['life']
            fear_factor = node['fear_factor']
            features.append([dist, ammo, life])

            # label as FLEE or ENGAGE based on some criteria
            # if life < 20 and ammo >= 90 and dist < 10 or \
            #         life <= 10 and dist <= 8 and compare_to_me and \
            #         on_same_axis(me_pos, node['pos']):
            #     label = "EGGS-Terminate"
            if fear_factor > .55 or life > 50:
                label = "FLEE"
            elif fear_factor <= .15 and life <= 10:
                label = "EGGS-Terminate"
            elif fear_factor < .70 and life <= 20:
                label = "Potential"
            else:
                label = "NOPE"
            labels.append(label)
    return features, labels
