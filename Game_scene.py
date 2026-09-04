from maze_display import MazeDisplayer
from Scene import Scene, SceneID
from typing import Optional
import pygame

class GameScene(Scene):
    def __init__(self, mazegen, asset_size: int = 64) -> None:
        self.asset_size = asset_size
        self.mazedisplayer = MazeDisplayer(mazegen=mazegen, asset_size=asset_size)
        self.player_x = 0
        self.player_y = 0
        self.entities = []  # Peuplé par la factory
        self.load_sprites()

    def load_sprites(self):
        """fonction appelant le load_sprites() de toutes les entites
        """
        self.mazedisplayer.load_sprites()
        for e in self.entities:
            e.load_sprites()

    def handle_event(self, event: pygame.event.Event) -> Optional[Scene]:
        if event.type == pygame.QUIT:
            self.is_running = False

        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                return SceneID.MENU
            elif event.key == pygame.K_UP:
                self.player_y += 50
            elif event.key == pygame.K_DOWN:
                self.player_y -= 50
            elif event.key == pygame.K_LEFT:
                self.player_x += 50
            elif event.key == pygame.K_RIGHT:
                self.player_x -= 50

    def update(self) -> None:
        pass

    def render(self, screen: pygame.Surface) -> None:
        offset = (self.player_x, self.player_y)
        self.mazedisplayer.render(screen=screen, offset=offset)
        for e in self.entities:
            e.render(screen, offset)