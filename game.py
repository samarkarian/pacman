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

# if __name__ == "__main__":

#     grid = generate_maze(19, 19, 42)
#     conf = Config()
#     mz = Maze(grid)
#     pf = PlayField(mz)

#     level = build_level(conf, 0)
