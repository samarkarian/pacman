from maze import Maze
from Display_abstractmethods import Entity
from typing import Tuple
import pygame


class Player:
    def __init__(self, field):
        self.posx, self.posy = field.player_spawn[0], field.player_spawn[1]
        self.controller = PlayerController(field)
        self.renderer = PlayerRenderer(field.player_spawn)
        self.spawn = field.player_spawn

    def set_direction(self, direction: str):
        self.controller.set_direction(direction)
        self.renderer.direction = direction

    def turn_update(self):
        self.controller.step()
        self.posx, self.posy = self.controller.x, self.controller.y
        self.renderer.posx, self.renderer.posy = self.posx, self.posy

    def load_sprites(self, asset_size):
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        self.renderer.render(screen=screen, animation_speed=animation_speed, offset=offset)

    def reset_position(self) -> None:
        self.posx, self.posy = self.spawn
        self.controller.reset(self.spawn)
        self.renderer.posx, self.renderer.posy = self.spawn
        self.renderer.direction = 'E'


class PlayerRenderer(Entity):
    def __init__(self, pos: Tuple[int, int]):
        super().__init__(pos)
        self.direction: str = 'E'

    def load_sprites(self, asset_size):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
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
                    surface = pygame.image.load(path).convert_alpha()
                    self.sprites[c].append(surface)

            self.pixel_offset = asset_size

        except Exception as e:
            print(e)

    def render(self, screen, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        animation speed pour le mode SUPER 
        """
        animation_speed = 200 #ecriture en dur pour plus de simplicite au debut
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_offset*self.posx + offset[0]
        draw_y = self.pixel_offset*self.posy + offset[1]
        current_sprite = self.sprites[self.direction][frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))


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
