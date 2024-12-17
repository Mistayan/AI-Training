from abc import ABC, abstractmethod


class IState(ABC):
    """ An IFace is an empty shell. Its only purpose is to define a standard structure for every children """

    @abstractmethod
    def handle(self):
        """ Abstract method to enforce children implementing this"""
        ...


class State(IState, ABC):
    """
    Base State class.
    defines standard actions for specific children states
    """

    def __init__(self):
        self.__context = None

    def setContext(self, context):
        self.__context = context

    def switch_state(self, state: int):
        self.__context.set_actual_state(state)


class StateMachine:
    def __init__(self):
        self.__actual_state = 0
        self.__states = []

    def add_state(self, state: State):
        print(f"Adding state {state} at {len(self.__states)}")
        state.setContext(self)
        self.__states.append(state)

    def set_actual_state(self, state: int):
        self.__actual_state = state

    def handle(self):
        """Execute the actual state handle method"""
        print(f'Handling state : {self.__actual_state}')
        self.__states[self.__actual_state].handle()
