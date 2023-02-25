from subprocess import Popen
from time import sleep

if __name__ == '__main__':
    python_venv = "C:/tmp/cours/IA/venv/Scripts/python.exe"
    run = ["smarter_runner2.py", "smarter_runner.py", "smarter_runner3.py"]

    running = []
    for executable in run:
        cmd = f"{python_venv} {executable}"
        running_script = Popen(cmd.split(" "))  # Execute la commande dans une tache de fond
        running.append(running_script)  # stock le 'pid' de la tache de fond, afin de pouvoir interagir avec
        # sans cette étape, si votre programme ne finit jamais, il faut redémarrer votre machine pour l'arrêter !

    try:
        while running:  # temps qu'au moins un script tourne, on attend
            sleep(1)
    except KeyboardInterrupt as ex:  # en cas d'interruption utilisateur, arrêter les programmes gently
        print(ex)
        for run in running:
            run.kill()
