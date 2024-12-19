import logging

from pytactx import env
from src.bot_de_course.smart_runner import SmartRunner
from src.bot_de_course.state_machine_config import RunnerStateEnum
from src.utils.algo.tsp.tsp_hamilton import HamiltonianSolver
from src.utils.pytactx.pytactx_utils import get_logging_level
from src.utils.state_machine import EasyStateMachine

if __name__ == '__main__':
    import coloredlogs

    coloredlogs.install(get_logging_level(), propagate=False)

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
