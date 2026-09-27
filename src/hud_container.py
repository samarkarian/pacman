from typing import Tuple
from src.game import Game
import pygame
from src.hud_render import (
    CheatRenderer,
    LevelRenderer,
    LivesRenderer,
    LivesTextRenderer,
    Renderer,
    ScoreRenderer,
    TimeRenderer,
)


class HUDContainer:
    """Display container for the HUD (MLX-compatible drawing only)."""

    def __init__(
        self,
        game: Game,
        asset_size: int = 64,
        bg_color: Tuple[int, int, int] = (15, 15, 25),
        border_color: Tuple[int, int, int] = (200, 200, 200),
        border_width: int = 2,
    ) -> None:
        """Create the HUD bar and its elements.

        Args:
            game: the game to show.
            asset_size: sprite size in pixels (32 or 64).
            bg_color: RGB background colour.
            border_color: RGB border colour.
            border_width: border width, in pixels.
        """
        self.game = game
        self.asset_size = asset_size
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.hud_elements: list[Renderer] = []

        self.width: int = 0
        self.height: int = 0
        self.surface: pygame.Surface | None = None
        self.inner_surface: pygame.Surface | None = None

        self.build()

    def build(self) -> None:
        """Create and place the HUD elements."""
        self.hud_elements.clear()

        field = getattr(self.game, "field", None)
        if not field or not hasattr(field, "maze"):
            return

        maze_w = field.maze.width
        hud_y = int(self.asset_size * 0.7)
        step_x = (maze_w * self.asset_size) // 4
        game = self.game

        self.hud_elements = [
            ScoreRenderer(pos=(int(step_x * 0.1), hud_y), game=game),
            TimeRenderer(pos=(int(step_x * 1.1), hud_y), game=game),
            LevelRenderer(pos=(int(step_x * 2.1), hud_y), game=game),
            LivesTextRenderer(pos=(int(step_x * 2.8), hud_y), game=game),
            LivesRenderer(pos=(int(step_x * 3.1), int(hud_y * 0.7)),
                          game=game),
            CheatRenderer(
                pos=(int(step_x * 0.1), hud_y + self.asset_size // 2),
                game=game,
            ),
        ]

        self.update_dimensions(maze_w, self.asset_size)
        self.load_sprites(self.asset_size)

    def load_sprites(self, asset_size: int) -> None:
        """Pass the loading call on to every child element.

        Args:
            asset_size: sprite size in pixels (32 or 64).
        """
        self.asset_size = asset_size
        for elem in self.hud_elements:
            if hasattr(elem, "load_sprites"):
                elem.load_sprites(asset_size)

    def update_dimensions(self, maze_grid_w: int, asset_size: int) -> None:
        """Recompute the outer and inner surfaces of the bar.

        Args:
            maze_grid_w: maze width, in cells.
            asset_size: sprite size in pixels (32 or 64).
        """
        self.asset_size = asset_size
        self.width = maze_grid_w * asset_size
        self.height = 2 * asset_size

        if self.width <= 0 or self.height <= 0:
            return

        inner_w = max(0, self.width - (self.border_width * 2))
        inner_h = max(0, self.height - (self.border_width * 2))

        self.surface = pygame.Surface((self.width, self.height))
        self.inner_surface = pygame.Surface((inner_w, inner_h))

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]) -> None:
        """Draw the HUD on an off-screen surface, then blit it.

        Args:
            screen: surface to draw on.
            pos: (x, y) of the bar.
        """
        if self.surface is None or self.inner_surface is None:
            return

        self.surface.fill(self.border_color)
        self.inner_surface.fill(self.bg_color)

        for hud in self.hud_elements:
            hud.render(self.inner_surface)

        self.surface.blit(self.inner_surface,
                          (self.border_width, self.border_width))

        screen.blit(self.surface, pos)
