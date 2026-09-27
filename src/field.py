from src.maze import Maze
from src.pacgums import Pacgum


class PlayField:
    """A level's play field: maze, pac-gums and spawn points."""

    def __init__(self, maze: Maze) -> None:
        """Build the play field and its pac-gums from the maze.

        Args:
            maze: maze of the level.
        """

        corners = maze.corners()
        self.maze = maze
        spawn = maze.center()
        self.player_spawn: tuple[int, int] = (
            spawn if spawn is not None else (0, 0))
        self.super_pacgums: dict[tuple[int, int], Pacgum] = {}
        self.ghost_spawns = corners

        self.pacgums: dict[tuple[int, int], Pacgum] = {}
        self.generate_pacgums()

    def generate_pacgums(self) -> None:
        """Put a super pac-gum in each corner, a pac-gum everywhere else."""
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
        """Remove the pac-gum on this cell; return True if there was one.

        Args:
            x: column of the cell.
            y: row of the cell.

        Returns:
            True if a pac-gum was eaten.
        """

        pacgum = self.pacgums.pop((x, y), None)
        if pacgum is not None:
            return True
        return False

    def eat_super_pacgum(self, x: int, y: int) -> bool:
        """Remove the super pac-gum on this cell; True if there was one.

        Args:
            x: column of the cell.
            y: row of the cell.

        Returns:
            True if a super pac-gum was eaten.
        """

        super_pacgum = self.super_pacgums.pop((x, y), None)
        if super_pacgum is not None:
            return True
        return False

    def is_level_complete(self) -> bool:
        """Return True when no pac-gum is left.

        Returns:
            True if the level is cleared.
        """

        if not self.pacgums and not self.super_pacgums:
            return True
        return False
