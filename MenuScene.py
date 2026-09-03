import pygame
from Scene import Scene, SceneID
from typing import Optional

class MenuScene(Scene):
    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 48)

    def load_sprites(self):
        pass

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return SceneID.GAME
            elif event.key == pygame.K_ESCAPE:
                return SceneID.QUIT
        return None

    def update(self) -> Optional[SceneID]:
        return None

    def render(self, screen: pygame.Surface) -> None:
        text_surf = self.font.render("Appuyez sur ESPACE pour jouer", True, (255, 255, 255))
        screen.blit(text_surf, (200, 200))

# class Menu:
#     def __init__(self, screen: pygame.Surface) -> None:
#         self.screen: pygame.Surface = screen
#         self.font: pygame.font.Font = pygame.font.Font(None, 48)
#         self.items: List[MenuItem] = []
#         self.selected_index: int = 0

#     def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], None]) -> None:
#         self.items.append(MenuItem(text, self.font, pos, action))

#     def handle_event(self, event: pygame.event.Event) -> None:
#         if event.type != pygame.KEYDOWN:
#             return

#         if event.key == pygame.K_UP:
#             self.selected_index = (self.selected_index - 1) % len(self.items)
#         elif event.key == pygame.K_DOWN:
#             self.selected_index = (self.selected_index + 1) % len(self.items)
#         elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
#             if self.items:
#                 self.items[self.selected_index].trigger()

#     def render(self) -> None:
#         for idx, item in enumerate(self.items):
#             item.render(self.screen, idx == self.selected_index)



# import pygame
# from typing import Callable, Tuple

# class MenuItem:
#     def __init__(self, text: str, font: pygame.font.Font, pos: Tuple[int, int], action: Callable[[], None]) -> None:
#         self.text: str = text
#         self.font: pygame.font.Font = font
#         self.pos: Tuple[int, int] = pos
#         self.action: Callable[[], None] = action

#     def render(self, screen: pygame.Surface, is_selected: bool) -> None:
#         color = (255, 255, 0) if is_selected else (200, 200, 200)
#         # Équivalent MLX de mlx_string_put
#         surface = self.font.render(self.text, True, color)
#         screen.blit(surface, self.pos)

#     def trigger(self) -> None:
#         self.action()