from Scene import SceneID
from Game_scene import GameScene
from MenuScene import MenuScene, MainMenuPage
import pygame

class GameLoop:
    def __init__(self, game, width: int = 1080, height: int = 1080) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.game = game
        self.asset_size: int = 64

        # Démarrage sur le MenuScene avec sa page initiale injectée
        self.current_scene = MenuScene(
            initial_page_cls=MainMenuPage,
            asset_size=self.asset_size,
        )

    def change_scene(self, target: SceneID) -> None:
        if target == SceneID.MENU:
            self.current_scene = MenuScene(
                initial_page_cls=MainMenuPage,
                asset_size=self.asset_size,
            )
        elif target == SceneID.GAME:
            self.current_scene = GameScene(
                game=self.game,
                asset_size=self.asset_size,
            )
        elif target == SceneID.QUIT:
            self.is_running = False

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



# import sys
# from maze_display import MazeDisplayer
# from Entity_factory import Entity_factory
# from Menu import Menu
# class GameLoop:
#     """
#     Classe principale gérant la fenêtre et la boucle de jeu, 
#     façon MLX.
#     """
#     def __init__(self, mazegen) -> None:
#         pygame.init()

#         self.width: int = 1080
#         self.height: int = 1080
#         self.asset_size: int = 64
#         self.animation_speed: int = 400
#         self.is_running: bool = False

#         self.screen: pygame.Surface = pygame.display.set_mode((self.width, self.height))

#         self.entities = []
#         self.mazedisplayer = MazeDisplayer(mazegen, self.screen, self.asset_size)

#         self.player_x = 0
#         self.player_y = 0

#         self.state = 'MENU'
#         # self.menu = Menu(self.screen)

#     def handle_events(self) -> None:
#         """
#         Équivalent de mlx_hook() : capture des événements clavier et fenêtre.
#         """
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 self.is_running = False
            
#             elif event.type == pygame.KEYDOWN:
#                 if event.key == pygame.K_ESCAPE:
#                     self.is_running = False
#                 elif event.key == pygame.K_UP:
#                     self.player_y += 50
#                 elif event.key == pygame.K_DOWN:
#                     self.player_y -= 50
#                 elif event.key == pygame.K_LEFT:
#                     self.player_x += 50
#                 elif event.key == pygame.K_RIGHT:
#                     self.player_x -= 50
#                 elif event.key == pygame.K_SPACE:
#                     if self.state == 'GAME':
#                         print('A')
#                         self.state = 'MENU'
#                     else:
#                         print('B')
#                         self.state = 'GAME' #A supprimer une fois le menu fait



#     def load_sprites(self):
#         """fonction appelant le load_sprites() de toutes les entites
#         """
#         self.mazedisplayer.load_sprites()
#         for e in self.entities:
#             e.load_sprites()

#     def render(self) -> None:
#         """
#         fonction appellant les render() de toutes les entites
#         """
#         self.screen.fill((0, 0, 0))
#         offset = (self.player_x, self.player_y)
#         self.mazedisplayer.render(offset)
#         for e in self.entities:
#             e.render(self.animation_speed, offset)
#         pygame.display.flip()
#         pygame.display.flip()

#     def future_menu_function(self):
#         """fonction de menu a rajouter, pernmettant notamment de reload de la taille 32 a 64
#         """
#         factory = Entity_factory(self.asset_size, self.screen)
#         # factory = Entity_factory(32, self.screen)
#         self.entities = factory.generate_entities()
#         self.load_sprites()

#     def run(self) -> None:
#         """
#         Équivalent de mlx_loop() : boucle infinie du jeu.
#         """
#         self.is_running = True
        
#         clock = pygame.time.Clock()
#         self.future_menu_function()

#         while self.is_running:
#             if self.state == 'MENU':
#                 self.handle_events()
#                 self.render()
#                 print(self.state)

#             elif self.state == 'GAME':
#                 self.handle_events()
#                 self.render()
#                 print(self.state)

#         clock.tick(60)

#         pygame.quit()
#         sys.exit(0)
