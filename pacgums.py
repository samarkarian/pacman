from Display_abstractmethods import Entity, Renderer
import pygame
from sprite_cache import load_image
from typing import Tuple


class Pacgum(Renderer):
    def __init__(self, pos: Tuple[int, int], gumtype: str):
        super().__init__()
        self.posx, self.posy = int(pos[0]), int(pos[1])
        self.gumtype = gumtype

    def load_sprites(self, asset_size: int):
        try:
            for sprite in range(2):
                self.sprites[sprite] = load_image(f"sprites/maze/{self.gumtype}/{self.gumtype}_{asset_size}/{self.gumtype}_{asset_size}_frame_{sprite}.png")
            self.pixel_offset = asset_size
        except Exception as e:
            print(e)

    def render(self, screen, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_offset * self.posx + offset[0] + self.pixel_offset/4
        draw_y = self.pixel_offset * self.posy + offset[1] + self.pixel_offset/4
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))
