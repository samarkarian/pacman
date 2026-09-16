import re
import json
from typing import Any


def player_writing() -> None:
    pass


def valid_name_score(name: str, score: int) -> bool:

    if not isinstance(name, str):
        return False

    if not isinstance(score, int) or isinstance(score, bool):
        return False

    if name.isspace():
        return False

    if not re.fullmatch("^[A-Za-z0-9 ]{1,10}$", name) or score < 0:
        return False

    return True


def sorted_value(scores: list[dict[str, Any]]) -> list[dict[str, Any]]:

    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    return sorted_scores[:10]


def scores_load(file_path: str) -> list[dict[str, Any]]:

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except OSError:
        print(f"Warning: cannot read highscore file '{file_path}'")
        return []
    except ValueError:
        print(f"Warning: highscore file '{file_path}' is not valid JSON")
        return []

    if not isinstance(data, list):
        print(f"Warning: highscore file '{file_path}' must contain a list")
        return []

    scores: list[dict[str, Any]] = []
    for player in data:
        if not isinstance(player, dict):
            continue
        name: Any = player.get('name')
        score: Any = player.get('score')
        if valid_name_score(name, score):
            scores.append({'name': name, 'score': score})

    return sorted_value(scores)


def scores_add(scores: list[dict[str, Any]], name: str, score: int) -> list[dict[str, Any]]:

    if not valid_name_score(name, score):
        return scores

    scores_cp = scores.copy()
    scores_cp.append({'name': name, 'score': score})

    return sorted_value(scores_cp)

def scores_save():
    pass


if __name__ == '__main__':

    scores_load('./scores.json')
