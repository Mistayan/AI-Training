import itertools
import logging
from typing import Dict, Iterable, Any
from typing import List, Tuple

import numpy as np

from src.utils.metrics import measure_perf
from src.utils.my_maths import calculate_pair_distance
from src.utils.plt.from_arrays import display_path_on_map


def distances(cities: List[Tuple[str, int, int]]) -> np.ndarray:
    n = len(cities)
    _distances = np.empty(shape=(n, n))
    for i in range(n):
        for j in range(i + 1, n):
            _distances[i, j] = _distances[j, i] = np.linalg.norm(np.array(cities[i][1:]) - np.array(cities[j][1:]))
    return _distances


def shortest_path(_grid: np.ndarray, start: int) -> Tuple[List[Tuple[str, int, int]], float]:
    """
    :param _grid: an n*n grid containing the board distances between entities
    :param start: where to start the run from
    :return: the shortest path possible, with distance
    """
    # self._log.info(f"Evaluating shortest paths possible...")
    best_path = None
    best_dist = float("inf")
    __size = len(_grid)
    # self._log.info(f"Grid of size {__size}*{__size}")
    for path in itertools.permutations(range(__size)):
        if path[0] != start: continue
        dist = 0
        for i in range(__size - 1):
            dist += _grid[path[i]][path[i + 1]]
        dist += _grid[path[-1]][path[0]]
        if best_dist > dist > 0:
            best_path = path
            best_dist = dist
    return list(best_path), int(best_dist)


def explore(city: str, remaining_cities: List[str], path: List = None) -> Tuple[Tuple[str]]:
    """
    evaluate all possible paths in 'remaining cities', starting from 'city'.

    :param city: city from which we desire to start
    :param remaining_cities: list of unexplored cities
    :param path: the current target path... ?
    :return: a 2D array containing all the possible paths, starting from 'city'
    """
    first = remaining_cities.pop(remaining_cities.index(city))
    iter_path = itertools.permutations(remaining_cities)
    return tuple((first, *tuple(possibility)) for possibility in iter_path)


def cities_from_game_dict(game_dict: Dict) -> List[Tuple[str, int, int]]:
    """ transforms dict to List of Tuple """
    """
    Exemple (v...)
    {'players': ['Grapher-42', 'Grapher-18', 'Grapher-29', 'Grapher-36'], 'robots': [], 'version': 0, 'arenaName': 'ovarena', 'tags': [], 'parent': 'x-arenas', 'restartOnExcept': True, 'factoryDir': 'tactx_arena', 'desc': 'Traveling salesman, be the first to deliver all planets in the galaxy 📦', 'gridColumns': 21, 'gridRows': 21, 'resPath': '/assets/', 'preview': 'space1.jpg', 'bgImg': 'space1.jpg', 'logo': 'j2l.png', 'bgColor': [255, 255, 255, 0], 'gridColor': [255, 255, 255, 0.4], 'viewer': 'tactx', 'enter': '', 'api': '/editor?load=pytactx&project=playground', 'help': 'https://tutos.jusdeliens.com/index.php/2020/01/14/pytactx-prise-en-main/', 'ideal': 'https://dev.jusdeliens.com', 'nPlayers': 4, 'nRobots': 0, 'maxPlayers': 16, 'onlyAuthorised': False, 'whiteList': [], 'blackList': [], 'maxRobots': 8, 'saveSrc': True, 'startedAt': '2024/12/14 10:42:11', 'resetAt': '2024/12/14 11:44:14', 'stoppedAt': '', 't': 211613, 'countdown': 300000, 'dtRestart': 10, 'dtPop': 3600000, 'dtIdle': 5000, 'info': '🧑➕ Adding agent Grapher-36', 'infoLog': True, 'pause': False, 'connected': True, 'open': True, 'public': True, 'hitImg': '', 'borderHit': 10, 'brownianMap': False, 'canLeaveMap': True, 'map': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], 'mapRand': True, 'mapRandFreq': 0, 'mapImgs': ['', ''], 'mapFriction': [0.35, 1], 'mapHit': [0, 1], 'mapBreakable': [False, False], 'checkpoints': {'START': {'x': 19, 'y': 17, 'i': 0, 'l': {'1': 1, '2': 1, '3': 1, '4': 1}}, '1': {'x': 20, 'y': 5, 'i': 1, 'l': {'START': 1, '2': 1, '3': 1, '4': 1}}, '2': {'x': 1, 'y': 11, 'i': 2, 'l': {'START': 1, '1': 1, '3': 1, '4': 1}}, '3': {'x': 6, 'y': 18, 'i': 3, 'l': {'START': 1, '1': 1, '2': 1, '4': 1}}, '4': {'x': 15, 'y': 0, 'i': 4, 'l': {'START': 1, '1': 1, '2': 1, '3': 1}}}, 'cpGraphml': '', 'gravity': [0, 0], 'cpRandN': 5, 'cpRandMode': 0, 'cpRandFreq': 1, 'score': 'TSP', 'spawnMode': 1, 'spawnAreas': [0], 'weapons': ['none', 'beam', 'wave', 'spray', 'launcher', 'force'], 'bullet': [-1, -1, -1, -1, 4, -1], 'wIcons': ['', '🎇', '💣', '🔥', '🚀', '🤜'], 'fireImgs': ['', '', '', '', '', ''], 'dtFire': [300, 300, 300, 300, 1000, 500], 'hitFire': [0, 10, 10, 10, 0, 0], 'ownerFire': [False, False, True, False, False, False], 'rangeFire': [0, 5, 10, 10, 1, 2], 'spreadFire': [0, 0, 360, 70, 0, 180], 'accelerationFire': [0, 0, 0, 0, 0, 100], 'profiles': ['default', 'arbitre', 'bot1', 'bot2', 'rocket'], 'pIcons': ['', '👮\u200d', '👾', '👾', ''], 'pImgs': ['spaceship.png', 'spaceship.png', 'spaceship.png', 'spaceship.png', 'rocket.svg'], 'pPnj': ['', '', '', '', ''], 'blind': [False, False, False, False, True], 'range': [6, 0, 6, 6, 0], 'spreadRange': [50, 360, 50, 50, 360], 'weaponIni': [1, 1, 1, 1, 1], 'fxFire': [True, True, True, True, False], 'hitCollision': [0, 0, 10, 10, 0], 'hitSelfCollision': [0, 0, 0, 0, 10], 'shieldFire': [0, 1, 0, 0, 0], 'shieldCollision': [0, 1, 0, 0, 0], 'dtDir': [10, 10, 10, 10, 10], 'dDirMax': [10, 10, 10, 10, 10], 'dtMove': [50, 10, 50, 50, 10], 'moveToDir': [True, True, True, True, False], 'mass': [1000, 10, 1000, 1000, 1], 'accelerationOnly': [True, True, True, True, True], 'accelerationMax': [100, 100, 100, 100, 100], 'dxMax': [1, 100, 1, 1, 1], 'dyMax': [1, 100, 1, 1, 1], 'speedIni': [[0, 0], [0, 0], [0, 0], [0, 0], [100, 100]], 'speedMax': [100, 100, 100, 100, 100], 'lifeIni': [100, 0, 100, 100, 1], 'lifeTime': [0, 0, 0, 0, 3000], 'invisible': [False, True, False, False, False], 'invincible': [False, True, False, False, False], 'infiniteAmmo': [False, True, False, False, False], 'collision': [True, False, True, True, True], 'canRulePlayer': [False, True, False, False, False], 'canRuleArena': [False, True, False, False, False], 'dtRespawn': [5000, 5000, 5000, 5000, 0], 'nRespawn': [0, 0, 0, 0, 1], 'popOnDeath': [False, False, False, False, True], 'forceField': [0, 0, 0, 0, 0], 'forceFieldRange': [0, 0, 0, 0, 0], 'areas': ['SPAWN ZONE', 'KILL REWARD ZONE'], 'aIcons': ['', ''], 'areasColor': [[0, 0, 0, 0], [0, 0, 0, 0]], 'areasX': [19, 0], 'areasY': [17, 0], 'areasW': [1, 0], 'areasH': [1, 0], 'areasPUps': [{}, {'life': [20, 0, '+'], 'ammo': [10, 0, '+']}], 'areasPUpsDt': [0, 0], 'areasPUpsEv': [[], ['nKill']], 'teamName': ['black', 'blue', 'pink', 'red', 'green', 'gold', 'copper', 'silver'], 'teamColor': [[0, 0, 0], [43, 250, 250], [255, 192, 203], [255, 0, 64], [0, 255, 128], [255, 215, 0], [184, 115, 51], [190, 194, 203]], 'teamAreas': [[0], [0], [0], [0], [0], [0], [0], [0]], 'ammoIni': [100, 100, 1, 100, 2, 1000], 'pWeapons': [[1], [1], [1], [1], [2]], 'dtWeapon': [1, 1, 1, 1, 2], 'energyIni': [100000, 1000000, 1000000, 1000000, 1000000], 'linkPortNb': [0, 0, 0, 0, 0], 'linkStiffness': [0, 0, 0, 0, 0], 'linkColor': 'rgba(0,0,0,0.4)', 'missions': [['Connect agent to arena', '🚪', '', 'https://tutos.jusdeliens.com/index.php/2020/01/14/pytactx-prise-en-main/#connexion', '', 'ConnectWith1Agent', 1, 600, [-1]]], 'areasR': [0, 0], 'canDie': [True, True, True, True, True], 'collisionMap': [True, False, True, True, True], 'linkDataDt': [300, 300, 300, 300, 300], 'linkDataLen': [1024, 1024, 1024, 1024, 1024]}
    """
    _cities = []
    logging.log(logging.DEBUG, f"parsing game dict : {game_dict}")
    _from = game_dict.get('checkpoints')
    logging.log(logging.DEBUG, f"parsing checkpoints : {_from}")
    for n, city_name in enumerate(_from):
        city = _from[city_name]
        logging.log(logging.DEBUG, f"parsing checkpoint {n} : {_from}")
        logging.log(logging.DEBUG, f"")
        _cities.append((city_name, city.get('x'), city.get('y')))
    return _cities


def path_distance(cities, distances: Dict, current_path: List[int], start_index: int):
    dist = 0
    for i in range(len(cities) - 1):
        pair_coords = (cities[current_path[i]][0], cities[current_path[i + 1]][0])
        try:
            dist += distances[pair_coords]
        except KeyError:  # the tuple tested is inverted
            dist += distances[pair_coords[::-1]]
    return current_path, dist


def rec_find_bests(iterable: Iterable, max_iter: int, best_dist: int, best_path: List):
    if max_iter == 0:
        return []
    try:
        p, d = next(iterable)
    except StopIteration:
        return [(best_path, best_dist)]
    if d < best_dist:
        best_dist = d
        best_path = p
    return rec_find_bests(iterable, max_iter - 1, best_dist, best_path) + [(p, d)]


@measure_perf
def get_city_pairs_distances(cities: List[Tuple[str, int, int]]):
    """
    return distances between each entity as a dict like:

    {   (0, 1): 12, (1, 2): 31, ...     }
    :param cities: cities
    :return:
    """
    size = len(cities)
    city_pairs = iter((cities[i], cities[j])
                      for i in range(size)
                      for j in range(i + 1, size))
    results: [Tuple[str, str], float | int | Any] = itertools.starmap(calculate_pair_distance, city_pairs)
    return dict(results)


if __name__ == '__main__':
    from src.utils.generation import random_cities

    cities = random_cities(20, 30)
    display_path_on_map(cities, 30, [])
    # self._log.info(iter_paths)
    # SVM
