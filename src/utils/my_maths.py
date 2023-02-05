import math


def euclidean_distance(a, b):
    """
    computes the Euclidean distance between two classes that contains attributes (x, y)
    :param a: from NodeA
    :param b: to NodeB
    :return: euclidian distance between entities
    """
    x1, y1 = (a.x, a.y)
    x2, y2 = (b.x, b.y)
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
