import pygame

class MazeDisplayer:
    def __init__(self, mazegen, screen):
        self.maze_grid = mazegen.maze
        self.wall_sprites = {}
        self.screen = screen

    def load_wall_sprites(self):
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = pygame.image.load(f"sprites/walls/wall_{n}.png")
        except Exception as e:
            print(e)

    def render_walls(self):
        self.screen.blit(self.wall_sprites['wall_10'], (800, 800))
