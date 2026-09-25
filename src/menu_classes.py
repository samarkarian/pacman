from typing import Any, List, Optional, Tuple, Dict, Callable
from src.scene import SceneID
import pygame
from abc import ABC, abstractmethod


class UIButton:
    """Menu button with two frames: normal and selected.

    Runs its action when triggered; add it to a page with
    self.buttons.append().
    """
    def __init__(
        self,
        name: str,
        pos: Tuple[int, int],
        action: Callable[[], Optional[SceneID]],
        asset_size: int = 64,
    ) -> None:
        """Create the button and load its 2 frames."""
        self.name: str = name
        self.pos: Tuple[int, int] = pos
        self.action: Callable[[], Optional[SceneID]] = action
        self.asset_size: int = asset_size
        self.sprites: Dict[int, pygame.Surface] = {}
        self.load_sprites()

    def load_sprites(self) -> None:
        """Load frame 0 (idle) and frame 1 (selected)."""
        try:
            for frame in range(2):
                path = (
                    f"sprites/ui/{self.name}/{self.name}_{self.asset_size}/"
                    f"{self.name}_{self.asset_size}_frame_{frame}.png"
                )
                self.sprites[frame] = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Error: cannot load the {self.name} button ({e})")

    def trigger(self) -> Optional[SceneID]:
        """Run the button action and return the requested scene."""
        return self.action()

    def render(self, screen: pygame.Surface, is_selected: bool) -> None:
        """Draw frame 1 if the button is selected, frame 0 otherwise."""
        frame_index = 1 if is_selected else 0
        if frame_index in self.sprites:
            screen.blit(self.sprites[frame_index], self.pos)


class UISprite:
    """Static image used as a menu decoration (not interactive).

    Add it to a page with self.decorations.append().
    """

    def __init__(
        self,
        name: str,
        pos: Tuple[float, float],
        asset_size: int,
    ) -> None:
        """Create the decoration and load its image."""
        self.pos: Tuple[float, float] = pos
        self.sprites: List[pygame.Surface] = []
        self.asset_size: int = asset_size
        self._load_sprites(name)

    def _load_sprites(self, name: str) -> None:
        """Load the image from the sprite name and size."""
        try:
            size = self.asset_size
            self.sprites.append(pygame.image.load(
                f"sprites/UISprite/{name}/{name}_{size}/{name}_{size}.png"))
        except Exception as e:
            print({e})

    def render(self, screen: pygame.Surface) -> None:
        """Draw the image at its position."""
        if not self.sprites:
            return

        screen.blit(self.sprites[0], self.pos)


class MenuPage(ABC):
    """Menu page: decorations, buttons and keyboard selection."""

    def __init__(self, scene_context: Any) -> None:
        """Create the page and its elements (build)."""
        self.context = scene_context
        self.buttons: List[UIButton] = []
        self.decorations: List[UISprite] = []
        self.selected_index: int = 0
        self.build()

    @abstractmethod
    def build(self) -> None:
        """Create the buttons and decorations of the page."""
        pass

    def rebuild(self) -> None:
        """Clear and rebuild the elements with the new size."""
        self.buttons.clear()
        self.decorations.clear()
        self.build()
        if self.buttons:
            self.selected_index = min(self.selected_index,
                                      len(self.buttons) - 1)

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        """Up/Down: change button. Enter/Space: trigger it."""
        if event.type != pygame.KEYDOWN or not self.buttons:
            return None

        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.buttons)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.buttons)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.buttons[self.selected_index].trigger()
        return None

    def render(self, screen: pygame.Surface) -> None:
        """Draw the decorations then the buttons."""
        for decor in self.decorations:
            decor.render(screen)

        for idx, btn in enumerate(self.buttons):
            btn.render(screen, idx == self.selected_index)

    def _select_resolution(self, size: int) -> Optional[SceneID]:
        """Change the sprite size and go back to the previous page."""
        self.context.set_asset_size(size)
        result: Optional[SceneID] = self.context.pop_page()
        return result
