from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from random import randint

from src.bot.enums import Orientation

COLORS = {
    "Flee": (117, 117, 117),
    "Patrol": (42, 212, 117),
    "Pursuit": (0, 0, 255),
    "Assist": (0, 255, 0),
    "Search": (122, 42, 117),
}


class Behavior(ABC):
    def __init__(self, bot, return_state: Behavior = None, goto: tuple[int, int] = None):
        self._log = logging.getLogger(__class__.__name__)

        self._bot = bot
        self._goto_coords = goto or self._bot.next_actions
        self._return_to = return_state

    @staticmethod
    def is_friendly(bot: dict):
        """ Renvoi True si le bot donné est dans les alliés """
        return bot['led'] == COLORS["Assist"]

    def update(self):
        """must at least return self"""
        return self

    @abstractmethod
    def execute(self):
        pass

    def _super_rand(self):
        rand = 0
        while rand == 0:
            rand = randint(-1, 1)
        if self._bot.orientation + rand == Orientation.WEST and \
                (self._bot.x <= 3 or self._bot.y <= 3) \
           or self._bot.orientation + rand == Orientation.NORTH and \
                (self._bot.x <= 3 or self._bot.y <= 3):
            rand = -rand
        return rand


class Patrol(Behavior):

    def execute(self):
        self._log.info(f"Patroling {self._goto_coords}")
        self._bot.changerCouleur(*COLORS["Patrol"])
        for enemy in self._bot.voisins:
            # Si un ennemi à portée
            if self._bot.a_portee_de_tir(enemy):
                self._bot.set_target(enemy)
                goto = self._bot.get_coords_from_nom(enemy)
                self._log.info(f"found an enemy {enemy}@{goto}")
                self._bot.behavior = Pursuit(bot=self._bot, return_state=self._return_to, goto=goto)

        #   si on est aux coords voulues
        if self._goto_coords == (self._bot.x, self._bot.y):
            self._goto_coords = self._bot.next_actions
            self._bot.behavior = Patrol(self._bot, goto=self._goto_coords)
        if self._goto_coords:
            self._log.info(f"moving to {self._goto_coords}")
            self._bot.deplacer(*self._goto_coords)


class Flee(Behavior):
    """ Passe en Patrouille si aucun ennemi à portée
    Sinon, évite les ennemis jusqu'à se retrouver seul."""

    def execute(self):
        self._log.info("Fleeing")
        self._bot.changerCouleur(*COLORS["Flee"])
        if self._bot.bots_a_portee:
            self._bot.orienter((self._bot.orientation + 2) % 4)  # Flee in opposite direction
            self._bot.avancer(2)
        else:  # Passe en patrouille si aucun ennemi en vue
            self._bot.behavior = (self._return_to or Patrol)(bot=self._bot, goto=self._goto_coords)
        return


class Pursuit(Behavior):
    def execute(self):
        self._log.info("Pursuit")
        self._bot.changerCouleur(*COLORS["Pursuit"])
        if not self._bot.bots_a_portee:
            self._bot.behavior = (self._return_to or Search)(bot=self._bot, goto=self._goto_coords)
        else:
            self._bot.orienter_vers_ennemi_plus_proche()
            not self._bot.a_portee_de_tir(self._bot.target) and self._bot.avancer()
        if self._bot.vie <= 50:
            self._bot.behavior = Flee(bot=self._bot, return_state=self._return_to)
        if 90 >= self._bot.vie > 50:
            self.switzzer_strat()

    def switzzer_strat(self):
        """ Effectue la methode SWITZZER pendant la bataille """
        if not hasattr(self, "_static_rounds") or self._static_rounds >= 2:
            self._static_rounds = 0
            ori = self._bot.orientation + self._super_rand()
            self._bot.orienter(ori)
            self._bot.avancer(2)
        else:
            self._static_rounds += 1



class Search(Behavior):
    def execute(self):
        self._log.info("Searching")
        self._bot.changerCouleur(*COLORS["Search"])

        if self._bot.bots_en_vue:
            self._bot.behavior = (self._return_to or Pursuit)(bot=self._bot)
        elif not hasattr(self, '_search_rounds') or self._search_rounds <= 0:
            self._search_rounds = 3
            self._bot.behavior = (self._return_to or Patrol)(bot=self._bot)
        else:
            self._bot.deplacer(self._bot.x + randint(-1, 1), self._bot.y + randint(-1, 1))
            self._bot.orienter((self._bot.orientation + 1) % 4)  # Turn around
            self._search_rounds -= 1


class Assist(Behavior):
    @staticmethod
    def is_friendly(bot: dict):
        return

    def execute(self):
        self._log.info(f"Assisting {self._bot.target}")
        self._bot.changerCouleur(*COLORS["Assist"])
        p_dict = self._bot.voisins[self._bot.target]
        x, y = p_dict['x'], p_dict['y']
        self._bot.deplacer(x, y)
