from src.utils.orientation import Orientation
from src.utils.pytactx_utils import get_orientation_form_coord_deltas, TargetAgent
from src.utils.state_machine import BaseStateEnum, AbcState


class DeliverState(AbcState):
    def handle(self, agent: TargetAgent):
        """ Move to target.
        If arrived at requested location, find next target to go to.
        Save current target in visited, in case path changes [fail-safe]"""
        self._log.debug(f"Handle :\n"
                        f"Last checkpoint : {agent.lastChecked}, Current objective : {agent.current_target}")
        # If already on desired location, or the game tells us that we crossed a checkpoint, then do next action
        name, x, y = agent.current_target
        if not self.wait:
            agent.moveTowards(x, y)
        if (agent.lastChecked == name or
                (agent.x == x and agent.y == y)):
            self._log.info(f"ARRIVED @{name, x, y}")
            agent.add_visited(name)
            agent.set_target(agent.next_action)
            self.switch_state(RunnerStateEnum.ORIENTATE.value)


class OrientateState(AbcState):
    def handle(self, agent: TargetAgent):
        """
        Orient Agent to desired location.
        Useful if you are near a wall; or facing the opposite direction you plan to move to, which might take longer
        """
        n, x, y = agent.current_target
        self._log.debug(f"Orientate @({n}, {x}, {y})")
        orientation = get_orientation_form_coord_deltas(agent.x, agent.y, x, y)
        if agent.dir == orientation.value:
            self.switch_state(RunnerStateEnum.DELIVER.value)
        elif not self.wait:
            self._log.info(f"From given coords, look @{Orientation(orientation).name}")
            agent.lookAt(orientation.value)
            self.performed()
        else:
            ...


class UnstuckState(AbcState):
    def handle(self, agent: TargetAgent):
        """
        In order to un-stuck ourselves, we are going to go one tile away, then turn back and go back to initial tile
        """
        # from orientation, calculate the delta to apply to moveTowards(dx, dy)
        name, x, y = agent.current_target
        dx, dy = None, None
        if not self.wait and (agent.x == x and agent.y == y):
            match Orientation(agent.dir % 4):
                case Orientation.NORTH: dx, dy = (agent.x - 1, agent.y)
                case Orientation.SOUTH: dx, dy = (agent.x + 1, agent.y)
                case Orientation.EAST: dx, dy = (agent.x, agent.y + 1)
                case Orientation.WEST: dx, dy = (agent.x, agent.y - 1)
            agent.moveTowards(dx, dy)
            self.performed()
        else:
            self.switch_state(RunnerStateEnum.DELIVER.value)

class RunnerStateEnum(BaseStateEnum):
    DELIVER = DeliverState      # Standard behavior : you have to deliver all your good to finish.
    ORIENTATE = OrientateState  # Before moving, make sure you are facing the right direction
    UNSTUCK = UnstuckState      # Since sometimes we spawn on "Start", it can get stuck. Avoid being stuck.
