import copy
import logging
from abc import ABC, abstractmethod
from time import sleep, time
from typing import Tuple, Dict

import math

from pytactx import env
from pytactx.agent import Agent
from pytactx.pyanalytx.logger import warning
from src.utils.orientation import Orientation
from src.utils.state_machine import StateMachine, BaseStateEnum


class WrongArenaRunnerException(Exception):
    """
    Use this to differentiate errors in assigning the wrong Runner
    [ exemple : the class requires a RunnerAgent(TargetAgent->StateMachineAgent->Agent)
        But, the class received a KillerAgent(TargetAgent)
    ]
    Most likely, having the wrong class passed to a StateMachine/States, thing might not work the same way !
    """

    def __init__(self, *args):
        logging.log(logging.ERROR, f"Wrong ArenaRunner  : {args}")
        super().__init__(*args)


def get_city_tuple(__next_action, __cities) -> tuple[str, int, int]:
    for city, x, y in __cities:
        if city == __next_action:
            return city, x, y
    raise KeyError


def wait_connection(robot: Agent, retries: int = 45):
    """
    Await agent to have values from game dict.
    This means that we are connected to the Arena, and the Arena effectively sends us data about the game.
    """
    while not robot.game and retries:
        sleep(.8)
        warning(f"No game values, retry...")
        robot.update()
        retries -= 1


def cities_from_game_dict(game_dict: Dict, first_is_last=False, return_to_first=False) -> list[tuple[str, int, int]]:
    """ transforms dict to List of Tuple """
    """
    Exemple (v...)
    {'players': ['Grapher-42', 'Grapher-18', 'Grapher-29', 'Grapher-36'],
    'arenaName': 'ovarena',
    'checkpoints': {
    'START': {'x': 19, 'y': 17, 'i': 0},
    '1': {'x': 20, 'y': 5, 'i': 1},
    '2': {'x': 1, 'y': 11, 'i': 2},
    '3': {'x': 6, 'y': 18, 'i': 3},
    '4': {'x': 15, 'y': 0, 'i': 4}
    },
    ...    """
    _cities = []
    logging.log(logging.DEBUG, f"parsing game dict : {game_dict}")
    _from = game_dict.get('checkpoints')
    logging.log(logging.DEBUG, f"parsing checkpoints : {_from}")
    last = None
    for n, city_name in enumerate(_from):
        if first_is_last and n == 0:
            last = city_name
            continue
        city = _from[city_name]
        logging.log(logging.DEBUG, f"parsing checkpoint {n} : {city}")
        _cities.append((city_name, int(city.get('x')), int(city.get('y'))))

    if first_is_last and last:
        _cities.append((last, int(_from[last].get('x')), int(_from[last].get('y'))))
    if return_to_first:
        _cities.append(_cities[0])
    return _cities


class StateAgent(Agent, ABC):
    """
    An Agent having a StateMachine to control the behaviors.

    This way, it is easier to maintain each state and their transitions.

    It will also be more maintainable, since you will want to improve your bot's capabilities.
    """

    def __init__(self, id: str):
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.info("Connecting ...")
        super().__init__(id or env.ROBOTID,
                         env.ARENA,
                         env.USERNAME,
                         env.PASSWORD,
                         env.BROKERADDRESS,
                         env.BROKERPORT,
                         env.VERBOSITY)
        self.__log.info("OK")
        self.__state_machine: StateMachine = None

    def set_state_machine(self, state_machine: StateMachine):
        self.__log.debug("Setting state Machine")
        if state_machine:
            if not isinstance(state_machine, StateMachine):
                raise ValueError("state_machine must be a StateMachine")
            self.__state_machine = state_machine
            state_machine.set_context(self)

    def unstuck(self, state: BaseStateEnum):
        self.__log.debug("Setting state Machine")
        self.__state_machine.set_actual_state(state.value)
        self._handle_loop()

    def _handle_loop(self):
        self.__state_machine.handle()


class TargetAgent(StateAgent, ABC):
    def __init__(self, id: str = None, *args, **kwargs):
        self.__current_target: Tuple[str, int, int] = None
        self.__visited = {}
        super().__init__(id)

    @property
    def current_target(self) -> Tuple[str, int, int]:
        return copy.deepcopy(self.__current_target)

    def set_target(self, target: Tuple[str, int, int]):
        if target and target != self.__current_target:
            print(f"Setting target {target}")
            self.__current_target = target

    def add_visited(self, name: str):
        self.__visited.setdefault(name, time() - self.game.get("t", 0))

    @property
    @abstractmethod
    def next_action(self):
        ...


def get_orientation_form_coord_deltas(x, y, wanted_x, wanted_y) -> Orientation:
    """
    Calculate the precise orientation based on the coordinate deltas.

    The method determines the orientation by calculating the angle between
    the current position and the target position, then mapping it to the
    appropriate cardinal or ordinal direction.

    Args:
        x (float): Current x coordinate
        y (float): Current y coordinate
        wanted_x (float): Target x coordinate
        wanted_y (float): Target y coordinate

    Returns:
        Orientation: The calculated orientation
    """
    # Calculate the delta between current and wanted coordinates
    dx = wanted_x - x
    dy = wanted_y - y

    # Calculate the angle
    angle = math.degrees(math.atan2(dy, dx))

    # Normalize angle to 0-360 range. Add 90 degrees clockwise, since x,y=0 is on top left corner, not bottom left
    angle = (angle + 360 + 90) % 360
    return Orientation.from_angle(angle)

