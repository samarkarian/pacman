import functools
import pygame


@functools.lru_cache(maxsize=None)
def load_image(path: str) -> pygame.Surface:
    """Load an image once, then return it from the cache."""
    return pygame.image.load(path)
