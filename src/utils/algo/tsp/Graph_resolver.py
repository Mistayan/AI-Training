import logging
from typing import List, Tuple

import networkx as nx

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.graphs import entities_to_graph


class MyGraph(ISolver):

    def __init__(self, cities: List[Tuple[str, int, int]], actual_position: Tuple[int, int]):
        self._log = logging.getLogger(__class__.__name__)
        self.__cities = cities
        self.__start = actual_position
        self.__G = entities_to_graph(cities)

    @property
    def distances(self):
        return self.__G.edges.data("dist")

    def solve(self) -> Tuple[List[str], float]:
        self._log.info(self.__G.nodes.items())
        self._log.info("################ DEPENDS ON CLOSEST CITY ################")

        paths = nx.shortest_paths.shortest_path_length(self.__G, source=self.__cities[0][0], weight="weight")
        self._log.info(paths, "\n", "#" * 30)
        for path in paths:
            self._log.info(path)
            if not path == self.__start:
                continue
            self._log.info(path)

        return list(paths), sum(paths.values())
