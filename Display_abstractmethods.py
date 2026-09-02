from abc import ABC, abstractmethod
from typing import Tuple
import pygame


class Renderer(ABC):
    def __init__(self, screen, asset_size: int):
        self.sprites: dict = {}
        self.asset_size: int = asset_size
        self.screen = screen

    @abstractmethod
    def load_sprites(self):
        pass

    @abstractmethod
    def render(self, offset: Tuple[int, int]):
        pass


class Entity(Renderer):
    def __init__(self, screen, asset_size: int):
        super().__init__(screen, asset_size)
        self.posx: int
        self.posy: int

    @abstractmethod
    def load_sprites(self):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/Entities/{self.__class__.__name__}/{self.__class__.__name__}_{self.asset_size}/{self.__class__.__name__}_{self.asset_size}_frame_{sprite}.png")
        except Exception as e:
            print(e)

    @abstractmethod
    def render(self, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.posx + offset[0]
        draw_y = self.posy + offset[1]
        current_sprite = self.sprites[frame_index]

        self.screen.blit(current_sprite, (draw_x, draw_y))


class Ghost(Entity):
    def __init__(self, posx: int, posy: int, screen, asset_size: int, color: str):
        super().__init__(screen, asset_size)
        self.posx = posx
        self.posy = posy
        self.color = color

    def load_sprites(self):
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/Entities/{self.__class__.__name__}/\
{self.__class__.__name__}_{self.color}/{self.__class__.__name__}_{self.color}_{self.asset_size}/\
{self.__class__.__name__}_{self.color}_{self.asset_size}_frame_{sprite}.png")
        except Exception as e:
            print(e)

    def render(self, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        super().render(animation_speed, offset)
