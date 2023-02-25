import logging
from datetime import datetime
from typing import Generator, List, Tuple

import pytactx
from src.utils.mapping.arrays import cities_from_game_dict
from src.utils.metrics import measure_perf


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
        self._log = logging.getLogger(myId)
        super().__init__(id=myId,
                         username="demo",
                         password="demo",
                         arena="pytactx",
                         server="mqtt.jusdeliens.com",
                         prompt=False,
                         verbose=False)
        self._target: str = None
        self.__path: list[tuple[str, int, int]] = []

        self.__visited: list[str] = []

    # ================================= PRIVATE METHODS ================================= #
    @property
    def __next_action(self) -> str:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self.path"""
        self._log.info(f"Next Action, based on {self.__path}")
        if not hasattr(self, '_path_iter'):
            self._path_iter = iter(self.__path)
        try:
            _next = next(self._path_iter)
            if _next and _next not in self.__visited:
                self._log.info(f"Next Target : {_next}")
                return _next[0] if isinstance(next, Tuple) else _next
            return self.__next_action
        except StopIteration:
            self._log.info("restart actions")
            self._path_iter = iter(self.__path)
            return self.__next_action


    # ================================= PROTECTED METHODS ================================= #
    def _handle(self, *args):
        """ Move to target.
        If arrived at requested location, find next target to go to.
        Save current target in visited, in case path changes [fail-safe]"""
        if not self._target or self.derniereDestinationAtteinte == self._target:
            self._log.info(f"ARRIVED @{self._target}")
            self.__visited.append(self._target)
            self._target = self.__next_action
            self._log.info(f"deplacerVers {self._target}")
        self.deplacerVers(self._target)

    def _set_path(self, path: List[Tuple[str, int, int]] | Generator | List[str]):
        self.__path = path

    # ================================= PUBLIC METHODS ================================= #

    def go(self):
        self.executerQuandActualiser(self._handle)
        while self.vie > 0:
            self.actualiser()
        self._log.warning("I won...")


# ================================= TEST FILE ================================= #


if __name__ == '__main__':
    import random

    agent = RunnerAgent(f"Dummy-{random.randint(0, 42)}")
    _path = cities_from_game_dict(agent.jeu)
    agent._set_path(_path)
    agent.go()
