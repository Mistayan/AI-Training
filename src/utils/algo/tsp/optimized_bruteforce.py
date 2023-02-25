from typing import List, Tuple

import networkx as nx

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.arrays import get_city_pairs_distances
from src.utils.mapping.graphs import entities_to_graph


class TSPMap(ISolver):
    def __init__(self, cities: List[Tuple[str, int, int]]):
        """
        Compute all possible distances between entities given for future uses
        :param cities: cities to explore, with coordinates
        """
        self.__cities = cities
        self.__size = len(cities)
        self.__distances = get_city_pairs_distances(cities)
        self.__graph = entities_to_graph(cities, self.__distances)
        self.__start_index = 0
        print("entities distances processed")

    @property
    def distances(self):
        return self.__distances.copy()

    # @measure_perf
    def solve(self, start_index: int = 0, end: int = 0, back_to_start=False, max_iter: int = float('inf')):
        """
        Compute the fastest path from permutations of the cities indexes

        Skip paths that doesn't start with starting city and process those that does

        :param max_iter: maximum of iterations to go through before returning current best_path
        :param start_index: index of the city to start from
        :param end: index of the city to end to (leave empty to find the fastest path of all)  # NOT IMPLEMENTED
        :param back_to_start: do you require to go back from where you came ?  # NOT IMPLEMENTED
        :return: a Tuple containing 'the fastest path' and its 'distance'
        """
        self.__start_index = start_index
        best_path = None
        best_dist = float('inf')

        # Find the optimal path using Dijkstra's algorithm
        start_node = self.__graph.nodes[self.__cities[start_index][0]]
        start_node["distance"] = 0
        queue = [start_node]
        visited = set()
        # Extract the best path
        best_path = [i for i in nx.shortest_path(self.__graph, source=start_node, target=end)]

        # Convert indexes to city coordinates
        path_coords = [self.__cities[i] for i in best_path]

        # Calculate total distance
        total_dist = sum(self.distances[i][j] for i, j in zip(best_path[:-1], best_path[1:]))

        return path_coords, total_dist
