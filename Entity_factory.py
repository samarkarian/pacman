from Display_abstractmethods import Entity, Ghost

class Entity_factory:
    def __init__(self, asset_size: int, screen):
        self.entities = []
        self.asset_size = asset_size
        self.screen = screen
        pass

    def generate_entities(self):
        self.entities.append(Ghost(posx=0, posy=0, asset_size=self.asset_size, screen=self.screen, color='cyan'))
        return self.entities
