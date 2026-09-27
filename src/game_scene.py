from src.maze_display import MazeDisplayer
from src.scene import Scene, SceneID
from typing import Any, Optional, Tuple
from src.game import Game
from src.hud_container import HUDContainer
from src.menu_classes import UIButton
import pygame


class GameScene(Scene):
    """Game screen: maze, HUD, input, pause and cheats."""

    def __init__(self, game: Game, asset_size: int = 64) -> None:
        """Prepare the display of the current (already started) level.

        Args:
            game: the game, with its level started.
            asset_size: sprite size in pixels (32 or 64).
        """
        if game.field is None or game.player is None:
            raise RuntimeError("the level could not be started")
        self.asset_size = asset_size
        self.game: Game = game
        self.mazedisplayer = MazeDisplayer(field=game.field,
                                           asset_size=asset_size)
        self.player_x = 0
        self.player_y = 0
        self.entities: list[Any] = []
        self.last_ghost_step = pygame.time.get_ticks()
        self.last_tick = pygame.time.get_ticks()
        self.loaded_field = self.game.field
        self.max_dt_ms = 100

        self.paused = False
        self.pause_index = 0
        self.pause_buttons = [
            UIButton(
                name="play",
                pos=(0, 0),
                action=self.resume,
                asset_size=self.asset_size,
            ),
            UIButton(
                name="quit",
                pos=(0, 0),
                action=lambda: SceneID.MENU,
                asset_size=self.asset_size,
            ),
        ]

        self.hud_container = HUDContainer(game=self.game,
                                          asset_size=self.asset_size)
        self.load_sprites()

    def load_sprites(self) -> None:
        """Call load_sprites() on every drawn element."""
        self.mazedisplayer.load_sprites()
        if self.game.player is not None:
            self.game.player.load_sprites(asset_size=self.asset_size)
        for e in self.game.ghosts:
            e.load_sprites(asset_size=self.asset_size)
        for entity in self.entities:
            entity.load_sprites()

        self.hud_container.load_sprites(self.asset_size)

    def resume(self) -> None:
        """Play button of the pause menu: resume the game."""
        self.paused = False

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        """Arrows: direction. Esc: pause. C then N/I/F/L: cheats.

        Args:
            event: pygame event.

        Returns:
            The scene to open, or None.
        """
        KEY_TO_DIRECTION = {
            pygame.K_UP: 'N',
            pygame.K_DOWN: 'S',
            pygame.K_LEFT: 'W',
            pygame.K_RIGHT: 'E',
        }
        if event.type == pygame.QUIT:
            self.is_running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                self.pause_index = 0
            elif self.paused:
                n = len(self.pause_buttons)
                if event.key == pygame.K_UP:
                    self.pause_index = (self.pause_index - 1) % n
                elif event.key == pygame.K_DOWN:
                    self.pause_index = (self.pause_index + 1) % n
                elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return self.pause_buttons[self.pause_index].trigger()
            elif event.key in KEY_TO_DIRECTION and self.game.player:
                self.game.player.set_direction(KEY_TO_DIRECTION[event.key])
            elif event.key == pygame.K_c:
                self.game.cheat = not self.game.cheat
                self.game.invincible = False
                self.game.ghosts_frozen = False
            elif self.game.cheat and event.key == pygame.K_n:
                self.game.skip_level()
            elif self.game.cheat and event.key == pygame.K_i:
                self.game.invincible = not self.game.invincible
            elif self.game.cheat and event.key == pygame.K_f:
                self.game.ghosts_frozen = not self.game.ghosts_frozen
            elif self.game.cheat and event.key == pygame.K_l:
                self.game.lives += 1
        return None

    def update(self) -> Optional[SceneID]:
        """Advance the game by the elapsed time; SceneID.NAME when it ends.

        Returns:
            SceneID.NAME when the game is over, else None.
        """
        if self.paused:
            self.last_tick = pygame.time.get_ticks()
            return None

        now = pygame.time.get_ticks()
        dt = now - self.last_tick
        self.last_tick = now
        dt = min(dt, self.max_dt_ms)

        self.game.update(dt)
        field = self.game.field
        if field is not None and field is not self.loaded_field:
            self.mazedisplayer.next_level(field)
            self.load_sprites()
            self.loaded_field = field

        if self.game.is_over():
            return SceneID.NAME

        return None

    def get_layout(
        self, screen: pygame.Surface
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        """Compute the (x, y) positions of the HUD and of the maze.

        Args:
            screen: window surface.

        Returns:
            (x, y) of the HUD and (x, y) of the maze.
        """
        screen_w, screen_h = screen.get_size()
        field = self.game.field
        if field is None:
            return (0, 0), (0, 0)
        grid_w = field.maze.width
        grid_h = field.maze.height

        maze_w = grid_w * self.asset_size
        maze_h = grid_h * self.asset_size
        hud_h = 2 * self.asset_size

        margin = 10
        total_content_h = hud_h + margin + maze_h

        pos_x = (screen_w - maze_w) // 2
        hud_y = (screen_h - total_content_h) // 2
        maze_y = hud_y + hud_h + margin

        return (pos_x, hud_y), (pos_x, maze_y)

    def render(self, screen: pygame.Surface) -> None:
        """Draw the HUD, the maze, the characters and the pause menu.

        Args:
            screen: surface to draw on.
        """
        hud_pos, maze_offset = self.get_layout(screen)

        self.hud_container.render(screen, hud_pos)

        self.mazedisplayer.render(screen=screen, offset=maze_offset)
        if self.game.player is not None:
            self.game.player.render(screen=screen, offset=maze_offset,
                                    animation_speed=400)
        for e in self.game.ghosts:
            e.render(screen=screen, offset=maze_offset, animation_speed=800)

        for entity in self.entities:
            entity.render(screen, maze_offset)

        if self.paused:
            screen_w, screen_h = screen.get_size()
            voile = pygame.Surface((screen_w, screen_h))
            voile.fill((0, 0, 0))
            voile.set_alpha(150)
            screen.blit(voile, (0, 0))

            x = (screen_w - 4 * self.asset_size) // 2
            for i, btn in enumerate(self.pause_buttons):
                btn.pos = (x, int(screen_h * (0.4 + 0.1 * i)))
                btn.render(screen, i == self.pause_index)
