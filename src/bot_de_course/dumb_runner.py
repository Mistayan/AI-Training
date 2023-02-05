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
        self.__path: list[tuple[str, int, int]] = []
        self.__last: tuple[str, int, int] = None
        self.__visited: list[str] = []
        self.__target, self.goto_x, self.goto_y = None, None, None

    @property
    def __next_action(self) -> tuple[str, int, int]:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self.path"""
        print("Next Action")
        if not hasattr(self, '_path_iter'):
            self._path_iter = iter(self.__path)
        try:
            _next = next(self._path_iter)
            if _next and _next[0] not in self.__visited:
                return _next
        except StopIteration:
            print("restart actions")
            self._path_iter = iter(self.__path)
            return self.__next_action

    def __handle(self):
        # print(self.__path)
        if not self.goto_x:
            self.__last = self.__target
        if not self.goto_x or self.derniereDestinationAtteinte == self.__target:
            print("ARRIVED @ ", self.__target)
            self.__target, self.goto_x, self.goto_y = self.__next_action
            self.__visited.append(self.__target)
            print(f"deplacerVers {self.__target}")
        self.deplacerVers(self.__target)

    def go(self):
        self.__path = mapping.cities_from_game_dict(agent.jeu)

        while self.vie > 0:
            self.actualiser()
            self.__handle()


if __name__ == '__main__':
    agent = RunnerAgent("Dummy-Runner0")
    agent.go()
