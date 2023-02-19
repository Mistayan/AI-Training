from typing import List, Tuple, Set

import networkx as nx

from src.utils import mapping
from src.utils.algo.ISolver import ISolver
from src.utils.mapping import graphs
from src.utils.metrics import measure_perf


class HamiltonianSolver(ISolver):
    @property
    def distances(self):
        return self.__distances

    def __init__(self, cities: List[Tuple[str, int, int]]):
        self.__graph = mapping.graphs.entities_to_graph(cities)
        # Add edges with their weights
        ng = nx.all_pairs_dijkstra_path_length(self.__graph, weight="distance")
        self.__distances = dict(ng)

    @property
    def graph(self):
        return self.__graph.copy(True)

    @measure_perf
    def solve(self, start_index: int = 0, end: int = 0, back_to_start=False, max_iter: int = -1, visited: Set = None) -> \
            Tuple[Tuple[str], float]:
        """
        finds a path that is fast.
        reduce number of possible iterations by popping items outs as they are is the path, allowing faster processing
        :param visited: set of city names already visited
        :param start_index: from which city index to start
        :param end: ending index wanted
        :param back_to_start: do you require to go back to first city visited after path is done ?
        :param max_iter: maximum number of iterations before returning a value
        :return: Tuple(best_path_found, path_distance)
        """

        # Solve TSP using the shortest Hamiltonian path algorithm from networkx
        nodes = list(self.__graph.nodes())
        visited = visited or {nodes[start_index]}
        path = [nodes[start_index]]
        unvisited = set(nodes)
        unvisited.remove(nodes[start_index])
        while unvisited:
            current = path[-1]
            nearest = None
            min_dist = float('inf')
            for neighbor in self.__graph[current]:
                if neighbor not in visited:
                    dist = self.__graph[current][neighbor]['distance']
                    if dist < min_dist:
                        nearest = neighbor
                        min_dist = dist
            if nearest is None:
                nearest = nodes[start_index]
                dist = self.__graph[current][nearest]['distance']
            else:
                dist = min_dist
            path.append(str(nearest))
            visited.add(nearest)
            unvisited.remove(nearest)

        dist = graphs.path_distance(self.__graph, path, start_index, end)
        if back_to_start:
            dist += self.__graph[path[-1]][path[0]]['distance']
        return tuple(path), dist
