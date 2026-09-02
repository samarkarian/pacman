from mazegenerator import MazeGenerator
from game_loop import GameLoop
import sys
from json_loader import json_load
import sys


def main() -> None:

    try:
        if len(sys.argv) == 2 and sys.argv[1].endswith('.json'):
            path = sys.argv[1]
        else:
            print('Usage: python3 pac-man.py config.json')
            sys.exit(1)
        with open(path, 'r') as f:
            content = f.read()
    except Exception:
        print(f"Error: cannot read config file '{path}'")
        sys.exit(1)

    config = json_load(content)

    return None


# def main() -> None:
#     try:
#         maze_gen = MazeGenerator(
#             size=(15,15),
#             entry_cell=(0,0),
#             exit_cell=(2,4),
#             perfect=True,
#             seed=42)

#         maze_gen.generate()
#         game = GameLoop(maze_gen)
#         game.run()
#     except KeyboardInterrupt:
#         sys.exit(1)
#     except Exception as e:
#         print(e)

if __name__ == "__main__":
    main()
