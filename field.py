from maze import Maze
from pacgums import Pacgum
# from maze import generate_maze


class PlayField:
    def __init__(self, maze: Maze) -> None:

        corners = maze.corners()
        self.maze = maze
        self.player_spawn = maze.center()
        self.super_pacgums: dict = {}
        self.ghost_spawns = corners

        self.pacgums: dict = {}
        self.generate_pacgums()

    def generate_pacgums(self):
        for c in self.maze.corners():
            self.super_pacgums[c] = (Pacgum(pos=(c), gumtype='super_pacgum'))
        for y in range(self.maze.height):
            for x in range(self.maze.width):
                if not self.maze.is_walkable(x, y):
                    continue
                if (x, y) in self.super_pacgums:
                    continue
                if (x, y) == self.player_spawn:
                    continue
                self.pacgums[(x, y)] = (Pacgum(pos=(x, y), gumtype='Pacgum'))

    def eat_pacgum(self, x: int, y: int) -> bool:

        pacgum = self.pacgums.pop((x, y), None)
        if pacgum is not None:
            # Tu as directement accès à l'instance pacgum ici
            return True
        return False

    def eat_super_pacgum(self, x: int, y: int) -> bool:

        super_pacgum = self.super_pacgums.pop((x, y), None)
        if super_pacgum is not None:
            # Tu as directement accès à l'instance pacgum ici
            return True
        return False

    def is_level_complete(self) -> bool:

        if not self.pacgums and not self.super_pacgums:
            return True
        return False
