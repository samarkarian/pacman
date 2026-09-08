from typing import List, Optional, Any, Tuple, Dict, Callable
from Scene import SceneID
import pygame
from abc import ABC, abstractmethod


class UIButton:
    def __init__(
        self,
        name: str,
        pos: Tuple[int, int],
        action: Callable[[], Optional[SceneID]],
        asset_size: int = 64,
    ) -> None:
        self.name: str = name
        self.pos: Tuple[int, int] = pos
        self.action: Callable[[], Optional[SceneID]] = action
        self.asset_size: int = asset_size
        self.sprites: Dict[int, pygame.Surface] = {}
        self.load_sprites()

    def load_sprites(self) -> None:
        """Charge la frame 0 (inactif) et la frame 1 (sélectionné)."""
        try:
            for frame in range(2):
                path = (
                    f"sprites/ui/{self.name}/{self.name}_{self.asset_size}/"
                    f"{self.name}_{self.asset_size}_frame_{frame}.png"
                )
                self.sprites[frame] = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Erreur de chargement pour {self.name}: {e}")

    def trigger(self) -> Optional[SceneID]:
        return self.action()

    def render(self, screen: pygame.Surface, is_selected: bool) -> None:
        frame_index = 1 if is_selected else 0
        if frame_index in self.sprites:
            screen.blit(self.sprites[frame_index], self.pos)


class MenuPage(ABC):
    def __init__(self, scene_context) -> None:
        self.context = scene_context
        self.buttons: List[UIButton] = []
        self.selected_index: int = 0
        self.build()

    @abstractmethod
    def build(self) -> None:
        """Chaque page instancie ses propres SpriteButtons ici."""
        pass

    def rebuild(self) -> None:
        """Vide et recrée les boutons avec la nouvelle taille."""
        self.buttons.clear()
        self.build()
        if self.buttons:
            self.selected_index = min(self.selected_index, len(self.buttons) - 1)

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
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
        for idx, btn in enumerate(self.buttons):
            btn.render(screen, idx == self.selected_index)

    def _select_resolution(self, size: int) -> Optional[SceneID]:
        self.context.set_asset_size(size)
        return self.context.pop_page()