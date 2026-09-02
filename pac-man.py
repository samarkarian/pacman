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


if __name__ == "__main__":
    main()
