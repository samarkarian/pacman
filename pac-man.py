from mazegenerator import MazeGenerator
from maze_display import MazeDisplayer
# class MazeConfig:
#     size: tuple[int, int]
#     entry_cell: tuple[int, int]
#     exit_cell: tuple[int, int]
#     perfect: bool
#     seed: int | None = None


import sys
import pygame
from typing import Tuple

class PacmanGame:
    """
    Classe principale gérant la fenêtre et la boucle de jeu, 
    façon MLX.
    """
    def __init__(self, mazegen) -> None:
        pygame.init()
        
        self.width: int = 1080
        self.height: int = 1080
        self.is_running: bool = False
        
        # Équivalent de mlx_new_window()
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))

        self.mazedisplayer = MazeDisplayer(mazegen, self.screen)
        self.sprites: dict = {}

        self.player_x = 0
        self.player_y = 0

    def handle_events(self) -> None:
        """
        Équivalent de mlx_hook() : capture des événements clavier et fenêtre.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_UP:
                    self.player_y -= 50
                elif event.key == pygame.K_DOWN:
                    self.player_y += 50
                elif event.key == pygame.K_LEFT:
                    self.player_x -= 50
                elif event.key == pygame.K_RIGHT:
                    self.player_x += 50



    def load_sprites(self):
        self.mazedisplayer.load_wall_sprites()
        player_frame_00 = pygame.image.load("sprites/player_frame_00.png")
        player_frame_01 = pygame.image.load("sprites/player_frame_01.png")
        self.sprites['player'] = [player_frame_00, player_frame_01]
        ghost_cyan_frame_00 = pygame.image.load("sprites/ghost_cyan_frame_00.png")
        ghost_cyan_frame_01 = pygame.image.load("sprites/ghost_cyan_frame_01.png")
        self.sprites['ghost_cyan'] = [ghost_cyan_frame_00, ghost_cyan_frame_01]



    def render(self) -> None:
        """
        Équivalent de mlx_put_image_to_window() avec un système de caméra.
        """
        self.screen.fill((0, 0, 0))
        
        
        # for entity in self.entities:
        #     if entity["type"] == "player":
        #         player_x = entity["x"]
        #         player_y = entity["y"]
        #         break  # On a trouvé le joueur, on arrête de chercher

        offset_x = (self.width // 2) - self.player_x
        offset_y = (self.height // 2) - self.player_y

        time = pygame.time.get_ticks()
        frame_index = (time // 400) % 2


        draw_x = 0 + offset_x
        draw_y = 0 + offset_y
        current_sprite = self.sprites['player'][frame_index]
            
        self.screen.blit(current_sprite, (draw_x, draw_y))

        draw_x = 400 + offset_x
        draw_y = 400 + offset_y
        current_sprite = self.sprites['ghost_cyan'][frame_index]
            
        self.screen.blit(current_sprite, (draw_x, draw_y))
        
        pygame.display.flip()



        pygame.display.flip()

    def run(self) -> None:
        """
        Équivalent de mlx_loop() : boucle infinie du jeu.
        """
        self.is_running = True
        
        clock = pygame.time.Clock()
        self.load_sprites()
        while self.is_running:
            self.handle_events()
            self.render()

            clock.tick(60)

        pygame.quit()
        sys.exit(0)

def main() -> None:
    try:
        maze_gen = MazeGenerator(
            size=(20,20),
            entry_cell=(0,0),
            exit_cell=(19,18),
            perfect=False,
            seed=0)

        maze_grid = maze_gen.maze

        maze_gen.generate()
        game = PacmanGame(maze_gen)
        game.run()
    except KeyboardInterrupt:
        sys.exit(1)

if __name__ == "__main__":
    main()


# def main():
#     maze_gen = MazeGenerator(
#         size=(20,20),
#         entry_cell=(0,0),
#         exit_cell=(19,18),
#         perfect=False,
#         seed=0)

#     maze_grid = maze_gen.maze

#     maze_gen.generate()
#     print(maze_gen.maze)
#     print(f"Maze dimensions: {len(maze_grid[0])}x{len(maze_grid)}")
#     print(f"Entry: {maze_gen.maze_entry}, Exit: {maze_gen.maze_exit}")


if __name__ == "__main__":
    main()
