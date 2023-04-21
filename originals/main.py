from ova import *

# Créer la variable robot pour récupérer les images
# "ovaXXXXXXXXXXXX" A REMPLACER PAR UNE STR CONTENANT L'IDENTIFIANT DE VOTRE OVA
robot: IRobot = OvaClientMqtt(id="ovaXXXXXXXXXXXX", arena="ishihara", username="", password="", server="192.168.10.103",
                              port=1883)

while True:
    # Appelle la fonction robot.update() pour récupèrer l'image de la caméra
    robot.update()

    # Efface la console. Utiliser 'cls' sur windows, 'clear' sous unix
    os.system('cls')

    # Si le robot est déconnecté
    if (robot.isConnected() == False):
        print("🔴", robot.getRobotId(), "déconnectée")

    # Si le robot est connecté
    else:
        # Affiche l'état et les capteurs du robot
        print("🟢", robot.getRobotId(), "connectée")
        print(
            f"🔋batterie {robot.getBatteryLevel()}% 💡avant {robot.getFrontLuminosityLevel()}% 💡arrière {robot.getBackLuminosityLevel()}%")

        # Affiche la taille de l'image reçue
        imageLargeur = robot.getImageWidth()
        imageHauteur = robot.getImageHeight()
        print("🖼️  Image reçue: " + str(imageLargeur) + "x" + str(imageHauteur) + "")

        # Pour chaque pixel de l'image ,de haut en bas par pas de 8
        for y in range(0, imageHauteur, 10):
            # Pour chaque pixel de l'image ,de gauche à droite par pas de 12
            for x in range(0, imageLargeur, 8):
                # Si la luminosité est forte
                if (robot.getImagePixelLuminosity(x, y) > 20):
                    # On affiche un soleil à la place du pixel dans la console
                    print("🌕", end="")
                # Si la luminosité est faible
                else:
                    # On affiche une ombre à la place du pixel dans la console
                    print("🌑", end="")
            print("")
