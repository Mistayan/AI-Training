from abc import abstractmethod
from enum import Enum

import networkx as nx

import pytactx
from src.evaluation.bots import BotSerializer, Bot
from src.evaluation.fsm import StateMachine, State

"""
classDiagram
    class IState
    IState : *handle()

    class State
    State o-- StateMachine
    IState <|-- State
    State : -StateMachine context
    State : +setContext(context)
    State : +switch_state(state)

    class BaseState
    State <|-- BaseState
    State : #agent
    State : -color
    State : +handle()
    State : *onHandle()


    class SmartMove
    BaseState <|-- SmartMove
    PatrolState : +onHandle()

    class FollowState
    BaseState <|-- FollowState
    FollowState : -xEnemy
    FollowState : -yEnemy
    FollowState : +onHandle()


    class InvestigateState
    BaseState <|-- InvestigateState
    InvestigateState : +onHandle()

    class StateMachine
    StateMachine *-- State
    StateMachine : -actualState
    StateMachine : -states
    StateMachine : +add_state(state)
    StateMachine : +set_actual_state(state)
    StateMachine : +handle()


    class Agent
    Agent : +x
    Agent : +y
    Agent : +distance
    Agent : +orientation
    Agent : +tirer(trigger)
    Agent : +changerCouleur(r ,g ,b)
    Agent : +actualiser()
    Agent : +deplacer(x, y)
    Agent : +orienter(direction)
    Agent : *quandActualiser()
    Agent *-- StateMachine

    class StateMachineAgent
    Agent <|-- StateMachineAgent
    StateMachineAgent : +quandActualiser() 

"""


class StateEnum(Enum):
    """ An Enum is a classy way to put a name on a value"""
    SMART = 0  # "SmartState"
    FOLLOW = 1  # "FollowState"


class BaseState(State):
    def __init__(self, agent, color):
        self._agent = agent
        self.__color = color

    def handle(self):
        ...  # ADD common behaviour to execute whatever the state
        r, g, b = self.__color
        self._agent.changerCouleur(r, g, b)
        # self._agent.tirer((self._agent.distance != 0))
        self.onHandle()

    @abstractmethod
    def onHandle(self):
        ...


class DecisionState(BaseState):
    def __init__(self, agent):
        super().__init__(agent, (1, 1, 1))
        self.__Graph = nx.Graph()

    def onHandle(self):
        self._agent.orienter((self._agent.orientation + 1) % 4)

        self.__voisins = BotSerializer(self._agent)
        for bot in self.__voisins:
            bot: Bot
            print(bot.name, bot.score)


class FollowState(BaseState):
    def __init__(self, agent):
        super().__init__(agent, (255, 0, 0))
        self.__xEnnemy = 0
        self.__yEnnemy = 0

    def onHandle(self):
        # If agent on sight, save location
        if (self._agent.distance != 0):
            if self._agent.orientation == 0:
                self.__xEnnemy = self._agent.x + self._agent.distance
                self.__yEnnemy = self._agent.y
            elif self._agent.orientation == 1:
                self.__xEnnemy = self._agent.x
                self.__yEnnemy = self._agent.y - self._agent.distance
            elif self._agent.orientation == 2:
                self.__xEnnemy = self._agent.x - self._agent.distance
                self.__yEnnemy = self._agent.y
            elif self._agent.orientation == 3:
                self.__xEnnemy = self._agent.x
                self.__yEnnemy = self._agent.y + self._agent.distance
        # If not arrived at the last known location of the ennemy
        if not (self._agent.x == self.__xEnnemy and self._agent.y == self.__yEnnemy):
            self._agent.deplacer(self.__xEnnemy, self.__yEnnemy)
        else:  # Enemy not on site anymore
            # Be Smart on your next move
            self.switch_state(StateEnum.SMART.value)


class StateMachineAgent(pytactx.Agent):
    def __init__(self, myId):
        # create state machine
        self.__state_machine = StateMachine()  # register all states depending on pytactx context
        # it uses append(), the order matter
        self.__state_machine.add_state(DecisionState(self))
        self.__state_machine.add_state(FollowState(self))
        # set the initial state depending on pytactx context
        self.__state_machine.set_actual_state(StateEnum.SMART.value)
        # finally the super init
        _pwd = input('pass ? ')
        super().__init__(id=myId,
                         username="demo",
                         password=_pwd,
                         arena="demo",
                         server="mqtt.jusdeliens.com",
                         prompt=False,
                         verbose=False)
        self.__set_context_from_game()

    def __set_context_from_game(self):
        self.MAP_MAX_DISTANCE = (self.jeu[""] ** 2 + 10 ** 2) ** 0.5
        self.DIST_PENALTY = 13
        self.LIFE_PENALTY = 6
        self.AMMO_PENALTY = 2

    def on_update(self):
        self.__state_machine.handle()


if __name__ == '__main__':
    agent = StateMachineAgent("steed1")
    while agent.vie > 0:
        agent.actualiser()
