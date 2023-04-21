import os
import re
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.svm import SVC

import src.utils.metrics
from config import base_dir
from src.utils import generation
from src.utils.algo.tsp.bruteforce import TSP
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.plt.graphs import display_graph_map


def sub_gen(num_cities, grid_size=30):
    # generate cities
    cc: List[Tuple[str, int, int]] = generation.random_cities(num_cities, grid_size)
    # Generate target data for shortest paths between each city
    tsp = TSP(cc)
    path, distance = tsp.solve()
    coords = [_[1:] for _ in cc]
    tsp.save((coords, path))
    print(coords, path)


def generate_data(N: int = 10):
    print("Generating Data...")
    sub_gen(N)
    # with Pool(cpu_count() - 1) as pool:
    #     pool.map(sub_gen, [30]*N)


def read_my_shitty_csv(file: str) -> pd.DataFrame:
    coords_list = []
    paths_list = []
    with open(file, 'r') as fp:
        # [(14, 19), (1, 12), (29, 19), (16, 18), (16, 18), (30, 25), (4, 24), (8, 0), (23, 30), (30, 0)];
        # [0, 3, 4, 2, 5, 8, 6, 1, 7, 9]
        for i, line in enumerate(fp.readlines()):
            if i == 0:
                continue
            string_coords, string_path = line.split(";")
            paths_list.append([int(_) for _ in re.findall(r"\d+", string_path)])
            coords = (_ for _ in re.findall(r"(?:\((\d+, \d+))", string_coords))
            coords_list.append([(int(_[0]), int(_[1])) for _ in [coord.split(',') for coord in coords]])

        return pd.DataFrame({"coords": coords_list, "path": paths_list})


def train(clf=None):
    generate_data()
    file = os.path.join(base_dir, "csv/paths.csv")

    df = read_my_shitty_csv(file)
    # IMPLEMENT CLASSIFIER TRAINING HERE
    if clf is None:
        # clf = Pipeline([
        #     ('scaler', StandardScaler()),
        #     ('svm', SVC(kernel='linear', C=0.03, max_iter=40))
        # ])
        clf = SVC(kernel='linear', C=0.03, max_iter=40)
        print(df)
    paths = df.get("path").values
    coords = df.get("coords").values

    for i, x in enumerate(coords):
        print(f"Training on sample {i + 1} / {len(coords)}")
        print(x)
        print(paths[i])
        try:
            clf.fit(x, paths[i])
        except:
            print("Error")
            continue
    return clf


def calc_pred(prediction_graph):
    print(prediction_graph)
    n = len(prediction_graph)
    ret = [0] * n
    for i in range(n):
        for j in range(n):
            p = prediction_graph[i][j]
            if p:
                ret[i] = p
                break
    return ret


if __name__ == '__main__':
    # Set values for generation
    import coloredlogs
    import logging

    coloredlogs.install(logging.DEBUG)
    grid_size = 100
    num_cities = 300
    # num_obstacles = 2

    clf = train()
    target = np.zeros((num_cities, num_cities))
    cc = generation.random_cities(num_cities, grid_size)
    tsp = HamiltonianSolver(cc)

    it = num_cities ** num_cities
    path, dist = tsp.solve()
    display_graph_map(tsp.graph, path, grid_size, with_edges=False)
    coords = [_[1:] for _ in cc]
    # tsp.save((coords, path))
    print(path, dist, coords)
    # prediction = clf.predict(coords)
    # print(prediction, "VS", path)
    # print(f"Accuracy: {np.mean(prediction == path)}")
    # print(calc_pred(prediction))
    src.utils.metrics.show_perfs()
