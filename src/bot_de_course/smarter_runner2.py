import logging

from src.bot_de_course.smarter_runner import SmartRunner
from src.utils.algo.tsp.tsp_links import TSPMap


if __name__ == '__main__':
    import random
    import coloredlogs
    name = "Mapper"
    coloredlogs.install(logging.DEBUG)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(TSPMap)
