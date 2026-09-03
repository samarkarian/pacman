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

class GameScene(Scene):
    def __init__(self, mazegen, asset_size: int = 64) -> None:
        self.asset_size = asset_size
        self.mazedisplayer = MazeDisplayer(mazegen, asset_size)
        self.player_x = 0
        self.player_y = 0
        self.entities = []  # Peuplé par la factory

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_y += 50
            elif event.key == pygame.K_DOWN:
                self.player_y -= 50
            # ...

    def update(self) -> None:
        pass  # Logique de mouvement des fantômes, etc.

    def render(self, screen: pygame.Surface) -> None:
        offset = (self.player_x, self.player_y)
        self.mazedisplayer.render(screen, offset)
        for e in self.entities:
            e.render(screen, offset)