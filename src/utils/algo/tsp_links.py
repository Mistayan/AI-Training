import itertools
from functools import partial
from multiprocessing import Pool, cpu_count
from typing import List, Tuple

from src.utils import mapping
from src.utils.algo.ISolver import ISolver
from src.utils.mapping import path_distance, rec_find_bests
from src.utils.metrics import measure_perf


# @measure_perf
class TSPMap(ISolver):
    # @measure_perf
    def __init__(self, cities: List[Tuple[str, int, int]]):
        """
        Compute all possible distances between entities given for future uses
        :param cities: cities to explore, with coordinates
        """
        self.__cities = cities
        self.__size = len(cities)
        self.__distances = mapping.get_city_pairs_distances(self.__cities)
        self.__start_index = 0
        print("entities distances processed")

    @property
    def distances(self):
        return self.__distances.copy()

    @measure_perf
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

        # for EVERY possible path
        possibilities = (
            (self.__cities, self.__distances, _, 0)
            for _ in itertools.permutations(range(self.__size))
            if _[0] == start_index
        )

        # calculate optimal distance to travel
        res = itertools.starmap(path_distance, possibilities).__iter__()
        print(f"advanced mapping done")

        # best_path, best_dist = min(res, key=lambda x: x[1])
        for p, d in res:
            if not max_iter > 0:
                break
            max_iter -= 1
            if d < best_dist:
                best_dist = d
                best_path = p
        return list(best_path), best_dist
