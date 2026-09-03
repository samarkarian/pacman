from abc import ABC, abstractmethod
import pygame

class Scene(ABC):
    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> None:
        """Gère les entrées clavier propres à cet écran."""
        pass

    @abstractmethod
    def update(self) -> None:
        """Met à jour la logique interne (animations, déplacements)."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Affiche les éléments sur l'écran fourni."""
        pass