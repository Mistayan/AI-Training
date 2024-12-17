import logging

from src.bot_de_course.smart_runner import SmartRunner
from src.utils.algo.tsp.bruteforce import TSP

if __name__ == '__main__':
    import random
    import coloredlogs

    name = "BaseTSP"
    coloredlogs.install(logging.DEBUG, propagate=False)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.init_path(TSP)
    smart.go()
