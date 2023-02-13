import itertools
from typing import List, Tuple

import numpy as np


class TSP:
    """The Shortest Path
    Compute all possible paths, given their distances and find the fastest
    """

    def __init__(self, cities: List[Tuple[str, int, int]], starting_city: tuple[str, int, int]):
        self.__cities = cities
        self.__start = starting_city
        self.__size = len(cities)

        # Set an empty 2D numpy array, from cities length
        self.__distances = np.empty(shape=(self.__size, self.__size))

        # Fill the array with distances between each entity
        for i in range(self.__size):
            for j in range(i + 1, self.__size):
                n1, *starting_city = self.__cities[i]
                n2, *ending_city = self.__cities[j]
                # if (n1, n2) not in visited:
                dist = np.linalg.norm(np.array(starting_city) - np.array(ending_city))
                self.__distances[i][j] = dist
                self.__distances[j][i] = dist

    @property
    def distances(self):
        return self.__distances

    def solve(self):

        start_index = self.__cities.index(self.__start)
        best_path = None
        best_dist = float("inf")
        # for EVERY possible path
        for path in itertools.permutations(range(self.__size)):
            # if it doesn't start with the wanted city, skip (most of possible paths)
            if path[0] != start_index:
                continue

            # calculate optimal distance to travel
            dist = 0
            for i in range(self.__size - 1):
                dist += self.__distances[path[i]][path[i + 1]]
            dist += self.__distances[path[-1]][path[0]]

            if dist < best_dist:
                best_path = path
                best_dist = dist

        return list(best_path), best_dist