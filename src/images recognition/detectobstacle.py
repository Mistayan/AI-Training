# Import les libs nécessaires (sklearn ...)

import math

import pandas as pd
from pandas import array
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC

from originals.ova import OvaClientMqtt

# Créer la variable camera pour récupérer les images
# 'PrenomNOM' A REMPLACER PAR VOTRE IDENTIFIANT (ex: JulienARNE)
# CamXXXX A REMPLACER PAR L'ID DERRIERE LA CARTE DE LA CAMERA (ex: CamZF56)
# USERNAME et PASSWORD A REMPLACER
# 'OvaYF23', 'CamRD63', 'CamCJ11', 'OvaSU75', 'CamRG67'
camera = OvaClientMqtt(id="ovaXXXXXXXXXXXX", arena="ishihara", username="", password="", server="192.168.10.103",
                       port=1883)
L = camera.lirePixelSaturation
force_training = False
csv_file = f"csv/imgs.csv"


def grad(L, x, y):
    """
    Calcul le gradient de l'information (luminosité, RGB, contrast, ...) autour du point x,y.
     L est la fonction qui renvoie une information sur un point (x, y) d'une image
     """
    return math.sqrt((L(x + 1, y) - L(x - 1, y)) ** 2 +
                     (L(x, y + 1) - L(x, y - 1)) ** 2)


def characterize(L):
    """
    Récupère l'image de la caméra, avec ses dimensions.
    Calcule et renvoi dans un array les variables explicatifs pour l'image donnée.
    'L' est la fonction qui renvoie UNE donnée d'un point x, y sur cette image
    """
    largeur, hauteur = camera.largeur, camera.hauteur
    _grad = 0
    for x in range(1, largeur - 1):
        # Evite les premières et dernières colones, dû à l'algo utilisé
        for y in range(1, hauteur - 1):
            _grad += grad(L, x, y)
    total_size = (largeur - 2) * (hauteur - 2)
    grad_mean = _grad / total_size
    print(f"gradiant mean : {grad_mean}")

    _vari = 0
    for x in range(1, largeur - 1):
        for y in range(1, hauteur - 1):
            _vari = (grad(L, x, y) - grad_mean) ** 2
    vari_mean = _vari / total_size
    print(f"variance carrée du gradiant : {_vari / total_size}")

    return grad_mean, vari_mean


##########################################
# 1. ENTRAINEMENT
data = x = y = init = None
try:
    with open(csv_file, 'r') as fp:
        data = pd.read_csv(fp)
        x = data.iloc[:, :-1].values
        y = data.iloc[:, -1].values
        print(x, y)
        fp.close()
except:
    # Pas de fichier de sauvegarde initialize

    with open(csv_file, 'r+') as fp:
        if fp.read(1) != "g":
            init = True
            fp.close()
    if init:
        with open(csv_file, 'w+') as fp:
            print("grad_mean,var_mean,category", file=fp)
            fp.close()
print(data)
print()
if force_training or (data is not None and data.empty):
    print("TRAINING !!")
    category = input("Camera's Images category ?\n0: No_Obstacle\n1: Obstacle")
    camera.actualiser()
    with open(csv_file, 'a+') as fp:
        while True:
            camera.actualiser()
            if camera.estConnecte == True:
                grad_mean, var_mean = characterize(L)
                print(f"{grad_mean},{var_mean},{category}",
                      file=fp,
                      flush=True)

# Fabrication des données d'entrainement (liste de variables explicatives et classes correspondantes déjà connues)
print(x, y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

# Création du modèle
classifier = SVC(kernel='linear')
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)
print(f"Predictions on dataset : {y_pred}")

# Génération de la matrice de confusion pour vérifier la bonne précision de notre modèle
print(f"Confusion Matrice :\n{confusion_matrix(y_test, y_pred)}")
print(classification_report(y_test, y_pred))
# plot_confusion_matrix("estimator", y_pred, y_test)

# On génère une couleur par obstacle
possible_colors = {
    "human": (255, 255, 255),
    "bottle": (0, 255, 255),
}

while True:
    # Récupère l'image de la caméra
    camera.actualiser()
    if not camera.estConnecte:
        continue
    y_pred = classifier.predict(array(characterize(L)).reshape(1, -1))
    print(y_pred)
    # Si la luminosité est forte
    # if ( camera.lirePixelLuminosite(x,y) > 50 ):
    #     # On colorie le pixel avec notre couleur aléatoire
    #     camera.ecrirePixel(x,y, rouge,vert,bleu)
    # else:
    #     # Sinon on change la couleur en noir
    #     camera.ecrirePixel(x,y, 0,0,0)
