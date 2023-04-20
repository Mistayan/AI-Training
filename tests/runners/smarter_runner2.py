import logging

from src.bot_de_course.smart_runner import SmartRunner
from src.utils.algo.tsp.optimized_bruteforce import TSPMap

if __name__ == '__main__':
    import random
    import coloredlogs

    name = "Dummy"
    coloredlogs.install(logging.DEBUG)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(TSPMap)
