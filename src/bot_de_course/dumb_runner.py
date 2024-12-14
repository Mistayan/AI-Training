import logging
from typing import Generator, List, Tuple

from pytactx import agent, env
from pytactx.pyrobotx.robot import RobotEvent
from src.utils.mapping.arrays import cities_from_game_dict
from src.utils.metrics import measure_perf


class RunnerAgent(agent.AgentFr):
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
        self._log.debug("INIT Agent")
        super().__init__(myId,
                         env.ARENA,
                         env.USERNAME,
                         env.PASSWORD,
                         env.BROKERADDRESS,
                         env.BROKERPORT,
                         env.VERBOSITY)
        self._log.debug("Agent connected")
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
        if not self._target or self.dernierCheck == self._target:
            self._log.info(f"ARRIVED @{self._target}")
            self.__visited.append(self._target)
            self._target = self.__next_action
            self._log.info(f"deplacerVers {self._target}")
        self.deplacerVers(self._target[0])

    def _set_path(self, path: List[Tuple[str, int, int]] | Generator | List[str]):
        self.__path = path

    # ================================= PUBLIC METHODS ================================= #

    @measure_perf
    def go(self):
        self.robot.addEventListener(RobotEvent.updated, self._handle)
        while self.vie > 0:
            self.actualiser()
        self._log.warning("I won...")


# ================================= TEST FILE ================================= #


if __name__ == '__main__':
    import random
    import coloredlogs

    coloredlogs.install(logging.DEBUG, propagate=False)
    agent = RunnerAgent(f"Dummy-{random.randint(0, 42)}")
    _path = [_[0] for _ in cities_from_game_dict(agent.jeu)]
    agent._set_path(_path)
    agent.go()
