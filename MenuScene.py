from typing import List, Optional, Any, Dict
import pygame
from Scene import SceneID, Scene
from Menu_classes import MenuPage


class MenuScene(Scene):
    def __init__(self, initial_page_cls: type[MenuPage], **shared_data: Any) -> None:
        self.game_data: Dict[str, Any] = shared_data
        self.page_stack: List[MenuPage] = []
        # Instanciation de la toute première page injectée
        self.push_page(initial_page_cls(self))

    def set_asset_size(self, size: int) -> None:
        """Met à jour la résolution et recharge les sprites de toutes les pages."""
        gameloop = self.game_data.get("gameloop")
        if gameloop:
            gameloop.set_resolution(size)

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
