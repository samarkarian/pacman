import re
import json
from typing import Any


def valid_name_score(name: str, score: int) -> bool:
    """Check the name (1-10 letters, digits, spaces) and a score >= 0.

    Args:
        name: player name.
        score: final score.

    Returns:
        True if both are valid.
    """

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
    """Sort the scores from best to worst and keep the top 10.

    Args:
        scores: list of {'name', 'score'}.

    Returns:
        The 10 best scores, best first.
    """

    sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)
    return sorted_scores[:10]


def scores_load(file_path: str) -> list[dict[str, Any]]:
    """Read the scores file; empty list if missing or invalid.

    Args:
        file_path: path of the scores file.

    Returns:
        The valid scores, sorted.
    """

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


def scores_add(
        scores: list[dict[str, Any]],
        name: str, score: int) -> list[dict[str, Any]]:
    """Return a new top 10 list including this score.

    Args:
        scores: current top 10.
        name: player name.
        score: final score.

    Returns:
        The new top 10 (unchanged if invalid).
    """

    if not valid_name_score(name, score):
        return scores

    scores_cp = scores.copy()
    scores_cp.append({'name': name, 'score': score})

    return sorted_value(scores_cp)


def scores_save(file_path: str, scores: list[dict[str, Any]]) -> bool:
    """Write the top 10 to the file; return False if writing fails.

    Args:
        file_path: path of the scores file.
        scores: scores to write.

    Returns:
        True if the file was written.
    """

    scores = sorted_value(scores)

    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(scores, file, indent=4)
    except OSError:
        print(f"Warning: cannot save highscore file '{file_path}'")
        return False

    return True
