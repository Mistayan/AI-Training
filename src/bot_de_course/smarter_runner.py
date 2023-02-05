from src.bot_de_course.dumb_runner import RunnerAgent
from src.utils import mapping
from src.utils.algo.tsp import TSP


class SmartRunner(RunnerAgent):
    def __init__(self, myId: str):
        super().__init__(myId)
        self._dist = float('inf')

    def go(self):
        """
        Override dumb_runner's go() method, to replace simple mapping with advanced path processing.
        """
        cities = mapping.cities_from_game_dict(self.jeu)
        self._target = cities[0][0]
        self.deplacerVers(self._target)
        self._path, self._dist = TSP(cities=cities, starting_city=cities[0]).solve()
        print(f"Done processing paths\nFastest found: {self._path} with a total distance of {self._dist}")
        while self.vie:
            self.actualiser()
            self._handle()


if __name__ == '__main__':
    import random

    smart = SmartRunner(f"Smart-Runner {random.randint(0, 42)}")
    smart.go()
