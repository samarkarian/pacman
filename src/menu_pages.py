from src.menu_classes import MenuPage
from src.scene import SceneID
from src.menu_classes import UIButton, UISprite
import pygame
from typing import Any, Optional
from src.high_score import valid_name_score, scores_add, scores_save


class MainMenuPage(MenuPage):
    """Main menu: play, quit, resize, score, instructions."""

    def build(self) -> None:
        """Create the background, the title and the 5 buttons."""
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop: Any = self.context.game_data.get("gameloop")
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
                pos=(center_x, int(screen_h * 0.9)),
                action=lambda: SceneID.GAME,
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
        self.buttons.append(
                UIButton(
                    name="score",
                    pos=(center_x, int(gameloop.height * 0.55)),
                    action=lambda: self.context.push_page(
                        HighscorePage(self.context)),
                    asset_size=current_size,
                )
            )
        self.buttons.append(
                UIButton(
                    name="resize",
                    pos=(center_x, int(gameloop.height * 0.6)),
                    action=lambda: self.context.push_page(
                        ResolutionPage(self.context)),
                    asset_size=current_size,
                )
            )
        self.buttons.append(
                UIButton(
                    name="instructions",
                    pos=(center_x, int(gameloop.height * 0.7)),
                    action=lambda: self.context.push_page(
                        InstructionsPages(self.context)),
                    asset_size=current_size,
                )
            )
        self.buttons.append(
                    UIButton(
                        name="quit",
                        pos=(center_x, int(gameloop.height * 0.8)),
                        action=lambda: SceneID.QUIT,
                        asset_size=current_size,
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
        """Centre the button column inside the background frame.

        Args:
            fond: background frame of the menu.
        """
        if not fond.sprites or not all(btn.sprites for btn in self.buttons):
            return

        fond_w, fond_h = fond.sprites[0].get_size()
        dessin = self.buttons[0].sprites[0].get_bounding_rect()
        ecart = dessin.height * 7 // 5.5
        total = dessin.height + ecart * (len(self.buttons) - 1)
        haut = fond.pos[1] + (fond_h - total) // 2

        for index, btn in enumerate(self.buttons):
            dessin = btn.sprites[0].get_bounding_rect()
            pos_x = fond.pos[0] + (fond_w - dessin.width) // 2 - dessin.x
            self.buttons[index].pos = (int(pos_x),
                                       int(haut + index * ecart - dessin.y))


class ResolutionPage(MenuPage):
    """Size choice: small (32 px) or medium (64 px)."""

    def build(self) -> None:
        """Create the small, medium and quit buttons."""
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop: Any = self.context.game_data.get("gameloop")

        screen_w = gameloop.width if gameloop else 1080
        screen_h = gameloop.height if gameloop else 1080
        center_x = (screen_w - current_size*3) // 2

        fond = UISprite(
                        name='Main_menu_bg',
                        pos=(center_x/1.6, int(screen_h)*0.2),
                        asset_size=self.context.game_data.get("asset_size", 64),
                    )
        
        self.decorations.append(fond)

        self.decorations.append(
            UISprite(
                name='Title',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
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
                name="back",
                pos=(center_x, int(gameloop.height * 0.61)),
                action=lambda: self.context.pop_page(),
                asset_size=current_size,
            )
        )
        self._center_buttons(fond)
    
    def _center_buttons(self, fond: UISprite) -> None:
        """Centre the button column inside the background frame.

        Args:
            fond: background frame of the menu.
        """
        if not fond.sprites or not all(btn.sprites for btn in self.buttons):
            return

        fond_w, fond_h = fond.sprites[0].get_size()
        dessin = self.buttons[0].sprites[0].get_bounding_rect()
        ecart = dessin.height * 7 // 5.5
        total = dessin.height + ecart * (len(self.buttons) - 1)
        haut = fond.pos[1] + (fond_h - total) // 2

        for index, btn in enumerate(self.buttons):
            dessin = btn.sprites[0].get_bounding_rect()
            pos_x = fond.pos[0] + (fond_w - dessin.width) // 2 - dessin.x
            self.buttons[index].pos = (int(pos_x),
                                        int(haut + index * ecart - dessin.y))


class HighscorePage(MenuPage):
    """Shows the top 10 scores."""

    def build(self) -> None:
        """Load the font, the title and the quit button."""
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop: Any = self.context.game_data.get("gameloop")
        self.rank = gameloop.game.rank
        font_path = "sprites/Font/KGPerfectPenmanship.ttf"
        font_size = max(12, current_size // 2)
        screen_w = gameloop.width if gameloop else 1080
        screen_h = gameloop.height if gameloop else 1080
        center_x = (screen_w - current_size*3) // 2
        try:
            self.font = pygame.font.Font(font_path, font_size)
        except (FileNotFoundError, pygame.error) as e:
            print(f"Font not found ({font_path}) : {e}.")
            self.font = pygame.font.Font(None, font_size)

        self.text_x = center_x + current_size*2
        self.screen_h = gameloop.height



        self.decorations.append(
            UISprite(
                        name='Main_menu_bg',
                        pos=(center_x/1.6, int(screen_h)*0.2),
                        asset_size=self.context.game_data.get("asset_size", 64),
                    )
        )
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
        """Draw one line per score, the first one in yellow.

        Args:
            screen: surface to draw on.
        """
        super().render(screen)

        self._render_line(screen, "Here are the all-time highscores", 0.32)
        if not self.rank:
            self._render_line(screen, "No score yet", 0.4)
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
        """Write text centred, at height_ratio of the screen height.

        Args:
            screen: surface to draw on.
            text: text to write.
            height_ratio: height, as a fraction of the screen.
            color: RGB colour.
        """
        image = self.font.render(text, True, color)
        pos = (self.text_x - image.get_width() // 2,
               int(self.screen_h * height_ratio))
        screen.blit(image, pos)


class NameEntry(MenuPage):
    """End screen (victory or game over): player name entry."""

    def __init__(self, scene_context: Any) -> None:
        """Start with an empty name.

        Args:
            scene_context: the MenuScene holding the page.
        """
        self.name = ""
        self.error = ""
        super().__init__(scene_context)

    def build(self) -> None:
        """Load the font and the Victory or Game Over image."""
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop: Any = self.context.game_data.get("gameloop")
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
        """Type the name (10 max); Enter saves it and returns to the menu.

        Args:
            event: pygame event.

        Returns:
            SceneID.MENU once the score is saved, else None.
        """

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
                    self.error = "Invalid name"
                    return None

                new_rank = scores_add(self.game.rank, self.name,
                                      self.game.score)
                filename = self.game.config.highscore_filename
                if not scores_save(filename, new_rank):
                    self.error = "Cannot save the score"
                    return None

                self.game.rank = new_rank
                return SceneID.MENU

        return None

    def render(self, screen: pygame.Surface) -> None:
        """Draw the score, the name being typed and the hint (or error).

        Args:
            screen: surface to draw on.
        """
        super().render(screen)

        if self.game.victory():
            self._render_line(screen, "Congratulations on your victory!", 0.35)
        self._render_line(screen, f"Score: {self.game.score}", 0.45)
        self._render_line(screen, self.name + "_", 0.55, (255, 255, 0))
        if self.error:
            self._render_line(screen, self.error, 0.65, (255, 80, 80))
        else:
            self._render_line(screen, "Type your name and press Enter", 0.65)

    def _render_line(
        self,
        screen: pygame.Surface,
        text: str,
        height_ratio: float,
        color: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        """Write text centred, at height_ratio of the screen height.

        Args:
            screen: surface to draw on.
            text: text to write.
            height_ratio: height, as a fraction of the screen.
            color: RGB colour.
        """
        image = self.font.render(text, True, color)
        pos = (self.text_x - image.get_width() // 2,
               int(self.screen_h * height_ratio))
        screen.blit(image, pos)


class InstructionsPages(MenuPage):
    """Controls and rules page (one image)."""

    def build(self) -> None:
        """Place the instructions image, the title and the quit button."""
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop: Any = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080
        screen_h = gameloop.height if gameloop else 1080
        center_x = (screen_w - current_size*3) // 2

        self.decorations.append(
            UISprite(
                        name='Main_menu_bg',
                        pos=(center_x/1.6, int(screen_h)*0.2),
                        asset_size=self.context.game_data.get("asset_size", 64),
                    )
        )
        self.decorations.append(
            UISprite(
                name='Instructions',
                pos=((screen_w - current_size*10.25) // 2,
                     int(gameloop.height * 0.28)),
                asset_size=current_size,
            )
        )
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
