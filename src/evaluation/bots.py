class BotSerializer:
    """
     Instanciate ennemies as 'dummy' bots (no action possible)
    """

    def __init__(self, voisins: dict):
        """

         dict from agent.voisins
         """
        self.__bots = []
        for name in voisins:
            self.__bots.append(Bot(name, voisins[name]))

    def __iter__(self):
        return iter(self.__bots)


class Bot:
    """
     {name: "Name",
        {'x': 6, 'y': 5, 'dir': range(1, 4), 'ammo': range(0, 100), 'life': range(0, 100), 'fire': bool, 'd': int}}
    """

    def __init__(self, name: str, player_dict: dict):
        self.name = name
        self.vie = player_dict.get('life')
        self.x = player_dict.get('x')
        self.y = player_dict.get('y')
        self.coords = (self.x, self.y)
        self.orientation = player_dict.get('dir')
        self.ammo = player_dict.get('ammo')
        self.fire = player_dict.get('fire')
        self.distance = player_dict.get('d')  # without obstacles, OK
        self.score = float('1.0')

    def set_score(self, score: float):
        self.score = score

    def set_distance(self, distance: float):
        self.distance = distance
