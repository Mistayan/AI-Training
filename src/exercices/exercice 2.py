import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

print("Charger le dataset des digits")
digits = load_digits()
X, y = digits.data, digits.target

print("Visualiser images & target")
_, axes = plt.subplots(nrows=1, ncols=4, figsize=(8, 8))
for ax, img, label in zip(axes, digits.images, digits.target):
    ax.set_axis_off()
    ax.imshow(img, cmap=plt.cm.gray_r, interpolation="nearest")
    ax.set_title(f"Image : {label}")

plt.show()

print("Diviser data en jeu d'entrainement et de tests")
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

print("Créer le Model KNN")
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(x_train, y_train)

print("Afficher le taux de précision")
score = knn.score(x_test, y_test)
print(f"Score : {score}")

print("Teste les différentes valeurs pour l'hyperparamètre k de 1 à 20")
neighbors = np.arange(1, 21)
print(neighbors)
train_accuracy = np.empty(len(neighbors))
test_accuracy = np.empty(len(neighbors))

for i, k in enumerate(neighbors):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train, y_train)
    train_accuracy[i] = knn.score(x_train, y_train)
    test_accuracy[i] = knn.score(x_test, y_test)
print(f"Accuracy:\n{test_accuracy}")
