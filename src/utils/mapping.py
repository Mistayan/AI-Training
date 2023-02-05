import itertools
import random
from typing import Dict, List, Tuple

import numpy as np

from src.utils.generation import random_cities


def map_distances(_cities: list[tuple[str, int, int]], visited=None):
    if not visited:
        visited = []
    for city in visited:
        for check in _cities:
            if check[0] == city:
                _cities.pop(_cities.index(check))

    __size = len(_cities)
    # Set an empty 2D numpy array, from cities length
    _distances = np.empty(shape=(__size, __size))
    # Fill the array with distances from given point
    for i in range(__size):
        for j in range(i + 1, __size):
            n1, *starting_city = _cities[i]
            n2, *ending_city = _cities[j]
            _distances[j][i] = _distances[i][j] = np. \
                linalg.norm(np.array(starting_city) - np.array(ending_city))
    return _distances


def shortest_path(possible_cities) -> Tuple[List[Tuple[str, int, int]], float]:
    """
        
    :param possible_cities: a n*n grid containing the board distances between entities
    :return: the shortest path possible, with it's distance 
    """
    print(f"Evaluating shortest paths possible  on {possible_cities}")
    best_path = None
    best_dist = float("inf")
    __size = len(possible_cities)
    print(f"Grid of size {__size}**2")
    for path in itertools.permutations(range(__size)):
        dist = 0
        for i in range(__size - 1):
            dist += possible_cities[path[i]][path[i + 1]]
        dist += possible_cities[path[-1]][path[0]]
        if (best_dist - 0.33) > dist > 0:
            best_path = path
            best_dist = dist
    return list(best_path), best_dist


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


if __name__ == '__main__':
    cities = random_cities(4, 30)
    print(cities)
    cities_names = [city[0] for city in cities]
    iter_paths = explore(cities[random.randint(0, len(cities) - 1)][0], cities_names, [])
    print(iter_paths)
    # SVM
