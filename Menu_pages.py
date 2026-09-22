from Menu_classes import MenuPage
from Scene import SceneID
from Menu_classes import UIButton, UISprite
import pygame
from typing import Optional
from high_score import valid_name_score, scores_add, scores_save


class MainMenuPage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080
        screen_h = gameloop.height if gameloop else 1080
        center_x = (screen_w - current_size*3) // 2

        fond = UISprite(
                name='Main_menu_bg',
                pos=(center_x/1.6, int(screen_h)*0.2),
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        self.decorations.append(fond)
        self.buttons.append(
            UIButton(
                name="play",
                pos=(center_x, int(screen_h * 0.4)),
                action=lambda: SceneID.GAME,
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
        self.buttons.append(
                    UIButton(
                        name="quit",
                        pos=(center_x, int(gameloop.height * 0.5)),
                        action=lambda: SceneID.QUIT,
                        asset_size=self.context.game_data.get("asset_size", 64),
                    )
                )
        self.buttons.append(
                UIButton(
                    name="resize",
                    pos=(center_x, int(gameloop.height * 0.6)),
                    action=lambda: self.context.push_page(ResolutionPage(self.context)),
                    asset_size=self.context.game_data.get("asset_size", 64),
                )
            )
        self.buttons.append(
                UIButton(
                    name="score",
                    pos=(center_x, int(gameloop.height * 0.7)),
                    action=lambda: self.context.push_page(HighscorePage(self.context)),
                    asset_size=self.context.game_data.get("asset_size", 64),
                )
            )
        self.decorations.append(
            UISprite(
                name='Title',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
        self._center_buttons(fond)

    def _center_buttons(self, fond: UISprite) -> None:
        if not fond.sprites or not all(btn.sprites for btn in self.buttons):
            return

        fond_w, fond_h = fond.sprites[0].get_size()
        dessin = self.buttons[0].sprites[0].get_bounding_rect()
        ecart = dessin.height * 7 // 4
        total = dessin.height + ecart * (len(self.buttons) - 1)
        haut = fond.pos[1] + (fond_h - total) // 2

        for index, btn in enumerate(self.buttons):
            dessin = btn.sprites[0].get_bounding_rect()
            pos_x = fond.pos[0] + (fond_w - dessin.width) // 2 - dessin.x
            self.buttons[index].pos = (int(pos_x), int(haut + index * ecart - dessin.y))


class ResolutionPage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080

        center_x = (screen_w - current_size*3) // 2

        self.buttons.append(
            UIButton(
                name="small",
                pos=(center_x, gameloop.height * 0.35),
                action=lambda: self._select_resolution(32),
                asset_size=current_size,
            )
        )
        self.buttons.append(
            UIButton(
                name="medium",
                pos=(center_x, int(gameloop.height * 0.48)),
                action=lambda: self._select_resolution(64),
                asset_size=current_size,
            )
        )
        self.buttons.append(
            UIButton(
                name="quit",
                pos=(center_x, int(gameloop.height * 0.61)),
                action=lambda: self.context.pop_page(),
                asset_size=current_size,
            )
        )


class HighscorePage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080
        self.rank = gameloop.game.rank
        font_path = "sprites/Font/KGPerfectPenmanship.ttf"
        font_size = max(12, current_size // 2)
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Font not found ({font_path}) : {e}.")
            self.font = pygame.font.Font(None, font_size)

        center_x = (screen_w - current_size*3) // 2
        self.text_x = center_x + current_size*2
        self.screen_h = gameloop.height

        self.buttons.append(
            UIButton(
                name="quit",
                pos=(center_x, int(gameloop.height * 0.8)),
                action=lambda: self.context.pop_page(),
                asset_size=current_size,
            )
        )
        self.decorations.append(
            UISprite(
                name='Title',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=current_size,
            )
        )

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)

        if not self.rank:
            self._render_line(screen, "Pas encore de score", 0.4)
            return

        for index, entry in enumerate(self.rank):
            line = f"{index + 1}. {entry['name']} {entry['score']}"
            color = (255, 255, 0) if index == 0 else (255, 255, 255)
            self._render_line(screen, line, 0.4 + index * 0.04, color)

    def _render_line(
        self,
        screen: pygame.Surface,
        text: str,
        height_ratio: float,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        image = self.font.render(text, True, color)
        pos = (self.text_x - image.get_width() // 2, int(self.screen_h * height_ratio))
        screen.blit(image, pos)

# class GameOverPage(MenuPage):
#     def build(self) -> None:
#         current_size = self.context.game_data.get("asset_size", 64)
#         gameloop = self.context.game_data.get("gameloop")
#         screen_w = gameloop.width if gameloop else 1080

#         center_x = (screen_w - current_size*3) // 2

#         self.decorations.append(
#             UISprite(
#                 name='Gameover',
#                 pos=(center_x*0.6, int(gameloop.height * 0.05)),
#                 asset_size=self.context.game_data.get("asset_size", 64),
#             )
#         )
#         self.buttons.append(
#             UIButton(
#                 name="quit",
#                 pos=(center_x, int(gameloop.height * 0.61)),
#                 action=lambda: SceneID.MENU,
#                 asset_size=current_size,
#             )
#         )


class NameEntry(MenuPage):
    def __init__(self, scene_context) -> None:
        self.name = ""
        self.error = ""
        super().__init__(scene_context)

    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080
        self.game = gameloop.game
        font_path = "sprites/Font/KGPerfectPenmanship.ttf"
        font_size = max(12, current_size // 2)
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Font not found ({font_path}) : {e}.")
            self.font = pygame.font.Font(None, font_size)

        center_x = (screen_w - current_size*3) // 2
        self.text_x = center_x + current_size*2
        self.screen_h = gameloop.height

        self.decorations.append(
            UISprite(
                name='Victory' if gameloop.game.victory() else 'Gameover',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64)
            )
        )

    def handle_event(self, event: pygame.event.Event) -> Optional[SceneID]:

        if event.type == pygame.TEXTINPUT:
            for char in event.text:
                if len(self.name) >= 10:
                    break
                if char.isascii() and (char.isalnum() or char == " "):
                    self.name += char
                    self.error = ""

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name = self.name[:-1]
                self.error = ""
            elif event.key == pygame.K_RETURN:
                if not valid_name_score(self.name, self.game.score):
                    self.error = "Nom invalide"
                    return None

                new_rank = scores_add(self.game.rank, self.name, self.game.score)
                if not scores_save(self.game.config.highscore_filename, new_rank):
                    self.error = "Sauvegarde impossible"
                    return None

                self.game.rank = new_rank
                return SceneID.MENU

        return None

    def render(self, screen: pygame.Surface) -> None:
        super().render(screen)

        self._render_line(screen, f"Score: {self.game.score}", 0.45)
        self._render_line(screen, self.name + "_", 0.55, (255, 255, 0))
        if self.error:
            self._render_line(screen, self.error, 0.65, (255, 80, 80))
        else:
            self._render_line(screen, "Entre ton nom puis Entree", 0.65)

    def _render_line(
        self,
        screen: pygame.Surface,
        text: str,
        height_ratio: float,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        image = self.font.render(text, True, color)
        pos = (self.text_x - image.get_width() // 2, int(self.screen_h * height_ratio))
        screen.blit(image, pos)
