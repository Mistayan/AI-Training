from __future__ import annotations

import logging
from time import sleep
from typing import Tuple
from pytactx import env
from src.utils.pytactx.generic_agents import TargetAgent
from src.utils.pytactx.pytactx_utils import wait_connection, WrongArenaRunnerException, cities_from_game_dict, \
    get_city_tuple
from src.utils.algo.ISolver import ISolver


class RunnerAgent(TargetAgent):
    """
    The agent holding possible states and context parameters
    """

    def __init__(self, myId: str = None):
        """
        :param myId: the name of your bot in arena (if not set in .env, or to override it)
        :param solver: the solver you made to complete TSP
        """
        # create state machine
        # finally the super init
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.addHandler(logging.NullHandler())
        self.__log.debug("INIT Runner Agent")
        # As long as __run is True, the bot do actions
        self.__run = False
        # If this value is None, the bot will follow the default path : from start to end.
        self._solver: ISolver = None
        self._path = []
        self._visited = []
        self.__show_log = env.VERBOSITY >= 3
        super().__init__(myId)
        self.__init_arena()
        if not self._cities:
            raise WrongArenaRunnerException("The current Arena doesn't have cities in game dict", env.ARENA)
        self.__start_from = self.game.get(self._cities[0][0])

    # ================================= PRIVATE METHODS ================================= #

    def __init_arena(self):
        """
        Initialise cities from game dict
        Then init path to default (ordered cities)
        Set the target to the first item of the list.
        """
        wait_connection(self)
        # Cities : the dictionary for cities with their coordinates
        self._cities: list[tuple[str, int, int]] = cities_from_game_dict(self.game, False, True)
        # Path : contains the cities names to go to (ordered path to travel)
        self._path: list[str] = [n for n, x, y in self._cities]
        # Set initial target to first element in the path.
        if self.current_target is None:
            self.set_target(get_city_tuple(self._path[0], self._cities))
        self.__run = True
        self.__show_log = True

    # ================================= PROTECTED METHODS ================================= #

    def __loop(self):
        while self.life > 0 and self.__run and self.isConnectedToArena():
            self.update(False)
            sleep(0.1)

    # ================================= PUBLIC METHODS ================================= #

    # @measure_perf
    def init_path(self):
        if not self._path:
            self._path = [_[0] for _ in self._cities]
            self.__log.info(f"Done loading paths\nRunning in order: {self._path}")

        if not self.current_target:
            self.set_target(get_city_tuple(self._path[0], self._cities))

        self.__log.debug(f"moving towards {self.current_target}")

    def go(self):
        """
        Game loop for the runner.
        Do not edit !
        """
        if not self._path:
            self.init_path()
        self.__run = True
        super().go()

    @property
    def next_action(self) -> tuple[str, int, int]:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self._path"""

        if not hasattr(self, '_path_iter'):
            self.__log.debug(f"Initiating paths to follow {self._path}")
            self.__start_from = self._path[0]
            self._path_iter = iter(self._path)

        try:
            self.__log.debug(f"Next Action, based on {self._path}")
            _next = next(self._path_iter)
            next_tuple = _next if isinstance(next, Tuple) else get_city_tuple(_next, self._cities)
            if self.current_target[0] != next_tuple[0]:
                self.__log.info(f"Next Target : {next_tuple}")
                self.set_target(next_tuple)

        except StopIteration:
            self.__run = False
            return self.__start_from
