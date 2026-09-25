from abc import ABC, abstractmethod
from typing import Any, Tuple
import pygame
from src.sprite_cache import load_image


class Renderer(ABC):
    """Base class for everything that loads and draws sprites."""

    def __init__(self) -> None:
        """Create the sprite dictionary."""
        self.sprites: dict[Any, Any] = {}

    @abstractmethod
    def load_sprites(self, *args: Any, **kwargs: Any) -> None:
        """Load the images for the given size."""
        pass

    @abstractmethod
    def render(self, screen: pygame.Surface,
               *args: Any, **kwargs: Any) -> None:
        """Draw the element on the screen."""
        pass


class Entity(Renderer):
    """Maze element placed on a cell, animated with 2 frames."""

    def __init__(self, position: Tuple[int, int]) -> None:
        """Place the element on the given cell."""
        super().__init__()
        self.posx: int = int(position[0])
        self.posy: int = int(position[1])
        self.pixel_offset: int = 64

    @abstractmethod
    def load_sprites(self, asset_size: int) -> None:
        """Load the 2 frames from the class name and the size."""
        name = self.__class__.__name__
        try:
            for sprite in range(2):
                self.sprites[sprite] = load_image(
                    f"sprites/Entities/{name}/{name}_{asset_size}/"
                    f"{name}_{asset_size}_frame_{sprite}.png"
                )
            self.pixel_pos = (self.posx * int(asset_size),
                              self.posy * int(asset_size))

        except Exception as e:
            print(e)

    @abstractmethod
    def render(self, screen: pygame.Surface, animation_speed: int,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the current frame, switching every animation_speed ms."""
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_offset*self.posx + offset[0]
        draw_y = self.pixel_offset*self.posy + offset[1]
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))
