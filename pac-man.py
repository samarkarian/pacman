from game_loop import GameLoop
import sys
from json_loader import json_load
from game import build_level

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
    field = build_level(config, 0)
    if field is None:
        print("Error: could not build level")
        sys.exit(1)

    try:
        game = GameLoop(field=field)
        game.run()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as err:
        print(err)

    return None


if __name__ == "__main__":
    main()
