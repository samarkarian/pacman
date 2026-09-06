from maze_display import MazeDisplayer
from Scene import Scene, SceneID
from player import Player
from typing import Optional
import pygame

PACGUM_COLOR = (255, 184, 151)

KEY_TO_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

class GameScene(Scene):
    def __init__(self, game, asset_size: int = 64) -> None:
        self.asset_size = asset_size
        self.game = game
        self.field = game.field
        self.mazedisplayer = MazeDisplayer(grid=self.field.maze.grid, asset_size=asset_size)
        self.player_x = 0
        self.player_y = 0
        self.entities = []  # Peuplé par la factory
        self.load_sprites()
        self.player = Player(self.field)

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
            elif event.key in KEY_TO_DIRECTION:
                direction = KEY_TO_DIRECTION[event.key]
                self.game.add_score(self.player.move(direction))

    def update(self) -> None:
        pass

    def render_pacgums(self, screen: pygame.Surface,
                       offset: tuple[int, int] = (0, 0)) -> None:
        """Dessine un petit point par pacgum, un gros par super-pacgum."""
        half = self.asset_size // 2
        small = self.asset_size // 10
        big = self.asset_size // 5

        for x, y in self.field.pacgums:
            draw_x = x * self.asset_size + half + offset[0]
            draw_y = y * self.asset_size + half + offset[1]
            pygame.draw.circle(screen, PACGUM_COLOR, (draw_x, draw_y), small)

        for x, y in self.field.super_pacgums:
            draw_x = x * self.asset_size + half + offset[0]
            draw_y = y * self.asset_size + half + offset[1]
            pygame.draw.circle(screen, PACGUM_COLOR, (draw_x, draw_y), big)

    def render(self, screen: pygame.Surface) -> None:
        offset = (self.player_x, self.player_y)
        self.mazedisplayer.render(screen=screen, offset=offset)
        self.render_pacgums(screen=screen, offset=offset)
        for e in self.entities:
            e.render(screen, offset)
        cx = self.player.x * self.asset_size + self.asset_size // 2 + offset[0]
        cy = self.player.y * self.asset_size + self.asset_size // 2 + offset[1]
        pygame.draw.circle(screen, (255, 255, 0), (cx, cy), self.asset_size // 2 - 4)