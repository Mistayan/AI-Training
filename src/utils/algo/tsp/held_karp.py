from typing import List, Tuple

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from networkx.algorithms.approximation.traveling_salesman import spanning_tree_distribution

from src.utils.algo.ISolver import ISolver
from src.utils.metrics import measure_perf


class HeldKarp(ISolver):

    @property
    def distances(self):
        pass

    @property
    def graph(self):
        return self.__graph.copy(True)

    def __init__(self, cities: List[Tuple[str, int, int]], current_location: Tuple[int, int] = None):
        self.__cities = cities
        self.__n = len(cities)
        self.__graph = nx.Graph()
        for i, (name_i, x_i, y_i) in enumerate(cities):
            self.__graph.add_node(i, name=name_i, pos=(x_i, y_i))
            for j in range(i):
                name_j, x_j, y_j = cities[j]
                if i != j:
                    self.__graph.add_edge(i, j, distance=np.linalg.norm([x_i - x_j, y_i - y_j]))

        pos = nx.kamada_kawai_layout(self.__graph)
        tree = spanning_tree_distribution(self.__graph, pos)
        print(pos)
        plt.show()
        print("showed")

    @measure_perf
    def solve(self):
        # Compute the minimum spanning tree of the graph
        print("initial adj : ", self.__graph.adj,
              flush=True)  # {0: {1: {'distance': 25.317977802344327}, 2: {'distance': 15.264337522473747}, 3: {'distance': 26.076809620810597}, 4: {'distance': 24.08318915758459}, 5: {'distance': 28.319604517012593}, 6: {'distance': 25.079872407968907}, 7: {'distance': 6.708203932499369}, 8: {'distance': 33.83784863137726}, 9: {'distance': 7.211102550927978}}, 1: {0: {'distance': 25.317977802344327}, 2: {'distance': 19.235384061671343}, 3: {'distance': 2.23606797749979}, 4: {'distance': 33.60059523282288}, 5: {'distance': 18.027756377319946}, 6: {'distance': 24.20743687382041}, 7: {'distance': 19.026297590440446}, 8: {'distance': 24.73863375370596}, 9: {'distance': 21.095023109728988}}, 2: {0: {'distance': 15.264337522473747}, 1: {'distance': 19.235384061671343}, 3: {'distance': 21.095023109728988}, 4: {'distance': 14.866068747318506}, 5: {'distance': 13.601470508735444}, 6: {'distance': 10.198039027185569}, 7: {'distance': 10.198039027185569}, 8: {'distance': 18.601075237738275}, 9: {'distance': 8.06225774829855}}, 3: {0: {'distance': 26.076809620810597}, 1: {'distance': 2.23606797749979}, 2: {'distance': 21.095023109728988}, 4: {'distance': 35.608987629529715}, 5: {'distance': 20.248456731316587}, 6: {'distance': 26.40075756488817}, 7: {'distance': 20.024984394500787}, 8: {'distance': 26.92582403567252}, 9: {'distance': 22.360679774997898}}, 4: {0: {'distance': 24.08318915758459}, 1: {'distance': 33.60059523282288}, 2: {'distance': 14.866068747318506}, 3: {'distance': 35.608987629529715}, 5: {'distance': 21.213203435596427}, 6: {'distance': 12.041594578792296}, 7: {'distance': 22.47220505424423}, 8: {'distance': 21.37755832643195}, 9: {'distance': 18.973665961010276}}, 5: {0: {'distance': 28.319604517012593}, 1: {'distance': 18.027756377319946}, 2: {'distance': 13.601470508735444}, 3: {'distance': 20.248456731316587}, 4: {'distance': 21.213203435596427}, 6: {'distance': 9.219544457292887}, 7: {'distance': 22.20360331117452}, 8: {'distance': 7.0}, 9: {'distance': 21.213203435596427}}, 6: {0: {'distance': 25.079872407968907}, 1: {'distance': 24.20743687382041}, 2: {'distance': 10.198039027185569}, 3: {'distance': 26.40075756488817}, 4: {'distance': 12.041594578792296}, 5: {'distance': 9.219544457292887}, 7: {'distance': 20.396078054371138}, 8: {'distance': 10.295630140987}, 9: {'distance': 18.027756377319946}}, 7: {0: {'distance': 6.708203932499369}, 1: {'distance': 19.026297590440446}, 2: {'distance': 10.198039027185569}, 3: {'distance': 20.024984394500787}, 4: {'distance': 22.47220505424423}, 5: {'distance': 22.20360331117452}, 6: {'distance': 20.396078054371138}, 8: {'distance': 28.178005607210743}, 9: {'distance': 3.605551275463989}}, 8: {0: {'distance': 33.83784863137726}, 1: {'distance': 24.73863375370596}, 2: {'distance': 18.601075237738275}, 3: {'distance': 26.92582403567252}, 4: {'distance': 21.37755832643195}, 5: {'distance': 7.0}, 6: {'distance': 10.295630140987}, 7: {'distance': 28.178005607210743}, 9: {'distance': 26.627053911388696}}, 9: {0: {'distance': 7.211102550927978}, 1: {'distance': 21.095023109728988}, 2: {'distance': 8.06225774829855}, 3: {'distance': 22.360679774997898}, 4: {'distance': 18.973665961010276}, 5: {'distance': 21.213203435596427}, 6: {'distance': 18.027756377319946}, 7: {'distance': 3.605551275463989}, 8: {'distance': 26.627053911388696}}}
        mst = nx.total_spanning_tree_weight(self.__graph, weight="distance")
        # print("mst : ", [_ for _ in mst])
        # srt = sorted(sorted(e) for e in mst.edges.data(False))
        # print("srt : ", srt)
        # print("MST adj : ", self.__graph.adj,
        #       flush=True)  # {0: {1: {'distance': 25.317977802344327}, 2: {'distance': 15.264337522473747}, 3: {'distance': 26.076809620810597}, 4: {'distance': 24.08318915758459}, 5: {'distance': 28.319604517012593}, 6: {'distance': 25.079872407968907}, 7: {'distance': 6.708203932499369}, 8: {'distance': 33.83784863137726}, 9: {'distance': 7.211102550927978}}, 1: {0: {'distance': 25.317977802344327}, 2: {'distance': 19.235384061671343}, 3: {'distance': 2.23606797749979}, 4: {'distance': 33.60059523282288}, 5: {'distance': 18.027756377319946}, 6: {'distance': 24.20743687382041}, 7: {'distance': 19.026297590440446}, 8: {'distance': 24.73863375370596}, 9: {'distance': 21.095023109728988}}, 2: {0: {'distance': 15.264337522473747}, 1: {'distance': 19.235384061671343}, 3: {'distance': 21.095023109728988}, 4: {'distance': 14.866068747318506}, 5: {'distance': 13.601470508735444}, 6: {'distance': 10.198039027185569}, 7: {'distance': 10.198039027185569}, 8: {'distance': 18.601075237738275}, 9: {'distance': 8.06225774829855}}, 3: {0: {'distance': 26.076809620810597}, 1: {'distance': 2.23606797749979}, 2: {'distance': 21.095023109728988}, 4: {'distance': 35.608987629529715}, 5: {'distance': 20.248456731316587}, 6: {'distance': 26.40075756488817}, 7: {'distance': 20.024984394500787}, 8: {'distance': 26.92582403567252}, 9: {'distance': 22.360679774997898}}, 4: {0: {'distance': 24.08318915758459}, 1: {'distance': 33.60059523282288}, 2: {'distance': 14.866068747318506}, 3: {'distance': 35.608987629529715}, 5: {'distance': 21.213203435596427}, 6: {'distance': 12.041594578792296}, 7: {'distance': 22.47220505424423}, 8: {'distance': 21.37755832643195}, 9: {'distance': 18.973665961010276}}, 5: {0: {'distance': 28.319604517012593}, 1: {'distance': 18.027756377319946}, 2: {'distance': 13.601470508735444}, 3: {'distance': 20.248456731316587}, 4: {'distance': 21.213203435596427}, 6: {'distance': 9.219544457292887}, 7: {'distance': 22.20360331117452}, 8: {'distance': 7.0}, 9: {'distance': 21.213203435596427}}, 6: {0: {'distance': 25.079872407968907}, 1: {'distance': 24.20743687382041}, 2: {'distance': 10.198039027185569}, 3: {'distance': 26.40075756488817}, 4: {'distance': 12.041594578792296}, 5: {'distance': 9.219544457292887}, 7: {'distance': 20.396078054371138}, 8: {'distance': 10.295630140987}, 9: {'distance': 18.027756377319946}}, 7: {0: {'distance': 6.708203932499369}, 1: {'distance': 19.026297590440446}, 2: {'distance': 10.198039027185569}, 3: {'distance': 20.024984394500787}, 4: {'distance': 22.47220505424423}, 5: {'distance': 22.20360331117452}, 6: {'distance': 20.396078054371138}, 8: {'distance': 28.178005607210743}, 9: {'distance': 3.605551275463989}}, 8: {0: {'distance': 33.83784863137726}, 1: {'distance': 24.73863375370596}, 2: {'distance': 18.601075237738275}, 3: {'distance': 26.92582403567252}, 4: {'distance': 21.37755832643195}, 5: {'distance': 7.0}, 6: {'distance': 10.295630140987}, 7: {'distance': 28.178005607210743}, 9: {'distance': 26.627053911388696}}, 9: {0: {'distance': 7.211102550927978}, 1: {'distance': 21.095023109728988}, 2: {'distance': 8.06225774829855}, 3: {'distance': 22.360679774997898}, 4: {'distance': 18.973665961010276}, 5: {'distance': 21.213203435596427}, 6: {'distance': 18.027756377319946}, 7: {'distance': 3.605551275463989}, 8: {'distance': 26.627053911388696}}}
        # distances = list(mst.dists.values())
        # print(distances)
        # Traverse the minimum spanning tree using depth-first search to obtain a TSP path

        # tsp_path = dfs(0, set())
        tsp_path = []

        # Build up the optimal solution
        tsp_path = [self.__cities[i][0] for i in tsp_path]
        print(tsp_path)
        # Compute the total distance of the TSP path
        edges = nx.to_dict_of_dicts(self.__graph)
        total_distance = 0
        for i in range(len(tsp_path) - 1):
            total_distance += edges[i][i + 1]["distance"]

        return tsp_path, total_distance
