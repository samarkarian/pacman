import functools
import pygame


@functools.lru_cache(maxsize=None)
def load_image(path: str) -> pygame.Surface:
    return pygame.image.load(path)
