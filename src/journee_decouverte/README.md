___
[__TOC__]
___

# TODO :

pickle load des meilleurs modèles et comparaison de perf/score

# How to build

## Dependances

voir le fichier requirements.txt

## Ide

InteliJ pour coder (et vscode pour l'image en temps réel, pour contrôler le résultat en jeu)

## Installation

Installation d'un environnement virtuel (recommandé) et des dépendances

```shell
py setup.py
```

# How to run

Lancement d'OVA (le client mqtt)

```shell
venv\Scripts\python.exe main.py
```

# cahier des charges:

Le besoin est le suivant :

* Nous contrôlons un robot appelé OVA.
* OVA est équipé de plusieurs capteurs, notamment une caméra
* On doit scanner ses images afin de déterminer la couleur de la couronne
  ![hishiara-crown-view.png](imgs%2Fdocs%2Fhishiara-crown-view.png)
* ayant une liste des couleurs du centre du cercle, on pourra utiliser la classification pour ressortir la couleur
  souahitée
* On doit pouvoir entrainer le modèle sur demande, au début du programme

## Contexte

Jeu développé par Jusdeliens.
Il a créé un environnement dédié à l'apprentissage de l'algorithmie et des intelligences artificielles

# Ressources

https://jusdeliens.com
https://scikit-learn.org/stable/modules/ensemble.html
https://www.geeksforgeeks.org/python-pil-image-crop-method/
https://jusdeliens.com/epsirennes3cda2223/Jusdeliens-EPSI-IA-J1.pdf
https://scikit-learn.org/stable/common_pitfalls.html#data-leakage
https://www.geeksforgeeks.org/matplotlib-pyplot-hist-in-python/
https://scikit-learn.org/stable/auto_examples/release_highlights/plot_release_highlights_1_2_0.html#sphx-glr-auto-examples-release-highlights-plot-release-highlights-1-2-0-py

## Materiel

Ova est équipé d'une caméra et d'un raspberry pi 3B+.
Elle est aussi équipée de plusieurs capteurs et d'un buzzer.

## Logiciel

paho-mqtt
numpy
matplotlib
scikit-learn

## Timeline du projet

Sur le temps d'une après midi, nous avons pu réaliser un modèle de classification de couleur de couronne.

Pour se faire, nous avons mis en place une fonction train,
qui récupère l'image d'OVA, fait la moyenne de la couleur de l'image et nous demande sa catégorie

* [main.py](main.py) en mode entrainement pour catégoriser une 10ène de chaque couleurs.

Après avoir récupéré un certain nombre d'images, nous pouvons entrainer un modèle de classification... Mais le quel ?

Le timing était serré, j'ai donc rapidement mis en place un script qui nous permet de déterminer quel classifier serait
le plus optimal.(après avoir trié les plus intéressants : voir ressources)

* [eval_classifiers.py](eval_classifiers.py)

Une fois le meilleur classifier trouvé, nous avons pu entrainer le modèle, et le sauvegarder dans un fichier pickle.

Le pickle étant sauvegardé, nous avons donc développé la fonction d'essai

* [main.py](main.py) en mode prédiction pour essayer de classifier les images en temps réel, et s'assurer du résultat.

Après vérifications, il y aura eu de nombreuses modifications dans le système d'heuristique.
Modifications apportées : nouvel entrainement !
on pourra trouver qu'un autre classifier peut être plus performant (en score ET en performance !!) selon les différents
inputs

## Explication des métriques input

Afin de classifier les images, nous avons décidé (étant donné l'environnement fixe de l'exercice et du temps imparti)
de prendre un échantillon de pixels dans la partie basse-gauche de l'image d'environ 10% de la taille de l'image.

Ce choix permet de limiter les risques de mauvaise détection, si le robot venait à bouger.

On fera donc une moyenne des couleurs sur cette zone.

Cette moyenne de couleur est notre input, il servira à classifier l'image.

## Classes à prédire output

Dans cet exercice, un total de 6 couleurs sont présentes dans le centre du cercle
![image_couleurs.jpeg](imgs%2Fdocs%2Fimage_couleurs.jpeg)

* **1** : rouge (255, 0, 0)
* **2** : jaune (255, 255, 0)
* **3** : vert (0, 255, 0)
* **4** : cyan (0, 255, 255)
* **5** : bleu (0, 0, 255)
* **6** : violet (255, 0, 255)
* **7** : noir (0, 0, 0) (uniquement pour signifier la fin de la partie)

Nous devons donc classifier les images en 7 catégories.

# Organisation

## Prévisionnel des tâches

* [x] savoir lire une image d'OVA
* [x] Récolter des images à catégoriser
* [x] Préparer une classe contenant les informations utiles.
    * [x] surcharger les méthodes utiles (_onImageReceived)
    * [x] définir un mode entrainement
    * [x] définir un mode prédiction

*[x] Préparer un modèle de classification
    * [x] Définir les métriques d'entrainement
    * [x] Définir les classes à prédire
    * [x] Définir les classifiers à tester
        * [x] SVM
        * [x] Random Forest
        * [x] Decision Tree
    * Tester et comparer les classifiers

* [x] Pickle.dump après l'entrainenement
* [x] Pickle.load avant la prédiction

## Temps

## Test validation

## Train

Au lancement du programme, il nous demande si l'on souhaite entrainer le modèle ou non.
Si oui, il nous demande de catégoriser les images récoltées (pour cela, une image est affichée à l'aide de matplotlib.

## Predict

![doc_run_program.png](imgs%2Fdocs%2Fdoc_run_program.png)

Si l'on décide de ne pas entrainer le modèle, alors il lance une boucle infinie, qui va lire les images de la caméra, et
les classifier.
On remportera un point par image correctement classifiée.

# Caractérisation

Afin de correctement classifier les images, nous avons décidé de nous baser sur la couleur de la couronne.
Pour cela, nous avons utilisé la méthode de la moyenne des couleurs de l'image. Cela permet d'augmenter la précision
lors de changements majeurs sur l'image.
En réduisant la taille de l'image, nous pouvons également augmenter la vitesse de traitement
En utilisant OpenCV, on pourrait aussi chercher le cercle, son cercle interrieur, et ainsi déterminer la couleur de la
couronne

Ces différentes étapes permettent en définitive de déterminer la couleur de la couronne.

## Graphiques matplotlib pour déterminer le meilleur classifier

![RandomForestClassifier(n_estimators=20)_confusion.png](imgs%2Fdocs%2FRandomForestClassifier%28n_estimators%3D20%29_confusion.png)
![RandomForestClassifier(n_estimators=20)_scores.png](imgs%2Fdocs%2FRandomForestClassifier%28n_estimators%3D20%29_scores.png)
![SVC(kernel='linear')_confusion.png](imgs%2Fdocs%2FSVC%28kernel%3D%27linear%27%29_confusion.png)
![SVC(kernel='linear')_scores.png](imgs%2Fdocs%2FSVC%28kernel%3D%27linear%27%29_scores.png)

# Crédits

JusDeliens ![Jusdeliens](https://jusdeliens.com/wp-content/uploads/2022/06/cropped-cropped-cropped-jusdeliens-logo-full-transparent.png)

## License

Les produits de jusdeliens sont sous license CC BY-NC-ND 3.0
![CC BY-NC-ND 3.0](https://i.creativecommons.org/l/by-nc-nd/3.0/88x31.png)

Le code produit est sous license Open Source (MIT)

## Auteurs

* **Jusdeliens** - *ova.py* - https://jusdeliens.com/ova
* **Mistayan** - *everyving in the folder, except ova.py* - https://github.com/Mistayan