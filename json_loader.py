import json
from typing import Any
from pydantic import (
    BaseModel,
    Field,
    ValidationError,
    ValidationInfo,
    field_validator,
)


def clamp_int(raw: Any, minimum: int, default: int) -> int:

    try:
        value = int(raw)
    except (TypeError, ValueError):
        return default
    return value if value >= minimum else default


class Level(BaseModel):

    width: int = 19
    height: int = 19

    @field_validator("width", mode="before")
    @classmethod
    def clamp_width(cls, value: Any) -> int:
        return clamp_int(value, 14, 19)

    @field_validator("height", mode="before")
    @classmethod
    def clamp_height(cls, value: Any) -> int:
        return clamp_int(value, 10, 19)


class Config(BaseModel):

    highscore_filename: str = 'scores.json'
    level: list[Level] = Field(default_factory=lambda: [Level()])
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
        name = info.field_name
        assert name is not None
        default = cls.model_fields[name].default
        return clamp_int(value, 0, default)

    @field_validator("lives", mode="before")
    @classmethod
    def clamp_lives(cls, value: Any) -> int:
        return clamp_int(value, 1, 3)

    @field_validator("level_max_time", mode="before")
    @classmethod
    def clamp_time(cls, value: Any) -> int:
        return clamp_int(value, 10, 90)

    @field_validator("highscore_filename", mode="before")
    @classmethod
    def clamp_filename(cls, value: Any) -> str:
        if isinstance(value, str) and value.strip() != "":
            return value
        return "scores.json"

    @field_validator("level", mode="before")
    @classmethod
    def clamp_level(cls, value: Any) -> Any:
        if isinstance(value, list) and len(value) > 0:
            return value
        return [Level()]


def json_load(content: str) -> Config:

    lines = content.splitlines()

    n_lines = []
    for line in lines:
        if not line.lstrip().startswith('#'):
            n_lines.append(line)

    cleaned = '\n'.join(n_lines)

    try:
        obj = json.loads(cleaned)
        return Config.model_validate(obj)
    except (json.JSONDecodeError, ValidationError):
        print("Invalid config file, using defaults.")
        return Config()
