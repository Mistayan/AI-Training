from subprocess import Popen
from time import sleep

if __name__ == '__main__':
    python_venv = "C:/tmp/cours/IA/venv/Scripts/python.exe"
    run = ["smarter_runner2.py", "smarter_runner.py", "smarter_runner3.py"]
    running = []
    for _exec in run:
        running.append(Popen(f"{python_venv} {_exec}".split(" ")))

    try:
        while running:
            sleep(1)
    except KeyboardInterrupt as ex:
        print(ex)
        for run in running:
            run.kill()
