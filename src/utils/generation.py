import logging
import random
from functools import partial
from typing import List, Tuple, Any, Dict

from src.utils.algo.evaluate_others import eval_fear_factor
from src.utils.mapping.arrays import distances_between_entities
from src.utils.mapping.graphs import entities_to_graph, extract_graph_features
from src.utils.metrics import measure_perf
from src.utils.my_maths import euclidean_distance
from src.utils.plt.graphs import generate_all_figs_from_graph

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
    rng = partial(random.randint, 0, map_size)
    for i in range(nb_cities):
        x, y = rng(), rng()
        while (Any, x, y) in cities:  # if coordinates are already taken, regen
            x, y = rng(), rng()
        cities.append((initials + str(i + 1), x, y))
    return cities


@measure_perf
def generate_entities_map(me, bots_map: List, factors: Dict, with_edges=False):
    rng = partial(random.randint, 1, 100)
    pairs = distances_between_entities(bots_map) if with_edges else None
    graph = entities_to_graph(bots_map, pairs, with_edges=with_edges)
    _len = len(graph.nodes)
    logging.log(logging.DEBUG, graph)
    pos = me[1:]
    me_name = me[0]
    graph.add_node(me_name, pos=pos)
    for i, (n, v) in enumerate(graph.nodes.data()):
        n: str
        v: dict
        v['ammo'] = v.get('ammo') or rng()
        v['life'] = v.get('life') or rng()
        if i < _len:
            # print(n, v, pos, v['pos'])
            dist = int(euclidean_distance(pos, v['pos']))
            v['distance'] = dist
            v['type'] = "bot" if n.lower().startswith("bot") else "#"

            ff = round(eval_fear_factor(factors, v), 2)
            v['fear_factor'] = ff
            graph.add_edge(me_name, n, distance=dist, fear_factor=ff)
    return graph


@measure_perf
def generate_data_fear_factor(nb_bots, grid_size, factors, display=False):
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors, with_edges=False)
    display and generate_all_figs_from_graph(graph, grid_size, colors_only=True)

    features, labels = extract_graph_features(graph, compare_to_me=True)

    # split data into training and test sets
    logging.log(logging.DEBUG, "%s, %s", features, labels)
    return features, labels, ["distance", "ammo", "life"]
