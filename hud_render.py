from abc import abstractmethod
from typing import Tuple
from game import Game
import pygame
from display_abstractmethods import Renderer
from sprite_cache import load_image


class HUDTextRenderer(Renderer):
    """Dynamic HUD text drawn at the given screen position."""

    def __init__(self, pos: Tuple[int, int], game: Game,
                 label: str = "") -> None:
        """Store the position, the game and the label."""
        super().__init__()
        self.posx: int = int(pos[0])
        self.posy: int = int(pos[1])
        self.game = game
        self.label: str = label
        self.font: pygame.font.Font | None = None

    def load_sprites(self, asset_size: int = 64) -> None:
        """Load the font for the chosen resolution."""
        font_path = "sprites/Font/KGPerfectPenmanship.ttf"
        font_size = max(12, asset_size // 3)
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Font not found ({font_path}) : {e}.")
            self.font = pygame.font.Font(None, font_size)

    @abstractmethod
    def get_text(self) -> str:
        """Return the text to display (one per subclass)."""
        pass

    def render(self, screen: pygame.Surface,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the text in white."""
        if self.font is None:
            self.load_sprites()

        if self.font:
            surface = self.font.render(self.get_text(), True,
                                       (255, 255, 255))
            screen.blit(surface, (self.posx + offset[0],
                                  self.posy + offset[1]))


class ScoreRenderer(HUDTextRenderer):
    """Score on 5 digits."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Create the score text."""
        super().__init__(pos, game, label="Score: ")

    def get_text(self) -> str:
        """Return "Score: 00000"."""
        return f"{self.label}{self.game.score:05d}"


class TimeRenderer(HUDTextRenderer):
    """Time left in the level, in seconds."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Create the time text."""
        super().__init__(pos, game, label="TIME: ")

    def get_text(self) -> str:
        """Return "TIME: 90s" (never negative)."""
        time_val = max(0.0, float(self.game.time_left))
        return f"{self.label}{time_val:.0f}s"


class LevelRenderer(HUDTextRenderer):
    """Level number, starting at 1."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Create the level text."""
        super().__init__(pos, game, label="LEVEL: ")

    def get_text(self) -> str:
        """Return "LEVEL: 1"."""
        return f"{self.label}{self.game.level_index + 1}"


class LivesTextRenderer(HUDTextRenderer):
    """"Lives:" label placed before the hearts."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Create the lives label."""
        super().__init__(pos, game, label="Lives: ")

    def get_text(self) -> str:
        """Return the label only."""
        return f"{self.label}"


class CheatRenderer(HUDTextRenderer):
    """Shows that cheat mode is on, with its active effects."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Create the cheat text."""
        super().__init__(pos, game, label="CHEAT")

    def get_text(self) -> str:
        """Return "CHEAT invincible frozen", or nothing without cheats."""
        if not self.game.cheat:
            return ""
        text = self.label
        if self.game.invincible:
            text += "  invincible"
        if self.game.ghosts_frozen:
            text += "  frozen"
        return text


class LivesRenderer(Renderer):
    """One heart per life, or "heart x10" when they do not fit."""

    def __init__(self, pos: Tuple[int, int], game: Game) -> None:
        """Store the position of the hearts and the game."""
        super().__init__()
        self.posx, self.posy = int(pos[0]), int(pos[1])
        self.game = game
        self.font: pygame.font.Font | None = None

    def load_sprites(self, asset_size: int = 64) -> None:
        """Load the heart image and the counter font."""
        self.sprites.clear()
        try:
            path = (
                f"sprites/ui/HUD/Lives/Lives_{asset_size}/"
                f"Lives_{asset_size}.png"
            )
            self.sprites[0] = load_image(path)
        except Exception as e:
            print(f"Error: cannot load the lives sprite ({e})")

        font_path = "sprites/Font/KGPerfectPenmanship.ttf"
        font_size = max(12, asset_size // 3)
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error):
            self.font = pygame.font.Font(None, font_size)

    def render(self, screen: pygame.Surface,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the hearts up to the edge of the bar."""
        icon = self.sprites.get(0)
        if not icon:
            return

        spacing = icon.get_width() + 4
        max_icons = (screen.get_width() - self.posx - offset[0]) // spacing
        if self.game.lives > max_icons and self.font:
            draw_x = self.posx + offset[0]
            draw_y = self.posy + offset[1]
            screen.blit(icon, (draw_x, draw_y))
            text = self.font.render(
                f"x{self.game.lives}", True, (255, 255, 255))
            text_y = draw_y + (icon.get_height() - text.get_height()) // 2
            screen.blit(text, (draw_x + spacing, text_y))
            return

        for i in range(max(0, self.game.lives)):
            draw_x = self.posx + (i * spacing) + offset[0]
            draw_y = self.posy + offset[1]
            screen.blit(icon, (draw_x, draw_y))
