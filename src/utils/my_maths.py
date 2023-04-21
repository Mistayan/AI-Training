import math
from typing import Tuple, Type

import numpy as np


def euclidean_distance(a, b):
    """
    computes the Euclidean distance between two classes that contains attributes (x, y)
    :param a: from NodeA
    :param b: to NodeB
    :return: euclidian distance between entities
    """
    x1, y1 = a
    x2, y2 = b
    print(a, b)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def calculate_pair_distance(city1: Tuple[str, int, int], city2: Tuple[str, int, int], distance_type: Type = float):
    """
    calcul la distance entre deux entités et la retourne
    :param city1: from
    :param city2: to
    :param distance_type: int | float | [NUMERIC VALUE]
    :return: (from, to), distance
    """
    return (city1[0], city2[0]), distance_type(np.linalg.norm(np.array(city1[1:]) - np.array(city2[1:])))
