import logging
import random
import coloredlogs

from src.bot_de_course.smart_runner import SmartRunner
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver

if __name__ == '__main__':
    name = "Grapher"
    coloredlogs.install(logging.DEBUG, propagate=False)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(HamiltonianSolver)
