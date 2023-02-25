from typing import List

import networkx as nx
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from networkx import Graph

from src.utils.os_utils import gen_file


def graph_heat_map(graph: Graph, map_size, weight: str = 'score', main_attribute='life', fig: Figure = None,
                   colors_only=False, ax=None):
    """

    :param graph: The graph containing the entities and their various information. Must contain 'pos', 'weight', 'main_attribute'
    :param map_size: used to place figure's axes for homogeneous display
    :param weight: Which factor do you require to draw a heat-map from ?
    :param fig: If you already draw a figure, and you want to append results on top of your previous graph

    :return:
        the figures filled with a heat map from graph

    """
    nodes = graph.nodes
    pos = nx.get_node_attributes(graph, 'pos')
    factors = nx.get_node_attributes(graph, weight)
    factors.setdefault("ME", 0)
    x, y = [], []
    for v in pos.values():
        x.append(v[0])
        y.append(v[1])

    # the higher values means avoid at all costs.
    if not fig:
        fig: Figure = fig or plt.figure(figsize=(10, 10))
        plt.axis([-5, map_size + 5, -5, map_size + 5])

    # ACTION / FLEE MAP
    if colors_only is False:  # annotate points with designated weight
        for node in nodes.values():
            plt.annotate(node.get(weight), xy=node.get('pos'), textcoords="offset points", xytext=(0, 10),
                         ha='center', fontsize=8)
            plt.annotate(node.get(main_attribute), xy=node.get('pos'), textcoords="offset points", xytext=(0, 18),
                         ha='center', fontsize=8)
    ax = sns.kdeplot(data=factors, bw_method='silverman', bw_adjust=.8,
                     x=x, y=y, cmap='viridis', n_levels=15,
                     warn_singular=False, common_grid=True,
                     common_norm=True, levels=100, gridsize=map_size)

    # compute weights to define plot's sizes
    sizes = [(1 / (_ + 0.1) * 20) + 50 for _ in list(factors.values())]
    sc = ax.scatter(x=x, y=y, data=factors, s=sizes,
                    c=list(factors.values()), cmap="viridis")

    # plot ME1 node
    me1 = nodes["ME1"]
    ax.scatter(x=me1["pos"][0], y=me1["pos"][1], data=factors, s=300, c='r', zorder=2)

    # display Heat-Bar to better understand the plots
    cbar = plt.colorbar(sc)
    cbar.set_label('Fear Factor')

    return fig


def display_graph_map(graph: Graph, path: List[str], graph_size, _fig: Figure = None, with_edges=False,
                      colors_only=False, ax=None) -> Figure:
    if _fig is None:
        _fig = plt.figure(figsize=(10, 10))
        ax = plt.axis([-5, graph_size + 5, -5, 30])
    pos = nx.get_node_attributes(graph, 'pos')
    colors = nx.get_node_attributes(graph, 'fear_factor')
    colors.setdefault("ME1", 0)

    if colors_only is False:
        nx.draw_networkx_labels(graph, pos, font_size=9)
    if not _fig:  # If no previous graph, display nodes as points
        nx.draw_networkx_nodes(graph, pos, node_size=10)
    if with_edges is True:  # print entities connections on demand
        nx.draw_networkx_edges(graph, pos, width=1)
    nx.draw_networkx_edges(graph, pos, edgelist=[(path[i], path[i + 1]) for i in range(len(path) - 1)],
                           width=4, edge_color='g')
    return _fig


def display_scatter_comparatif(graph: Graph, type='bot', colors_only=False):
    # Extract the X and Y coordinates of each node
    nodes = [_[:][1] for _ in graph.nodes.items()]
    x, y, size, color = [], [], [], []

    for node in nodes:
        if not node.get('type') == type:
            continue
        x.append(node['distance'])
        y.append(node['life'])
        size.append(node['ammo'])
        color.append(node['fear_factor'])

    fig, ax = plt.subplots(figsize=(5, 5))
    sc = ax.scatter(x, y, s=size, c=color, cmap='viridis')
    ax.set_xlabel('Distance')
    ax.set_ylabel('Life')
    ax.set_title('Scatter plot of nodes in the graph')
    n = len(x)
    for i, node in enumerate(graph.nodes):
        if i == n:
            break
        if not node.lower().startswith(type):
            continue
        if colors_only is False:
            ax.annotate(node, (x[i], y[i]))

    # display Heat-Bar to better understand the plots
    cbar = plt.colorbar(sc)
    cbar.set_label('Fear Factor')
    return fig


def display_all_figs_from_graph(graph, grid_size, colors_only=True, predictions: List = None):
    # superpose plot layers for better visualization
    fig = display_graph_map(graph, [], grid_size, colors_only=colors_only)
    fig2 = graph_heat_map(graph, map_size=grid_size, fig=fig, weight='fear_factor', colors_only=colors_only)
    fig2.savefig(gen_file("#heat-map.png"))
    plt.show()

    # comparatif between different values
    fig3 = display_scatter_comparatif(graph, colors_only=colors_only)
    fig3.savefig(gen_file("#factors-map.png"))
    plt.show()
