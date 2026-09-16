from abc import abstractmethod
from typing import Tuple
import pygame
from Display_abstractmethods import Renderer


class HUDTextRenderer(Renderer):
    """Affiche un texte dynamique du HUD aux coordonnées écran données."""

    def __init__(self, pos: Tuple[int, int], game, label: str = "") -> None:
        super().__init__()
        self.posx: int = int(pos[0])
        self.posy: int = int(pos[1])
        self.game = game
        self.label: str = label
        self.font: pygame.font.Font | None = None

    def load_sprites(self, asset_size: int = 64) -> None:
        """Initialise la police selon la résolution choisie."""
        font_size = max(18, asset_size // 2)
        self.font = pygame.font.Font(None, font_size)

    @abstractmethod
    def get_text(self) -> str:
        """Chaque sous-classe implémente sa propre chaîne de caractères."""
        pass

    def render(self, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)) -> None:
        if self.font is None:
            self.load_sprites()

        if self.font:
            surface = self.font.render(self.get_text(), True, (255, 255, 255))
            screen.blit(surface, (self.posx + offset[0], self.posy + offset[1]))


class ScoreRenderer(HUDTextRenderer):
    def __init__(self, pos: Tuple[int, int], game) -> None:
        super().__init__(pos, game, label="SCORE: ")

    def get_text(self) -> str:
        return f"{self.label}{self.game.score:05d}"


class TimeRenderer(HUDTextRenderer):
    def __init__(self, pos: Tuple[int, int], game) -> None:
        super().__init__(pos, game, label="TIME: ")

    def get_text(self) -> str:
        time_val = max(0.0, float(self.game.time_left))
        return f"{self.label}{time_val:.0f}s"


class LevelRenderer(HUDTextRenderer):
    def __init__(self, pos: Tuple[int, int], game) -> None:
        super().__init__(pos, game, label="LEVEL: ")

    def get_text(self) -> str:
        return f"{self.label}{self.game.level_index + 1}"
