from mazegenerator import MazeGenerator


class Maze:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def is_walkable(self, x, y) -> bool:

        print(grid)

def generate_maze(width, height, seed):

    try:
        mg = MazeGenerator(size=(width, height), perfect=False, seed=seed)
        return mg.maze
    except Exception as err:
        print(f"Error: could not generate maze ({err})")
        return None


def display_walls(grid):
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

    grid = generate_maze(4, 3, 42)

    for y in grid:
        print(y)

    if grid is not None:
        display_walls(grid)