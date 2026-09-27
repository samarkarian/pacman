from src.display_abstractmethods import Entity
import pygame
from src.sprite_cache import load_image
import random
from typing import Tuple, Dict, List
from src.field import PlayField


class Ghost:
    """Ghost: links its AI (ai) and its display (renderer)."""

    def __init__(self, play_field: PlayField, spawn: Tuple[int, int],
                 color: str, behavior: str) -> None:
        """Create the ghost in its corner, with its colour and AI.

        Args:
            play_field: field of the level.
            spawn: corner cell.
            color: 'cyan', 'red', 'orange' or 'pink'.
            behavior: 'follow', 'random' or 'copy'.
        """
        self.ai = GhostAI(play_field, spawn, behavior)
        self.renderer = GhostRenderer(spawn, color)
        self.posx, self.posy = spawn[0], spawn[1]
        self.state = 'normal'
        self.spawn = spawn

    def reset_position(self) -> None:
        """Send the ghost back to its corner, in the normal state."""
        self.posx, self.posy = self.spawn
        self.ai.reset(self.spawn)
        self.renderer.posx, self.renderer.posy = self.spawn
        self.renderer.start_pos = self.spawn
        self.renderer.target_pos = self.spawn
        self.state = "normal"
        self.renderer.state = "normal"

    def turn_update(self, player_pos: Tuple[int, int], new_state: str,
                    step_duration: int = 200,
                    direction: str | None = None) -> None:
        """Update the state (colour), move one cell and start the slide.

        Args:
            player_pos: Pac-Man's cell.
            new_state: 'normal', 'vulnerable', 'end' or 'dead'.
            step_duration: slide duration, in ms.
            direction: Pac-Man's wanted direction.
        """

        if self.ai.respawn_count > 0:
            new_state = "dead"
        if new_state != self.state:
            self.state = new_state
            self.renderer.state = self.state

        old_pos = (self.posx, self.posy)

        self.posx, self.posy = self.ai.step(player_pos, state=self.state,
                                            direction=direction)

        self.renderer.start_move(old_pos, (self.posx, self.posy),
                                 step_duration)

    def load_sprites(self, asset_size: int) -> None:
        """Load the ghost's images for this size.

        Args:
            asset_size: sprite size in pixels (32 or 64).
        """
        self.renderer.load_sprites(asset_size=asset_size)

    def render(self, screen: pygame.Surface, animation_speed: int,
               offset: Tuple[int, int] = (0, 0)) -> None:
        """Draw the ghost.

        Args:
            screen: surface to draw on.
            animation_speed: time between two frames, in ms.
            offset: (x, y) of the maze on the screen, in pixels.
        """
        self.renderer.render(screen=screen, animation_speed=animation_speed,
                             offset=offset)


class GhostRenderer(Entity):
    """Ghost display: one pair of frames per state."""

    def __init__(self, pos: Tuple[int, int], color: str) -> None:
        """Prepare the image lists of every state.

        Args:
            pos: starting cell.
            color: ghost colour.
        """
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

    def load_sprites(self, asset_size: int) -> None:
        """Load the frames: own colour when normal, neutral otherwise.

        Args:
            asset_size: sprite size in pixels (32 or 64).
        """
        color = self.color
        try:
            for state in self.sprites.keys():
                self.sprites[state].clear()
                if state == 'normal':
                    folder = (f"sprites/Entities/Ghost/Ghost_{color}/"
                              f"Ghost_{color}_{asset_size}/"
                              f"Ghost_{color}_{asset_size}")
                else:
                    folder = (f"sprites/Entities/Ghost/Ghost_neutral/"
                              f"Ghost_{state}/Ghost_{state}_{asset_size}/"
                              f"Ghost_{state}_{asset_size}")
                for sprite in range(2):
                    self.sprites[state].append(
                        load_image(f"{folder}_frame_{sprite}.png"))

            self.pixel_offset = asset_size

        except Exception as e:
            print(e)

    def start_move(
        self,
        from_pos: Tuple[int, int],
        to_pos: Tuple[int, int],
        duration_ms: int = 200,
    ) -> None:
        """Start a slide from from_pos to to_pos lasting duration_ms.

        Args:
            from_pos: cell left.
            to_pos: cell reached.
            duration_ms: slide duration, in ms.
        """
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
        """Draw the ghost at its current position along the slide.

        Args:
            screen: surface to draw on.
            animation_speed: time between two frames, in ms.
            offset: (x, y) of the maze on the screen, in pixels.
        """
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
        sprites_list = self.sprites.get(self.state, self.sprites["normal"])
        if sprites_list:
            screen.blit(sprites_list[frame_index], (draw_x, draw_y))


class GhostAI:
    """Choose a ghost's next cell according to its behaviour."""

    def __init__(self, field: PlayField, spawn: Tuple[int, int],
                 behavior: str) -> None:
        """Place the AI on spawn with its behaviour.

        Args:
            field: field of the level.
            spawn: corner cell.
            behavior: 'follow', 'random' or 'copy'.
        """

        self.field = field
        self.x, self.y = spawn
        self.behavior = behavior
        self.previous: Tuple[int, int] | None = None
        self.respawn_count = 0

    def reset(self, spawn: Tuple[int, int]) -> None:
        """Put the ghost back on spawn and cancel its waiting time.

        Args:
            spawn: corner cell.
        """
        self.x, self.y = spawn
        self.previous = None
        self.respawn_count = 0

    def start_respawn(self, steps: int) -> None:
        """Keep the ghost still for the given steps (after being eaten).

        Args:
            steps: number of steps to wait.
        """

        self.respawn_count = steps

    def step(self, player_pos: Tuple[int, int], state: str,
             direction: str | None) -> Tuple[int, int]:
        """Return the next cell: chase when normal, flee otherwise.

        'follow' gets closer to Pac-Man, 'random' picks at random, 'copy'
        follows Pac-Man's direction. No U-turn unless in a dead end.

        Args:
            player_pos: Pac-Man's cell.
            state: ghost state ('normal' = chase).
            direction: Pac-Man's wanted direction.

        Returns:
            The new (x, y) cell.
        """
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
            if self.behavior == 'random':
                self.x, self.y = random.choice(choices)
            elif self.behavior == 'copy':
                if (direction is not None
                        and maze.can_move(self.x, self.y, direction)):
                    self.x, self.y = maze.next_cell(self.x, self.y, direction)
                else:
                    self.x, self.y = random.choice(choices)
            elif self.behavior == 'follow':
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
