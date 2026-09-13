# from typing import Tuple
# from Display_abstractmethods import Renderer
# import pygame


# class GhostRenderer(Entity):
#     def __init__(self, pos: Tuple[int, int], color):
#         super().__init__(pos)
#         self.color = color
#         self.sprites: Dict[str, List[pygame.Surface]] = {
#             "normal": [],
#             "vulnerable": [],
#         }
#         self.state = 'normal'

#     def load_sprites(self, asset_size):
#         """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
#         """
#         try:
#             for sprite in range(2):
#                 self.sprites['normal'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_{self.color}/Ghost_{self.color}_{asset_size}/Ghost_{self.color}_{asset_size}_frame_{sprite}.png"))
#             for sprite in range(2):
#                 self.sprites['vulnerable'].append(pygame.image.load(f"sprites/Entities/Ghost/Ghost_vulnerable/Ghost_vulnerable_{asset_size}/Ghost_vulnerable_{asset_size}_frame_{sprite}.png"))

#             self.pixel_offset = asset_size

#         except Exception as e:
#             print(e)

#     def render(self, screen, animation_speed: int = 800, offset: Tuple[int, int] = (0, 0)):
#         """rendu automatique avec 2 frames pour l'animation en deux temps
#         """
#         time = pygame.time.get_ticks()
#         frame_index = (time // animation_speed) % 2

#         draw_x = self.pixel_offset * self.posx + offset[0]
#         draw_y = self.pixel_offset * self.posy + offset[1]
#         current_sprite = self.sprites[self.state][frame_index]

#         screen.blit(current_sprite, (draw_x, draw_y))


# class HUDDisplayer(Renderer):
#     def __init__(self, asset_size: int = 64) -> None:
#         self.asset_size: int = asset_size
#         # Équivalent de la gestion des polices raster en MLX
#         self.font: pygame.font.Font = pygame.font.Font(None, int(asset_size * 0.45))
#         self.life_icon: pygame.Surface | None = None
#         self.load_sprites(asset_size)

#     def load_sprites(self, asset_size: int) -> None:
#         self.asset_size = asset_size
#         self.font = pygame.font.Font(None, max(18, int(asset_size * 0.45)))
#         try:
#             path = (
#                 f"sprites/Entities/Player/Player_{asset_size}/"
#                 f"Player_{asset_size}_E_frame_0.png"
#             )
#             # Petite icône pour représenter chaque vie restante
#             icon = pygame.image.load(path).convert_alpha()
#             # Si besoin d'une icône plus discrète que la taille d'une tuile standard
#             self.life_icon = icon
#         except Exception as e:
#             print(f"HUD : icône de vie introuvable ({e})")

#     def render(
#         self,
#         screen: pygame.Surface,
#         score: int,
#         lives: int,
#         level_index: int,
#         offset: Tuple[int, int] = (0, 0),
#     ) -> None:
#         # 1. Rendu du score et du niveau
#         score_text = f"SCORE  {score:05d}"
#         level_text = f"LEVEL  {level_index + 1}"

#         score_surface = self.font.render(score_text, True, (255, 255, 255))
#         level_surface = self.font.render(level_text, True, (255, 255, 255))

#         # Positionnement façon HUD classique en haut ou en bas d'écran
#         screen.blit(score_surface, (20 + offset[0], 15 + offset[1]))
#         screen.blit(level_surface, (300 + offset[0], 15 + offset[1]))

#         # 2. Rendu des vies
#         lives_start_x = 550 + offset[0]
#         lives_y = 10 + offset[1]

#         if self.life_icon:
#             # Affiche une icône par vie restante
#             for i in range(max(0, lives)):
#                 screen.blit(self.life_icon, (lives_start_x + (i * (self.asset_size // 2 + 5)), lives_y))
#         else:
#             # Fallback en texte si l'icône n'est pas chargée
#             lives_surface = self.font.render(f"LIVES  {lives}", True, (255, 255, 255))
#             screen.blit(lives_surface, (lives_start_x, 15 + offset[1]))