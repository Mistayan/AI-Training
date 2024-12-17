import logging

from typing_extensions import override

from src.bot_de_course.runner_agent import RunnerAgent
from src.bot_de_course.state_machine_config import RunnerStateEnum
from src.utils.algo.ISolver import ISolver
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.pytactx_utils import get_city_tuple
from src.utils.state_machine import EasyStateMachine


class SmartRunner(RunnerAgent):
    def __init__(self, myId: str = None, *args, **kwargs):
        print("init Smart Runner")
        super().__init__(myId, args=args, kwargs=kwargs)
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__log.addHandler(logging.NullHandler())
        self._dist = float('inf')

    @override
    def init_path(self, solver: ISolver.__class__ = None):
        self.__log.info(f"Using solver : {solver.__name__}")
        self._solver = solver or self._solver
        self._path, dist = solver(cities=self._cities).solve(start_index=0, back_to_start=True, visited=self._visited)
        self.set_target(get_city_tuple(self._path[0], self._cities)) # init path smart
        self.__log.info(f"Done processing paths\nFastest found: {self._path} with a total distance of {dist}")


if __name__ == '__main__':
    import coloredlogs

    coloredlogs.install(logging.DEBUG, propagate=False)
    agent = SmartRunner()
    agent.init_path(solver=HamiltonianSolver)
    agent_state_machine = EasyStateMachine(initial_state=RunnerStateEnum.ORIENTATE,
                                           states=[RunnerStateEnum.ORIENTATE.value,
                                                   RunnerStateEnum.DELIVER.value,
                                                   RunnerStateEnum.UNSTUCK.value,
                                                   ]
                                           )
    agent.set_state_machine(agent_state_machine)
    agent.go()
