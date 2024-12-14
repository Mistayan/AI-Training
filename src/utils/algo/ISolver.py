import logging
import os
from abc import ABC, abstractmethod
from typing import Tuple, List

from config import base_dir


class ISolver(ABC):
    # @measure_perf
    @abstractmethod
    def __init__(self, cities: List[Tuple[str, int, int]]):
        self._log = logging.getLogger(__class__.__name__)
        pass

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

    def save(self, data: Tuple[List[Tuple[int, int]], List[int]]):
        with open(os.path.join('\\'.join([base_dir, "csv", f"{self.__class__.__name__}-paths.csv"])), 'a+') as fp:
            print(data[0], file=fp, end=";")
            print(data[1], file=fp, flush=True)

    def __str__(self):
        return self.__class__.__name__
