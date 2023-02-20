from enum import Enum


# Bonjour à tous

class StateEnum(Enum):
    PATROL: 0  # "PatrolState"
    FOLLOW: 1  # "FollowState"
    INVESTIGATE: 2  # "InvestigateState"


class IState:
    def handle(self):
        ...


class State(IState):
    def __init__(self, context):
        self.__context = context

    def switch_state(self, state):
        self.__context.set_actual_state(state)


class PatrolState(State):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        # if agent detected
        if (...):
            # switch to FollowState
            self.switch_state(StateEnum.INVESTIGATE)
        # otherwise
        else:
            # Move agent around a patrol point
            ...


class FollowState(State):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        ...


class InvestigateState(State):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        ...


class StateMachine:
    def __init__(self):
        self.__actual_state = StateEnum.PATROL.value
        self.__states = [PatrolState(self), InvestigateState(self), FollowState(self)]

    # LUT: look Up table : comment faire le lien entre actual_state et l'instance du state correspondant ?

    def handle(self):
        """Execute the actual state handle method"""
        self.__states[self.__actual_state].handle()

    def set_actual_state(self, state):
        self.__actual_state = state.value

# camelCase
# snake_case <3
# PascalCase pascal c'est camel + maj au debut
# kebab-case
# UPPER_CASE

# QUESTIONS
# pourquoi passer par une enum et pas juste = PatrolState() ? => l'allocation dynamique apporte des potentielles erreurs
