import pygame
from sprite_cache import load_image
from typing import Tuple
from Display_abstractmethods import Renderer


class MazeDisplayer(Renderer):
    def __init__(self, field, asset_size: int = 64):
        self.field = field
        self.wall_sprites = {}
        self.asset_size = asset_size

    def next_level(self, newfield):
        self.field = newfield
        
    def load_sprites(self):
        self.load_wall_sprites(asset_size=self.asset_size)
        for p in self.field.pacgums.values():
            p.load_sprites(asset_size=self.asset_size)
        for p in self.field.super_pacgums.values():
            p.load_sprites(asset_size=self.asset_size)


    def render(self, screen, offset):
        self.render_walls(screen=screen, offset=offset, asset_size=self.asset_size)
        # torender = self.game.field.pacgums.values() + self.game.field.super_pacgums.values()
        # for t in torender:
        #     t.render(screen=screen, offset=offset, animation_speed=800, asset_size=self.asset_size)
        for p in self.field.pacgums.values():
            p.render(screen=screen, offset=offset, animation_speed=800)
        for p in self.field.super_pacgums.values():
            p.render(screen=screen, offset=offset, animation_speed=800)

    def load_wall_sprites(self, asset_size):
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = load_image(f"sprites/maze/walls/walls_{asset_size}/wall_by{asset_size}_{n}.png")
        except Exception as e:
            print(e)

    def render_walls(self, asset_size, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)):
        for y, line in enumerate(self.field.maze.grid):
            for x, cell in enumerate(line):

                draw_x = x*asset_size + offset[0]
                draw_y = y*asset_size + offset[1]

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                screen.blit(current_sprite, (draw_x, draw_y))
