# -*- coding: utf-8 -*-

"""
Librairie développée par Julien Arné - jusdeliens.com
sous licence CC BY-NC-ND 3.0 (plus d'informations sur https://creativecommons.org/licenses/by-nc-nd/3.0/)
Elle permet d'incarner un agent capable d'évoluer dans un jeu jusdeliens selon le code que vous développerez
L'agent est doté de variables d'état :
- vie : de 0 (mort) à 100 (maximum initial)
- orientation : 4 points cardinaux (Nord = 1, Sud = 3, Est = 0, Ouest = 2)
- x et y : position respectivement l'abscisse et l'ordonnée sur le terrain de jeu
- distance : frontale de 0 (pas d'obstacle) à 100 (obstacle lointain dans l'orientation de l'agent)
- munitions : pour tirer sur son adversaire et lui infliger des dégats
- voisins : dictionnaire repertoriant les agents voisins
ainsi que de fonction d'action pour intéragir dans le jeu :
- déplacer : modifier la position x,y pour aller sur une case adjacente
- orienter : changer l'orientation
- tirer : pour activer un tir en rafal dans l'orientation en cours, ou bien arrêter de tirer
Selon les règles du jeu, vous devrez utiliser ses fonctions pour gagner !
Attention à bien rester en vie !!
"""

__version__ = '0.9.17'

import json
import random
import time
from datetime import datetime

import paho.mqtt.client as mqtt


def _onConnect(client, agent, flags, rc):
    print("Connexion de " + agent.nom + " au serveur valide")
    if (rc == 0):
        agent._estConnecteAuBroker = True
        if (agent.verbose):
            print("Abonnement de", agent.nom, "au topic", agent._topicAgentsRead, "en cours ...")
        agent._mqtt.subscribe(agent._topicAgentsRead)
        if (agent.verbose):
            print("Abonnement de", agent.nom, "au topic", agent._topicGameRead, "en cours ...")
        agent._mqtt.subscribe(agent._topicGameRead)
    else:
        print("Connexion de " + agent.nom + " au serveur retourne code", str(rc))


def _onDisconnect(client, agent, rc):
    print("Deconnexion de " + agent.nom + " du serveur")
    agent._estConnecteAuBroker = False


def _onSubscribe(client, agent, mid, granted_qos):
    if (agent.verbose):
        print("Abonnement de", agent.nom, "au topic", mid, "valide")


def _onUnsubscribe(client, agent, mid):
    if (agent.verbose):
        print("Desabonnement de", agent.nom, "au topic", mid)


def _onMessage(client, agent, msg):
    agent._dernierReception = datetime.now()
    payload = str(msg.payload.decode())
    if agent.verbose == True:
        print("Reception sur", msg.topic, "de", payload)
    state = json.loads(payload)
    if (msg.topic == agent._topicGameRead):
        jeuAChange = False
        for cle, valeur in state.items():
            if (cle not in agent.jeu):
                if agent.verbose == True:
                    print("Changement du jeu :", cle, "=", valeur)
                jeuAChange = True
                continue
            if (type(agent.jeu[cle]) != type(valeur)):
                continue
            if (agent.jeu[cle] != valeur):
                if agent.verbose == True:
                    print("Changement du jeu :", cle, "=", valeur)
                jeuAChange = True
        if (jeuAChange):
            agent.quandJeuChange(agent.jeu, state)
            if (agent._quandJeuChange != None):
                agent._quandJeuChange(agent, agent.jeu, state)
            agent.jeu = state
    elif (msg.topic == agent._topicAgentRead):
        if ('x' in state):
            nouveauX = int(state['x'])
            if (nouveauX != agent.x):
                agent.quandXChange(agent.x, nouveauX)
                if (agent._quandXChange != None):
                    agent._quandXChange(agent, agent.x, nouveauX)
            agent.x = nouveauX
            agent.pose = (agent.x, agent.y, agent.orientation)
        if ('y' in state):
            nouveauY = int(state['y'])
            if (nouveauY != agent.y):
                agent.quandYChange(agent.y, nouveauY)
                if (agent._quandYChange != None):
                    agent._quandYChange(agent, agent.y, nouveauY)
            agent.y = nouveauY
            agent.pose = (agent.x, agent.y, agent.orientation)
        if ('dir' in state):
            nouvelleOrientation = int(state['dir'])
            if (nouvelleOrientation != agent.orientation):
                agent.quandOrientationChange(agent.orientation, nouvelleOrientation)
                if (agent._quandOrientationChange != None):
                    agent._quandOrientationChange(agent, agent.orientation, nouvelleOrientation)
            agent.orientation = nouvelleOrientation
            agent.pose = (agent.x, agent.y, agent.orientation)
        if ('life' in state):
            nouvelleVie = int(state['life'])
            if (nouvelleVie != agent.vie):
                agent.quandVieChange(agent.vie, nouvelleVie)
                if (agent._quandVieChange != None):
                    agent._quandVieChange(agent, agent.vie, nouvelleVie)
            agent.vie = nouvelleVie
        if ('ammo' in state):
            nouvellesMunitions = int(state['ammo'])
            if (nouvellesMunitions != agent.munitions):
                agent.quandMunitionsChange(agent.munitions, nouvellesMunitions)
                if (agent._quandMunitionsChange != None):
                    agent._quandMunitionsChange(agent, agent.munitions, nouvellesMunitions)
            agent.munitions = nouvellesMunitions
        if ('d' in state):
            nouvelleDistance = int(state['d'])
            if (nouvelleDistance != agent.distance):
                agent.quandDistanceChange(agent.distance, nouvelleDistance)
                if (agent._quandDistanceChange != None):
                    agent._quandDistanceChange(agent, agent.distance, nouvelleDistance)
            agent.distance = nouvelleDistance
        if ('dest' in state):
            nouvelleDestinationAtteinte = str(state['dest'])
            if (nouvelleDestinationAtteinte != agent.derniereDestinationAtteinte):
                agent.quandDestinationAtteinte(agent.derniereDestinationAtteinte, nouvelleDestinationAtteinte)
                if (agent._quandDestinationAtteinte != None):
                    agent._quandDestinationAtteinte(agent, agent.derniereDestinationAtteinte,
                                                    nouvelleDestinationAtteinte)
            agent.derniereDestinationAtteinte = nouvelleDestinationAtteinte
        if ('fire' in state):
            if (isinstance(state['fire'], bool)):
                agent.tir = state['fire']
            else:
                agent.tir = True
        if ('profile' in state):
            agent.profile = state['profile']
        if ('team' in state):
            agent.team = state['team']
        if ('led' in state):
            agent.couleur = state['led']
        if ('eta' in state):
            agent.villesRestantes = state['eta']
        if ('range' in state):
            agent.voisins = state['range']
        if ('chat' in state):
            agent.chat = state['chat']
        if (agent._premiereReception):
            agent._premiereReception = False


def _toRequest(agent):
    request = {}
    for cle, valeur in agent._ordre.items():
        request[cle] = valeur
    if (agent._premiereReception):
        if ('dir' not in request):
            request['dir'] = 0
    else:
        tir = agent.tir
        if ('fire' in agent._ordre):
            tir = agent._ordre['fire']
        if (tir and agent._fonctionTir != None):
            x = agent.x
            y = agent.y
            gridColumns = agent.jeu["gridColumns"]
            gridRows = agent.jeu["gridRows"]
            gridDim = max((gridColumns, gridRows))
            t = 0
            pts = []
            while (x >= 0 and x < gridColumns and y >= 0 and y < gridRows and t < gridDim):
                if (agent.orientation == 0):
                    fx = agent.y - int(round(agent._fonctionTir(x - agent.x)))
                    n = len(pts)
                    for yfx in range(y - 1, fx - 1, -1):
                        pts.append((x, yfx))
                    if (n == len(pts)):
                        pts.append((x, y))
                    y = fx
                    x = x + 1
                elif (agent.orientation == 1):
                    fx = agent.x - int(round(agent._fonctionTir(agent.y - y)))
                    n = len(pts)
                    for xfx in range(x - 1, fx - 1, -1):
                        pts.append((xfx, y))
                    if (n == len(pts)):
                        pts.append((x, y))
                    x = fx
                    y = y - 1
                elif (agent.orientation == 2):
                    fx = agent.y + int(round(agent._fonctionTir(agent.x - x)))
                    n = len(pts)
                    for yfx in range(y + 1, fx + 1, 1):
                        pts.append((x, yfx))
                    if (n == len(pts)):
                        pts.append((x, y))
                    y = fx
                    x = x - 1
                elif (agent.orientation == 3):
                    fx = agent.x + int(round(agent._fonctionTir(y - agent.y)))
                    n = len(pts)
                    for xfx in range(x + 1, fx + 1, 1):
                        pts.append((xfx, y))
                    if (n == len(pts)):
                        pts.append((x, y))
                    x = fx
                    y = y + 1
                else:
                    break
                t = t + 1
            if (agent.verbose):
                print("Tir trajectoire:", pts)
            request['fire'] = pts
    return json.dumps(request)


def _updateConnection(agent):
    maintenant = datetime.now()

    if (agent._isLoopStarted == False):
        agent.connecter()

    dtJeuHorsLigne = 11000
    if ("dtPing" in agent.jeu):
        dtJeuHorsLigne = agent.jeu["dtPing"] + 1000
    dtReception = (maintenant - agent._dernierReception).total_seconds() * 1000
    if (dtReception > dtJeuHorsLigne):
        if (agent.estConnecte == True):
            print("Deconnecté du jeu")
            agent._premiereReception = True
            agent.estConnecte = False
            agent.jeu['connected'] = False
            agent.quandDeconnecte()
            if (agent._quandDeconnecte != None):
                agent._quandDeconnecte(agent)
    else:
        if (agent.estConnecte == False):
            print("Connecté au jeu")
            agent.estConnecte = True
            agent.quandConnecte()
            if (agent._quandConnecte != None):
                agent._quandConnecte(agent)


class Agent:
    """Classe permettant d'incarner un agent dans un jeu jusdeliens et de le faire évoluer"""
    print("Agent init")
    actualiserAvecSleep = True
    dtEnvoiRequete = 300
    topicAgentRead = "pytactx/agents/state"
    topicAgentWrite = "pytactx/agents/request"
    topicGameRead = "pytactx/game/state"

    def __init__(self, id="", username="", password="", arena="", server="", prompt=False, verbose=False):
        """Valeurs possibles pour username, password, arena et server : chaines de caracteres communiquees par l'administrateur jusdeliens
        Choix du nom a votre guise"""
        print(
            "Bonjour a tous les jusdeliens ! Pour participer aux prochains affrontements, rendez-vous sur https://jusdeliens.com\nPour visualiser l'arene de jeu, allez sur https://jusdeliens.com/play/pytactx-viewer\nPour en savoir plus sur comment coder l'intelligence de votre agent, rdv sur https://tutos.jusdeliens.com/index.php/2020/01/14/pytactx-prise-en-main/")
        if (type(id) is not str or type(username) is not str or type(password) is not str or type(
                arena) is not str or type(server) is not str):
            print(
                "ATTENTION: utiliser des texte entre guillement (str) pour les parametres nom,username,password,server pour construire un objet Agent")
            id = str(id)
            username = str(username)
            password = str(password)
            arena = str(arena)
            server = str(server)
        if (type(verbose) is not bool or type(prompt) is not bool):
            print(
                "ATTENTION: utiliser un booleen (bool) pour les parametres verbose et prompt pour construire un objet Agent")
            verbose = False

        if (id == "" and prompt == True):
            id = input("Entrer le nom de votre agent : ")
        if (id == ""):
            id = "Agent" + str(random.randint(0, 9999))
        if (username == "" and prompt == True):
            username = input("Entrer le username : ")
            password = input("Entrer le password : ")
        if (username == ""):
            username = "demo"
            password = "demo"
        if (password == "" and prompt == True):
            password = input("Entrer le password : ")
        if (arena == "" and prompt == True):
            arena = input("Entrer le nom de l'arene: ")
        if (arena == ""):
            arena = "demo"
        if (server == "" and prompt == True):
            server = input("Entrer l'url vers le serveur: ")
        if (server == ""):
            server = "mqtt.jusdeliens.com"

        while (id == arena and prompt == True):
            id = input("Entrer un nom d'agent différent de l'arène : ")
        while (id == arena):
            id = "Agent" + str(random.randint(0, 9999))

        self.verbose = verbose
        self.nom = id
        self.server = server
        self.x = 0
        self.y = 0
        self.orientation = 0
        self.pose = (self.x, self.y, self.orientation)
        self.vie = 100
        self.munitions = 10
        self.distance = 0
        self.profile = 0
        self.team = 0
        self.chat = ""
        self.tir = False
        self.couleur = (0, 255, 0)
        self.derniereDestinationAtteinte = ""
        self.villesRestantes = []
        self.jeu = {"agents": [], "modeMove": "free", "dests": {}, "dtDir": 1000, "dtMove": 1000, "dtPop": 15000,
                    "dtFire": 1000, "hitFire": 10, "hitCollision": 10, "dxMax": 1, "dyMax": 1, "gridColumns": 10,
                    "gridRows": 10, "maxAgents": 8, "lifeIni": 100, "ammoIni": 10, "dtPing": 10000,
                    "onlyAuthorised": False, "chat": "", "pause": False, "connected": False}
        self.voisins = {}
        self._ordre = {}
        self._fonctionTir = None
        self._premiereReception = True
        self._isLoopStarted = False
        self._dernierEnvoi = datetime.fromtimestamp(0)
        self._dernierReception = datetime.fromtimestamp(0)
        self.estConnecte = False
        self._estConnecteAuBroker = False
        self._quandActualiser = None
        self._quandJeuChange = None
        self._quandDestinationAtteinte = None
        self._quandXChange = None
        self._quandYChange = None
        self._quandOrientationChange = None
        self._quandMunitionsChange = None
        self._quandVieChange = None
        self._quandDistanceChange = None
        self._quandConnecte = None
        self._quandDeconnecte = None
        self._topicGameRead = Agent.topicGameRead + "/" + arena
        self._topicAgentsRead = Agent.topicAgentRead + "/" + arena + "/+"
        self._topicAgentRead = Agent.topicAgentRead + "/" + arena + "/" + self.nom
        self._topicAgentWrite = Agent.topicAgentWrite + "/" + arena + "/" + self.nom
        self._qos = 0
        print("Creation de l'agent " + self.nom + " en cours ...")
        self._mqtt = mqtt.Client(client_id=self.nom, userdata=self)
        self._mqtt.on_connect = _onConnect
        self._mqtt.on_disconnect = _onDisconnect
        self._mqtt.on_subscribe = _onSubscribe
        self._mqtt.on_unsubscribe = _onUnsubscribe
        self._mqtt.on_message = _onMessage
        self._mqtt.username_pw_set(username, password)
        while (self._premiereReception == True):
            self.actualiser()
            time.sleep(0.5)
            print(".", end="")
        print("")

    def connecter(self):
        """Se connecte au serveur et au jeu"""
        if (self._isLoopStarted == False):
            print("Connexion de " + self.nom + " au seveur en cours ...")
            self._mqtt.connect(self.server)
            self._mqtt.loop_start()
            self._isLoopStarted = True

    def deconnecter(self):
        """Se deconnecte du serveur et du jeu"""
        if (self._isLoopStarted):
            self._mqtt.loop_stop(force=True)
        if (self._estConnecteAuBroker):
            self._mqtt.disconnect()

    def actualiser(self):
        """Synchronise les ordres et états de l'agent avec le serveur"""
        maintenant = datetime.now()

        _updateConnection(self)

        self.quandActualiser()
        if (self._quandActualiser != None):
            self._quandActualiser(self)

        if (self._estConnecteAuBroker == False):
            return

        dtEnvoi = (maintenant - self._dernierEnvoi).total_seconds() * 1000
        if ((self._premiereReception or len(self._ordre) > 0) and (
                dtEnvoi > Agent.dtEnvoiRequete or Agent.actualiserAvecSleep)):
            self._dernierEnvoi = maintenant
            request = _toRequest(self)
            self._ordre = {}
            if self.verbose == True:
                print("Envoi sur", self._topicAgentWrite, "de", request)
            self._mqtt.publish(self._topicAgentWrite, request, self._qos)

        if (Agent.actualiserAvecSleep):
            time.sleep(Agent.dtEnvoiRequete / 1000)

    def tirer(self, activer=True, fonction=None):
        """
        Valeurs bool possibles activer : True (tir en rafale) ou False (arrête de tirer)
        Valeur possible pour fonction : une fonction de la forme nomDeLaFonction(x) qui retourne un y = f(x)
        """
        if (type(activer) is not bool):
            print("ATTENTION: utiliser un paramètre booleen (bool) pour appeler la fonction tirer !!")
            activer = False
        if (activer == self.tir and fonction == self._fonctionTir):
            return False
        self._fonctionTir = fonction
        self._ordre['fire'] = activer
        return True

    def deplacerVers(self, destination):
        """Se déplacer vers un lieu au format str parmi jeu["dest"] en mode jeu["modeMove"] destination"""
        if ("modeMove" not in self.jeu):
            return False
        if (self.jeu["modeMove"] != "destination"):
            return False
        if (type(destination) is not str):
            print("ATTENTION: deplacerVers attend une destination au format str!!")
            return False
        self._ordre['dest'] = destination
        if (destination not in self.jeu["dests"]):
            return
        destinationX = self.jeu["dests"][destination]['x']
        destinationY = self.jeu["dests"][destination]['y']
        if (self.x > destinationX):
            self._ordre['x'] = self.x - 1
        elif (self.x < destinationX):
            self._ordre['x'] = self.x + 1
        if (self.y > destinationY):
            self._ordre['y'] = self.y - 1
        elif (self.y < destinationY):
            self._ordre['y'] = self.y + 1

    def deplacer(self, x, y):
        """Valeurs int possibles pour x et y : int supérieure ou égale à 0"""
        if ("modeMove" in self.jeu):
            if (self.jeu["modeMove"] != "free"):
                print("ATTENTION: déplacement en x,y possible uniquement en mode libre")
                return False
        if (type(x) is not int or type(y) is not int):
            print("ATTENTION: utiliser des x,y entiers (int) pour appeler la fonction deplacer !!")
            x = int(x)
            y = int(y)
        if (x < 0 or y < 0):
            return False
        if (x == self.x and y == self.y):
            return False
        self._ordre['x'] = x
        self._ordre['y'] = y
        return True

    def orienter(self, orientation):
        """Valeurs int possibles pour orientation : 0 (pour Est ou droite), 1 (pour Nord ou haut), 2 (Ouest ou gauche), 3 (Sud ou bas)"""
        if (type(orientation) is not int):
            print("ATTENTION: utiliser une orientationt entière (int) pour appeler la fonction orienter !!")
            orientation = int(orientation)
        if (orientation < 0 or orientation > 3):
            print("ATTENTION: orientation doit être compris entre 0 et 3 pour appeler la fonction orienter !!")
            return False
        if (self.orientation == orientation):
            return False
        self._ordre['dir'] = orientation
        return True

    def publier(self, message, public=True):
        """Ecrire un message public dans l'arène"""
        if (type(message) is not str):
            print("ATTENTION: message à publier doit être un str !!")
            message = str(message)
        if (len(message) > 300):
            print("Impossible de publier message trop long !!")
            return
        if (public):
            if (message != self.jeu["chat"]):
                self._ordre['ppublic'] = message
        else:
            if (message != self.chat):
                self._ordre['pprivate'] = message

    def changerCouleur(self, rouge, vert, bleu):
        """Change la couleur de l'agent avec les composantes RVB de type int de 0 à 255"""
        if (type(rouge) is not int or type(vert) is not int or type(bleu) is not int):
            print("ATTENTION: utiliser des rouge,vert,bleu entiers (int) pour appeler la fonction changerCouleur !!")
            rouge = int(rouge)
            vert = int(vert)
            bleu = int(bleu)
        if (rouge < 0 or rouge > 255 or vert < 0 or vert > 255 or bleu < 0 or bleu > 255):
            print(
                "ATTENTION: rouge,vert,bleu doivent être compris entre 0 et 255 pour appeler la fonction changerCouleur !!")
            return False
        if (self.couleur[0] == rouge and self.couleur[1] == vert and self.couleur[2] == bleu):
            return False
        self._ordre['led'] = (rouge, vert, bleu)

    def quandActualiser(self):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandJeuChange(self, ancienJeu, nouveauJeu):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandDestinationAtteinte(self, ancienneDestinationAtteinte, nouvelleDestinationAtteinte):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandXChange(self, ancienX, nouveauX):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandYChange(self, ancienY, nouveauY):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandOrientationChange(self, ancienneOrientation, nouvelleOrientation):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandMunitionsChange(self, anciennesMunitions, nouvellesMunitions):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandDistanceChange(self, ancienneDistance, nouvelleDistance):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandVieChange(self, ancienneVie, nouvelleVie):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandConnecte(self):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def quandDeconnecte(self):
        """Méthode à surcharger dans la classe enfante"""
        pass

    def executerQuandActualiser(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent)"""
        self._quandActualiser = callback

    def executerQuandJeuChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienJeu, nouveauJeu)"""
        self._quandJeuChange = callback

    def executerQuandDestinationAtteinte(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienneDestinationAtteinte, nouvelleDestinationAtteinte)"""
        self._quandDestinationAtteinte = callback

    def executerQuandXChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienX, nouveauX)"""
        self._quandXChange = callback

    def executerQuandYChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienY, nouveauY)"""
        self._quandYChange = callback

    def executerQuandOrientationChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienneOrientation, nouvelleOrientation)"""
        self._quandOrientationChange = callback

    def executerQuandMunitionsChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, anciennesMunitions, nouvelleMunitions)"""
        self._quandMunitionsChange = callback

    def executerQuandVieChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienneVie, nouvelleVie)"""
        self._quandVieChange = callback

    def executerQuandDistanceChange(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent, ancienneDistance, nouvelleDistance)"""
        self._quandDistanceChange = callback

    def executerQuandConnecte(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent)"""
        self._quandConnecte = callback

    def executerQuandDeconnecte(self, callback):
        """Valeur possible pour callback : une fonction de la forme nomDeLaFonction(agent)"""
        self._quandDeconnecte = callback
