import pickle

import numpy as np

from src.bot_de_combat.Guard import Bot
from src.bot_de_combat.behavior.Behavior import Dodge


def format_input(voisins: dict):
    """
    Les voisins : {bob: {'x': 0, 'y': 0, 'life': 100, 'ammo': 87, 'distance': 11, 'orientation': 0, ...}, ...}
    Sortie : [names], [[distance, ammo, life], ...]
    """
    if not voisins:
        names = []
        features = []
    else:
        names = list(voisins.keys())
        features = np.array(
            [[voisins[name]['distance'],
              voisins[name]['ammo'],
              voisins[name]['life']]
             for name in names])
    return names, features


class Hunter(Bot):

    def __init__(self):
        super().__init__()
        self.__go = False
        self.behavior = Dodge(self)
        self.path = []
        self.__decision_center = pickle.load(open("tests/fighter/pkl/svm-fear_factors-11.pkl", 'rb'))
        self.changerCouleur(255, 42, 42)
        self.executerQuandVieChange(Dodge(self))

    def on_update(self):
        if self.__go:
            choices = self.__decision_center.predict(format_input(self.voisins))
            self.path = [self.voisins[name]
                         for name, choice in zip(self.voisins, choices)
                         if choice == "EGGS-Terminate"]
            self.attaquer_si_ennemi_en_vue()
            self.deplacerVers(self.next_actions)
            self.update_behavior()
