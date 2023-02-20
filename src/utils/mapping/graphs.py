from typing import List, Tuple

import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from networkx import Graph

from src.utils.mapping.arrays import get_city_pairs_distances


def path_distance(graph: nx.Graph, path: List[str], start_index: int = 0, end_index: int = -1) -> float:
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


def graph_heat_map(graph: Graph, graph_size, weight: str = 'score', fig: Figure = None):
    nodes = graph.nodes
    # print(nodes)
    pos = nx.get_node_attributes(graph, 'pos')
    factors = nx.get_node_attributes(graph, weight)
    # print(factors)
    # print(pos)
    x = [v[0] for v in pos.values()]
    y = [v[1] for v in pos.values()]
    # scores is like :
    # { (x, y) : 0.3268906891569111,
    #   (x, y) : 0.9968906891569111,
    #   (x, y) : 0.6268986891569111}
    # the higher values means avoid at all costs.
    if not fig:
        fig: Figure = fig or plt.figure(figsize=(5, 5))
        ax = plt.axis([-5, graph_size + 5, -5, graph_size + 5])

    # ACTION / FLEE MAP
    for node in nodes.values():
        # print(node)
        plt.annotate(node.get('fear_factor'), xy=node.get('pos'), textcoords="offset points", xytext=(0, 10),
                     ha='center', fontsize=8)
        plt.annotate(node.get('life'), xy=node.get('pos'), textcoords="offset points", xytext=(0, 18),
                     ha='center', fontsize=8)
    plt.scatter(x=x, y=y, data=pos, s=50)
    sns.kdeplot(data=factors, bw_method='silverman',
                x=x, y=y, cmap='Reds', n_levels=15,
                warn_singular=False, common_grid=True,
                common_norm=True, levels=15, )
    # for k, v in scores.items():
    #     plt.annotate(text=)
    # plt.show()
    return fig


def entities_to_graph(entities, pairs=None) -> Graph:
    graph = nx.Graph()
    pairs = pairs or get_city_pairs_distances(entities)
    for name, *coords in entities:
        graph.add_node(name, pos=tuple(coords))
    for pair, dist in pairs.items():
        graph.add_edge(pair[0], pair[1], distance=dist)
    return graph


def display_graph_map(graph: Graph, path: List[str], graph_size, _fig: Figure = None, with_edges=False) -> Figure:
    if not _fig:
        _fig = plt.figure(figsize=(20, 20))
        plt.axis([-5, graph_size + 5, -5, 30])
    pos = nx.get_node_attributes(graph, 'pos')
    # print(pos)
    nx.draw_networkx_nodes(graph, pos, node_size=30)
    nx.draw_networkx_labels(graph, pos, font_size=9)
    if with_edges:
        nx.draw_networkx_edges(graph, pos, width=1)
    nx.draw_networkx_edges(graph, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                           width=4, edge_color='g')
    plt.axis('off')
    plt.show()
    return _fig


def display_scatter_comparatif(graph: Graph):
    # Extract the X and Y coordinates of each node
    print([_[:][1] for _ in graph.nodes.items()])
    x = [node['distance'] for node in graph.nodes.items() if node['bot']]
    y = [node['bot']['life'] for node in graph.nodes.items() if node['bot']]
    size = [node['ammo'] for node in graph.nodes.items() if node['bot']]
    color = [node['fear_factor'] for node in graph.nodes.items() if node['bot']]

    # Create a scatter plot of the nodes
    fig, ax = plt.subplots()
    ax.scatter(x, y, s=size, c=color, cmap='viridis')

    # Add labels to each point in the scatter plot
    for i, node in enumerate(graph.nodes):
        ax.annotate(node, (x[i], y[i]))

    # Add color bar to show the meaning of the colors
    cbar = plt.colorbar()
    cbar.set_label('Fear Factor')

    # Add axis labels and a title
    ax.set_xlabel('Distance')
    ax.set_ylabel('Life')
    ax.set_title('Scatter plot of nodes in the graph')

    # Show the plot
    fig.tight_layout()
    fig.savefig("facet_plot.png")
    plt.show()
    return fig


def extract_graph(graph: Graph) -> Tuple[List, List]:
    # extract features and labels
    features = []
    labels = []
    for n, node in graph.nodes.items():
        if node.get('bot'):
            # extract features
            dist = node['distance']
            ammo = node['ammo']
            life = node['life']
            fear_factor = node['fear_factor']
            # print(f'{n} => {node}')
            features.append([dist, ammo, life])
            # label as FLEE or ENGAGE based on some criteria
            if fear_factor > .33 and life:
                labels.append('FLEE')
            else:
                labels.append('ENGAGE')

    return features, labels
