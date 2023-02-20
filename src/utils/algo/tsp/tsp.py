import itertools
from typing import List, Tuple

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.arrays import distances


class TSP(ISolver):
    """The Shortest Path
    Compute all possible paths, given their distances and find the fastest

    Distances matrice may be used to train an AI model.

    >>> shortest_path, distance = TSP(cities=list()).solve(start_index=0, end=0, back_to_start=False)
    """

    def __init__(self, cities: List[Tuple[str, int, int]]):
        """
        Compute all possible distances between entities given for future uses
        :param cities: cities to explore, with coordinates
        """
        self.__cities = cities
        self.__size = len(cities)

        # Set an empty 2D numpy array, from cities length
        self.__distances = distances(cities)

    @property
    def distances(self):
        return self.__distances.copy()

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
        dist_dict = {}
        # for EVERY possible path
        for path in itertools.permutations(range(self.__size)):
            # if it doesn't start with the wanted city, skip (most of possible paths)
            if path[0] != start_index:
                continue

            # calculate optimal distance to travel
            # Calculations optimized at the cost of a bit of memory => save previously encountered tuple of cities dists
            dist = 0
            for i in range(self.__size - 1):
                path_tuple = (path[i], path[i + 1])
                if path_tuple in dist_dict:
                    dist += dist_dict[path_tuple]
                else:
                    distance = self.__distances[path[i]][path[i + 1]]
                    dist += distance
                    dist_dict[path_tuple] = distance

            dist += back_to_start * self.__distances[path[-1]][path[0]]

            if dist < best_dist:
                best_path = path
                best_dist = dist
        return [self.__cities[_][0] for _ in best_path], best_dist
