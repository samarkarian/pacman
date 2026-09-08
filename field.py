from maze import Maze
<<<<<<< HEAD
from maze import generate_maze
=======
# from maze import generate_maze
>>>>>>> origin/main


class PlayField:
    def __init__(self, maze: Maze) -> None:

        corners = maze.corners()
        self.maze = maze
        self.player_spawn = maze.center()
        self.super_pacgums = set(corners)
        self.ghost_spawns = corners

        self.pacgums = set()
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if not self.maze.is_walkable(x, y):
                    continue
                if (x, y) in self.super_pacgums:
                    continue
                if (x, y) == self.player_spawn:
                    continue
                self.pacgums.add((x, y))

    def eat_pacgum(self, x: int, y: int) -> bool:

        if (x, y) in self.pacgums:
            self.pacgums.remove((x, y))
            return True
        return False

    def eat_super_pacgum(self, x: int, y: int) -> bool:

        if (x, y) in self.super_pacgums:
            self.super_pacgums.remove((x, y))
            return True
        return False

    def is_level_complete(self) -> bool:

<<<<<<< HEAD
        if bool(self.pacgums) is False:
=======
        if not self.pacgums and not self.super_pacgums:
>>>>>>> origin/main
            return True
        return False


<<<<<<< HEAD
if __name__ == "__main__":

    grid = generate_maze(19, 19, 42)
    if grid is not None:
        mz = Maze(grid)
        pf = PlayField(mz)

        print(pf.player_spawn)
        print(pf.ghost_spawns)
        print(mz.is_walkable(9, 9))
        print(pf.pacgums)
        print(pf.eat_pacgum(18, 8))
        print(pf.is_level_complete())
=======
# if __name__ == "__main__":

#     grid = generate_maze(19, 19, 42)
#     if grid is not None:
#         mz = Maze(grid)
#         pf = PlayField(mz)

#         print(pf.player_spawn)
#         print(pf.ghost_spawns)
#         print(mz.is_walkable(9, 9))
#         print(pf.pacgums)
#         print(pf.eat_pacgum(18, 8))
#         print(pf.is_level_complete())
>>>>>>> origin/main
