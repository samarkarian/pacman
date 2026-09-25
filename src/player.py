from src.display_abstractmethods import Entity
from typing import Tuple
from src.field import PlayField
import pygame
from src.sprite_cache import load_image


class Player:
    """Pac-Man: links the logic (controller) and the display (renderer)."""

    def __init__(self, field: PlayField) -> None:
        """Create Pac-Man in the middle of the field."""
        self.posx, self.posy = field.player_spawn[0], field.player_spawn[1]
        self.controller = PlayerController(field)
        self.renderer = PlayerRenderer(field.player_spawn)
        self.spawn = field.player_spawn

    def set_direction(self, direction: str) -> None:
        """Store the wanted direction ('N', 'S', 'E' or 'W')."""
        self.controller.set_direction(direction)
        self.renderer.direction = direction

    def turn_update(self, step_duration_ms: int = 150) -> None:
        """Move one cell if possible and start the sprite slide."""
        old_pos = (self.posx, self.posy)
        self.controller.step()
        self.posx, self.posy = self.controller.x, self.controller.y

        if old_pos != (self.posx, self.posy):
            self.renderer.start_move(old_pos, (self.posx, self.posy),
                                     step_duration_ms)
        else:
            self.renderer.posx, self.renderer.posy = self.posx, self.posy

    def load_sprites(self, asset_size: int) -> None:
        """Load Pac-Man's images for this size."""
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen: pygame.Surface, animation_speed: int,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw Pac-Man."""
        self.renderer.render(screen=screen, animation_speed=animation_speed,
                             offset=offset)

    def reset_position(self) -> None:
        """Put Pac-Man back in the middle, facing south."""
        self.posx, self.posy = self.spawn
        self.controller.reset(self.spawn)
        self.renderer.posx, self.renderer.posy = self.spawn
        self.renderer.start_pos = self.spawn
        self.renderer.target_pos = self.spawn
        self.set_direction('S')


class PlayerRenderer(Entity):
    """Pac-Man display: oriented sprite sliding from cell to cell."""

    def __init__(self, pos: Tuple[int, int]) -> None:
        """Place the sprite on pos, facing east."""
        super().__init__(pos)
        self.direction: str = 'E'

        self.start_pos: Tuple[int, int] = pos
        self.target_pos: Tuple[int, int] = pos
        self.move_start_time: int = pygame.time.get_ticks()
        self.step_duration_ms: int = 150

    def load_sprites(self, asset_size: int) -> None:
        """Load the 2 frames of every direction."""
        try:
            cardinals = ['N', 'S', 'E', 'W']
            self.sprites.clear()

            for c in cardinals:
                self.sprites[c] = []
                for sprite in range(2):
                    path = (
                        f"sprites/Entities/Player/Player_{asset_size}/"
                        f"Player_{asset_size}_{c}_frame_{sprite}.png"
                    )
                    surface = load_image(path).convert_alpha()
                    self.sprites[c].append(surface)

            self.pixel_offset = asset_size

        except Exception as e:
            print(e)

    def start_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int],
                   duration_ms: int) -> None:
        """Start a slide from from_pos to to_pos lasting duration_ms."""
        self.start_pos = from_pos
        self.target_pos = to_pos
        self.move_start_time = pygame.time.get_ticks()
        self.step_duration_ms = duration_ms

    def render(self, screen: pygame.Surface, animation_speed: int = 200,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw Pac-Man at the current position along the slide."""
        now = pygame.time.get_ticks()

        elapsed = now - self.move_start_time
        if self.step_duration_ms > 0:
            t = min(1.0, elapsed / self.step_duration_ms)
        else:
            t = 1.0

        start_x, start_y = self.start_pos
        target_x, target_y = self.target_pos
        interp_x = start_x + (target_x - start_x) * t
        interp_y = start_y + (target_y - start_y) * t

        draw_x = int(interp_x * self.pixel_offset) + offset[0]
        draw_y = int(interp_y * self.pixel_offset) + offset[1]

        frame_index = (now // animation_speed) % 2
        sprites = self.sprites.get(self.direction, [])
        if sprites:
            screen.blit(sprites[frame_index], (draw_x, draw_y))


class PlayerController:
    """Pac-Man's movement logic, cell by cell."""

    def __init__(self, field: PlayField) -> None:
        """Place Pac-Man in the middle, not moving."""

        self.field = field
        self.x, self.y = field.player_spawn
        self.direction: str | None = None
        self.next_direction: str | None = None

    def reset(self, spawn: Tuple[int, int]) -> None:
        """Put Pac-Man back on spawn, with no direction."""
        self.x, self.y = spawn
        self.direction = None
        self.next_direction = None

    def move(self, direction: str) -> str | None:
        """Move one cell in direction if no wall blocks the way."""

        maze = self.field.maze
        if maze.can_move(self.x, self.y, direction):
            dx, dy = maze.DIRECTIONS[direction]
            self.x += dx
            self.y += dy

        return None

    def set_direction(self, direction: str) -> None:
        """Store the direction to take as soon as possible."""

        self.next_direction = direction

    def step(self) -> str | None:
        """Turn if the wanted direction is free, then move one cell."""

        maze = self.field.maze
        if (self.next_direction is not None
                and maze.can_move(self.x, self.y, self.next_direction)):
            self.direction = self.next_direction

        if self.direction is None:
            return None

        return self.move(self.direction)
