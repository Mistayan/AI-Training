from src.utils.algo.tsp.Graph_resolver import MyGraph
from src.utils.algo.tsp.bruteforce import TSP
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.generation import random_cities
from src.utils.mapping.arrays import display_path_on_map

if __name__ == '__main__':
    # Solver = TSP | TSPMap  # Bruteforce, up to 10 cities [7 secondes]
    # Solver = Hamilton  # Dijkstra to avoid obstacles + Hamilton solution resolution
    # thought through resolution, closest is next : ultra fast solver, at the cost of extra distance
    Solvers = [MyGraph, HamiltonianSolver, TSP]  # , TSPMap
    cities = random_cities(100, 30)

    for Solver in Solvers:
        print(Solver)
        path, dist = Solver(cities=cities).solve()
        display_path_on_map(cities, 30, path, name=Solver)
        print(f"""Solver : {Solver}
        Evaluated path : {path}
        Total distance : {dist}
        """)
