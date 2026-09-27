import json
from typing import Any
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
)


def clamp_int(
        raw: Any, minimum: int | None,
        maximum: int | None, default: int, name: str) -> int:
    """Convert to int, clamped to [minimum, maximum], with a warning.

    Args:
        raw: value read in the config.
        minimum: lowest value, or None.
        maximum: highest value, or None.
        default: value used if raw is not a number.
        name: key name, for the warning.

    Returns:
        The value, clamped.
    """

    try:
        value = int(raw)
    except (TypeError, ValueError, OverflowError):
        print(f"Warning: {name} {raw} is not a number, "
              f"using {default} by default.")
        return default

    if maximum is not None and value > maximum:
        print(f"Warning: {name} {value} is too big, "
              f"using {maximum} by default.")
        return maximum
    elif minimum is not None and value < minimum:
        print(f"Warning: {name} {value} is too small, "
              f"using {minimum} by default.")
        return minimum
    else:
        return value


class Level(BaseModel):
    """Size of a level, clamped for the window and the generator."""

    width: int = 15
    height: int = 11

    @field_validator("width", mode="before")
    @classmethod
    def clamp_width(cls, value: Any) -> int:
        """Clamp the width between 14 and 23.

        Args:
            value: width read in the config.

        Returns:
            A width between 14 and 23.
        """
        return clamp_int(value, 14, 23, 15, 'width')

    @field_validator("height", mode="before")
    @classmethod
    def clamp_height(cls, value: Any) -> int:
        """Clamp the height between 10 and 21.

        Args:
            value: height read in the config.

        Returns:
            A height between 10 and 21.
        """
        return clamp_int(value, 10, 21, 11, 'height')


class Config(BaseModel):
    """Game configuration, with a default value for every key."""

    highscore_filename: str = 'scores.json'
    level: list[Level] = Field(
        default_factory=lambda: [Level() for _ in range(10)])
    lives: int = 3
    pacgum: int = 42
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 50
    points_per_ghost: int = 200
    seed: int = 42
    level_max_time: int = 90

    @field_validator(
        "pacgum",
        "points_per_pacgum",
        "points_per_super_pacgum",
        "points_per_ghost",
        mode="before",
    )
    @classmethod
    def clamp_points(cls, value: Any, info: ValidationInfo) -> int:
        """Refuse negative points.

        Args:
            value: value read in the config.
            info: pydantic info, gives the key name.

        Returns:
            The value, at least 0.
        """
        name = info.field_name
        assert name is not None
        default = cls.model_fields[name].default
        return clamp_int(value, 0, None, default, name)

    @field_validator("lives", mode="before")
    @classmethod
    def clamp_lives(cls, value: Any) -> int:
        """Require at least 1 life.

        Args:
            value: lives read in the config.

        Returns:
            The lives, at least 1.
        """
        return clamp_int(value, 1, None, 3, 'lives')

    @field_validator("level_max_time", mode="before")
    @classmethod
    def clamp_time(cls, value: Any) -> int:
        """Require at least 10 seconds per level.

        Args:
            value: time read in the config.

        Returns:
            The time in seconds, at least 10.
        """
        return clamp_int(value, 10, None, 90, 'level_max_time')

    @field_validator("seed", mode="before")
    @classmethod
    def clamp_seed(cls, value: Any) -> int:
        """Keep the seed if it is a number, or 42.

        Args:
            value: seed read in the config.

        Returns:
            The seed, as an int.
        """
        return clamp_int(value, None, None, 42, 'seed')

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def clamp_filename(cls, value: Any) -> str:
        """Keep the scores file name, or scores.json if it is empty.

        Args:
            value: file name read in the config.

        Returns:
            A non-empty file name.
        """
        if isinstance(value, str) and value.strip() != "":
            return value
        print(f"Warning: highscore_filename '{value}' is empty or not a "
              f"text, using scores.json by default.")
        return "scores.json"

    @field_validator("level", mode="before")
    @classmethod
    def clamp_level(cls, value: Any) -> Any:
        """Keep the valid levels, completed with 15x11 levels up to 10.

        Args:
            value: level list read in the config.

        Returns:
            At least 10 levels.
        """
        if not isinstance(value, list) or len(value) == 0:
            print("Warning: level is empty or not a list, "
                  "using 10 levels of 15x11 by default.")
            return [Level() for _ in range(10)]

        levels: list[Any] = []
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                print(f"Warning: level {index + 1} is not an object, "
                      f"using 15x11 by default.")
                levels.append(Level())
                continue
            for key in ("width", "height"):
                if key not in item:
                    default = Level.model_fields[key].default
                    print(f"Warning: level {index + 1} has no {key}, "
                          f"using {default} by default.")
            levels.append(item)

        if len(levels) < 10:
            print(f"Warning: {len(levels)} level(s) given, the game needs 10, "
                  f"adding 15x11 levels.")
            for _ in range(10 - len(levels)):
                levels.append(Level())
        return levels


def json_load(content: str) -> Config:
    """Parse the JSON config, skipping # lines; defaults if invalid.

    Args:
        content: text of the config file.

    Returns:
        The validated configuration.
    """

    lines = content.splitlines()

    n_lines = []
    for line in lines:
        if not line.lstrip().startswith('#'):
            n_lines.append(line)

    cleaned = '\n'.join(n_lines)

    try:
        obj = json.loads(cleaned)
        if isinstance(obj, dict):
            for key in Config.model_fields:
                if key not in obj:
                    print(f"Warning: {key} is missing, "
                          f"using the default value.")
        return Config.model_validate(obj)
    except (json.JSONDecodeError, ValidationError):
        print("Invalid config file, using defaults.")
        return Config()
