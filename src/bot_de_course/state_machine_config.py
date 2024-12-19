from src.utils.pytactx.orientation import Orientation
from src.utils.pytactx.generic_agents import TargetAgent
from src.utils.pytactx.pytactx_utils import get_orientation_form_coord_deltas
from src.utils.state_machine import BaseStateEnum, MemoryState, AbcState


class DeliverState(AbcState):
    def handle(self, agent: TargetAgent):
        """ Move to target.
        If arrived at requested location, find next target to go to.
        Save current target in visited, in case path changes [fail-safe]"""
        # If arrived at desired location, the game tells us that we crossed a checkpoint, then we can do the next action
        n, x, y = agent.current_target
        at_location = (agent.x == x and agent.y == y)
        self._log.debug(f"Deliver @({n}, {x}, {y}) - dir:{agent.dir} - at_location:{at_location}")
        # START stuck prevention
        if at_location and n in ("START", "0") and agent.lastChecked == "":
            return self.__handle_stuck()

        elif at_location and n == agent.lastChecked:
            return self.__handle_arrived(agent, n)

        else:
            self._log.info(f"Moving to {n}")
            agent.moveTowards(x, y)
            return


    def __handle_stuck(self):
        self._log.info("Stuck on START !")
        self.switch_state(RunnerStateEnum.UNSTUCK.value)

    def __handle_arrived(self, agent, current_target_name):
        self._log.info(f"ARRIVED @{agent.current_target} !")
        agent.add_visited(current_target_name)
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
            self._log.debug(f"Now facing @{n} -> {orientation.name}")
            return self.switch_state(RunnerStateEnum.DELIVER.value)
        else:
            self._log.info(f"Turning @{n} -> {orientation.name}")
            agent.lookAt(orientation.value)
            return


class UnstuckState(AbcState):
    def handle(self, agent: TargetAgent):
        """
        In order to un-stuck ourselves, we are going to go one tile away, then turn back and go back to initial tile
        """
        # from orientation, calculate the delta to apply to moveTowards(dx, dy)
        n, x, y = agent.current_target
        at_location = (agent.x == x and agent.y == y)

        if not at_location:
            self._log.info("Now Unstuck.")
            return self.switch_state(RunnerStateEnum.ORIENTATE.value)
        else:
            self._log.info("Performing actions to unstuck...")
            dx, dy = Orientation(agent.dir).get_coords_delta()
            agent.moveTowards( agent.x + dx, agent.y + dy)
            return


class RunnerStateEnum(BaseStateEnum):
    DELIVER = DeliverState  # Standard behavior : you have to deliver all your good to finish.
    ORIENTATE = OrientateState  # Before moving, make sure you are facing the right direction
    UNSTUCK = UnstuckState  # Since sometimes we spawn on "Start", it can get stuck. Avoid being stuck.
