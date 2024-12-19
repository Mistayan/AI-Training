import copy
import logging
from abc import ABC, abstractmethod
from time import time
from typing import Tuple, Any

from pytactx import env
from pytactx.agent import Agent
from src.utils.state_machine import BaseStateEnum, StateMachine


class StateAgent(Agent, ABC):
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
        super().__init__(id or env.ROBOTID,
                         env.ARENA,
                         env.USERNAME,
                         env.PASSWORD,
                         env.BROKERADDRESS,
                         env.BROKERPORT,
                         env.VERBOSITY)
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

    def force_state(self, state: BaseStateEnum):
        """
        Sets the specified state of the state machine. This method updates the current
        state of the state machine to the provided state and invokes the handler loop
        after the transition, ensuring the requested action immediately executes.
        """
        self.__log.debug("Setting state Machine")
        self.__state_machine.set_actual_state(state.value)
        self._handle_loop()

    def _handle_loop(self):
        """ Signals the state machine to handle its current state to perform its action """
        self.__state_machine.handle()


class TargetAgent(StateAgent, ABC):
    """
    A "Target Agent" means that the agent you are going to build has location-based behaviors
    Use this class for TSP, Labyrinths, moving to specified coordinates
    """

    def __init__(self, id: str = None):
        self.__current_target: Tuple[str, int, int] = None
        self.__visited = {}
        super().__init__(id)

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
            print(f"Setting target {target}")
            self.__current_target = target

    def add_visited(self, name: str):
        """ Once visited, save the city for future use """
        self.__visited.setdefault(name, time() - self.game.get("t", 0))

    @property
    @abstractmethod
    def next_action(self) -> Any:
        """
        Define your method to select the next action to be performed
        Save the result in your customized class
        """
        ...

