from maze_display import MazeDisplayer
from Scene import Scene, SceneID
from player import Player
from typing import Optional
import pygame

PACGUM_COLOR = (255, 184, 151)

HUD_HEIGHT = 40         # bande reservee en haut pour le score
MOVE_DELAY = 150        # millisecondes entre deux cases du joueur
GHOST_DELAY = 200       # les fantomes sont un peu plus lents

GHOST_COLORS = [
    (255, 0, 0),        # rouge
    (255, 184, 255),    # rose
    (0, 255, 255),      # cyan
    (255, 184, 82),     # orange
]
VULNERABLE_COLOR = (33, 33, 255)   # fantomes mangeables

KEY_TO_DIRECTION = {
    pygame.K_UP: 'N',
    pygame.K_DOWN: 'S',
    pygame.K_LEFT: 'W',
    pygame.K_RIGHT: 'E',
}

class GameScene(Scene):
    def __init__(self, game, asset_size: int = 64,
                 cell_size: int | None = None) -> None:
        self.asset_size = asset_size
        self.cell_size = cell_size if cell_size else asset_size
        self.game = game
        self.field = game.field
        self.mazedisplayer = MazeDisplayer(grid=self.field.maze.grid,
                                          asset_size=asset_size,
                                          cell_size=self.cell_size)
        self.player_x = 0
        self.player_y = 0
        self.entities = []  # Peuplé par la factory
        self.load_sprites()
        self.player = Player(self.field)
        self.last_move = pygame.time.get_ticks()
        self.last_ghost_move = self.last_move
        self.font = pygame.font.Font(None, 28)

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
                self.player.set_direction(KEY_TO_DIRECTION[event.key])

    def update(self) -> Optional[SceneID]:
        """Avance d'une case au rythme fixe, puis teste la fin de niveau."""
        now = pygame.time.get_ticks()
        if now - self.last_move >= MOVE_DELAY:
            self.last_move = now
            self.game.eaten_effect(self.player.step())
            self.game.check_collision(self.player)

        if now - self.last_ghost_move >= GHOST_DELAY:
            self.last_ghost_move = now
            for ghost in self.game.ghosts:
                ghost.step()
            self.game.check_collision(self.player)
            if self.game.vulnerable_count > 0:
                self.game.vulnerable_count -= 1

        if self.game.is_over():
            return SceneID.MENU

        if not self.field.is_level_complete():
            return None
        if self.game.next_level():
            return SceneID.GAME
        return SceneID.MENU

    def render_pacgums(self, screen: pygame.Surface,
                       offset: tuple[int, int] = (0, 0)) -> None:
        """Dessine un petit point par pacgum, un gros par super-pacgum."""
        half = self.cell_size // 2
        small = self.cell_size // 10
        big = self.cell_size // 5

        for x, y in self.field.pacgums:
            draw_x = x * self.cell_size + half + offset[0]
            draw_y = y * self.cell_size + half + offset[1]
            pygame.draw.circle(screen, PACGUM_COLOR, (draw_x, draw_y), small)

        for x, y in self.field.super_pacgums:
            draw_x = x * self.cell_size + half + offset[0]
            draw_y = y * self.cell_size + half + offset[1]
            pygame.draw.circle(screen, PACGUM_COLOR, (draw_x, draw_y), big)

    def render_ghosts(self, screen: pygame.Surface,
                      offset: tuple[int, int] = (0, 0)) -> None:
        """Un disque colore par fantome, une couleur par coin de depart."""
        half = self.cell_size // 2
        radius = half - 4
        vulnerable = self.game.vulnerable_count != 0

        for index, ghost in enumerate(self.game.ghosts):
            if vulnerable:
                color = VULNERABLE_COLOR
            else:
                color = GHOST_COLORS[index % len(GHOST_COLORS)]
            draw_x = ghost.x * self.cell_size + half + offset[0]
            draw_y = ghost.y * self.cell_size + half + offset[1]
            pygame.draw.circle(screen, color, (draw_x, draw_y), radius)

    def render_hud(self, screen: pygame.Surface) -> None:
        """Score, vies et numero de niveau, en haut a gauche."""
        text = (f"Score {self.game.score}"
                f"   Vies {self.game.lives}"
                f"   Niveau {self.game.level_index + 1}")
        surface = self.font.render(text, True, (255, 255, 255))
        screen.blit(surface, (10, 10))

    def render(self, screen: pygame.Surface) -> None:
        offset = (self.player_x, self.player_y + HUD_HEIGHT)
        self.mazedisplayer.render(screen=screen, offset=offset)
        self.render_pacgums(screen=screen, offset=offset)
        self.render_ghosts(screen=screen, offset=offset)
        for e in self.entities:
            e.render(screen, offset)
        cx = self.player.x * self.cell_size + self.cell_size // 2 + offset[0]
        cy = self.player.y * self.cell_size + self.cell_size // 2 + offset[1]
        pygame.draw.circle(screen, (255, 255, 0), (cx, cy), self.cell_size // 2 - 4)
        self.render_hud(screen)
