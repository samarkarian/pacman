from maze import Maze


class Player:
    def __init__(self, field) -> None:

        self.field = field
        self.x, self.y = field.player_spawn
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
            if self.field.eat_pacgum(self.x, self.y):
                return "pacgum"
            if self.field.eat_super_pacgum(self.x, self.y):
                return "super_pacgum"

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
