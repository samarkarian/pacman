import functools
import pygame


@functools.lru_cache(maxsize=None)
def load_image(path: str) -> pygame.Surface:
    """Load an image once, then return it from the cache.

    Args:
        path: image path, from the game folder.

    Returns:
        The loaded image.
    """
    return pygame.image.load(path)
