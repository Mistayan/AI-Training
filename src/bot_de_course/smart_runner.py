from typing_extensions import override

from src.bot_de_course.dumb_runner import RunnerAgent
from src.utils.algo.ISolver import ISolver
from src.utils.mapping.arrays import cities_from_game_dict
from src.utils.plt.from_arrays import display_path_on_map


class SmartRunner(RunnerAgent):
    def __init__(self, myId: str):
        super().__init__(myId)
        self.__cities = cities_from_game_dict(self.jeu)
        self._dist = float('inf')

    @override
    def go(self, Solver: ISolver):
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
