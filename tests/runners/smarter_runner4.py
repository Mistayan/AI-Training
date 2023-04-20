import logging

from src.bot_de_course.smart_runner import SmartRunner
from src.utils.algo.tsp.Graph_resolver import MyGraph

if __name__ == '__main__':
    import random
    import coloredlogs

    name = "Grapher"
    coloredlogs.install(logging.DEBUG, propagate=False)
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(MyGraph)
