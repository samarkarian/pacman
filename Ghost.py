from Display_abstractmethods import Entity, Renderer
import pygame
import random
from typing import Tuple, Dict, List

class Ghost:
    def __init__(self, play_field, spawn, color: str):
        self.ai = GhostAI(play_field, spawn)
        self.renderer = GhostRenderer(spawn, color)
        self.posx, self.posy = spawn[0], spawn[1]
        self.state = 'normal'
        self.spawn = spawn

    def reset_position(self) -> None:
        self.posx, self.posy = self.spawn
        self.ai.reset(self.spawn)
        self.renderer.posx, self.renderer.posy = self.spawn
        self.state = 'normal'
        self.renderer.state = 'normal'

    def turn_update(self, player_pos, new_state):

        if new_state != self.state:
            self.state = new_state
            self.renderer.state = self.state

        self.posx, self.posy = self.ai.step(player_pos, state=self.state)
        self.renderer.posx, self.renderer.posy = self.posx, self.posy

    def load_sprites(self, asset_size):
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        self.renderer.render(screen=screen, animation_speed=animation_speed, offset=offset)


class GhostRenderer(Entity):
    def __init__(self, pos: Tuple[int, int], color):
        super().__init__(pos)
        self.color = color
        self.sprites: Dict[str, List[pygame.Surface]] = {
            "normal": [],
            "vulnerable": [],
            "end": [],
        }
        self.state = 'normal'

    def load_sprites(self, asset_size):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for sprite in range(2):
                self.sprites['normal'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_{self.color}/Ghost_{self.color}_{asset_size}/Ghost_{self.color}_{asset_size}_frame_{sprite}.png"))
            for sprite in range(2):
                self.sprites['vulnerable'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_vulnerable/Ghost_vulnerable_{asset_size}/Ghost_vulnerable_{asset_size}_frame_{sprite}.png"))
            for sprite in range(2):
                self.sprites['end'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_vulnerable/Ghost_end_{asset_size}/Ghost_end_{asset_size}_frame_{sprite}.png"))

            self.pixel_offset = asset_size

        except Exception as e:
            print(e)

    def render(self, screen, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.pixel_offset * self.posx + offset[0]
        draw_y = self.pixel_offset * self.posy + offset[1]
        current_sprite = self.sprites[self.state][frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))


class GhostAI:
    def __init__(self, field, spawn):

        self.field = field
        self.x, self.y = spawn
        self.previous = None
        self.respawn_count = 0

    def reset(self, spawn: Tuple[int, int]) -> None:
        self.x, self.y = spawn
        self.previous = None
        self.respawn_count = 0

    def start_respawn(self, steps: int) -> None:

        self.respawn_count = steps

    def step(self, player_pos, state) -> None:
        player_x, player_y = player_pos
        if self.respawn_count != 0:
            self.respawn_count -= 1
            return self.x, self.y

        maze = self.field.maze
        cells = maze.neighbors(self.x, self.y)
        if not cells:
            return self.x, self.y

        choices = []
        for cell in cells:
            if cell != self.previous:
                choices.append(cell)

        if not choices:
            choices = cells

        self.previous = (self.x, self.y)
        dist_dict = {}
        for choice in choices:
            choice_x, choice_y = choice
            x_dist = player_x - choice_x
            y_dist = player_y - choice_y
            abs_dist = abs(x_dist) + abs(y_dist)
            dist_dict.update({choice: abs_dist})
        if state == 'normal':
            min_value = min(dist_dict.values())
            min_key = []
            for key, value in dist_dict.items():
                if value == min_value:
                    min_key.append(key)
            self.x, self.y = random.choice(min_key)
            return self.x, self.y
        else:
            max_value = max(dist_dict.values())
            max_key = []
            for key, value in dist_dict.items():
                if value == max_value:
                    max_key.append(key)
            self.x, self.y = random.choice(max_key)
            return self.x, self.y