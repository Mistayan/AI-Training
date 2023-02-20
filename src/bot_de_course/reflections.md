# Runner Bot

The goal for this bot is to race against others.

The map, of variable size (default 30*30) contains a random number of cities (default 10)

Our bot spawns randomly near a game-chosen city

As usual, we use pytactx to visualize our progresses when our tests satisfies us.

# Class Diagram

```mermaid
classDiagram
    Agent <|-- DumbRunner
    DumbRunner <|-- SmarterRunner
    SmarterRunner --o ISolver
    SmarterRunner --* mapping
    ISolver --> TSP
    ISolver --> SmarterRunner
    ISolver --> TSPMap
    ISolver --> Dijkstra
    ISolver --> NN
    ISolver --> SVM
    
    class Agent{
    int x
    int y
    Dict jeu 
    +executerQuandActualiser()
    +actualiser()
    }
    
    class DumbRunner{
    List __path
    str __target
    Iter __next_action
    List __visited
    +go()
    #handle()
    }
    
    class SmarterRunner{
    @overwrite
    +go(Solver)
    }
    
    class ISolver{
        init(cities)
    }
   
    class mapping{
        cities_from_game_dict(Agent)
        distances(cities)
        map_cities(cities)
        get_city_pairs(cities)
    }
```
