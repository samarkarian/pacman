import pygame
from typing import Tuple
from Display_abstractmethods import Renderer


class MazeDisplayer(Renderer):
    def __init__(self, game, asset_size: int = 64):
        self.game = game
        self.maze_grid = game.field.maze.grid
        self.wall_sprites = {}
        self.asset_size = asset_size

    def load_sprites(self):
        self.load_wall_sprites(asset_size=self.asset_size)
        for p in self.game.field.pacgums.values():
            p.load_sprites(asset_size=self.asset_size)
        # print('\n\n\n\n',self.game.field)
        # print('\n\n\n\n',self.game.field.pacgums)


    def render(self, screen, offset):
        self.render_walls(screen=screen, offset=offset, asset_size=self.asset_size)
        for p in self.game.field.pacgums.values():
            p.render(screen=screen, offset=offset, animation_speed=800, asset_size=self.asset_size)

    def load_wall_sprites(self, asset_size):
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = pygame.image.load(f"sprites/maze/walls/walls_{asset_size}/wall_by{asset_size}_{n}.png")
        except Exception as e:
            print(e)

    def render_walls(self, asset_size, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)):
        for y, line in enumerate(self.maze_grid):
            for x, cell in enumerate(line):

                draw_x = x*asset_size + offset[0]
                draw_y = y*asset_size + offset[1]

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                screen.blit(current_sprite, (draw_x, draw_y))
