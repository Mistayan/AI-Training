import logging
import math
import random
from functools import partial
from typing import List, Tuple, Any, Dict

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from src.utils.algo.evaluate_others import eval_fear_factor
from src.utils.mapping.arrays import get_city_pairs_distances
from src.utils.mapping.graphs import entities_to_graph, graph_heat_map, display_graph_map, extract_graph, \
    display_scatter_comparatif
from src.utils.my_maths import euclidean_distance

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


def generate_entities_map(me, bots_map: List, factors:Dict, display=False):
    rng = partial(random.randint, 1, 100)
    pairs = get_city_pairs_distances(bots_map)
    graph = entities_to_graph(bots_map, pairs)
    _len = len(graph.nodes)
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
            v['bot'] = n.lower().startswith("bot")

            weight = round(eval_fear_factor(factors, v), 2)
            v['fear_factor'] = weight
            graph.add_edge(me[0], n, distance=dist, weigth=weight)
    if display:
        fig = graph_heat_map(graph, graph_size=grid_size, weight='fear_factor')
        display_graph_map(graph, [], grid_size, _fig=fig)
        display_scatter_comparatif(graph)
    return graph


def generate_data_fear_factor(nb_bots, grid_size, factors):
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors, display=False)
    features, labels = extract_graph(graph)
    logging.log(logging.DEBUG, features, labels)
    # split data into training and test sets
    # print(features, labels)
    return train_test_split(features, labels, test_size=0.2, random_state=42)


if __name__ == '__main__':
    from pandas import DataFrame
    import coloredlogs

    # coloredlogs.install(logging.DEBUG)
    factors = {
        'DIST_PENALTY': 0.53,
        'LIFE_PENALTY': 1.1,
        'AMMO_PENALTY': 0.33,
        'MAP_MAX_DISTANCE': math.sqrt(grid_size ** 2)
    }
    # train SVM on training set
    svm = SVC(kernel='linear')
    for i in range(100):
        X_train, X_test, y_train, y_test = generate_data_fear_factor(nb_bots, grid_size, factors)
        svm.fit(X_train, y_train)
        #     # evaluate performance on test set
        #     accuracy = svm.score(X_test, y_test)
        #     print(f"Accuracy on test set: {accuracy:.2f}")
        #     y_pred = svm.predict(X_test)
        #     print(f"Predictions on dataset :\n{y_pred}")
        #
        #     print(f"Confusion Matrice :\n{confusion_matrix(y_test, y_pred)}")
        #     print(classification_report(y_test, y_pred))
        # except:
        #     pass
    # ####### test_case ######## #
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors, display=True)
    features, labels = extract_graph(graph)

    pred = svm.predict(features)
    print(f"{pred}\n")
    print(f"Accuracy: {np.mean(pred == labels)}")
    print(f"on DataFrame : \n{DataFrame(features, index=labels, columns=['dist', 'ammo', 'life'])}")
