from Display_abstractmethods import Entity, Renderer
import pygame
import random


class Ghost:
    def __init__(self, play_field, spawn):
        self.renderer = GhostRenderer()
        self.ai = GhostAI(play_field, spawn)
        self.posx, self.posy = spawn

    
class GhostRenderer(Entity):
    def __init__(self, pos):
        super().__init__()
        self.posx, self.posy = pos

    def load_sprites(self, asset_size):
        """volonte de creer un systeme de path de fichier automatique avec le nom de la classe et la taille (size) en pixels
        """
        try:
            for sprite in range(2):
                self.sprites[sprite] = pygame.image.load(f"sprites/Entities/{self.__class__.__name__}/{self.__class__.__name__}_{asset_size}/{self.__class__.__name__}_{asset_size}_frame_{sprite}.png")
        except Exception as e:
            print(e)

    def render(self, screen, animation_speed: int, offset: Tuple[int, int] = (0, 0)):
        """rendu automatique avec 2 frames pour l'animation en deux temps
        """
        time = pygame.time.get_ticks()
        frame_index = (time // animation_speed) % 2

        draw_x = self.posx + offset[0]
        draw_y = self.posy + offset[1]
        current_sprite = self.sprites[frame_index]

        screen.blit(current_sprite, (draw_x, draw_y))


class GhostAI:
    def __init__(self, field, spawn):

        self.field = field
        self.x, self.y = spawn
        self.previous = None
        self.respawn_count = 0

    def start_respawn(self, steps: int) -> None:

        self.respawn_count = steps

    def step(self, player_x, player_y, vulnerable_count) -> None:

        if self.respawn_count != 0:
            self.respawn_count -= 1
            return None

        maze = self.field.maze
        cells = maze.neighbors(self.x, self.y)
        if not cells:
            return None

        choices = []
        for cell in cells:
            if cell != self.previous:
                choices.append(cell)

        if not choices:
            choices = cells

        self.previous = (self.x, self.y)
        dist_dict = {}
        for choice in choices:
            choice_x, choice_y = choice
            x_dist = player_x - choice_x
            y_dist = player_y - choice_y
            abs_dist = abs(x_dist) + abs(y_dist)
            dist_dict.update({choice: abs_dist})
        if vulnerable_count == 0:
            min_value = min(dist_dict.values())
            min_key = []
            for key, value in dist_dict.items():
                if value == min_value:
                    min_key.append(key)
            self.x, self.y = random.choice(min_key)
            return self.x, self.y
        else:
            max_value = max(dist_dict.values())
            max_key = []
            for key, value in dist_dict.items():
                if value == max_value:
                    max_key.append(key)
            self.x, self.y = random.choice(max_key)
            return self.x, self.y