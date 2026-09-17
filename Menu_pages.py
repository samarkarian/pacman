from Menu_classes import MenuPage
from Scene import SceneID
from Menu_classes import UIButton, UISprite


class MainMenuPage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080
        screen_h = gameloop.height if gameloop else 1080
        print(screen_h, screen_w)
        center_x = (screen_w - current_size*3) // 2

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
        self.decorations.append(
            UISprite(
                name='Title',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )


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

class GameOverPage(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080

        center_x = (screen_w - current_size*3) // 2

        self.decorations.append(
            UISprite(
                name='Gameover',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64),
            )
        )
        self.buttons.append(
            UIButton(
                name="quit",
                pos=(center_x, int(gameloop.height * 0.61)),
                action=lambda: SceneID.MENU,
                asset_size=current_size,
            )
        )


class NameEntry(MenuPage):
    def build(self) -> None:
        current_size = self.context.game_data.get("asset_size", 64)
        gameloop = self.context.game_data.get("gameloop")
        screen_w = gameloop.width if gameloop else 1080

        center_x = (screen_w - current_size*3) // 2

        self.buttons.append(
            UISprite(
                name='Victory',
                pos=(center_x*0.6, int(gameloop.height * 0.05)),
                asset_size=self.context.game_data.get("asset_size", 64)
            )
        )
