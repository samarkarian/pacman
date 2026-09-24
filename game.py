from json_loader import Config
from maze import Maze, generate_maze
from field import PlayField
from Ghost import Ghost
from player import Player
from high_score import scores_load


def build_level(config: Config, level_index: int) -> PlayField | None:

    if not 0 <= level_index < len(config.level):
        return None

    level = config.level[level_index]
    seed = config.seed if level_index == 0 else 0
    grid = generate_maze(level.width, level.height, seed)
    if grid is None:
        return None
    maze = Maze(grid)

    return PlayField(maze)

class Game:
    def __init__(self, config: Config) -> None:

        self.config = config
        self.level_index = 0
        self.score = 0
        self.lives = config.lives
        self.field = None
        self.ghosts = []
        self.player = None
        self.vulnerable_count = 0
        self.time_left = 0
        self.rank = scores_load(config.highscore_filename)

        self.ghost_timer_ms: int = 0
        self.player_timer_ms: int = 0
        self.player_step_ms: int = 150
        self.ghost_step_ms: int = 200

        self.vulnerable_seconds: int = 6
        self.vulnerable_steps: int = (self.vulnerable_seconds * 1000
                                      // self.ghost_step_ms)

        self.respawn_seconds: int = 5
        self.respawn_steps: int = (self.respawn_seconds * 1000
                                   // self.ghost_step_ms)

        self.cheat = False
        self.invincible = False
        self.ghosts_frozen = False

    def start_level(self, level_index) -> bool:

        play_field = build_level(self.config, level_index)

        if play_field is None:
            return False
        self.field = play_field
        self.player = Player(play_field)
        self.vulnerable_count = 0
        self.time_left = self.config.level_max_time

        self.ghosts = []
        ghost_colors = ['cyan', 'red', 'orange', 'pink']
        ghost_behaviors = ['follow', 'follow', 'random', 'copy']
        for spawn, color, behavior in zip(play_field.ghost_spawns, ghost_colors, ghost_behaviors):
            self.ghosts.append(Ghost(play_field, spawn, color, behavior))

        self.level_index = level_index
        self.player.set_direction('S')

        return True

    def eaten_effect(self, eaten: str | None) -> None:

        if eaten == 'pacgum':
            self.score += self.config.points_per_pacgum
        elif eaten == 'super_pacgum':
            self.score += self.config.points_per_super_pacgum
            self.vulnerable_count = self.vulnerable_steps
        return None

    def next_level(self) -> bool:

        return self.start_level(self.level_index + 1)

    def skip_level(self) -> None:

        self.field.pacgums.clear()
        self.field.super_pacgums.clear()
        if self.level_index < len(self.config.level) - 1:
            self.next_level()

    def reset(self) -> bool:

        self.score = 0
        self.lives = self.config.lives
        self.cheat = False
        self.invincible = False
        self.ghosts_frozen = False

        return self.start_level(0)

    def is_over(self) -> bool:

        if self.lives <= 0:
            return True
        if self.field is None:
            return False
        if self.time_left <= 0:
            return True

        last_index = len(self.config.level) - 1
        if self.level_index == last_index:
            return self.field.is_level_complete()
        return False

    def check_collision(self, player) -> bool:

        for ghost in self.ghosts:
            if ghost.ai.respawn_count != 0:
                continue

            if (ghost.posx, ghost.posy) == (player.posx, player.posy):
                if self.vulnerable_count != 0:
                    self.score += self.config.points_per_ghost
                    ghost.reset_position()
                    ghost.ai.start_respawn(self.respawn_steps)
                elif self.invincible:
                    continue
                else:
                    self.lives -= 1
                    if self.lives <= 0:
                        return True
                    player.reset_position()
                    for ghos in self.ghosts:
                        ghos.reset_position()

                    self.vulnerable_count = 0
                return True

        return False

    def step_ghosts(self) -> None:
        if self.vulnerable_count > 0:
            self.vulnerable_count -= 1

        for ghost in self.ghosts:
            if ghost.ai.respawn_count > 0:
                new_state = "dead"
            elif self.vulnerable_count == 0:
                new_state = "normal"
            elif self.vulnerable_count <= (self.vulnerable_steps / 3) and self.vulnerable_count % 2 == 0:
                new_state = "end"
            else:
                new_state = "vulnerable"

            if self.ghosts_frozen:
                ghost.state = new_state
                ghost.renderer.state = new_state
                continue

            ghost.turn_update((self.player.posx, self.player.posy), new_state, self.ghost_step_ms, self.player.controller.next_direction)

    def step_player(self) -> None:
        self.player.turn_update(self.player_step_ms)

        eaten = None
        if self.field.eat_pacgum(self.player.posx, self.player.posy):
            eaten = "pacgum"
        elif self.field.eat_super_pacgum(self.player.posx, self.player.posy):
            eaten = "super_pacgum"

        if eaten:
            self.eaten_effect(eaten)
            if self.field.is_level_complete():
                self.next_level()

    def update(self, dt_ms: int) -> None:
        if self.time_left > 0:
            self.time_left -= dt_ms / 1000
        if self.field is None or self.player is None or self.is_over():
            return

        self.player_timer_ms += dt_ms

        can_start_moving = (
            self.player.controller.direction is None
            and self.player.controller.next_direction is not None
            and self.field.maze.can_move(
                self.player.posx, self.player.posy, self.player.controller.next_direction
            )
        )

        if can_start_moving or self.player_timer_ms >= self.player_step_ms:
            if can_start_moving:
                self.player_timer_ms = 0
            else:
                self.player_timer_ms -= self.player_step_ms

            self.step_player()
            if self.check_collision(self.player):
                return

        self.ghost_timer_ms += dt_ms
        if self.ghost_timer_ms >= self.ghost_step_ms:
            self.ghost_timer_ms -= self.ghost_step_ms
            self.step_ghosts()
            if self.check_collision(self.player):
                return

    def victory(self) -> bool:

        if self.level_index == len(self.config.level) - 1:
            if self.is_over():
                if self.lives > 0 and self.time_left > 0:
                    return True
        return False
