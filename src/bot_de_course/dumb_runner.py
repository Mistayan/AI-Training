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
        self.__path:list[tuple[str, int, int]] = []
        self.__last:tuple[str, int, int] = None
        self.__visited:list[str] = []
        self.__target, self.goto_x, self.goto_y = None, None, None

    @property
    def next_action(self) -> tuple[str, int, int]:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self.path"""
        print("Next Action")
        if not hasattr(self, '_path_iter'):
            self._path_iter = iter(self.__path)
        try:
            return next(self._path_iter)
        except StopIteration:
            print("restart actions")
            self._path_iter = iter(self.__path)
            return next(self._path_iter)

    def handle(self):
        # print(self.__path)
        if not self.goto_x:
            self.__last = self.__target
        if not self.goto_x or self.derniereDestinationAtteinte == self.__target:
            print("ARRIVED @ ", self.__target)
            self.__target, self.goto_x, self.goto_y = self.next_action
            self.__visited.append(self.__target)
            print(f"deplacerVers {self.__target}")

        self.deplacerVers(self.__target)

    def __set_path(self, path: list[tuple[str, int, int]]):
        self.__path = path

    def go(self):
        self.__set_path(mapping.cities_from_game_dict(agent.jeu))

        while self.vie > 0:
            self.actualiser()
            self.handle()


if __name__ == '__main__':
    agent = RunnerAgent("sten")
    agent.go()
    # pprint(agent.jeu)
    # villes = agent.jeu['dests']
    # coords_list = []
    # for city_name in villes:
    #     city = villes[city_name]
    #     x, y = city.get('x'), city.get('y')
    #     coords_list.append((city_name, x, y))
