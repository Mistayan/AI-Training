from typing import List, Tuple

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler

from config import FACTORS
from src.utils.generation import generate_data_fear_factor, random_cities, generate_entities_map
from src.utils.mapping.graphs import extract_graph_features
from src.utils.plt.graphs import display_all_figs_from_graph

# Define the dataset of labeled examples
# The three input features are "distance", "ammo", and "life"
# The target variable is "engage", which is 1 if we should engage the enemy and 0 if we should flee
if __name__ == '__main__':
    grid_size = 30
    nb_bots = 3000
    factors = FACTORS(grid_size)
    features, labels, _ = generate_data_fear_factor(nb_bots, grid_size, factors)

    # Split the dataset into inputs and targets
    X_train, X_test, y_train, y_test = train_test_split(features, labels)

    # Scale the input features to have zero mean and unit variance
    scaler = StandardScaler()
    X = scaler.fit_transform(X_train)

    # Train a neural network on the dataset
    model = MLPClassifier(hidden_layer_sizes=(10, 10, 4), max_iter=1000)
    model.fit(X, y_train)

    # ####### test_case ######## #
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors)
    features, labels = extract_graph_features(graph)

    new_inputs = scaler.transform(features)
    pred = model.predict(new_inputs)
    print(f"{pred}\n")
    print(f"Accuracy: {np.mean(pred == labels)}")
    print(f"on DataFrame : \n{DataFrame(features, index=labels, columns=['dist', 'ammo', 'life'])}")
    display_all_figs_from_graph(graph, grid_size, colors_only=True, predictions=pred)
