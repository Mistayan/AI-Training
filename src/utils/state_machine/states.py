import logging
from abc import ABC, abstractmethod
from enum import Enum


class BaseStateEnum(Enum):
    ...


class IState(ABC):
    @abstractmethod
    def handle(self, *args):
        """
        What operations does this state have to perform in order to accomplish its objective ?
        Implement this method in a named State(BaseState)
        """
        ...


class AbcState(IState, ABC):
    """
    To be used in a StateMachine
    Must be overridden to implement handle method.
    """

    def __init__(self, context):
        self._log = logging.getLogger(self.__class__.__name__)
        self.__context = context
        self.__wait = False

    def switch_state(self, state):
        self.__context.set_actual_state(state)

    def set_context(self, other):
        self.__context = other

    @property
    def wait(self):
        return self.__wait

    def refresh(self):
        self.__wait = False

    def performed(self):
        self.__wait = True
