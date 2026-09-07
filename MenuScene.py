# import pygame
# from Scene import Scene, SceneID
# from typing import Optional, List, Tuple, Callable

# class MenuScene(Scene):
#     def __init__(self) -> None:
#         self.items: List[MenuItem] = []
#         self.selected_index: int = 0
#         self.menu = Menu()
#         self.menu.add_item("Jouer", (400, 300), lambda: SceneID.GAME)
#         self.menu.add_item("Taille: 64px", (400, 380), self.toggle_asset_size)
#         self.menu.add_item("Quitter", (400, 460), lambda: SceneID.QUIT)

#     def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], None]) -> None:
#             self.items.append(MenuItem(text, pos, action))

#     # def load_sprites(self):
#     #     pass

#     def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
#         if event.type == pygame.KEYDOWN:
#             if event.key in (pygame.K_RETURN, pygame.K_SPACE):
#                 return SceneID.GAME
#             elif event.key == pygame.K_ESCAPE:
#                 return SceneID.QUIT
#             elif event.key == pygame.K_UP:
#                 self.selected_index = (self.selected_index - 1) % len(self.items)
#             elif event.key == pygame.K_DOWN:
#                 self.selected_index = (self.selected_index + 1) % len(self.items)
#             elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
#                 if self.items:
#                     self.items[self.selected_index].trigger()
#         return None

#     def toggle_asset_size(self) -> Optional[SceneID]:
#             # Logique de bascule 32 / 64
#             return None

#     def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
#         return self.menu.handle_event(event)

#     def update(self) -> Optional[SceneID]:
#         return None

#     def render(self, screen: pygame.Surface) -> None:
#         self.menu.render(screen)

# class Menu:
#     """Widget autonome de menu utilisable dans n'importe quelle Scene."""
#     def __init__(self, font_size: int = 48) -> None:
#         self.font = pygame.font.Font(None, font_size)
#         self.items: List[MenuItem] = []
#         self.selected_index: int = 0

#     def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], Optional[SceneID]]) -> None:
#         self.items.append(MenuItem(text, pos, action))

#     def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
#         if event.type != pygame.KEYDOWN or not self.items:
#             return None

#         if event.key == pygame.K_UP:
#             self.selected_index = (self.selected_index - 1) % len(self.items)
#         elif event.key == pygame.K_DOWN:
#             self.selected_index = (self.selected_index + 1) % len(self.items)
#         elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
#             return self.items[self.selected_index].trigger()
#         return None

#     def render(self, screen: pygame.Surface) -> None:
#         for idx, item in enumerate(self.items):
#             item.render(screen, idx == self.selected_index)


# class MenuItem:
#     def __init__(self, text: str, pos: Tuple[int, int], action: Callable[[], None]) -> None:
#         self.text: str = text
#         self.font: pygame.font.Font = pygame.font.Font(None, 48)
#         self.pos: Tuple[int, int] = pos
#         self.action: Callable[[], None] = action

#     def render(self, screen: pygame.Surface, is_selected: bool) -> None:
#         color = (255, 255, 0) if is_selected else (200, 200, 200)
#         # Équivalent MLX de mlx_string_put
#         surface = self.font.render(self.text, True, color)
#         screen.blit(surface, self.pos)

#     def trigger(self) -> Optional[SceneID]:
#         return self.action()

from abc import ABC, abstractmethod
from typing import List, Optional, Any, Tuple, Dict, Callable
import pygame
from Scene import SceneID, Scene

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
    def __init__(self, scene_context: "MenuScene") -> None:
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

class MainMenuPage(MenuPage):
    def build(self) -> None:
        self.buttons.append(
            UIButton(
                name="play",
                pos=(450, 300),
                action=lambda: SceneID.GAME,
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
        self.buttons.append(
                    UIButton(
                        name="quit",
                        pos=(450, 400),
                        action=lambda: SceneID.QUIT,
                        asset_size=self.context.game_data.get("asset_size", 64),
                    )
                )
        self.buttons.append(
                UIButton(
                    name="resize",
                    pos=(450, 500),
                    action=lambda: self.context.push_page(ResolutionPage(self.context)),
                    asset_size=self.context.game_data.get("asset_size", 64),
            )
        )

class ResolutionPage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)

        self.buttons.append(
            UIButton(
                name="small",
                pos=(450, 300),
                action=lambda: self._select_resolution(32),
                asset_size=current_size,
            )
        )
        self.buttons.append(
            UIButton(
                name="medium",
                pos=(450, 400),
                action=lambda: self._select_resolution(64),
                asset_size=current_size,
            )
        )
        self.buttons.append(
            UIButton(
                name="quit",
                pos=(450, 500),
                action=lambda: self.context.pop_page(),
                asset_size=current_size,
            )
        )

    def _select_resolution(self, size: int) -> Optional[SceneID]:
        self.context.set_asset_size(size)
        return self.context.pop_page()

class MenuScene(Scene):
    def __init__(self, initial_page_cls: type[MenuPage], **shared_data: Any) -> None:
        self.game_data: Dict[str, Any] = shared_data
        self.page_stack: List[MenuPage] = []
        # Instanciation de la toute première page injectée
        self.push_page(initial_page_cls(self))

    def set_asset_size(self, size: int) -> None:
        """Met à jour la résolution et recharge les sprites de toutes les pages."""
        self.game_data["asset_size"] = size
        for page in self.page_stack:
            page.rebuild()

    def push_page(self, page: MenuPage) -> Optional[SceneID]:
        self.page_stack.append(page)
        return None

    def pop_page(self) -> Optional[SceneID]:
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            return None
        return SceneID.QUIT

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.pop_page()
        if self.page_stack:
            return self.page_stack[-1].handle_event(event)
        return None

    def update(self) -> Optional[SceneID]:
        return None

    def render(self, screen: pygame.Surface) -> None:
        if self.page_stack:
            self.page_stack[-1].render(screen)




from typing import Callable, Optional, Tuple
import pygame
# En supposant que Renderer est dans le même module ou importé
from Display_abstractmethods import Renderer


