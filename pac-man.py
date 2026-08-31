from mazegenerator import MazeGenerator

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
    def __init__(self, width: int, height: int, title: str) -> None:
        # Équivalent de mlx_init()
        pygame.init()
        
        self.width: int = width
        self.height: int = height
        self.is_running: bool = False
        
        # Équivalent de mlx_new_window()
        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

        self.sprites: dict = {}

    def handle_events(self) -> None:
        """
        Équivalent de mlx_hook() : capture des événements clavier et fenêtre.
        """
        for event in pygame.event.get():
            # Gestion de la croix rouge de la fenêtre
            if event.type == pygame.QUIT:
                self.is_running = False
            
            # Gestion des touches clavier
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_running = False
                elif event.key == pygame.K_UP:
                    print("Haut")
                elif event.key == pygame.K_DOWN:
                    print("Bas")
                elif event.key == pygame.K_LEFT:
                    print("Gauche")
                elif event.key == pygame.K_RIGHT:
                    print("Droite")

    def load_sprites(self):
        player_frame_00 = pygame.image.load("sprites/player_frame_00.png")
        player_frame_01 = pygame.image.load("sprites/player_frame_01.png")
        self.sprites['player'] = [player_frame_00, player_frame_01]
        ghost_cyan_frame_00 = pygame.image.load("sprites/ghost_cyan_frame_00.png")
        ghost_cyan_frame_01 = pygame.image.load("sprites/ghost_cyan_frame_01.png")
        self.sprites['ghost_cyan'] = [ghost_cyan_frame_00, ghost_cyan_frame_01]




    def render(self, time) -> None:
        """
        Équivalent de mlx_put_image_to_window() et gestion du buffer.
        """
        self.screen.fill((0, 0, 0))
        print(time)
        if time % 800 >= 399:
            self.screen.blit(self.sprites['player'][0], (0, 0))
            self.screen.blit(self.sprites['ghost_cyan'][0], (400, 400))

        else:
            self.screen.blit(self.sprites['player'][1], (0, 0))
            self.screen.blit(self.sprites['ghost_cyan'][1], (400, 400))


        
        pygame.display.flip()

    def run(self) -> None:
        """
        Équivalent de mlx_loop() : boucle infinie du jeu.
        """
        self.is_running = True
        
        clock = pygame.time.Clock()
        self.load_sprites()
        time = 0
        while self.is_running:
            time = pygame.time.get_ticks()
            self.handle_events()
            self.render(time)

            clock.tick(60)

        pygame.quit()
        sys.exit(0)

def main() -> None:
    try:
        # Initialisation avec une taille de fenêtre arbitraire
        game = PacmanGame(1080, 1080, "Pacman - 42")
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
