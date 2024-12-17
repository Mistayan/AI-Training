import copy
import logging
from abc import ABC, abstractmethod
from time import time
from typing import Tuple

from pytactx import env
from pytactx.agent import Agent
from src.utils.state_machine import StateMachine, BaseStateEnum


class StateAgent(Agent, ABC):
    """
    An Agent having a StateMachine to control the behaviors.

    This way, it is easier to maintain each state and their transitions.

    It will also be more maintainable, since you will want to improve your bot's capabilities as you go.
    """

    def __init__(self, id: str):
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
        if not state_machine or not isinstance(state_machine, StateMachine):
            raise ValueError("state_machine must be a StateMachine")
        self.__log.debug("Setting state Machine")
        self.__state_machine = state_machine
        state_machine.set_context(self)

    def force_state(self, state: BaseStateEnum):
        self.__log.debug("Setting state Machine")
        self.__state_machine.set_actual_state(state.value)
        self._handle_loop()

    def _handle_loop(self):
        self.__state_machine.handle()


class TargetAgent(StateAgent, ABC):
    """
    A "Target Agent" means that the agent you are going to build has location-based behaviors
    Use this class for TSP, Labyrinths, moving to specified coordinates
    """

    def __init__(self, id: str = None, *args, **kwargs):
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
    def next_action(self):
        """
        Define your method to select the next action to be performed
        Save the result in your customized class
        """
        ...

