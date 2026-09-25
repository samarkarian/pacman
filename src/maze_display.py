import pygame
from src.sprite_cache import load_image
from typing import Tuple
from src.field import PlayField
from src.display_abstractmethods import Renderer


class MazeDisplayer(Renderer):
    """Draw the level's walls and pac-gums."""

    def __init__(self, field: PlayField, asset_size: int = 64) -> None:
        """Store the field to draw and the sprite size."""
        self.field = field
        self.wall_sprites: dict[str, pygame.Surface] = {}
        self.asset_size = asset_size

    def next_level(self, newfield: PlayField) -> None:
        """Switch to the new level's field."""
        self.field = newfield

    def load_sprites(self) -> None:
        """Load the walls and the images of every pac-gum."""
        self.load_wall_sprites(asset_size=self.asset_size)
        for p in self.field.pacgums.values():
            p.load_sprites(asset_size=self.asset_size)
        for p in self.field.super_pacgums.values():
            p.load_sprites(asset_size=self.asset_size)

    def render(self, screen: pygame.Surface,
               offset: Tuple[int, int]) -> None:
        """Draw the walls then the pac-gums, shifted by offset."""
        self.render_walls(screen=screen, offset=offset,
                          asset_size=self.asset_size)
        for p in self.field.pacgums.values():
            p.render(screen=screen, offset=offset, animation_speed=800)
        for p in self.field.super_pacgums.values():
            p.render(screen=screen, offset=offset, animation_speed=800)

    def load_wall_sprites(self, asset_size: int) -> None:
        """Load the 16 wall images (one per combination of sides)."""
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = load_image(
                    f"sprites/maze/walls/walls_{asset_size}/"
                    f"wall_by{asset_size}_{n}.png"
                )
        except Exception as e:
            print(e)

    def render_walls(self, asset_size: int, screen: pygame.Surface,
                     offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the wall of every cell from its 4 wall bits."""
        for y, line in enumerate(self.field.maze.grid):
            for x, cell in enumerate(line):

                draw_x = x*asset_size + offset[0]
                draw_y = y*asset_size + offset[1]

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                screen.blit(current_sprite, (draw_x, draw_y))
