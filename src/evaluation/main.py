from abc import abstractmethod, ABC
from enum import Enum

import networkx as nx

import pytactx
from src.bot_de_combat.behavior_correction import fsm
from src.evaluation.bots import BotSerializer, Bot
from src.utils.algo.evaluate_others import eval_fear_factor
from src.utils.my_maths import euclidean_distance


class StateEnum(Enum):
    """ An Enum is a classy way to put a name on a value"""
    SMART = 0  # "DecisionState"
    FOLLOW = 1  # "FollowState"


class BaseState(fsm.State, ABC):
    """ """

    def __init__(self, agent, color):
        super().__init__()
        self._agent = agent
        self.__color = color

    def handle(self):
        r, g, b = self.__color
        self._agent.changerCouleur(r, g, b)
        # self._agent.tirer((self._agent.distance != 0))
        self.onHandle()

    @abstractmethod
    def onHandle(self):
        ...


class DecisionState(BaseState):
    def __str__(self):
        return "DecisionState"

    def __init__(self, agent):
        super().__init__(agent, (1, 1, 1))
        self.__graph = nx.Graph()

    def onHandle(self):
        # dummy move
        self._agent.orienter((self._agent.orientation + 1) % 4)

        # map neighbors
        self.__voisins = BotSerializer(self._agent.voisins)
        for bot in self.__voisins:
            bot: Bot
            bot.set_score(eval_fear_factor(self._agent, bot))
            if not bot.distance:
                bot.set_distance(euclidean_distance(self._agent, bot))
            pos = (bot.x, bot.y)
            self.__graph.add_node(pos, score=bot.score, pos=pos)
            print(bot.name, bot.score)
        print("#" * 20, "Mapping Done")
        self.display_map()
        del self.__graph
        self.__graph = nx.Graph()


class FollowState(BaseState):
    def __str__(self):
        return "FollowState"

    def __init__(self, agent):
        super().__init__(agent, (255, 0, 0))
        self.__xEnnemy = 0
        self.__yEnnemy = 0

    def onHandle(self):
        # If agent on sight, save location
        ori = self._agent.orientation
        dist = self._agent.distance
        if dist != 0:
            if ori in (0, 2):
                self.__xEnnemy = self._agent.x - dist * (
                        ori - 1)
                self.__yEnnemy = self._agent.y
            elif ori in (1, 3):
                self.__xEnnemy = self._agent.x
                self.__yEnnemy = self._agent.y - dist * (
                        ori - 2)

        # If not arrived at the last known location of the ennemy
        if not (self._agent.x == self.__xEnnemy
                and self._agent.y == self.__yEnnemy):
            self._agent.deplacer(self.__xEnnemy, self.__yEnnemy)
        else:  # Enemy not on site anymore
            # Be Smart on your next move
            self.switch_state(StateEnum.SMART.value)


class StateMachineAgent(pytactx.Agent):
    """
    The agent holding possible states and context parameters
    """

    def __init__(self, myId: str):
        """
        :param myId: the name of your bot in arena
        """
        # create state machine
        self.__state_machine = fsm.StateMachine()

        # register all states depending on pytactx context
        self.__state_machine.add_state(DecisionState(self))
        self.__state_machine.add_state(FollowState(self))

        # set the initial state depending on pytactx context
        self.__state_machine.set_actual_state(StateEnum.SMART.value)
        # finally the super init
        _pwd = input('pass ? ')
        super().__init__(id=myId,
                         username="pytactx",
                         password=_pwd,
                         arena="Arena",
                         server="mqtt.jusdeliens.com",
                         prompt=False,
                         verbose=False)
        self.__set_context_from_game()

    def __set_context_from_game(self):
        self.MAP_MAX_DISTANCE = (self.jeu.get("gridColumns") ** 2 + self.jeu.get("gridRows") ** 2) ** 0.5

        # penalties represents the weight we put on the data to (depending on other contexts) evaluate efficiently different attributes
        # TODO: find ways to evaluate those
        self.DIST_PENALTY = 0.32
        self.LIFE_PENALTY = 0.55
        self.AMMO_PENALTY = 0.13

    def on_update(self):
        self.__state_machine.handle()


if __name__ == '__main__':
    agent = StateMachineAgent("stee2")
    while agent.vie > 0:
        agent.actualiser()
