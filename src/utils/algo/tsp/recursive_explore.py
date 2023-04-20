import copy
import random

import matplotlib.pyplot as plt

import pytactx


def drawDataViz(x, y1, y2, labelY1='bruteforce', labelY2='random', axisX='👉x', axisY='👉y'):
    plt.scatter(x, y1, c='coral', label=labelY1)
    plt.scatter(x, y2, c='lightblue', label=labelY2)
    plt.legend()
    plt.title('Nuage de points avec Matplotlib')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('ScatterPlot_04.png')
    plt.show()


def distance(city1, city2):
    x1 = city1['x']
    y1 = city1['y']
    x2 = city2['x']
    y2 = city2['y']
    return math.sqrt(
        (x1 - x2) ** 2
        +
        (y1 - y2) ** 2
    )


# new_distance = np.linalg.norm(np.array(city_info['x'], city_info['y']) - np.array(next_city_info['x'], next_city_info['y'])
# Déterminer tous les itinéraires possibles en calculant leur distance cumulée
def explore(city, cities_remaining, route=None, distance_route=0):
    if route == None:
        route = []
    # Supprimer ville de villesRestantes
    cityInfo = cities_remaining.pop(city)
    # Ajouter ville à itinéraire
    route.append(city)
    # Répéter pour chaque ville dans villesRestantes
    for next_city_name, next_city_info in cities_remaining.items():
        cities_copy = copy.deepcopy(cities_remaining)
        routes_copy = copy.deepcopy(route)
        # Appeler la fonction explorer en passant :
        # - le nom de la ville voisine
        # - la copie de la liste villeRestantes
        # - la copie de la liste itinéraire
        explore(city, cities_copy, routes_copy, sum([distance_route, distance(cityInfo, next_city_info)]))
    # Si nombreVoisins est égal à 0
    if len(cities_remaining) == 0:
        # Actualisation du i et d itineraire min
        global iItineraireMin, dItineraireMin
        if dItineraireMin > distance_route:
            iItineraireMin = distance_route
            dItineraireMin = routes_copy
        # Ajouter la liste itinéraire locale à la liste globale itinérairesPossibles
        possible_routes.append(routes_copy)


if __name__ == '__main__':
    agent = pytactx.Agent(id="🧑‍🚀Mist-1", arena="pytactx", username="demo")
    # Créer un dictionnaire global cities_graph
    cities_graph = copy.deepcopy(agent.jeu["dests"])
    # Créer une liste globale itinérairesPossibles vide
    possible_routes = []
    iItineraireMin = None
    dItineraireMin = float('inf')
    explore("0", cities_graph)
    print(f"Routes possibles :{len(possible_routes)}")

    # déterminer l'itinéraire à empreinter
    itineraire = None
    if (iItineraireMin != None):
        itineraire = possible_routes[iItineraireMin]
    else:
        itineraire = list(cities_graph.keys())
        itineraire.remove("0")
        random.shuffle(itineraire)
        itineraire.append("0")
        print(itineraire)
    dItineraireMin
    # Pour chaque ville de la liste itinéraire
    for ville in itineraire:
        agent.changer
        # On repète le déplacement de notre agent jusqu'à arriver à cette ville
        while agent.derniereDestinationAtteinte != ville:
            agent.deplacerVers(ville)  # deplacer l'agent vers la ville
            agent.orienter((agent.orientation + 1) % 4)
            agent.actualiser()
