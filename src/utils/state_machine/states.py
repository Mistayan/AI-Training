import logging
from abc import ABC, abstractmethod
from enum import Enum


class BaseStateEnum(Enum):
    """ Base Enum for States to be."""
    ...


class IState(ABC):
    """Base methods that your Implementations of `IState` must implement"""
    @abstractmethod
    def handle(self, *args):
        """
        What operations does this state have to perform in order to accomplish its objective ?
        Implement this method in a named State(BaseState)
        """
        ...


class AbcState(IState, ABC):
    """
    To be used in a StateMachine
    Must be overridden to implement handle method.
    """

    def __init__(self, context):
        """
        Args:
            context: Le contexte (Agent dans notre cas) sur lequel notre state machine agira.
            Les états contenus dans le State Machine effectueront des actions sur ce contexte. (dans votre implémentation  de handle())
        """
        super().__init__()
        self._log = logging.getLogger(self.__class__.__name__)
        self.__context = context

    def switch_state(self, state):
        """
        Demande au context (State Machine) de changer d'état.
        C'est à l'état de base de faire cette demande, afin de pouvoir changer de comportement.
        """
        self._log.debug(f"Switching state to : {state}")
        self.__context.set_actual_state(state)

    def set_context(self, other):
        """ Défini le context (State Machine) lié à l'état, afin de pouvoir demander à celui-ci """
        self._log.debug(f"Setting {self.__class__.__name__}'s context to {other.__class__.__name__}")
        self.__context = other


class MemoryState(AbcState, ABC):
    """
    Ajoute la possibilité de rester en attente d'un evenement 'refresh',
    une fois que l'action a été envoyée au serveur de jeu.
    Cela nous permet d'économiser les ressources de traitements locaux, comme sur le serveur.
    """
    def __init__(self, context):
        super().__init__(context)
        self.__wait = False

    @property
    def wait(self):
        """
        Le State est-il en attente d'un refresh ?
        Implémentez la logique dans le handle() de votre état, pour savoir si il est en attente.
        """
        return self.__wait

    def refresh(self):
        """
        Informe l'état qu'il devra effectuer un action lors du prochain cycle
        Implémentez la logique dans le handle() de votre état, pour contrôler l'attente de l'état.
        """
        self._log.info("Refreshing. Next action will be performed")
        self.__wait = False

    def performed(self):
        """
        Implémentez la logique dans le handle() de votre état, pour le mettre en attente.
        """
        self._log.debug("Performed action, awaiting refresh")
        self.__wait = True

    def switch_state(self, new_state):
        # Ensure the next action will be performed. Since we leave the current state, we except next state's switch to perform its actions.
        self.refresh()
        super().switch_state(new_state)
