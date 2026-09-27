from src.display_abstractmethods import Renderer
import pygame
from src.sprite_cache import load_image
from typing import Tuple


class Pacgum(Renderer):
    """Pac-gum or super pac-gum lying on a cell."""

    def __init__(self, pos: Tuple[int, int], gumtype: str) -> None:
        """Place the pac-gum; gumtype is 'Pacgum' or 'super_pacgum'.

        Args:
            pos: (x, y) cell.
            gumtype: 'Pacgum' or 'super_pacgum'.
        """
        super().__init__()
        self.posx, self.posy = int(pos[0]), int(pos[1])
        self.gumtype = gumtype

    def load_sprites(self, asset_size: int) -> None:
        """Load the 2 frames of the pac-gum for this size.

        Args:
            asset_size: sprite size in pixels (32 or 64).
        """
        gum = self.gumtype
        try:
            for sprite in range(2):
                self.sprites[sprite] = load_image(
                    f"sprites/maze/{gum}/{gum}_{asset_size}/"
                    f"{gum}_{asset_size}_frame_{sprite}.png"
                )
            self.pixel_offset = asset_size
        except Exception as e:
            print(e)

    def render(self, screen: pygame.Surface, animation_speed: int = 800,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the pac-gum in the middle of its cell.

        Args:
            screen: surface to draw on.
            animation_speed: time between two frames, in ms.
            offset: (x, y) of the maze on the screen, in pixels.
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        margin = self.pixel_offset / 4
        draw_x = self.pixel_offset * self.posx + offset[0] + margin
        draw_y = self.pixel_offset * self.posy + offset[1] + margin
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))
