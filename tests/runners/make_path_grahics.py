from src.utils.algo.tsp.Graph_resolver import MyGraph
from src.utils.algo.tsp.bruteforce import TSP
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.generation import random_cities
from src.utils.plt.from_arrays import display_path_on_map

if __name__ == '__main__':
    # Solver = TSP | TSPMap  # Bruteforce, up to 10 cities [7 secondes]
    # Solver = Hamilton  # Dijkstra to avoid obstacles + Hamilton solution resolution
    # thought through resolution, closest is next : ultra fast solver, at the cost of extra distance
    Solvers = [HamiltonianSolver, TSP, MyGraph]  # , TSPMap
    cities = random_cities(10, 30)
    me = random_cities(1, 30, "ME")[0]

    for Solver in Solvers:
        # print(Solver)
        sol = Solver(cities=cities, current_location=me[1:])
        path, dist = sol.solve()
        fig = display_path_on_map(cities, 30, set(path), name=Solver)
        print(f"""Solver : {Solver.__name__}
        Evaluated path : {path}
        Total distance : {dist}
        """)
