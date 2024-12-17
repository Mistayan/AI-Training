from src.utils.state_machine import BaseStateEnum, AbcState


class FighterStateEnum(BaseStateEnum):
    PATROL: 0  # "PatrolState"
    FOLLOW: 1  # "FollowState"
    INVESTIGATE: 2  # "InvestigateState"


class PatrolState(AbcState):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        # if agent detected
        if (...):
            # switch to FollowState
            self.switch_state(FighterStateEnum.INVESTIGATE)
        # otherwise
        else:
            # Move agent around a patrol point
            ...


class FollowState(AbcState):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        ...


class InvestigateState(AbcState):
    def __init__(self, context):
        super().__init__(context)

    def handle(self):
        ...
