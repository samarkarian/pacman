from maze_display import MazeDisplayer
from Scene import Scene, SceneID
from typing import Optional
from player import Player
from game import Game
import pygame


class GameScene(Scene):
    def __init__(self, game, asset_size: int = 64) -> None:
        self.asset_size = asset_size
        self.game = game
        self.mazedisplayer = MazeDisplayer(field=game.field, asset_size=asset_size)
        self.player_x = 0
        self.player_y = 0
        self.entities = []  # a retirer
        self.last_ghost_step = pygame.time.get_ticks()
        self.last_tick = pygame.time.get_ticks()
        self.load_sprites()
        self.loaded_field = self.game.field
        self.max_dt_ms: int = 100

    def load_sprites(self):
        """fonction appelant le load_sprites() de toutes les entites
        """
        self.mazedisplayer.load_sprites()
        self.game.player.load_sprites(asset_size=self.asset_size)
        for e in self.game.ghosts:
            e.load_sprites(asset_size=self.asset_size)
        for e in self.entities:
            e.load_sprites()

    def handle_event(self, event: pygame.event.Event) -> Optional[Scene]:
        KEY_TO_DIRECTION = {
            pygame.K_UP: 'N',
            pygame.K_DOWN: 'S',
            pygame.K_LEFT: 'W',
            pygame.K_RIGHT: 'E',
        }
        if event.type == pygame.QUIT:
            self.is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
                return SceneID.MENU
            elif event.key in KEY_TO_DIRECTION and self.game.player:
                self.game.player.set_direction(KEY_TO_DIRECTION[event.key])
            elif event.key == pygame.K_n:
                self.game.next_level()
            elif event.key == pygame.K_b:
                pygame.time.wait(2000)
        return None

    def update(self) -> Optional[SceneID]:
        now = pygame.time.get_ticks()
        dt = now - self.last_tick
        self.last_tick = now
        dt = min(dt, self.max_dt_ms)

        # Un seul appel unifié
        self.game.update(dt)
        if self.game.field is not self.loaded_field:
            self.mazedisplayer.next_level(self.game.field)
            self.load_sprites()
            self.loaded_field = self.game.field

        if self.game.is_over():
            return SceneID.GAMEOVER

        return None

    def render(self, screen: pygame.Surface) -> None:
        offset = (self.player_x, self.player_y)
        self.mazedisplayer.render(screen=screen, offset=offset)
        self.game.player.render(screen=screen, offset=offset, animation_speed=400)
        for e in self.game.ghosts:
            e.render(screen=screen, offset=offset, animation_speed=800)

        for e in self.entities:
            e.render(screen, offset)
