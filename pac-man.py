from game_loop import GameLoop
import os
import sys
from json_loader import json_load
from game import Game


def main() -> None:
    """Read the config file given as argument, then start the game."""

    try:
        if len(sys.argv) == 2 and sys.argv[1].endswith('.json'):
            path = sys.argv[1]
        else:
            print('Usage: python3 pac-man.py config.json')
            sys.exit(1)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        print(f"Error: cannot read config file '{path}'")
        sys.exit(1)

    game_dir = getattr(sys, "_MEIPASS", os.path.dirname(
        os.path.abspath(__file__)))
    os.chdir(game_dir)

    config = json_load(content)
    game = Game(config)
    if not game.start_level(0):
        print("Error: could not build level")
        sys.exit(1)

    try:
        loop = GameLoop(game=game)
        loop.run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as err:
        print(f"Error: {err}")
        sys.exit(1)

    return None


if __name__ == "__main__":
    main()
