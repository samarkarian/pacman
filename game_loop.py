import sys
import pygame
from maze_display import MazeDisplayer
from Entity_factory import Entity_factory

class GameLoop:
    """
    Classe principale gérant la fenêtre et la boucle de jeu, 
    façon MLX.
    """
    def __init__(self, mazegen) -> None:
        pygame.init()

        self.width: int = 1080
        self.height: int = 1080
        self.asset_size: int = 64
        self.animation_speed: int = 400
        self.is_running: bool = False

        self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))

        self.entities = []
        self.mazedisplayer = MazeDisplayer(mazegen, self.screen, self.asset_size)

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
                    self.player_y += 50
                elif event.key == pygame.K_DOWN:
                    self.player_y -= 50
                elif event.key == pygame.K_LEFT:
                    self.player_x += 50
                elif event.key == pygame.K_RIGHT:
                    self.player_x -= 50


    def load_sprites(self):
        """fonction appelant le load_sprites() de toutes les entites
        """
        self.mazedisplayer.load_sprites()
        for e in self.entities:
            e.load_sprites()

    def render(self) -> None:
        """
        fonction appellant les render() de toutes les entites
        """
        self.screen.fill((0, 0, 0))
        offset = (self.player_x, self.player_y)
        self.mazedisplayer.render(offset)
        for e in self.entities:
            e.render(self.animation_speed, offset)
        pygame.display.flip()
        pygame.display.flip()

    def future_menu_function(self):
        factory = Entity_factory(self.asset_size, self.screen)
        self.entities = factory.generate_entities()
        self.load_sprites()

    def run(self) -> None:
        """
        Équivalent de mlx_loop() : boucle infinie du jeu.
        """
        self.is_running = True
        
        clock = pygame.time.Clock()
        self.future_menu_function()

        while self.is_running:
            self.handle_events()
            self.render()

            clock.tick(60)

        pygame.quit()
        sys.exit(0)