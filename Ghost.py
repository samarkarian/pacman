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
        self.renderer.start_pos = self.spawn
        self.renderer.target_pos = self.spawn
        self.state = "normal"
        self.renderer.state = "normal"

    def turn_update(self, player_pos, new_state, step_duration: int = 200,):

        if self.ai.respawn_count > 0:
            new_state = "dead"
        if new_state != self.state:
            self.state = new_state
            self.renderer.state = self.state

        old_pos = (self.posx, self.posy)

        self.posx, self.posy = self.ai.step(player_pos, state=self.state)

        self.renderer.start_move(old_pos, (self.posx, self.posy),
                                 step_duration)

    def load_sprites(self, asset_size):
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen, animation_speed: int,
               offset: Tuple[int, int] = (0, 0)):
        self.renderer.render(screen=screen, animation_speed=animation_speed,
                             offset=offset)


class GhostRenderer(Entity):
    def __init__(self, pos: Tuple[int, int], color):
        super().__init__(pos)
        self.color = color
        self.sprites: Dict[str, List[pygame.Surface]] = {
            "normal": [],
            "vulnerable": [],
            "end": [],
            "dead": [],
        }
        self.state = 'normal'

        self.start_pos: Tuple[int, int] = (int(pos[0]), int(pos[1]))
        self.target_pos: Tuple[int, int] = (int(pos[0]), int(pos[1]))
        self.move_start_time: int = pygame.time.get_ticks()
        self.step_duration_ms: int = 200

    def load_sprites(self, asset_size):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for state in self.sprites.keys():
                if state == 'normal':
                    for sprite in range(2):
                        self.sprites['normal'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_{self.color}/Ghost_{self.color}_{asset_size}/Ghost_{self.color}_{asset_size}_frame_{sprite}.png"))
                else:
                    for sprite in range(2):
                        self.sprites[state].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_neutral/Ghost_{state}/Ghost_{state}_{asset_size}/Ghost_{state}_{asset_size}_frame_{sprite}.png"))

            self.pixel_offset = asset_size

        except Exception as e:
            print(e)

    def start_move(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        duration_ms: int = 200,
    ) -> None:
        self.start_pos = from_pos
        self.target_pos = to_pos
        self.move_start_time = pygame.time.get_ticks()
        self.step_duration_ms = duration_ms

    def render(
        self,
        screen: pygame.Surface,
        animation_speed: int = 800,
        offset: Tuple[int, int] = (0, 0),
    ) -> None:
        now = pygame.time.get_ticks()

        elapsed = now - self.move_start_time
        t = min(1.0, elapsed / self.step_duration_ms) if self.step_duration_ms > 0 else 1.0

        interp_x = self.start_pos[0] + (self.target_pos[0] - self.start_pos[0]) * t
        interp_y = self.start_pos[1] + (self.target_pos[1] - self.start_pos[1]) * t

        draw_x = int(interp_x * self.pixel_offset) + offset[0]
        draw_y = int(interp_y * self.pixel_offset) + offset[1]

        frame_index = (now // animation_speed) % 2
        sprites_list = self.sprites.get(self.state, self.sprites["normal"])
        if sprites_list:
            screen.blit(sprites_list[frame_index], (draw_x, draw_y))


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
