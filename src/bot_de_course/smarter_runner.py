import datetime
import logging

from typing_extensions import override

from src.bot_de_course.dumb_runner import RunnerAgent
from src.utils.mapping.arrays import cities_from_game_dict, display_path_on_map
from src.utils.metrics import measure_perf


class SmartRunner(RunnerAgent):
    def __init__(self, myId: str):
        super().__init__(myId)
        self.__cities = cities_from_game_dict(self.jeu)
        self._dist = float('inf')

    @override
    @measure_perf
    def go(self, Solver):
        """
        Override dumb_runner's go() method, to replace simple mapping with advanced path processing.
        """
        self._target = self.__cities[0][0]
        self.deplacerVers(self._target)
        _path, self._dist = Solver(cities=self.__cities).solve(start_index=0, back_to_start=False)
        self._set_path(_path)
        display_path_on_map(self.__cities, 30, _path)

        self._log.info(f"Done processing paths\nFastest found: {_path} with a total distance of {self._dist}")
        super().go()

    def deplacerVers(self, index):
        if isinstance(index, int):
            index = self.__cities[index]
        super().deplacerVers(str(index))


if __name__ == '__main__':
    import random
    import coloredlogs
    from src.utils.algo.tsp.tsp import TSP

    name = "BaseTSP"
    coloredlogs.install(logging.DEBUG, propagate=False)
    start_time = datetime.datetime.now().time()
    smart = SmartRunner(f"{name}-{random.randint(0, 42)}")
    smart.go(TSP)
