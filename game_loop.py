from Scene import SceneID
from Game_scene import GameScene
from MenuScene import MenuScene
from Menu_pages import MainMenuPage, GameOverPage, NameEntry
import pygame
import sys


class GameLoop:
    RESOLUTIONS: dict[int, tuple[int, int]] = {
        64: (1500, 1500),
        32: (1080, 1080),
    }

    def __init__(self, game) -> None:
        pygame.init()
        self.asset_size: int = 64
        self.width, self.height = self.RESOLUTIONS[self.asset_size]
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.game = game


        # Démarrage sur le MenuScene avec sa page initiale injectée
        self.current_scene = MenuScene(
            initial_page_cls=MainMenuPage,
            asset_size=self.asset_size,
            gameloop=self,
        )

    def set_resolution(self, asset_size: int) -> None:
        if asset_size not in self.RESOLUTIONS:
            return
        self.asset_size = asset_size
        self.width, self.height = self.RESOLUTIONS[self.asset_size]
        self.screen = pygame.display.set_mode((self.width, self.height))

    def change_scene(self, target: SceneID) -> None:
        if target == SceneID.GAME:
            self.game.reset()
            self.current_scene = GameScene(
                game=self.game,
                asset_size=self.asset_size,
            )
        elif target == SceneID.MENU:
            self.current_scene = MenuScene(
                initial_page_cls=MainMenuPage,
                gameloop=self,
                asset_size=self.asset_size,
            )
        elif target == SceneID.GAMEOVER:
            self.current_scene = MenuScene(
                initial_page_cls=GameOverPage,
                gameloop=self,
                asset_size=self.asset_size,
            )
        elif target == SceneID.QUIT:
            self.is_running = False
        elif target == SceneID.NAME:
            self.current_scene = MenuScene(
                initial_page_cls=NameEntry,
                gameloop=self,
                asset_size=self.asset_size,
            )

    def run(self) -> None:
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                else:
                    action = self.current_scene.handle_event(event)
                    if action:
                        self.change_scene(action)

            action = self.current_scene.update()
            if action:
                self.change_scene(action)

            self.screen.fill((0, 0, 0))
            self.current_scene.render(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()
        sys.exit(0)
