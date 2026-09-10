from maze import Maze
from Display_abstractmethods import Entity
from typing import Tuple
import pygame


class Player:
    def __init__(self, field):
        self.posx, self.posy = field.player_spawn[0], field.player_spawn[1]
        self.controller = PlayerController(field)
        self.renderer = PlayerRenderer(field.player_spawn)

    def set_direction(self, direction: str):
        self.controller.set_direction(direction)

    def turn_update(self):
        self.posx, self.posy = self.controller.step()
        self.renderer.posx, self.renderer.posy = self.posx, self.posy

    def load_sprites(self, asset_size):
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        self.renderer.render(screen=screen, animation_speed=animation_speed, offset=offset)


class PlayerRenderer(Entity):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__(pos)

    def load_sprites(self, asset_size):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/Entities/Player/Player_{asset_size}/Player_{asset_size}_frame_{sprite}.png")
            self.pixel_pos = (self.posx * asset_size, self.posy * asset_size)

        except Exception as e:
            print(e)

    def render(self, screen, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_pos[0] + offset[0]
        draw_y = self.pixel_pos[1] + offset[1]
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))


class PlayerController:
    def __init__(self, field) -> None:

        self.field = field
        self.x, self.y = field.player_spawn
        self.direction = None
        self.next_direction = None

    def move(self, direction: str) -> str | None:

        dir_dict = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        maze = self.field.maze
        if maze.can_move(self.x, self.y, direction):
            dx, dy = dir_dict[direction]
            self.x += dx
            self.y += dy
            if self.field.eat_pacgum(self.x, self.y):
                return "pacgum"
            if self.field.eat_super_pacgum(self.x, self.y):
                return "super_pacgum"

        return None

    def set_direction(self, direction: str) -> None:

        self.next_direction = direction
        print(direction)

    def step(self) -> str | None:

        maze = self.field.maze
        if maze.can_move(self.x, self.y, self.next_direction):
            self.direction = self.next_direction

        if self.direction is None:
            return None

        return self.move(self.direction)
