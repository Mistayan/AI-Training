from src.bot.behavior_correction.all_in_one import StateEnum, PatrolState, InvestigateState, FollowState


class StateMachine:
    def __init__(self):
        self.__actual_state = StateEnum.PATROL.value
        self.__states = [PatrolState(self), InvestigateState(self), FollowState(self)]

    # LUT: look Up table : comment faire le lien entre actual_state et l'instance du state correspondant ?

    def handle(self):
        """Execute the actual state handle method"""
        print(f'Handling state : {self.__actual_state}')
        self.__states[self.__actual_state].handle()

    def set_actual_state(self, state):
        self.__actual_state = state.value