import time
import tracemalloc

from matplotlib import pyplot as plt

from src.utils.algo.tsp.bruteforce import TSP
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.generation import random_cities

if __name__ == '__main__':
    # Solver = TSP | TSPMap  # Bruteforce, up to 10 cities [7-10 secondes]
    # Solver = Hamilton  # Dijkstra to avoid obstacles + Hamilton solution resolution
    # thought through resolution, closest is next : ultra fast solver, at the cost of extra distance
    Solvers = [HamiltonianSolver, TSP]
    # make a matplotlib grid
    fig, axs = plt.subplots(2, 2)
    # make a scatter containing performance of each solver
    axs[0, 0].set_title("Time taken comparison")
    axs[0, 0].set_xlabel("Number of cities")
    axs[0, 0].set_ylabel("Time taken (ns)")
    axs[0, 1].set_xlabel("Number of cities")
    axs[0, 1].set_ylabel("Total distance")
    axs[0, 1].set_title("Distance comparison")
    axs[1, 0].set_xlabel("time taken (ns)")
    axs[1, 0].set_ylabel("Total distance")
    axs[1, 0].set_title("Distance comparison")
    axs[1, 1].set_xlabel("Number of cities")
    axs[1, 1].set_ylabel("Memory used (bytes)")
    axs[1, 1].set_title("Memory used comparison")
    ax = axs[0, 0]
    ax2 = axs[0, 1]
    ax3 = axs[1, 0]
    ax4 = axs[1, 1]
    ax.grid()
    ax2.grid()
    ax3.grid()

    for nb_cities in range(2, 10):
        cities = random_cities(nb_cities, 30)
        for Solver in Solvers:
            print(Solver)
            t0 = time.perf_counter_ns()
            path, dist = Solver(cities=cities).solve()
            perf = time.perf_counter_ns() - t0
            current, peak = tracemalloc.get_traced_memory()
            # display_path_on_map(cities, 30, set(path), name=Solver)
            print(f"""Solver : {Solver.__name__}
            Evaluated path : {path}
            Total distance : {dist}
            Time Taken : {perf} ns
            Memory used : {peak:.0f} MB
            """)
            color = "red" if Solver == HamiltonianSolver else "blue"
            ax.scatter(nb_cities, perf, color=color)
            ax2.scatter(nb_cities, dist, color=color)
            ax3.scatter(perf, dist, color=color)
            ax4.scatter(nb_cities, peak, color=color)

    ax.legend(["HamiltonianSolver", "TSP"])
    plt.tight_layout()
    plt.show()
