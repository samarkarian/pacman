from maze import Maze
from Display_abstractmethods import Entity
from typing import Tuple
import pygame
from sprite_cache import load_image


class Player:
    def __init__(self, field):
        self.posx, self.posy = field.player_spawn[0], field.player_spawn[1]
        self.controller = PlayerController(field)
        self.renderer = PlayerRenderer(field.player_spawn)
        self.spawn = field.player_spawn

    def set_direction(self, direction: str):
        self.controller.set_direction(direction)
        self.renderer.direction = direction

    # def turn_update(self):
    #     self.controller.step()
    #     self.posx, self.posy = self.controller.x, self.controller.y
    #     self.renderer.posx, self.renderer.posy = self.posx, self.posy

    def turn_update(self, step_duration_ms: int = 150) -> None:
        old_pos = (self.posx, self.posy)
        self.controller.step()
        self.posx, self.posy = self.controller.x, self.controller.y

        if old_pos != (self.posx, self.posy):
            self.renderer.start_move(old_pos, (self.posx, self.posy), step_duration_ms)
        else:
            self.renderer.posx, self.renderer.posy = self.posx, self.posy
    
    def load_sprites(self, asset_size):
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        self.renderer.render(screen=screen, animation_speed=animation_speed, offset=offset)

    def reset_position(self) -> None:
        self.posx, self.posy = self.spawn
        self.controller.reset(self.spawn)
        self.renderer.posx, self.renderer.posy = self.spawn
        self.renderer.start_pos = self.spawn
        self.renderer.target_pos = self.spawn
        self.renderer.direction = 'E'


class PlayerRenderer(Entity):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__(pos)
        self.direction: str = 'E'

        self.start_pos: Tuple[int, int] = pos
        self.target_pos: Tuple[int, int] = pos
        self.move_start_time: int = pygame.time.get_ticks()
        self.step_duration_ms: int = 150

    def load_sprites(self, asset_size):
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


    def start_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], duration_ms: int) -> None:
        self.start_pos = from_pos
        self.target_pos = to_pos
        self.move_start_time = pygame.time.get_ticks()
        self.step_duration_ms = duration_ms

    def render(self, screen: pygame.Surface, animation_speed: int = 200, offset: Tuple[int, int] = (0, 0)) -> None:
        now = pygame.time.get_ticks()

        elapsed = now - self.move_start_time
        t = min(1.0, elapsed / self.step_duration_ms) if self.step_duration_ms > 0 else 1.0

        interp_x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * t
        interp_y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * t

        draw_x = int(interp_x * self.pixel_offset) + offset[0]
        draw_y = int(interp_y * self.pixel_offset) + offset[1]

        frame_index = (now // animation_speed) % 2
        sprites = self.sprites.get(self.direction, [])
        if sprites:
            screen.blit(sprites[frame_index], (draw_x, draw_y))


class PlayerController:
    def __init__(self, field) -> None:

        self.field = field
        self.x, self.y = field.player_spawn
        self.direction = None
        self.next_direction = None

    def reset(self, spawn: Tuple[int, int]) -> None:
        self.x, self.y = spawn
        self.direction = None
        self.next_direction = None

    def move(self, direction: str) -> str | None:

        maze = self.field.maze
        if maze.can_move(self.x, self.y, direction):
            dx, dy = maze.DIRECTIONS[direction]
            self.x += dx
            self.y += dy

        return None

    def set_direction(self, direction: str) -> None:

        self.next_direction = direction

    def step(self) -> str | None:

        maze = self.field.maze
        if maze.can_move(self.x, self.y, self.next_direction):
            self.direction = self.next_direction

        if self.direction is None:
            return None

        return self.move(self.direction)
