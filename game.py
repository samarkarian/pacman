from json_loader import Config
from maze import Maze, generate_maze
from field import PlayField

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

    def start_level(self, level_index) -> bool:

        play_field = build_level(self.config, level_index)

        if play_field is None:
            return False
        self.field = play_field
        self.level_index = level_index

        return True

    def add_score(self, eaten: str | None) -> None:

        if eaten == 'pacgum':
            self.score += self.config.points_per_pacgum
        elif eaten == 'super_pacgum':
            self.score += self.config.points_per_super_pacgum

        return None

    def next_level(self) -> bool:

        return self.start_level(self.level_index + 1)


# if __name__ == "__main__":

#     grid = generate_maze(19, 19, 42)
#     conf = Config()
#     mz = Maze(grid)
#     pf = PlayField(mz)

#     level = build_level(conf, 0)
