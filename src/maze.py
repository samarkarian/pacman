from mazegenerator import MazeGenerator


class Maze:
    """Maze grid: 4 wall bits per cell (N=1, E=2, S=4, W=8)."""

    DIRECTIONS: dict[str, tuple[int, int]] = {
        'N': (0, -1),
        'E': (1, 0),
        'S': (0, 1),
        'W': (-1, 0)
    }

    def __init__(self, grid: list[list[int]]) -> None:
        """Store the grid and its size."""
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def is_walkable(self, x: int, y: int) -> bool:
        """Return True if the cell exists and is not a closed block."""

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return False

        if self.grid[y][x] == 15:
            return False

        return True

    def can_move(self, x: int, y: int, direction: str) -> bool:
        """Return True if one can move from (x, y) in this direction."""

        walkable = self.is_walkable(x, y)
        if walkable is False:
            return False

        if direction == 'N':
            if self.grid[y][x] & 1:
                return False
            walkable = self.is_walkable(x, y - 1)
            if walkable is False:
                return False
            return True

        if direction == 'E':
            if self.grid[y][x] & 2:
                return False
            walkable = self.is_walkable(x + 1, y)
            if walkable is False:
                return False
            return True

        if direction == 'S':
            if self.grid[y][x] & 4:
                return False
            walkable = self.is_walkable(x, y + 1)
            if walkable is False:
                return False
            return True

        if direction == 'W':
            if self.grid[y][x] & 8:
                return False
            walkable = self.is_walkable(x - 1, y)
            if walkable is False:
                return False
            return True

        return False

    def neighbors(self, x: int, y: int) -> list[tuple[int, int]]:
        """Return the reachable neighbour cells of (x, y)."""

        neighbors_lst = []
        for dir in self.DIRECTIONS:
            neighbor = self.can_move(x, y, dir)
            if neighbor is True:
                dx, dy = self.DIRECTIONS[dir]
                neighbors_lst.append((x + dx, y + dy))

        return neighbors_lst

    def center(self) -> tuple[int, int] | None:
        """Return the walkable cell closest to the centre, or None."""

        cy, cx = self.height // 2, self.width // 2

        if self.is_walkable(cx, cy):
            return (cx, cy)

        cases = []
        for y in range(self.height):
            for x in range(self.width):
                cases.append((x, y))

        cases = sorted(
            cases,
            key=lambda c: abs(c[0] - cx) + abs(c[1] - cy)
        )

        for x, y in cases:
            if self.is_walkable(x, y):
                return (x, y)

        return None

    def corners(self) -> list[tuple[int, int]]:
        """Return the 4 corners of the grid."""

        return [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1)
        ]

    def next_cell(self, pos_x: int, pos_y: int,
                  direction: str) -> tuple[int, int]:
        """Return the next cell in this direction (same cell if unknown)."""

        if direction not in self.DIRECTIONS:
            return (pos_x, pos_y)

        dx, dy = self.DIRECTIONS[direction]
        return (pos_x + dx, pos_y + dy)


def generate_maze(
    width: int,
    height: int,
    seed: int,
) -> list[list[int]] | None:
    """Generate the grid with the A-Maze-ing package; None on error."""

    try:
        mg = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        maze: list[list[int]] = mg.maze
        return maze
    except Exception as err:
        print(f"Error: could not generate maze ({err})")
        return None
