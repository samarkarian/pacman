from mazegenerator import MazeGenerator
from game_loop import GameLoop
import sys


def main() -> None:
    try:
        maze_gen = MazeGenerator(
            size=(15,15),
            entry_cell=(0,0),
            exit_cell=(2,4),
            perfect=True,
            seed=42)

        maze_gen.generate()
        game = GameLoop(maze_gen)
        game.run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
