# -*- coding: utf-8 -*-

"""
Librairie développée par Julien Arné - jusdeliens.com
sous licence CC BY-NC-ND 3.0 (plus d'informations sur https://creativecommons.org/licenses/by-nc-nd/3.0/)
Elle permet de manipuler une camera pyscopx pour récupérer et modifier les images reçues
"""
__version__ = '0.9.2'

import base64
import io
import random
import sys
import time
from datetime import datetime

import paho.mqtt.client as mqtt
from PIL import Image


def _onConnect(client, camera, flags, rc):
    print("Connexion de " + camera.userId + " au serveur retourne code", str(rc))
    if (rc == 0):
        camera._estConnecteAuBroker = True
        if (camera.verbose):
            print("Abonnement de", camera.userId, "au topic", camera._topicCameraRead, "en cours ...")
        camera._mqtt.subscribe(camera._topicCameraRead)


def _onDisconnect(client, camera, rc):
    print("Deconnexion de " + camera.userId + " du serveur")
    camera._estConnecteAuBroker = False


def _onSubscribe(client, camera, mid, granted_qos):
    print("Abonnement de", camera.userId, "au topic", mid, "valide")


def _onUnsubscribe(client, camera, mid):
    print("Desabonnement de", camera.userId, "au topic", mid)


def _onMessage(client, camera, msg):
    camera._prevReception = datetime.now()
    if camera.verbose == True:
        print("Reception sur", msg.topic, "de", len(msg.payload), "octets")
    if (msg.topic == camera._topicCameraRead):
        # Convert response to image
        try:
            image_data = msg.payload
            if (Camera.useBase64Decoding):
                image_data = base64.b64decode(image_data)
            camera._rawImageBuffer = Image.open(io.BytesIO(image_data))
            if (camera.verbose):
                print("Nouvelle image reçue de", camera.cameraId)
        except:
            camera._rawImageBuffer = None
            if (camera.verbose):
                print("Erreur durant la réception de l'image:", sys.exc_info()[0])
        # Callback call
        camera.quandImageRecue(camera._rawImage, camera._rawImageBuffer)
        if (camera._onImageReceived != None):
            camera._onImageReceived(camera, camera._rawImage, camera._rawImageBuffer)


def _updateConnection(camera):
    maintenant = datetime.now()

    if (camera._isLoopStarted == False):
        camera.connecter()

    dtReception = (maintenant - camera._prevReception).total_seconds() * 1000
    if (dtReception > Camera.dtDeconnexion):
        if (camera.estConnecte == True):
            if (camera.verbose):
                print("Deconnecté de la caméra")
            camera.estConnecte = False
            camera.quandDeconnecte()
            if (camera._onDisconnected != None):
                camera._onDisconnected(camera)
    else:
        if (camera.estConnecte == False):
            if (camera.verbose):
                print("Connecté à la caméra")
            camera.estConnecte = True
            camera.quandConnecte()
            if (camera._onConnected != None):
                camera._onConnected(camera)


def RGBToHSL(r, g, b):
    # Make r, g, and b fractions of 1
    r /= 255
    g /= 255
    b /= 255

    # Find greatest and smallest channel values
    cmin = min(r, g, b)
    cmax = max(r, g, b)
    delta = cmax - cmin
    h = 0
    s = 0
    l = 0

    # Calculate hue
    # No difference
    if (delta == 0):
        h = 0
    # Red is max
    elif (cmax == r):
        h = ((g - b) / delta) % 6
    # Green is max
    elif (cmax == g):
        h = (b - r) / delta + 2
    # Blue is max
    else:
        h = (r - g) / delta + 4

    h = int(h * 60)

    # Make negative hues positive behind 360°
    if (h < 0):
        h += 360

    # Calculate lightness
    l = (cmax + cmin) / 2

    # Calculate saturation
    if (delta == 0):
        s = 0
    else:
        s = delta / (1 - abs(2 * l - 1))

    # Multiply l and s by 100
    s = int(s * 100)
    if (s > 100):
        s = 100
    l = int(l * 100)
    if (l > 100):
        l = 100

    return (h, s, l)


def HSLToRGB(h, s, l):
    # Must be fractions of 1
    s /= 100.0
    l /= 100.0

    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2
    r = 0
    g = 0
    b = 0

    if (0 <= h and h < 60):
        r = c
        g = x
        b = 0
    elif (60 <= h and h < 120):
        r = x
        g = c
        b = 0
    elif (120 <= h and h < 180):
        r = 0
        g = c
        b = x
    elif (180 <= h and h < 240):
        r = 0
        g = x
        b = c
    elif (240 <= h and h < 300):
        r = x
        g = 0
        b = c
    elif (300 <= h and h < 360):
        r = c
        g = 0
        b = x

    r = int((r + m) * 255)
    if (r > 255):
        r = 255
        g = int((g + m) * 255)
    if (g > 255):
        g = 255
        b = int((b + m) * 255)
    if (b > 255):
        b = 255

    return (r, g, b)


class Camera:
    """Classe permettant de manipuler une camera pyscopx"""
    topicCameraRead = "pyscopx/camera/image"
    topicFiltreWrite = "pyscopx/filter/image"
    dtDeconnexion = 3000
    useBase64Decoding = True
    useBase64Encoding = True

    def __init__(self, cameraId="", filtreId="", username="", password="", server="", prompt=True, verbose=False):
        """Construit une variable caméra pour récupérer et modifier l'image recue"""
        print("Bonjour à vous jusdeliens en herbe ! Allumez votre robot ou votre caméra pour en prendre le contrôle.")
        print("Vous n'en avez pas ? Rendez-vous sur https://jusdeliens.com/")
        print("Vous avez besoin d'un coup de main ? Rendez-vous sur https://tutos.jusdeliens.com/")
        # Prompt console si constructeur sans parametres
        if ((cameraId == "" and prompt == True) or cameraId == "CamXXXX"):
            cameraId = input("Entrer l'id de votre camera: ")
        if (cameraId == ""):
            cameraId = "Cam" + str(random.randint(0, 9999))
        if ((filtreId == "" and prompt == True) or filtreId == "PrenomNOM"):
            filtreId = input("Entrer l'id de votre filtre: ")
        if (filtreId == ""):
            filtreId = "filtre" + str(random.randint(0, 9999))
        if ((username == "" and prompt == True) or username == 'USERNAME'):
            username = input("Entrer le username: ")
        if (password == "" or password == "PASSWORD"):
            password = input("Entrer le password : ")
        if (server == "" and prompt == True):
            server = input("Entrer le chemin vers le serveur: ")
        if (server == ""):
            server = "mqtt.jusdeliens.com"

        self.userId = filtreId
        self.server = server
        self.cameraId = cameraId
        self.filtreId = filtreId
        self.verbose = verbose
        self.estConnecte = False
        self.hauteur = 0
        self.largeur = 0
        self._estConnecteAuBroker = False
        self._rawImage = None
        self._rawImageBuffer = None
        self._filteredImage = None
        self._filteredImageBuffer = None
        self._onImageReceived = None
        self._onConnected = None
        self._onDisconnected = None
        self._topicCameraRead = Camera.topicCameraRead + "/" + self.cameraId
        self._topicFiltreWrite = Camera.topicFiltreWrite + "/" + self.filtreId
        self._prevSend = datetime.fromtimestamp(0)
        self._prevReception = datetime.fromtimestamp(0)
        self._isLoopStarted = False
        self._qos = 0
        self._mqtt = mqtt.Client(client_id=self.userId, userdata=self)
        self._mqtt.on_connect = _onConnect
        self._mqtt.on_disconnect = _onDisconnect
        self._mqtt.on_subscribe = _onSubscribe
        self._mqtt.on_unsubscribe = _onUnsubscribe
        self._mqtt.on_message = _onMessage
        self._mqtt.username_pw_set(username, password)

    def connecter(self):
        """Se connecte au serveur et au jeu"""
        if (self._isLoopStarted == False):
            print("Connexion de " + self.userId + " au serveur en cours ...")
            self._mqtt.connect(self.server)
            self._mqtt.loop_start()
            self._isLoopStarted = True

    def deconnecter(self):
        """Se deconnecte du serveur et du jeu"""
        if (self._isLoopStarted):
            self._mqtt.loop_stop(force=True)
        if (self._estConnecteAuBroker):
            self._mqtt.disconnect()

    def lirePixel(self, x, y):
        """Renvoie un typle (rouge,vert,bleu, teinte,saturation,luminosité) du pixel à la position spécifiée."""
        if (self._rawImage == None):
            print("Aucune image recue. Appeler la fonction actualiser ou vérifier vos identifiants et connexion.")
            return (0, 0, 0, 0, 0, 0)
        if (x < 0 or x >= self._rawImage.width or isinstance(x, int) == False):
            print("Valeur de x incorrecte. Doit être comprise entre 0 et", self._rawImage.width - 1)
            return (0, 0, 0, 0, 0, 0)
        if (y < 0 or y >= self._rawImage.height or isinstance(y, int) == False):
            print("Valeur de y incorrecte. Doit être comprise entre 0 et", self._rawImage.height - 1)
            return (0, 0, 0, 0, 0, 0)
        r, g, b = self._rawImage.getpixel((x, y))
        h, s, l = RGBToHSL(r, g, b)
        return (r, g, b, h, s, l)

    def lirePixelRouge(self, x, y):
        """Renvoie la composante rouge du pixel à la position spécifiée. Comprise entre 0 et 255."""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return r

    def lirePixelVert(self, x, y):
        """Renvoie la composante vert du pixel à la position spécifiée. Comprise entre 0 et 255."""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return g

    def lirePixelBleu(self, x, y):
        """Renvoie la composante bleu du pixel à la position spécifiée. Comprise entre 0 et 255."""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return b

    def lirePixelTeinte(self, x, y):
        """Renvoie la composante teinte (du rouge au violet) du pixel à la position spécifiée. Comprise entre 0 et 359"""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return h

    def lirePixelSaturation(self, x, y):
        """Renvoie la composante saturation du pixel à la position spécifiée. Comprise entre 0 (gris) et 100 (vive)"""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return s

    def lirePixelLuminosite(self, x, y):
        """Renvoie la composante luminosité du pixel à la position spécifiée. Comprise entre 0 (noir) et 100 (blanc)"""
        r, g, b, h, s, l = self.lirePixel(x, y)
        return l

    def ecrirePixel(self, x, y, rouge, vert, bleu):
        """Modifie les compostante rouge,vert,bleu du pixel à la position spécifiée."""
        if (self._filteredImageBuffer == None):
            print("Aucune image recue. Appeler la fonction actualiser ou vérifier vos identifiants et connexion.")
            return
        if (x < 0 or x >= self._filteredImageBuffer.width or isinstance(x, int) == False):
            print("Valeur de x incorrecte. Doit être comprise entre 0 et", self._filteredImageBuffer.width - 1)
            return
        if (y < 0 or y >= self._filteredImageBuffer.height or isinstance(y, int) == False):
            print("Valeur de y incorrecte. Doit être comprise entre 0 et", self._filteredImageBuffer.height - 1)
            return
        if (rouge < 0 or rouge > 255 or isinstance(rouge, int) == False):
            print("Valeur de rouge incorrecte. Doit être comprise entre 0 et 255")
            return
        if (vert < 0 or vert > 255 or isinstance(vert, int) == False):
            print("Valeur de vert incorrecte. Doit être comprise entre 0 et 255")
            return
        if (bleu < 0 or bleu > 255 or isinstance(bleu, int) == False):
            print("Valeur de bleu incorrecte. Doit être comprise entre 0 et 255")
            return
        self._filteredImageBuffer.putpixel((x, y), (rouge, vert, bleu))

    def actualiser(self):
        """Recoit la dernière image envoyée par la caméra."""
        time.sleep(0.5)

        _updateConnection(self)

        if (self._estConnecteAuBroker == False):
            return

        try:
            # Publish transform image data
            if (
                    self._filteredImageBuffer is not None and self._filteredImageBuffer != self._filteredImage and self._filteredImageBuffer != self._rawImage):
                self._prevSend = datetime.now()
                self._filteredImage = self._filteredImageBuffer
                imgByteArr = io.BytesIO()
                self._filteredImageBuffer.save(imgByteArr, format='jpeg')
                imgByteArr = imgByteArr.getvalue()
                if (Camera.useBase64Encoding):
                    imgByteArr = base64.b64encode(imgByteArr)
                if self.verbose == True:
                    print("Envoi sur", self._topicFiltreWrite, "de", len(imgByteArr), "octets")
                self._mqtt.publish(self._topicFiltreWrite, imgByteArr, self._qos)

            # Get camera image from buffer
            self._rawImage = self._rawImageBuffer
            self._rawImageBuffer = None

            # Reset filter image
            if (self._rawImage is not None):
                self._filteredImageBuffer = self._rawImage.copy()
                self.hauteur = self._rawImage.height
                self.largeur = self._rawImage.width
            else:
                self.hauteur = 0
                self.largeur = 0

        # Reset image if error while receiving image
        except:
            self._rawImageBuffer = None
            self._filteredImageBuffer = None

    def quandImageRecue(self, ancienneImage, nouvelleImage):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandConnecte(self):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandDeconnecte(self):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def executerQuandImageRecue(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(camera, ancienneImage, nouvelleImage)"""
        self._onImageReceived = callback

    def executerQuandConnecte(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(camera)"""
        self._onConnected = callback

    def executerQuandDeconnecte(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(camera)"""
        self._onDisconnected = callback
