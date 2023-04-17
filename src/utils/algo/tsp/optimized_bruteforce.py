import itertools
from typing import List, Tuple

import networkx as nx

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.graphs import entities_to_graph
from src.utils.metrics import measure_perf


class TSPMap(ISolver):
    """The Shortest Path
    Compute all possible paths, given their distances and find the fastest

    Distances matrice may be used to train an AI model.

    >>> shortest_path, distance = TSP(cities=list()).solve(start_index=0, end=0, back_to_start=False)
    """

    @property
    def distances(self):
        return nx.get_edge_attributes(self.__graph, "distance")

    def __init__(self, cities: List[Tuple[str, int, int]], current_location: Tuple[int, int] = None):
        """
        Create the graph representation of the cities
        :param cities: cities to explore, with coordinates
        """
        self.__cities = cities
        self.__size = len(cities)

        self.__graph = entities_to_graph(cities)

    @property
    def graph(self):
        return self.__graph.copy(True)

    @measure_perf
    def solve(self, start_index: int = 0, end: int = 0, back_to_start=False):
        """
        Compute the fastest path from permutations of the cities indexes

        Skip paths that doesn't start with starting city and process those that does

        :param start_index: index of the city to start from
        :param end: index of the city to end to (leave empty to find the fastest path of all) # NO IMPLEMENTED
        :param back_to_start: do you require to go back from where you came ?
        :return: a Tuple containing 'the fastest path' and its 'distance'
        """
        best_path = None
        best_dist = float("inf")
        dist_dict = dict(nx.get_edge_attributes(self.__graph, "distance"))
        # for EVERY possible path
        for path in itertools.permutations(range(self.__size)):
            # if it doesn't start with the wanted city, skip (most of possible paths)
            if path[0] != start_index:
                continue

            # calculate optimal distance to travel
            dist = 0
            for i in range(self.__size - 1):
                # get the weight (distance) between the two
                weight = dist_dict.get((self.__cities[i][0], self.__cities[i + 1][0]))
                dist += weight

            # add the distance to return to the starting node if required
            if back_to_start:
                weight = dist_dict.get(path[-1], path[0])
                dist += weight

            if dist < best_dist:
                best_path = path
                best_dist = dist
        print(best_path)
        return [self.__cities[_][0] for _ in best_path], best_dist
