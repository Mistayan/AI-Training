import os
from abc import ABC, abstractmethod
from typing import Tuple, List

from config import base_dir
from src.utils.metrics import measure_perf


class ISolver(ABC):
    # @measure_perf
    @abstractmethod
    def __init__(self, cities: List[Tuple[str, int, int]]):
        pass

    @measure_perf
    @abstractmethod
    def solve(self):
        """
        to fill distances, use either of these methods
        implement
        >>># distances: Dict[Tuple[str, str, int]] = get_city_pairs_distances(self.__cities)
        >>># distances: List[Tuple[str, int, int]]= mapping.distances(self.__cities)
        >>># distances: nx.Graph = mapping.map_cities(self.__cities)
        """
        pass

    @property
    @abstractmethod
    def distances(self):
        pass

    @staticmethod
    def save(data: Tuple[List[Tuple[int, int]], List[int]]):
        with open(os.path.join('\\'.join([base_dir, "csv", "paths.csv"])), 'a+') as fp:
            print(data[0], file=fp, end=";")
            print(data[1], file=fp, flush=True)
