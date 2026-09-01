import pygame

class MazeDisplayer:
    def __init__(self, mazegen, screen):
        self.maze_grid = mazegen.maze
        self.maze_walls_id = self.calculate_wall_value()
        self.wall_sprites = {}
        self.screen = screen

    def load_wall_sprites(self):
        try:
            for n in range(16):
                self.wall_sprites[f'wall_{n}'] = pygame.image.load(f"sprites/walls/walls_64*64/wall_by64_{n}.png")
        except Exception as e:
            print(e)

    def render_walls(self, offset_x, offset_y, size: int = 64):
        for y, line in enumerate(self.maze_walls_id):
            for x, cell in enumerate(line):

                draw_x = x*size + offset_x
                draw_y = y*size + offset_y

                current_sprite = self.wall_sprites[f'wall_{15-cell}']
                self.screen.blit(current_sprite, (draw_x, draw_y))


    def calculate_wall_value(self):
        print(self.maze_grid)
        for row in self.maze_grid:
            for cell in row:
                print(cell)
        return self.maze_grid
