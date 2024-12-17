import logging
from abc import ABC, abstractmethod
from enum import Enum
from typing import List


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

class StateMachine:
    def __init__(self):
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__actual_state = None
        self.__context = None
        self.__refresh_next = False
        self.__states = []

    def set_context(self, context):
        self.__log.debug(f"Setting context to : {context}")
        self.__context = context

    def add_state(self, state: AbcState):
        self.__log.debug(f"Adding state {state} at {len(self.__states)}")
        state.set_context(self)
        self.__states.append(state)

    def set_actual_state(self, state: AbcState):
        self.__actual_state = state
        self.__refresh_next = True


    def handle(self):
        """Execute the actual state handle method"""
        self.__log.debug(f'Handling state : {self.__actual_state}')

        for state in self.__states:
            if isinstance(state, self.__actual_state):
                if self.__refresh_next:
                    state.refresh()
                    self.__refresh_next = False
                state.handle(self.__context)


class EasyStateMachine(StateMachine):
    def __init__(self, initial_state: BaseStateEnum, states: List[AbcState.__class__]):
        super().__init__()
        self.set_actual_state(initial_state.value)
        [self.add_state(new_state(self)) for new_state in states]
