from __future__ import annotations

from random import randint

from src.bot.behavior.Behavior import COLORS, Behavior
from src.bot.utils import Orientation

from src.utils.algo.Djirska import PathFinder


class Patrol(Behavior):
    def execute(self):
        self._log.info("Patrolling")
        self._bot.changerCouleur(*COLORS["Patrol"])
        if self._bot.bots_en_vue:
            enemy = next(bot for bot in self._bot.bots_en_vue if not self.is_friendly(bot))
            self._bot.behavior = self.change_state(Pursuit, enemy)
        else:
            if self._goto_coords:
                x, y = self._goto_coords.pop(0)
                self._bot.deplacer(x, y)
            else:
                self._bot.path = [(randint(0, self._bot.longueur), randint(0, self._bot.largeur)) for _ in range(3)]
                self._goto_coords = self._bot.path.copy()


class Pursuit(Behavior):
    def __init__(self, bot, return_state: Behavior = None, goto: tuple[int, int] = None):
        super().__init__(bot, return_state, goto)
        self._path_finder = PathFinder(self._bot.world)

    def execute(self):
        self._log.info("Pursuing")
        self._bot.changerCouleur(*COLORS["Pursuit"])
        if self._bot.bots_en_vue:
            enemy = next(bot for bot in self._bot.bots_en_vue if not self.is_friendly(bot))
            enemy_coords = self._bot.get_coords_from_nom(enemy)
            x, y = enemy_coords
            self._bot.deplacer(x, y)
        else:
            x, y = self._goto_coords
            if x < self._bot.x:
                self._bot.orienter(Orientation.WEST)
                self._bot.avancer(self._bot.x - x)
            elif x > self._bot.x:
                self._bot.orienter(Orientation.EAST)
                self._bot.avancer(x - self._bot.x)
            elif y < self._bot.y:
                self._bot.orienter(Orientation.NORTH)
                self._bot.avancer(self._bot.y - y)
            elif y > self._bot.y:
                self._bot.orienter(Orientation.SOUTH)
                self._bot.avancer(y - self._bot.y)
            else:  # reached target
                self._bot.behavior = self.change_state(Patrol)


class Flee(Behavior):
    def execute(self):
        self._log.info("Fleeing")
        self._bot.changerCouleur(*COLORS["Flee"])
        enemy_coords = [bot['coords'] for bot in self._bot.bots_en_vue if not self.is_friendly(bot)]
        if not enemy_coords:
            # If there are no enemies in sight, switch back to previous behavior
            self.change_state(self._return_to)
            return

        # Determine the average position of all enemies
        avg_x = sum(x for x, y in enemy_coords) / len(enemy_coords)
        avg_y = sum(y for x, y in enemy_coords) / len(enemy_coords)

        # Choose a destination that's as far away as possible from the average enemy position
        if avg_x < self._bot.x:
            x = self._bot.x + 1
        else:
            x = self._bot.x - 1
        if avg_y < self._bot.y:
            y = self._bot.y + 1
        else:
            y = self._bot.y - 1

        # Make sure the destination is within the game board
        if not self._bot.coords_in_board(x, y):
            pass
        else:
            # Move to the destination
            self._bot.deplacer(x, y)


class Search(Behavior):
    def __init__(self, bot, return_state: Behavior = None, goto: tuple[int, int] = None):
        super().__init__(bot, return_state, goto)
        self.count_search = 5

    def execute(self):
        self._log.info("Searching")
        self._bot.changerCouleur(*COLORS["Search"])

        if self._bot.bots_en_vue:
            self.count_search = 5
            self._bot.behavior = Pursuit(bot=self._bot)
        elif self.count_search <= 0:
            self.count_search = 5
            self._bot.behavior = (self._return_to or Patrol)(bot=self._bot)

        self._bot.deplacer(
            self._bot.x + randint(-1, 1),
            self._bot.y + randint(-1, 1)
        )
        self._bot.orienter((self._bot.orientation + self._super_rand()) % 4)
        self.count_search -= 1
