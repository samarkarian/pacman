from json_loader import Config
from maze import Maze, generate_maze
from field import PlayField
from Ghost import Ghost
from player import Player

GHOST_STEP_MS = 200
VULNERABLE_SECONDS = 6
VULNERABLE_STEPS = VULNERABLE_SECONDS * 1000 // GHOST_STEP_MS

RESPAWN_SECONDS = 5
RESPAWN_STEPS = RESPAWN_SECONDS * 1000 // GHOST_STEP_MS

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

    def start_level(self, level_index) -> bool:

        play_field = build_level(self.config, level_index)

        if play_field is None:
            return False
        self.field = play_field
        self.player = Player(play_field)
        self.vulnerable_count = 0
        self.time_left = (self.config.level_max_time * 1000
                          // GHOST_STEP_MS)

        self.ghosts = []
        # ghost_colors = ['cyan', 'red', 'orange', 'pink']
        ghost_colors_test = ['cyan', 'cyan', 'cyan', 'cyan']
        for spawn, color in zip(play_field.ghost_spawns, ghost_colors_test):
            self.ghosts.append(Ghost(play_field, spawn, color))

        self.level_index = level_index

        return True

    def eaten_effect(self, eaten: str | None) -> None:

        if eaten == 'pacgum':
            self.score += self.config.points_per_pacgum
        elif eaten == 'super_pacgum':
            self.score += self.config.points_per_super_pacgum
            self.vulnerable_count = VULNERABLE_STEPS

        return None

    def next_level(self) -> bool:

        return self.start_level(self.level_index + 1)

    def reset(self) -> bool:

        self.score = 0
        self.lives = self.config.lives

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

        for idx, ghost in enumerate(self.ghosts):
            if ghost.ai.respawn_count != 0:
                continue
            if (ghost.posx, ghost.posy) == (player.posx, player.posy):
                if self.vulnerable_count != 0:
                    self.score += self.config.points_per_ghost
                    ghost.posx, ghost.posy = self.field.ghost_spawns[idx]
                    ghost.ai.start_respawn(RESPAWN_STEPS)
                else:
                    self.lives -= 1
                    player.posx, player.possy = self.field.player_spawn
                    player.controller.direction = None
                    player.controller.next_direction = None
                    spawns = self.field.ghost_spawns
                    for caught, spawn in zip(self.ghosts, spawns):
                        caught.x, caught.y = spawn
                return True

        return False

    def step_ghosts(self) -> None:
        """Appelée uniquement toutes les GHOST_STEP_MS millisecondes."""
        if self.field is None or self.player is None or self.is_over():
            return

        # 1. Mise à jour des timers
        if self.time_left > 0:
            self.time_left -= 1
        if self.vulnerable_count > 0:
            self.vulnerable_count -= 1

        # 2. Déplacement de l'IA des fantômes
        for ghost in self.ghosts:
            ghost.turn_update((self.player.posx, self.player.posy), self.vulnerable_count)

        # 3. Vérification des collisions après le saut des fantômes
        self.check_collision(self.player)

    def update(self) -> None:
        """Appelée à chaque frame (ou tick de scène)."""
        if self.field is None or self.player is None or self.is_over():
            return

        # 1. Déplacement du joueur
        self.player.turn_update()

        # 2. Vérification immédiate de collision (si le joueur fonce sur un fantôme)
        if self.check_collision(self.player):
            return

        eaten = None
        if self.field.eat_pacgum(self.player.posx, self.player.posy):
            eaten = "pacgum"
        if self.field.eat_super_pacgum(self.player.posx, self.player.posy):
            eaten = "super_pacgum"
        if eaten:
            self.eaten_effect(eaten)
            if self.field.is_level_complete():
                self.next_level()
