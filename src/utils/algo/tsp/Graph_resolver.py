import logging
from typing import List, Tuple

import networkx as nx

from src.utils.algo.ISolver import ISolver
from src.utils.mapping.graphs import entities_to_graph
from src.utils.metrics import measure_perf


class MyGraph(ISolver):

    def __init__(self, cities: List[Tuple[str, int, int]], actual_position: Tuple[int, int] = None):
        self._log = logging.getLogger(__class__.__name__)
        self.__cities = cities
        self.__start = actual_position or cities[0][0]
        self.__G = entities_to_graph(cities, with_edges=True)
        print(dict(self.__G.nodes.items()))
        print(dict(self.__G.edges.items()))

    @property
    def distances(self):
        return self.__G.edges.data("distance")

    @measure_perf
    def solve(self) -> Tuple[List[str], float]:
        self._log.info(self.__G.nodes.items())
        self._log.info("################ DEPENDS ON CLOSEST CITY ################")

        paths = nx.shortest_paths.all_pairs_dijkstra_path_length(self.__G, weight="distance")
        self._log.info(paths, "\n", "#" * 30)
        print(paths)
        final = None
        for path in paths:
            if path[0] == self.__start:
                print(path)
                final = path[1]
                break
            self._log.info(path)
        print(final)
        return list(final), sum(final.values())
