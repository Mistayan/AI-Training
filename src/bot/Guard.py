from __future__ import annotations

from gymnasium.envs.toy_text.blackjack import cmp

from pytactx import Agent
from src.bot.behavior import Patrol
from src.bot.behavior.Behavior import Behavior
from src.bot.enums import Orientation

"""
tous les bots de la map sont contenus dans un dict.
un bot est représenté par le dict suivant:
{name: "Name", 
    {'x': 6, 'y': 5, 'dir': 1, 'ammo': 100, 'd': 1, 'life': 100,
     'fire': False, 'led': [0, 0, 255], 'profile': 0,
     'team': 0, 'dest': '', 'eta': [], 'chat': ''}}


"""


class Bot(Agent):
    def __init__(self, name: str = None, default_behavior=None, initial_target: str = None):
        self.__go = False
        super().__init__(id=name, verbose=False)
        self.path = [(self.x + 3, self.y + 3),
                     (self.x - 3, self.y - 3),
                     (self.x + 1, self.y + 1)]
        self.behavior = default_behavior(self) if default_behavior else Patrol(self)  # set initial behavior
        self.target = initial_target
        self.changerCouleur(42, 42, 42)
        # self.executerQuandVieChange(
        #     partial(self.publier, "\\\\\\\Pas cool\\\\\\\\"))

    def quandActualiser(self):
        print("Actualisation")
        if self.__go:
            self.attaquer_si_ennemi_en_vue()
            self.behavior.execute()
            self.update_behavior()

    def go(self) -> None:
        """ Lance le traitement automatique jusqu'à victoire du robot"""
        self.__go = True
        while self.vie > 0:
            self.actualiser()

    @property
    def next_actions(self) -> tuple[int, int]:
        """ Methode à mémoire.
        Renvoi la prochaine action à effectuer dans la liste self.path"""
        print("Next Action")
        if not hasattr(self, '_path_iter'):
            self._path_iter = iter(self.path)
        try:
            return next(self._path_iter)
        except StopIteration:
            print("restart actions")
            self._path_iter = iter(self.path)
            return next(self._path_iter)

    def attaquer_si_ennemi_en_vue(self):
        """ Methode qui fait tirer notre robot automatiquement
         sur un ennemi qui se trouverait en face de nous"""
        print("Attaquer si ennemi en vue")
        if self.__go and self.target and self.a_portee_de_tir(self.target):
            print(f"{self.target} à portée")
            if self.est_vivant(self.target):  # and not self.behavior.is_friendly(target_dict):
                print("ET VIVANT !!")
                # target_dict = self.voisins[self.target]
                # self.orienter_vers((target_dict['x'], target_dict['y']))
                self.tirer()
                return
        self.tirer(False)

    def update_behavior(self) -> None:
        """ Met à jour le comportement du robot, en fonction des changements du comportement """
        if isinstance(self.behavior, Behavior):
            self.behavior = self.behavior.update()

    def orienter_vers(self, coords: tuple) -> None:
        """ Oriente le robot vers l'angle le plus proche de celui de la cible donnée """
        if coords is None:
            return
        x, y = coords
        # en fonction de la différence x/y, renvoi une orientation
        orientation = {(1, 0): Orientation.EAST, (-1, 0): Orientation.WEST,
                       (0, 1): Orientation.NORTH, (0, -1): Orientation.SOUTH}
        dx, dy = x - self.x, y - self.y
        self.orienter(orientation[(cmp(dx, 0), cmp(dy, 0))].value)

    def orienter_vers_ennemi_plus_proche(self) -> None:
        """ Oriente le robot vers **l'ennemi** le plus proche """
        name = self.ennemi_plus_proche()
        if name:
            self.orienter_vers(self.get_coords_from_nom(name))

    def ennemi_plus_proche(self) -> str:
        """ Renvoi le nom de **l'ennemi** le plus proche
        [Vérifie que ce n'est pas un allié, en fonction du comportement]"""
        enemies = [n for n in self.voisins if not self.behavior.is_friendly(self.voisins[n]) and self.voisins[n][
            "life"] > 0 and self.a_portee_de_tir(n)]
        closest_enemy = min(enemies, key=lambda x: ((self.voisins[x]['x'] - self.x) ** 2 + (
                self.voisins[x]['y'] - self.y) ** 2) ** 0.5, default=None)
        return closest_enemy

    def get_coords_from_nom(self, nom: str) -> tuple[int, int]:
        """ Retourne les coordonnées du robot choisi """
        print(f"Chercher coords de {nom}")
        target = self.voisins[nom] if nom in self.voisins else None
        if target:
            return target['x'], target['y']

    def __distance(self, coords: tuple[int, int]) -> float:
        """ Retourne la distance entre le robot et la cible"""
        x, y = coords
        return ((x - self.x) ** 2 + (y - self.y) ** 2) ** 0.5

    @property
    def bots_a_portee(self) -> list[str]:
        """ Liste de **TOUS** les bots à portée """
        bots = []
        for nom_ennemi in self.voisins:
            x, y = self.get_coords_from_nom(nom_ennemi)
            if self.__distance((x, y)) <= 6:
                bots.append(nom_ennemi)
        return bots

    def a_portee_de_tir(self, name: str) -> bool:
        """ True si la cible est à portée """
        coords = self.get_coords_from_nom(name)
        if not coords:
            return False
        x, y = coords
        # angle = cmath.phase(complex(x - self.x, y - self.y))
        distance = self.__distance((x, y)) <= 6
        aligne = self.x == x or self.y == y
        res = aligne and (self.distance or distance)
        print(f"a portée de tir de {name} ? => {res}")
        return res

    def est_vivant(self, name: str) -> bool:
        """ True si la cible est vivante """
        print(f"{name} est vivant ?")
        name = name or self.target
        if name:
            b = self.voisins[name]
            print(b['life'])
            return b['life'] > 0
        else:
            return False

    @property
    def bots_en_vue(self) -> list[str]:
        """ Liste des bots à portée de tir"""
        en_vue = []
        for nom_bot in self.bots_a_portee:
            if self.a_portee_de_tir(nom_bot):
                en_vue.append(nom_bot)
        return en_vue

    def set_target(self, target_name: str):
        """ Définit le nom de la cible à suivre """
        self.target = target_name

    # OVERRIDES
    # def tirer(self, activer=True, fonction=None):
    #     """ Override pour s'assurer de ne pas bloquer sur un ennemi mort"""
    #     if self.distance:
    #         print(f"tente de tirer @{self.distance} distance")
    #         return super().tirer(self.est_vivant(self.target))
    #     print("NOTHING IN DISTANCE")
    #     return False if activer else super().tirer(False)

    def avancer(self, dist: int = 1) -> None:
        """ Avance de N cases dans l'orientation actuelle du robot """
        ori = self.orientation
        y = self.y + (dist * -(ori - 2)) if ori in (Orientation.SOUTH, Orientation.NORTH) else 0
        x = self.x + (dist * -(ori - 1)) if ori in (Orientation.WEST, Orientation.EAST) else 0
        self.deplacer(x, y)
