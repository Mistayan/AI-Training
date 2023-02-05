import pytactx
from src.utils import mapping


class RunnerAgent(pytactx.Agent):
    """
    The agent holding possible states and context parameters
    """

    def __init__(self, myId: str):
        """
        :param myId: the name of your bot in arena
        """
        # create state machine
        # finally the super init
        super().__init__(id=myId,
                         username="demo",
                         password="demo",
                         arena="pytactx",
                         server="mqtt.jusdeliens.com",
                         prompt=False,
                         verbose=False)
        self._target: str = None
        self._path: list[tuple[str, int, int]] = []

        self.__visited: list[str] = []
        self.__last: tuple[str, int, int] = None

    # ================================= PRIVATE METHODS ================================= #
    @property
    def __next_action(self) -> str:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self.path"""
        print(f"Next Action, based on {self._path}")
        if not hasattr(self, '_path_iter'):
            self._path_iter = iter(self._path)
        try:
            _next = next(self._path_iter)
            _next = str(_next if isinstance(_next, int) else _next[0] if isinstance(_next, tuple) else _next)
            if _next and _next not in self.__visited:
                print("Next Target : ", _next)
                return _next
        except StopIteration:
            print("restart actions")
            self._path_iter = iter(self._path)
            return self.__next_action

    # ================================= PROTECTED METHODS ================================= #
    def _handle(self):
        """ Move to target.
        If arrived at requested location, find next target to go to.
        Save current target in visited, in case path changes [fail-safe]"""
        if not self._target or self.derniereDestinationAtteinte == self._target:
            print("ARRIVED @ ", self._target)
            self.__visited.append(self._target)
            self._target = self.__next_action
            print(f"deplacerVers {self._target}")
        self.deplacerVers(self._target)

    # ================================= PUBLIC METHODS ================================= #
    def go(self):
        self._path = mapping.cities_from_game_dict(agent.jeu)

        while self.vie > 0:
            self.actualiser()
            self._handle()


# ================================= TEST FILE ================================= #


if __name__ == '__main__':
    import random

    agent = RunnerAgent(f"Dummy-Runner {random.randint(0, 42)}")
    agent.go()
