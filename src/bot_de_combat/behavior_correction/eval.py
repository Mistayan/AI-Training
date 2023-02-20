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
        self.vie = player_dict.__getitem__('life')
        self.x = player_dict.__getitem__('x')
        self.y = player_dict.__getitem__('y')
        # self.coords = (self.x, self.y)
        self.ammo = player_dict.__getitem__('ammo')
        self.fire = player_dict.__getitem__('fire')
        self.distance = player_dict.__getitem__('d')  # without obstacles, OK
        self.fear_factor = float('1.0')

    def __set_score(self, fear_factor: float):
        self.fear_factor = fear_factor


######################################


def smart_eval(our_bot, ref_bot):
    """ Evaluate the fear_factor for each bot"""
    # ecreases if bot is far away:
    # We may encounter random events that could harm us
    dist_factor = 1 / ref_bot.distance * our_bot.DIST_PENALTY

    # penalize if bot has low life
    life_factor = (ref_bot.vie / 100) * our_bot.LIFE_PENALTY

    # penalize if bot has low ammo
    ammo_factor = (ref_bot.ammo / 100) * our_bot.AMMO_PENALTY

    fear_factor = ((our_bot.ammo / 100) * ammo_factor + (our_bot.vie / 100) * life_factor + dist_factor) / 3
    return fear_factor / 8  # After observations, max factor is 8  #TODO find a better way...


if __name__ == "__main__":
    class DummyBot:
        def __init__(self, name: str, distance: int, vie: int, ammo: int):
            self.name = name
            self.distance = distance
            self.vie = vie
            self.ammo = ammo


    class DummyAgent(DummyBot):
        def __init__(self, name: str, vie: int, ammo: int):
            super().__init__(name, 0, vie, ammo)

        MAP_MAX_DISTANCE = (11 ** 2 + 11 ** 2) ** 0.5

        # penalties represents the weight we put on the data to (depending on other contexts) evaluate efficiently different attributes
        # TODO: find ways to evaluate those
        DIST_PENALTY = 13 / MAP_MAX_DISTANCE
        LIFE_PENALTY = 6
        AMMO_PENALTY = 2


    my_dummy_bot = DummyAgent(name="me", vie=100, ammo=100)
    print("# Evaluating full-life, full-ammo with distance variance")
    print("Contact : ", smart_eval(my_dummy_bot, DummyBot("1", 1, 100, 100)))
    print("real-close : ", smart_eval(my_dummy_bot, DummyBot("2", 3, 100, 100)))
    print("mid-max range", smart_eval(my_dummy_bot, DummyBot("3", 5, 100, 100)))
    print("2/3 max : ", smart_eval(my_dummy_bot, DummyBot("4", 7, 100, 100)))
    print("Far", smart_eval(my_dummy_bot, DummyBot("5", 9, 100, 100)))
    print("...on the other edge...", smart_eval(my_dummy_bot, DummyBot("6", 11, 100, 100)))

    print("# Evaluating easy preys factor, full ammunition, health variance")
    print("Hard target: ", smart_eval(my_dummy_bot, DummyBot("1", 10, 100, 100)))
    print("Hard-- target: ", smart_eval(my_dummy_bot, DummyBot("2", 10, 80, 100)))
    print("Medium-HARD++: ", smart_eval(my_dummy_bot, DummyBot("3", 10, 60, 100)))
    print("Medium-Hard target, lot of ammunition: ", smart_eval(my_dummy_bot, DummyBot("4", 10, 20, 100)))
    print("Easy target, lot of ammunition: ", smart_eval(my_dummy_bot, DummyBot("5", 11, 10, 100)))

    print("# Evaluating ammo_requirements, medium-health, medium-range, ammo variance")
    print("", smart_eval(my_dummy_bot, DummyBot("1", 5, 50, 100)))
    print("", smart_eval(my_dummy_bot, DummyBot("2", 5, 50, 80)))
    print("", smart_eval(my_dummy_bot, DummyBot("3", 5, 50, 60)))
    print("", smart_eval(my_dummy_bot, DummyBot("4", 5, 50, 40)))
    print("", smart_eval(my_dummy_bot, DummyBot("5", 5, 50, 20)))
    print("", smart_eval(my_dummy_bot, DummyBot("6", 5, 50, 0)))
