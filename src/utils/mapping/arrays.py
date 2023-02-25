import itertools
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
    _cities = []
    _from = game_dict.get('dests')
    for city_name in _from:
        city = _from[city_name]
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
