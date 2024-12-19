import logging
from typing import List

from src.utils.state_machine.states import AbcState, BaseStateEnum


class StateMachine:
    """
    Machine à état finie (classique).
    Ce mécanisme nous permet de facilement gérer les `comportements` que l'on souhaite `implémenter` dans notre logique.

    Exemple d'utilisation :
    """
    def __init__(self):
        self.__log = logging.getLogger(self.__class__.__name__)
        self.__actual_state = None
        self.__context = None
        self.__states = []

    def set_context(self, context):
        """ Donne un context, sur lequel les états de la machine pourront intéragir. ( voir AbcState.handle() )"""
        self.__log.debug(f"Setting context to : {context.__class__.__name__}")
        self.__context = context

    def add_state(self, state: AbcState):
        """
        Ajoute un état au StateMachine, ajoutant de nouvelles possibilités de transition.
        Cet état aura accès au contexte transmit par l'application, et doit contenir ses transitions.
        """
        self.__log.debug(f"Adding state {state} at {len(self.__states)}")
        state.set_context(self)
        self.__states.append(state)

    def set_actual_state(self, state: AbcState):
        """ Change l'état actuel, à activer lors du prochain cycle ( utilisation de handle() ) """
        self.__actual_state = state

    def handle(self):
        """ Execute the `actual state`'s handle method, passing the context for it to act on, defined at __init__() """
        self.__log.debug(f'StateMachine: Handling state : {self.__actual_state}')

        for state in self.__states:
            if isinstance(state, self.__actual_state):
                state.handle(self.__context)


class EasyStateMachine(StateMachine):
    """
    Classe simplifiant l'utilisation de StateMachine,
     en créant un constructeur initialisant l'intégralité de la machine à états.
    """
    def __init__(self, initial_state: BaseStateEnum, states: List[AbcState.__class__]):
        super().__init__()
        self.set_actual_state(initial_state.value)
        [self.add_state(new_state(self)) for new_state in states]
