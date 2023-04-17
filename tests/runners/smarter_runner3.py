import logging

from src.bot_de_course.smart_runner import SmartRunner
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver

if __name__ == '__main__':
    import random
    import coloredlogs

    name = u"\u26A0Mist"
    coloredlogs.install(logging.DEBUG, propagate=False)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(HamiltonianSolver)
