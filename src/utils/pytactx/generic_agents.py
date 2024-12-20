import copy
import logging
from abc import ABC, abstractmethod
from time import time, sleep
from typing import Tuple, Any

from pytactx import env
from pytactx.agent import Agent
from src.utils.state_machine import BaseStateEnum, StateMachine


class BaseAgent(Agent):
    """
    An Agent connected to the arena
    """

    def __init__(self, id: str):
        """
        Initialise the Agent and connect to the server.
        Then, prepare the property __state_machine, that will hold the StateMachine, controlling the Agent's behaviors.

        Do not forget to use `set_state_machine(StateMachine)` for it to work !

        Args:
            (optional) id: the name of the agent in the arena's ACLs
                            should be defined in .env file. But this is a simple way to override it.
        """
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.info("Connecting ...")
        super().__init__(id or env.ROBOTID,
                         env.ARENA,
                         env.USERNAME,
                         env.PASSWORD,
                         env.BROKERADDRESS,
                         env.BROKERPORT,
                         env.VERBOSITY)
        self.__log.info("OK")

    def _onUpdated(self, *args, **kwargs):
        """ Every time self.update() is used !
        Signals the state machine to handle its current state to perform its action
        """
        # add your code here !
        self.lookAt((self.dir + 1) % 4) # exemple

        # use super() at the end.
        super()._onUpdated(*args, **kwargs)
        # any code below might be overwritten on next loop

    def go(self):
        while self.life > 0 and self.isConnectedToArena():
            self.update(False)
            sleep(0.1)


class StateAgent(BaseAgent, ABC):
    """
    An Agent having a StateMachine to control the behaviors.

    This way, it is easier to maintain each state and their transitions.

    It will also be more maintainable, since you will want to improve your bot's capabilities as you go.
    """

    def __init__(self, id: str):
        """
        Initialise the Agent and connect to the server.
        Then, prepare the property __state_machine, that will hold the StateMachine, controlling the Agent's behaviors.

        Do not forget to use `set_state_machine(StateMachine)` for it to work !

        Args:
            (optional) id: the name of the agent in the arena's ACLs
                            should be defined in .env file. But this is a simple way to override it.
        """
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.info("Connecting ...")
        super().__init__(id)
        self.__log.info("OK")
        self.__state_machine: StateMachine = None

    def set_state_machine(self, state_machine: StateMachine):
        """
        Defines the StateMachine that will be used control the Agent's behaviors.
        This StateMachine must be initialised with an initial state, and some behaviors (States) implementations.

        Initialises the context for the state machine. ( it will be passed to states, using handle() method )
        """
        if not state_machine or not isinstance(state_machine, StateMachine):
            raise ValueError("state_machine must be a StateMachine")
        self.__log.debug("Setting state Machine")
        self.__state_machine = state_machine
        state_machine.set_context(self)

    # @measure_perf
    def _onUpdated(self, *args, **kwargs):
        """ Every time self.update() is used !
        Signals the state machine to handle its current state to perform its action
        """
        self.__state_machine.handle()
        super(Agent)._onUpdated(*args, **kwargs)


class TargetAgent(StateAgent, ABC):
    """
    A "Target Agent" means that the agent you are going to build has location-based behaviors
    Use this class for TSP, Labyrinths, moving to specified coordinates
    """

    def __init__(self, id: str = None):
        self.__log = logging.getLogger(self.__class__.__name__)
        super().__init__(id)
        self.__current_target: Tuple[str, int, int] = None
        self.__visited = {}

    @property
    def current_target(self) -> Tuple[str, int, int]:
        """
        :returns: the current target as a Tuple
        """
        return copy.deepcopy(self.__current_target)

    def set_target(self, target: Tuple[str, int, int]):
        """ Set the target for the agent.
        This value will be used by certain states to perform actions
        """

        if target and target != self.__current_target:
            self.__log.debug(f"Setting target to {target}")
            self.__current_target = target

    def add_visited(self, name: str):
        """ Once visited, save the city for future use """
        self.__visited.setdefault(name, time())

    @property
    @abstractmethod
    def next_action(self) -> Any:
        """
        Define your method to select the next action to be performed
        Save the result in your customized class
        """
        ...
