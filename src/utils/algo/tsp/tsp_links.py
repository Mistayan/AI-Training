import itertools
import threading
from queue import Queue
from typing import List, Tuple, Iterable

from src.utils import mapping
from src.utils.algo.ISolver import ISolver
from src.utils.mapping.arrays import path_distance
from src.utils.metrics import measure_perf

print_lock = threading.Lock()  # A comprendre


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
        self.__distances = mapping.arrays.get_city_pairs_distances(self.__cities)
        self.__start_index = 0
        print("entities distances processed")

    @property
    def distances(self):
        return self.__distances.copy()

    @measure_perf
    def solve(self, start_index: int = 0, end: int = 0, back_to_start=False, max_iter: int = -1):
        self.__start_index = start_index

        # for EVERY possible path
        possibilities = (
            (self.__cities, self.__distances, path)
            for path in itertools.permutations(range(self.__size), self.__size)
            if path[0] == self.__start_index
        )
        # prepare optimal distances to travel calculations
        res = iter(itertools.starmap(find_best_path, possibilities))
        # get the minimum distance path
        best_path, best_dist = min(res, key=lambda x: x[1])
        return tuple(self.__cities[_][0] for _ in best_path), best_dist


def solve_chunk(chunk: Iterable, q: Queue):
    """
    Process a chunk of the `res` iterator to find the best path
    :param q: where to save threading infos
    :param chunk: a chunk of the `res` iterator
    :return: a tuple containing the best path and its distance
    """
    res = min(chunk, key=lambda x: x[1])
    q.put(res)
    q.task_done()


def find_best_path(cities, distances, path, start_index=0):
    """
    Wrapper function for `path_distance` that filters out paths that don't start with `start_index`
    :param cities: a list of city coordinates
    :param distances: a distance matrix
    :param path: a tuple of city indices
    :param start_index: the index of the starting city
    :return: a tuple containing the path and its distance, or `None` if the path doesn't start with `start_index`
    """
    return path_distance(cities, distances, path, start_index)
