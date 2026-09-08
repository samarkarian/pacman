from Display_abstractmethods import Entity, Renderer
import pygame
from typing import Tuple


class Pacgum(Renderer):
    def __init__(self, pos):
        super().__init__()
        self.posx, self.posy = pos[0], pos[1]

    def load_sprites(self, asset_size):
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/maze/{self.__class__.__name__}/{self.__class__.__name__}_{asset_size}/{self.__class__.__name__}_{asset_size}_frame_{sprite}.png")
        except Exception as e:
            print(e)

    def render(self, screen, asset_size, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.posx * asset_size + offset[0] + asset_size/4
        draw_y = self.posy * asset_size + offset[1] + asset_size/4
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))