from typing import List, Optional, Any, Dict
import pygame
from src.scene import SceneID, Scene
from src.menu_classes import MenuPage
from src.menu_pages import MainMenuPage


class MenuScene(Scene):
    """Menu screen: a stack of pages, only the top one is active."""

    def __init__(self, initial_page_cls: type[MenuPage],
                 **shared_data: Any) -> None:
        """Open the first page; shared_data is shared by all pages.

        Args:
            initial_page_cls: class of the first page.
            **shared_data: data shared by the pages (gameloop, asset_size).
        """
        self.game_data: Dict[str, Any] = shared_data
        self.page_stack: List[MenuPage] = []
        self.push_page(initial_page_cls(self))

    def set_asset_size(self, size: int) -> None:
        """Change the resolution and rebuild every page.

        Args:
            size: sprite size in pixels (32 or 64).
        """
        gameloop = self.game_data.get("gameloop")
        if gameloop:
            gameloop.set_resolution(size)

        self.game_data["asset_size"] = size
        for page in self.page_stack:
            page.rebuild()

    def push_page(self, page: MenuPage) -> Optional[SceneID]:
        """Open a page on top of the current one.

        Args:
            page: page to open.

        Returns:
            None (no scene change).
        """
        self.page_stack.append(page)
        return None

    def pop_page(self) -> Optional[SceneID]:
        """Close the top page; on the last one, go to the menu or quit.

        Main menu: SceneID.QUIT. Elsewhere (end screen): SceneID.MENU.

        Returns:
            None, SceneID.MENU or SceneID.QUIT.
        """
        if len(self.page_stack) > 1:
            self.page_stack.pop()
            return None
        if (self.page_stack
                and not isinstance(self.page_stack[-1], MainMenuPage)):
            return SceneID.MENU
        return SceneID.QUIT

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        """Esc closes the page; other keys go to the active page.

        Args:
            event: pygame event.

        Returns:
            The scene to open, or None.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return self.pop_page()
        if self.page_stack:
            return self.page_stack[-1].handle_event(event)
        return None

    def update(self) -> Optional[SceneID]:
        """Nothing to update in a menu.

        Returns:
            None (nothing changes).
        """
        return None

    def render(self, screen: pygame.Surface) -> None:
        """Draw the top page.

        Args:
            screen: surface to draw on.
        """
        if self.page_stack:
            self.page_stack[-1].render(screen=screen)
