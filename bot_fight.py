import pytactx
import pandas as pd

agent = pytactx.Agent("Stephen")
agent.changerCouleur(42, 42, 42)
print(agent.jeu)


def map_it():
    arr = pd.array(agent.voisins)
    print(arr)


while agent.vie > 0:
    map_it()
    agent.orienter((agent.orientation + 1) % 4)
    agent.publier("\\\\\\\Pas cool\\\\\\\\")
    print(agent.voisins)
    agent.tirer(True)
    agent.actualiser()
