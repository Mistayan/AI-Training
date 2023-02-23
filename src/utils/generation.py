import logging
import random
from functools import partial
from typing import List, Tuple, Any, Dict

from src.utils.algo.evaluate_others import eval_fear_factor
from src.utils.mapping.arrays import get_city_pairs_distances
from src.utils.mapping.graphs import entities_to_graph, extract_graph_features
from src.utils.my_maths import euclidean_distance
from src.utils.plt.graphs import display_all_figs_from_graph

grid_size = 30
nb_bots = 50


def random_cities(nb_cities: int, map_size: int, initials: str = "city ") -> List[Tuple[str, int, int]]:
    """
    Generate a random number of cities on random coordinates in a grid of given size
    :param nb_cities: number of cities to generate on the grid
    :param map_size: the size of the grid in which to generate cities
    :param initials: (optional) if you want to generate something other than a 'city '
    :return: List of Tuple of the generated cities (name, x, y)
    """
    cities: List[Tuple[str, int, int]] = []
    for i in range(nb_cities):
        x = random.randint(0, map_size)
        y = random.randint(0, map_size)
        while (Any, x, y) in cities:
            x = random.randint(0, map_size)
            y = random.randint(0, map_size)
        cities.append((initials + str(i + 1), x, y))
    return cities


def generate_entities_map(me, bots_map: List, factors: Dict):
    rng = partial(random.randint, 1, 100)
    pairs = get_city_pairs_distances(bots_map)
    graph = entities_to_graph(bots_map, pairs, with_edges=False)
    _len = len(graph.nodes)
    logging.log(logging.DEBUG, graph)
    pos = me[1:]
    graph.add_node(me[0], pos=pos)
    for i, (n, v) in enumerate(graph.nodes.data()):
        n: str
        v['ammo'] = rng()
        v['life'] = rng()
        if i < _len:
            # print(n, v, pos, v['pos'])
            dist = int(euclidean_distance(pos, v['pos']))
            v['distance'] = dist
            v['type'] = "bot" if n.lower().startswith("bot") else "#"

            weight = round(eval_fear_factor(factors, v), 2)
            v['fear_factor'] = weight
            graph.add_edge(me[0], n, distance=dist, weigth=weight)
    return graph


def generate_data_fear_factor(nb_bots, grid_size, factors, display=False):
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors)
    display and display_all_figs_from_graph(graph, grid_size)
    features, labels = extract_graph_features(graph)
    # split data into training and test sets
    logging.log(logging.DEBUG, "%s, %s", features, labels)
    return features, labels, ["distance", "ammo", "life"]
