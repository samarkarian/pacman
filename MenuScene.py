import pygame
from Scene import Scene, SceneID
from typing import Optional, List, Tuple, Callable

class MenuScene(Scene):
    def __init__(self) -> None:
        self.items: List[MenuItem] = []
        self.selected_index: int = 0
        self.menu = Menu()
        self.menu.add_item("Jouer", (400, 300), lambda: SceneID.GAME)
        self.menu.add_item("Taille: 64px", (400, 380), self.toggle_asset_size)
        self.menu.add_item("Quitter", (400, 460), lambda: SceneID.QUIT)

    def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], None]) -> None:
            self.items.append(MenuItem(text, pos, action))

    # def load_sprites(self):
    #     pass

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                return SceneID.GAME
            elif event.key == pygame.K_ESCAPE:
                return SceneID.QUIT
            elif event.key == pygame.K_UP:
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif event.key == pygame.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.items:
                    self.items[self.selected_index].trigger()
        return None

    def toggle_asset_size(self) -> Optional[SceneID]:
            # Logique de bascule 32 / 64
            return None

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        return self.menu.handle_event(event)

    def update(self) -> Optional[SceneID]:
        return None

    def render(self, screen: pygame.Surface) -> None:
        self.menu.render(screen)

class Menu:
    """Widget autonome de menu utilisable dans n'importe quelle Scene."""
    def __init__(self, font_size: int = 48) -> None:
        self.font = pygame.font.Font(None, font_size)
        self.items: List[MenuItem] = []
        self.selected_index: int = 0

    def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], Optional[SceneID]]) -> None:
        self.items.append(MenuItem(text, pos, action))

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
        if event.type != pygame.KEYDOWN or not self.items:
            return None

        if event.key == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.items)
        elif event.key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.items)
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            return self.items[self.selected_index].trigger()
        return None

    def render(self, screen: pygame.Surface) -> None:
        for idx, item in enumerate(self.items):
            item.render(screen, idx == self.selected_index)



# from typing import Callable, Dict, List, Optional, Tuple
# import pygame
# from scene import SceneID


# class MenuItem:
#     def __init__(
#         self,
#         text: str,
#         font: pygame.font.Font,
#         pos: Tuple[int, int],
#         action: Callable[[], Optional[SceneID]],
#     ) -> None:
#         self.text = text
#         self.font = font
#         self.pos = pos
#         self.action = action

#     def render(self, screen: pygame.Surface, is_selected: bool) -> None:
#         color = (255, 255, 0) if is_selected else (200, 200, 200)
#         # Équivalent MLX de mlx_string_put
#         surface = self.font.render(self.text, True, color)
#         screen.blit(surface, self.pos)

#     def trigger(self) -> Optional[SceneID]:
#         return self.action()













# class MenuPage:
#     """Représente un onglet/sous-menu précis."""
#     def __init__(self, title: str, font_size: int = 42) -> None:
#         self.title = title
#         self.font = pygame.font.Font(None, font_size)
#         self.title_font = pygame.font.Font(None, int(font_size * 1.3))
#         self.items: List[MenuItem] = []
#         self.selected_index: int = 0

#     def add_item(self, text: str, pos: Tuple[int, int], action: Callable[[], Optional[SceneID]]) -> None:
#         self.items.append(MenuItem(text, self.font, pos, action))

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
#         # Titre de l'onglet
#         title_surf = self.title_font.render(self.title, True, (255, 180, 0))
#         screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 120))

#         # Éléments sélectionnables
#         for idx, item in enumerate(self.items):
#             item.render(screen, idx == self.selected_index)

# class MenuNavigator:
#     def __init__(self) -> None:
#         self.pages: Dict[str, MenuPage] = {}
#         self.history: List[str] = []

#     def register_page(self, name: str, page: MenuPage) -> None:
#         self.pages[name] = page

#     def go_to(self, page_name: str) -> None:
#         if page_name in self.pages:
#             self.history.append(page_name)
#             self.pages[page_name].selected_index = 0

#     def go_back(self) -> bool:
#         """Revient à l'onglet précédent. Renvoie False si on est déjà à la racine."""
#         if len(self.history) > 1:
#             self.history.pop()
#             return True
#         return False

#     @property
#     def current_page(self) -> MenuPage:
#         return self.pages[self.history[-1]]

# import pygame
# from typing import Callable, Tuple

class MenuItem:
    def __init__(self, text: str, pos: Tuple[int, int], action: Callable[[], None]) -> None:
        self.text: str = text
        self.font: pygame.font.Font = pygame.font.Font(None, 48)
        self.pos: Tuple[int, int] = pos
        self.action: Callable[[], None] = action

    def render(self, screen: pygame.Surface, is_selected: bool) -> None:
        color = (255, 255, 0) if is_selected else (200, 200, 200)
        # Équivalent MLX de mlx_string_put
        surface = self.font.render(self.text, True, color)
        screen.blit(surface, self.pos)

    def trigger(self) -> Optional[SceneID]:
        return self.action()


# class MenuScene(Scene):
#     def __init__(self, mazegen) -> None:
#         self.mazegen = mazegen
#         self.asset_size = 64
#         self.navigator = MenuNavigator()
        
#         self._build_pages()
#         self.navigator.go_to("MAIN")

#     def _build_pages(self) -> None:
#         # 1. Page Principale
#         main_page = MenuPage("MENU PRINCIPAL")
#         main_page.add_item("Jouer", (450, 350), lambda: SceneID.GAME)
#         main_page.add_item("Sélection du Niveau", (450, 420), lambda: self._open("LEVELS"))
#         main_page.add_item("Options", (450, 490), lambda: self._open("OPTIONS"))
#         main_page.add_item("Quitter", (450, 560), lambda: SceneID.QUIT)
#         self.navigator.register_page("MAIN", main_page)

#         # 2. Page Options
#         opt_page = MenuPage("OPTIONS")
#         opt_page.add_item("Taille des tuiles (32/64)", (380, 380), self._toggle_size)
#         opt_page.add_item("Retour", (380, 460), self._back)
#         self.navigator.register_page("OPTIONS", opt_page)

#         # 3. Page Sélection du niveau
#         lvl_page = MenuPage("CHOIX DU NIVEAU")
#         lvl_page.add_item("Labyrinthe 15x15", (420, 360), lambda: self._select_maze((15, 15)))
#         lvl_page.add_item("Labyrinthe 25x25", (420, 430), lambda: self._select_maze((25, 25)))
#         lvl_page.add_item("Retour", (420, 500), self._back)
#         self.navigator.register_page("LEVELS", lvl_page)

#     def _open(self, target: str) -> Optional[SceneID]:
#         self.navigator.go_to(target)
#         return None

#     def _back(self) -> Optional[SceneID]:
#         self.navigator.go_back()
#         return None

#     def _toggle_size(self) -> Optional[SceneID]:
#         self.asset_size = 32 if self.asset_size == 64 else 64
#         return None

#     def _select_maze(self, size: Tuple[int, int]) -> Optional[SceneID]:
#         self.mazegen.size = size
#         self.mazegen.generate()
#         return SceneID.GAME

#     def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:
#         if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
#             # Échap revient à l'onglet parent, ou quitte si déjà à l'accueil
#             if not self.navigator.go_back():
#                 return SceneID.QUIT
#             return None

#         return self.navigator.current_page.handle_event(event)

#     def update(self) -> Optional[SceneID]:
#         return None

#     def render(self, screen: pygame.Surface) -> None:
#         self.navigator.current_page.render(screen)