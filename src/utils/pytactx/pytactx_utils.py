import logging
from time import sleep
from typing import Tuple, Dict, List

import math

from pytactx import env
from pytactx.agent import Agent
from pytactx.pyanalytx.logger import warning
from src.utils.pytactx.orientation import Orientation


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


def get_logging_level():
    logging_level = 0
    match env.VERBOSITY:
        case 1: logging_level = logging.ERROR
        case 2: logging_level = logging.WARNING
        case 3: logging_level = logging.INFO
        case 4: logging_level = logging.DEBUG
    if logging_level == 0:
        raise ValueError("Env value VERBOSITY must be between 1 and 4")
    return logging_level

def get_city_tuple(__next_action: str, __cities: List[Tuple]) -> tuple[str, int, int]:
    """ Get the city Tuple having for name __next_action """
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
