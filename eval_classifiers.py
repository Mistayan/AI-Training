import pickle
import re
from functools import partial
from time import sleep

import numpy as np
import pandas as pd
import seaborn
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score, \
    PredictionErrorDisplay
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from rendu_julien_arne_data_visu.utils.metrics import measure_perf, show_perfs
from rendu_julien_arne_data_visu.utils.os_utils import gen_file

fig_dir = "plots"
pickle_dir = "pickles"


def svm_general_overview(y_test, y_pred, clf, name=None, display=True):
    if not name:
        name = "_".join(re.findall("\w", clf.__class__.__name__))
    cm = confusion_matrix(y_test, y_pred)
    print(f"Confusion matrix : {cm}")
    fig1 = seaborn.heatmap(cm, annot=True)
    fig1.set_title(f"Confusion matrix for {clf}")
    plt.savefig(gen_file(str(name).strip() + "_confusion", fig_dir, ".png"))
    plt.show()

    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy : {accuracy}")
    precision = precision_score(y_test, y_pred, average='weighted')
    print(f"Precision : {precision}")
    recall = recall_score(y_test, y_pred, average='weighted')
    print(f"Recall : {recall}")
    f1 = f1_score(y_test, y_pred, average='weighted')
    print(f"F1 : {f1}")
    seaborn.barplot(x=["Accuracy", "Precision", "Recall", "F1"], y=[accuracy, precision, recall, f1])
    plt.title(f"Scores for {clf}")
    plt.savefig(gen_file(str(name) + "_scores", fig_dir, ".png"))
    plt.show()
    display_prediction_on_training_set(x_train, y_train, clf, fig_dir)

    return accuracy * precision * recall * f1


def pickle_it(clf, dir, name=None):
    if not name:
        name = "_".join(re.findall("\w+", clf.__class__.__name__))
    with open(gen_file(str(name) + ".pkl", str(dir)), "wb") as file:
        pickle.dump(clf, file)


@measure_perf
def predict_with(_clf, _x_test):
    # test
    _y_pred = np.array(_clf.predict(_x_test), int)
    print(f"Predictions on dataset : {_y_pred}")
    return _y_pred


def display_prediction_on_training_set(x_train, y_train, clf, fig_dir):
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))
    _ = PredictionErrorDisplay.from_estimator(
        clf, x_train, y_train, kind="actual_vs_predicted", ax=axs[0]
    )
    _ = PredictionErrorDisplay.from_estimator(
        clf, x_train, y_train, kind="residual_vs_predicted", ax=axs[1]
    )
    fig.savefig(gen_file(re.sub(r"[\n \"'<>]", "", clf.__class__.__name__) + "_prediction", fig_dir, ".png"))
    plt.show()


if __name__ == "__main__":
    # make a list of viable classifiers to scan images in order to find the main color
    # set as partial to avoid memory sharing between classifiers and memory over-use
    classifiers = [
        partial(SVC, **{'kernel': 'linear'}),
        partial(SVC, **{'kernel': 'sigmoid'}),
        partial(SVC, **{'kernel': 'rbf'}),
        # partial(SVR, **{'kernel': 'linear'}),
        partial(DecisionTreeClassifier, **{}),
        partial(RandomForestClassifier, **{'n_estimators': 20}),
        partial(MLPClassifier,
                **{'hidden_layer_sizes': (3, 10, 7), 'max_iter': 500, 'alpha': 0.0001, 'solver': 'sgd',
                   'verbose': 10, 'random_state': 21, 'learning_rate_init': 0.01}),
        # partial(Lasso, **{'alpha': 1, 'max_iter': 1000})
    ]
    df = pd.read_csv("training.csv")
    df_fig = df.hist(bins=5, figsize=(12, 8), color='#86bf91', zorder=2, rwidth=0.9, grid=False, layout=(3, 3),
                     sharex=False, sharey=False, xlabelsize=8, ylabelsize=8, edgecolor='black', linewidth=1.2)
    df_fig = df_fig.flatten()
    for ax in df_fig:
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
    plt.legend()
    plt.title("Histogram of each numeric input variable")
    plt.show()
    x_train = df.drop("category", axis=1)
    y_train = df["category"]
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, test_size=0.2)
    for i in range(2):
        for classifier in classifiers:
            # create a classifier
            if i:
                clf = make_pipeline(StandardScaler(), classifier(), verbose=True)
            else:
                clf = classifier()
            print(f"Testing {classifier}...")

            # train
            clf.fit(x_train, y_train)

            y_pred = predict_with(clf, x_test)

            # generate multiple graphs to see if model is worth saving
            mega_score = svm_general_overview(y_test, y_pred, clf)

            # save model if score is good enough, or if user wants to
            if mega_score != 1:
                save = input("Save this classifier ? (y/n)")
            else:
                save = "y"
            if save == "y":
                pickle_it(clf, dir=pickle_dir)

            # force delete references to classifier
            del clf
            del classifier
            # let garbage collector do its job (avoid memory sharing between classifiers)
            sleep(1)

    show_perfs()
