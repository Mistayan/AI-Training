import random
import sys
from subprocess import Popen
from time import sleep

from src.bot_de_combat.Guard import Bot
from src.bot_de_combat.behavior.Behavior import Assist

NB_BOTS = 3
configs = {
    0: ["Guard", [(5, 2), (2, 5)]],
    1: ["Hunter", [(1, 1), (2, 5), (4, 10), (3, 3)]],
    2: ["Assist", None, "Stephen-1"],
}


def load_bot_config(conf_id: int = 0):
    return configs[conf_id]


def start_one_agent(num: int = 0, _type: str = "Guard", coords: list | str = None):
    """
    Guard : patrol on a small area around the given coords
    Watcher: patrol on a range of coords
    Inquisitor: patrol on random coords in order to find heretics
    Assist: stays near the given Bot-Name
    """
    agent = Bot(name=f"Stephen-{num or random.randint(1, 999)}")
    agent.changerCouleur(42, 42, 42)  # Inactive
    if isinstance(coords, str):
        agent.behavior = Assist(agent)
        agent.target = coords
    else:
        agent.path = coords if isinstance(coords, list) else [(5, 2), (2, 5)]
    agent.go()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(sys.argv)
        config = load_bot_config(int(sys.argv[1]))
        start_one_agent()
        exit()

    running = []
    for i in range(NB_BOTS):
        running.append(Popen(f"python run_pytactx_bot.py {i}".split()))

    try:
        for process in running:
            process.communicate()
    except KeyboardInterrupt:
        print("SHUTTING DOWN INSTANCES GRACEFULLY")
        _try = 5 * len(running)
        while running:
            process = running.pop()
            process.kill()
            sleep(0.2)
            if not _try:
                print("TAKING TOO LONG")
                process.terminate()
            elif not process.returncode:
                running.append(process)
