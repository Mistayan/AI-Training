import logging
from typing import List

from src.utils.state_machine.states import AbcState, BaseStateEnum


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
