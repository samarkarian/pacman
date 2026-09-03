from abc import ABC, abstractmethod
from typing import Optional
import pygame


from enum import Enum, auto


class SceneID(Enum):
    NONE = auto()
    MENU = auto()
    GAME = auto()
    QUIT = auto()


class Scene(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        """Gère les entrées clavier propres à cet écran."""
        pass

    @abstractmethod
    def update(self) -> Optional[SceneID]:
        """Met à jour la logique interne (animations, déplacements)."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Affiche les éléments sur l'écran fourni."""
        pass