import pygame
from typing import Tuple
from Display_abstractmethods import Renderer


class MazeDisplayer(Renderer):
    def __init__(self, grid, asset_size: int = 64,
                 cell_size: int | None = None):
        self.maze_grid = grid
        self.wall_sprites = {}
        self.asset_size = asset_size
        self.cell_size = cell_size if cell_size else asset_size

    def load_sprites(self):
        self.load_wall_sprites()

    def render(self, screen, offset):
        self.render_walls(screen=screen, offset=offset)

    def load_wall_sprites(self):
        try:
            for n in range(16):
                sprite = pygame.image.load(f"sprites/walls/walls_{self.asset_size}/wall_by{self.asset_size}_{n}.png")
                if self.cell_size != self.asset_size:
                    sprite = pygame.transform.smoothscale(
                        sprite, (self.cell_size, self.cell_size))
                self.wall_sprites[f'wall_{n}'] = sprite
        except Exception as e:
            print(e)

    def render_walls(self, screen: pygame.Surface, offset: Tuple[int, int] = (0, 0)):
        for y, line in enumerate(self.maze_grid):
            for x, cell in enumerate(line):

                draw_x = x*self.cell_size + offset[0]
                draw_y = y*self.cell_size + offset[1]

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                screen.blit(current_sprite, (draw_x, draw_y))
