from typing import List, Tuple
import pygame
from HUD_Render import ScoreRenderer, TimeRenderer, LevelRenderer, Renderer, LivesRenderer, LivesTextRenderer



from typing import List, Tuple
import pygame
from HUD_Render import ScoreRenderer, TimeRenderer, LevelRenderer, Renderer, LivesRenderer, LivesTextRenderer


class HUDContainer:
    """Conteneur d'affichage pour le HUD (conforme aux contraintes MLX)."""

    def __init__(
        self,
        game,
        asset_size: int = 64,
        bg_color: Tuple[int, int, int] = (15, 15, 25),
        border_color: Tuple[int, int, int] = (200, 200, 200),
        border_width: int = 2,
    ) -> None:
        self.game = game
        self.asset_size = asset_size
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.hud_elements: list[Renderer] = []

        self.width: int = 0
        self.height: int = 0
        self.surface: pygame.Surface | None = None
        self.inner_surface: pygame.Surface | None = None

        self.build()

    def build(self) -> None:
        """Instancie et configure les composants internes du HUD."""
        self.hud_elements.clear()

        # Sécurisation si la grille ou le labyrinthe n'est pas encore prêt
        if not hasattr(self.game, "field") or not self.game.field or not hasattr(self.game.field, "maze"):
            return

        maze_w = self.game.field.maze.width
        hud_y = int(self.asset_size * 0.7)
        step_x = (maze_w * self.asset_size) // 4

        self.hud_elements = [
            ScoreRenderer(pos=(int(step_x * 0.1), hud_y), game=self.game),
            TimeRenderer(pos=(int(step_x * 1.1), hud_y), game=self.game),
            LevelRenderer(pos=(int(step_x * 2.1), hud_y), game=self.game),
            LivesTextRenderer(pos=(int(step_x * 2.8), hud_y), game=self.game),
            LivesRenderer(pos=(int(step_x * 3.1), int(hud_y * 0.7)), game=self.game),
        ]

        self.update_dimensions(maze_w, self.asset_size)
        self.load_sprites(self.asset_size)

    def load_sprites(self, asset_size: int) -> None:
        """Transmet l'ordre de chargement des ressources à tous les éléments enfants."""
        self.asset_size = asset_size
        for elem in self.hud_elements:
            if hasattr(elem, "load_sprites"):
                elem.load_sprites(asset_size)

    def update_dimensions(self, maze_grid_w: int, asset_size: int) -> None:
        """Recalcule la surface extérieure et intérieure sans méthode vectorielle."""
        self.asset_size = asset_size
        self.width = maze_grid_w * asset_size
        self.height = 2 * asset_size

        if self.width <= 0 or self.height <= 0:
            return

        inner_w = max(0, self.width - (self.border_width * 2))
        inner_h = max(0, self.height - (self.border_width * 2))

        self.surface = pygame.Surface((self.width, self.height))
        self.inner_surface = pygame.Surface((inner_w, inner_h))

    def render(self, screen: pygame.Surface, pos: Tuple[int, int]) -> None:
        """Effectue le rendu par double buffer et blit."""
        if self.surface is None or self.inner_surface is None:
            return

        self.surface.fill(self.border_color)
        self.inner_surface.fill(self.bg_color)

        for hud in self.hud_elements:
            hud.render(self.inner_surface)

        self.surface.blit(self.inner_surface, (self.border_width, self.border_width))

        screen.blit(self.surface, pos)