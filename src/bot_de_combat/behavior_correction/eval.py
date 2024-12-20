class DummyBot:
    """
    DummyBot is a simplified representation (Serialization) of a `Bot` `Arena`
    It holds these properties : name, distance, vie, ammo
    """
    def __init__(self, name: str, distance: int, life: int, ammo: int):
        self.name = name
        self.distance = distance
        self.life = life
        self.ammo = ammo


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
            self.__bots.append(Enemy(name, voisins[name]))

    def __iter__(self):
        return iter(self.__bots)


class Enemy(DummyBot):
    """
    Advanced representation (Serialisation) of a DummyBot, holding additional properties to be used:
    x: the x position of the bot in the `Arena`
    y: the y position of the bot in the `Arena`
    fire: is the Enemy firing right now ? (occupied)
    fear_factor: how fearful should we be of that enemy ?

     {name: "Name",
    {'x': 6, 'y': 5, 'dir': range(1, 4), 'ammo': range(0, 100), 'life': range(0, 100), 'fire': bool, 'd': int}}
        """

    def __init__(self, name: str, player_dict: dict):
        super().__init__(name, player_dict.get('d'), player_dict.get('life'), player_dict.get('ammo'))
        self.x = player_dict.get('x')
        self.y = player_dict.get('y')
        self.fire = player_dict.get('fire')
        self.fear_factor = float('1.0') # default value : strong fear, avoid


######################################


def smart_eval(our_bot, ref_bot):
    """ Evaluate the fear_factor for each bot"""
    # decreases if bot is far away:
    # We may encounter random events that could harm us
    dist_factor = 1 / ref_bot.distance * our_bot.DIST_PENALTY

    # penalize if bot has low life
    life_factor = (ref_bot.life / 100) * our_bot.LIFE_PENALTY

    # penalize if bot has low ammo
    ammo_factor = (ref_bot.ammo / 100) * our_bot.AMMO_PENALTY

    fear_factor = ((our_bot.ammo / 100) * ammo_factor + (our_bot.life / 100) * life_factor + dist_factor) / 3
    return fear_factor / 8  # After observations, max factor is 8  #TODO find a better way...


if __name__ == "__main__":
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
