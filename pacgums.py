from Display_abstractmethods import Entity, Renderer
import pygame
from typing import Tuple


class Pacgum(Renderer):
    def __init__(self, pos: Tuple[int, int], gumtype: str):
        super().__init__()
        self.posx, self.posy = int(pos[0]), int(pos[1])
        self.pixelpos = pos
        self.gumtype = gumtype

    def load_sprites(self, asset_size: int):
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/maze/{self.gumtype}/{self.gumtype}_{asset_size}/{self.gumtype}_{asset_size}_frame_{sprite}.png")
            self.pixel_pos = (self.posx * asset_size, self.posy * asset_size)
        except Exception as e:
            print(e)

    def render(self, screen, asset_size: int, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_pos[0] + offset[0] + asset_size/4
        draw_y = self.pixel_pos[1] + offset[1] + asset_size/4
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))
