from maze import Maze


class Player:
    def __init__(self, field) -> None:

        self.field = field
        self.x, self.y = field.player_spawn

    def move(self, direction: str) -> str | None:

        dir_dict = {
            'N': (0, -1),
            'E': (1, 0),
            'S': (0, 1),
            'W': (-1, 0)
        }

        maze = self.field.maze
        if maze.can_move(self.x, self.y, direction):
            dx, dy = dir_dict[direction]
            self.x += dx
            self.y += dy
            if self.field.eat_pacgum(self.x, self.y):
                return "pacgum"
            if self.field.eat_super_pacgum(self.x, self.y):
                return "super_pacgum"

        return None

# if __name__ == "__main__":
#     from json_loader import Config
#     from game import build_level

#     field = build_level(Config(), 0)
#     if field is not None:
#         player = Player(field)

#         print("spawn  :", player.x, player.y)      # (9, 9)

#         player.move('N')
#         print("apres N:", player.x, player.y)       # (9, 8)  couloir libre

#         player.move('S')
#         print("apres S:", player.x, player.y)       # (9, 9)  retour

#         player.move('E')
#         print("apres E:", player.x, player.y)       # (9, 9)  mur -> bloque

#         player.move('W')
#         print("apres W:", player.x, player.y)       # (9, 9)  mur -> bloque

#         print([player.move(d) for d in "NNNWWWNWNNNWNNWSWNWW"])
#         print(len(field.pacgums), len(field.super_pacgums))
