from abc import ABC, abstractmethod
from typing import Tuple
import pygame


class Renderer(ABC):
    def __init__(self):
        self.sprites: dict = {}

    @abstractmethod
    def load_sprites(self):
        pass

    @abstractmethod
    def render(self, screen, offset: Tuple[int, int]):
        pass


class Entity(Renderer):
    def __init__(self, position: Tuple[int, int]):
        super().__init__()
        self.posx: int = int(position[0])
        self.posy: int = int(position[1])
        self.pixel_offset: int = 64

    @abstractmethod
    def load_sprites(self, asset_size: int):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/Entities/{self.__class__.__name__}/{self.__class__.__name__}_{asset_size}/{self.__class__.__name__}_{asset_size}_frame_{sprite}.png")
            self.pixel_pos = (self.posx * int(asset_size), self.posy * int(asset_size))

        except Exception as e:
            print(e)

    @abstractmethod
    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_offset*self.posx + offset[0]
        draw_y = self.pixel_offset*self.posy + offset[1]
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))

# class livingEntity
#     self.Entity(Renderer
#     self.EntityAi = pos, comportement














# class Ghost(Entity):
#     def __init__(self, posx: int, posy: int, asset_size: int, color: str):
#         super().__init__(asset_size)
#         self.posx = posx
#         self.posy = posy
#         self.color = color

#     def load_sprites(self):
#         try:
#             for sprite in range(2):
#                 self.sprites[sprite] = pygame.image.load(f"sprites/Entities/{self.__class__.__name__}/\
# {self.__class__.__name__}_{self.color}/{self.__class__.__name__}_{self.color}_{self.asset_size}/\
# {self.__class__.__name__}_{self.color}_{self.asset_size}_frame_{sprite}.png")
#         except Exception as e:
#             print(e)

#     def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
#         super().render(screen, animation_speed, offset)
