from typing import List, Tuple

import networkx as nx
from networkx.algorithms.shortest_paths.astar import astar_path_length

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.graphs import entities_to_graph


class MyGraph(ISolver):

    def __init__(self, cities: List[Tuple[str, int, int]], current_location: Tuple[int, int] = None):
        self.__cities = cities
        self.__graph = entities_to_graph(cities, with_edges=True)
        self.__me = None
        self.__paths = nx.single_source_dijkstra_path(self.__graph, cities[0][0], weight="distance")

    @property
    def distances(self):
        return self.__graph.edges.data("distance")

    def solve(self, start_index: int = 0, end: int = 0, back_to_start=False):

        # Use A* algorithm to find the shortest path that visits all cities
        paths = []
        previous_node = None
        for i, (node, data) in enumerate(self.__graph.nodes.items()):
            if i == 0:
                previous_node = node
                continue
            paths.append(
                nx.algorithms.astar_path(self.__graph, source=previous_node, target=node, weight="distance")[1])
        tsp_path = [city for city in paths]

        # Compute the total distance of the TSP path
        total_distance = 0
        for i in range(len(tsp_path) - 1):
            src, dest = tsp_path[i], tsp_path[i + 1]
            total_distance += astar_path_length(self.__graph, src, dest, weight="distance")
        return [self.__cities[0][0]] + tsp_path, total_distance
