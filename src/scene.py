from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Optional
import pygame


class SceneID(Enum):
    """Identifiers of the scenes requested from the game loop."""

    NONE = auto()
    MENU = auto()
    GAME = auto()
    QUIT = auto()
    GAMEOVER = auto()
    NAME = auto()


class Scene(ABC):
    """A game screen: handles its own input, logic and drawing."""

    @abstractmethod
    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        """Handle the keyboard input of this screen.

        Args:
            event: pygame event.

        Returns:
            The scene to open, or None.
        """
        pass

    @abstractmethod
    def update(self) -> Optional[SceneID]:
        """Update the internal logic (animations, movement).

        Returns:
            The scene to open, or None.
        """
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface) -> None:
        """Draw the elements on the given screen.

        Args:
            screen: surface to draw on.
        """
        pass
