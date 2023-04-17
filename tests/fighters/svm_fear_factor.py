import pickle
from typing import Tuple, List

import numpy as np
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from config import FACTORS
from src.utils.generation import random_cities, generate_entities_map, generate_data_fear_factor
from src.utils.mapping.graphs import extract_graph_features
from src.utils.os_utils import gen_file
from src.utils.plt.graphs import display_all_figs_from_graph

if __name__ == '__main__':
    nb_bots = 3500
    grid_size = 30
    factors = FACTORS(grid_size)
    # coloredlogs.install(logging.DEBUG)

    # train SVM
    svm = SVC(kernel='linear', random_state=42)
    features, labels, feat_names = generate_data_fear_factor(nb_bots, grid_size, factors)
    df = DataFrame(features, index=labels, columns=['distance', 'ammo', 'life'])
    df.to_csv(gen_file("fear_factors.csv", "csv"))
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)
    train_result = svm.fit(X_train, y_train)
    y_pred = svm.predict(X_test)
    print(f"Predictions on dataset :\n{y_pred}")

    print(f"Confusion Matrice :\n{confusion_matrix(y_test, y_pred)}")
    print(classification_report(y_test, y_pred))

    # ####### test_case ######## #
    bots_map: List[Tuple[str, int, int]] = random_cities(nb_bots, grid_size, "bot")
    me = random_cities(1, grid_size, "ME")[0]
    graph = generate_entities_map(me, bots_map, factors)
    features, labels = extract_graph_features(graph)

    pred = svm.predict(features)
    df = DataFrame(features, index=pred, columns=['distance', 'ammo', 'life'])
    print("#" * 20, "SVM", "#" * 20)
    print(f"{pred}\n")
    print(f"Accuracy: {np.mean(pred == labels)} On this case, we do not want 100%, since it would fit our poor choices")
    print(f"on DataFrame : \n{df}")
    df.to_csv(gen_file("svm-fear_factors.csv", "csv"))

    # modelize the algorithm's results as a graph to be better compare
    display_all_figs_from_graph(graph, grid_size, colors_only=True, predictions=pred)

    # modelize the SVM's results as a graph to be better visualize changes
    # replace the predictions by a fear factor from 0 to 1
    for i, p in enumerate(pred):
        if p == "EGGS-Terminate":
            pred[i] = 0.1
        elif p == "FLEE":
            pred[i] = 1
        elif p == "ENGAGE":
            pred[i] = 0.3
        elif p == "Potential":
            pred[i] = 0.5
        else:
            pred[i] = 0.7
    # replace the graph's fear factor by the predictions
    try:
        for i, node in enumerate(graph.nodes):
            graph.nodes[node]["fear_factor"] = float(pred[i])
    except IndexError:
        ...
    # show the new graph
    display_all_figs_from_graph(graph, grid_size, colors_only=True)
    # Save the model
    with open(gen_file("svm-fear_factors.pkl", "pkl"), "wb") as file:
        pickle.dump(svm, file)
