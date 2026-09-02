import pygame
from typing import Tuple
from Display_abstractmethods import Renderer


class MazeDisplayer(Renderer):
    def __init__(self, mazegen, screen, size: int = 64):
        self.maze_grid = mazegen.maze
        self.wall_sprites = {}
        self.screen = screen
        self.size = size

    def load_sprites(self):
        self.load_wall_sprites()

    def render(self, offset):
        self.render_walls(offset=offset)

    def load_wall_sprites(self):
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = pygame.image.load(f"sprites/walls/walls_{self.size}/wall_by{self.size}_{n}.png")
        except Exception as e:
            print(e)

    def render_walls(self, offset: Tuple[int, int] = (0, 0)):
        for y, line in enumerate(self.maze_grid):
            for x, cell in enumerate(line):

                draw_x = x*self.size + offset[0]
                draw_y = y*self.size + offset[1]

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                self.screen.blit(current_sprite, (draw_x, draw_y))
