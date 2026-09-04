from mazegenerator import MazeGenerator


class Maze:
    def __init__(self, grid: list[list[int]]) -> None:
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def is_walkable(self, x: int, y: int) -> bool:

        if not 0 <= x < self.width or not 0 <= y < self.height:
            return False

        if self.grid[y][x] == 15:
            return False

        return True

    def can_move(self, x: int, y: int, direction: str) -> bool:

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

        dir_dict = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        neighbors_lst = []
        for dir in dir_dict:
            neighbor = self.can_move(x, y, dir)
            if neighbor is True:
                dx, dy = dir_dict[dir]
                neighbors_lst.append((x + dx, y + dy))

        return neighbors_lst

    def center(self) -> tuple[int, int]:
        # Pas encore pris en compte si case 15 ou pas dans la limite du maze
        return (self.width // 2, self.height // 2)

    def corners(self) -> list[tuple[int, int]]:

        return [
            (0, 0),
            (self.width - 1, 0),
            (0, self.height - 1),
            (self.width - 1, self.height - 1)
        ]


def generate_maze(
    width: int,
    height: int,
    seed: int,
) -> list[list[int]] | None:

    try:
        mg = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        maze: list[list[int]] = mg.maze
        return maze
    except Exception as err:
        print(f"Error: could not generate maze ({err})")
        return None


def display_walls(grid: list[list[int]]) -> None:
    height = len(grid)
    width = len(grid[0])
    lines = []
    for y in range(height):
        roof = ""
        for x in range(width):
            roof += "+"
            roof += "-" if grid[y][x] & 1 else " "
        roof += "+"
        lines.append(roof)
        body = ""
        for x in range(width):
            body += "|" if grid[y][x] & 8 else " "
            body += " "
        body += "|" if grid[y][width - 1] & 2 else " "
        lines.append(body)
    floor = ""
    for x in range(width):
        floor += "+"
        floor += "-" if grid[height - 1][x] & 4 else " "
    floor += "+"
    lines.append(floor)
    print("\n".join(lines))


if __name__ == "__main__":

    grid = generate_maze(19, 19, 42)

    if grid is not None:
        for row in grid:
            print(row)

        # display_walls(grid)

        mz = Maze(grid)

        x = 1
        y = 1

        north = 'N'
        east = 'E'
        south = 'S'
        west = 'W'

        mz.is_walkable(x, y)
        # print(mz.can_move(x, y, north))
        # print(mz.neighbors(x, y))
        # print(mz.center())
        # print(mz.corners())
