import random
from typing import List, Tuple

from src.utils.metrics import measure_perf


@measure_perf
def random_cities(n, map_size) -> List[Tuple[str, int, int]]:
    """
    Generate a random number of cities on random coordinates in a grid of given size
    :param n: number of cities to generate on the grid
    :param map_size: the size of the grid in which to generate cities
    :return: List of Tuple of the generated cities (name, x, y)
    """
    cities = []
    for i in range(n):
        cities.append((str(i), random.randint(0, map_size), random.randint(0, map_size)))
    return cities
