import random


class GhostIA:
    def __init__(self, field, spawn):

        self.field = field
        self.x, self.y = spawn
        self.previous = None

    def step(self) -> None:

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
        self.x, self.y = random.choice(choices)

        return None


if __name__ == "__main__":
    from json_loader import json_load
    from game import build_level

    config = json_load(open("config.json").read())
    field = build_level(config, 0)

    if field is not None:
        maze = field.maze
        spawns = field.ghost_spawns
        print("spawns :", spawns)          # les 4 coins

        # 1. placement : chaque fantome demarre sur son coin
        ghosts = [GhostIA(field, spawn) for spawn in spawns]
        for ghost in ghosts:
            print("spawn  :", (ghost.x, ghost.y))

        # 2. un pas : il doit atterrir sur une case voisine accessible
        ghost = ghosts[0]
        depart = (ghost.x, ghost.y)
        voisins = maze.neighbors(depart[0], depart[1])
        ghost.step()
        arrivee = (ghost.x, ghost.y)
        print("depart :", depart, "voisins :", voisins)
        print("arrivee:", arrivee, "-> legal ?", arrivee in voisins)

        # 3. 50 pas : jamais de traversee de mur
        ghost = GhostIA(field, spawns[0])
        illegal = 0
        for _ in range(50):
            avant = (ghost.x, ghost.y)
            ghost.step()
            if (ghost.x, ghost.y) not in maze.neighbors(avant[0], avant[1]):
                illegal += 1
        print("deplacements illegaux sur 50 pas :", illegal)   # attendu 0

        # 4. pas d'oscillation : il doit explorer, pas faire l'aller-retour
        ghost = GhostIA(field, spawns[0])
        vues = set()
        for _ in range(50):
            ghost.step()
            vues.add((ghost.x, ghost.y))
        print("cases distinctes visitees en 50 pas :", len(vues))
        print("   (2 ou 3 = il oscille, il faut exclure la case precedente)")

        # 5. cul-de-sac : une case a un seul voisin ne doit pas le bloquer
        impasses = [
            (x, y)
            for y in range(maze.height)
            for x in range(maze.width)
            if maze.is_walkable(x, y) and len(maze.neighbors(x, y)) == 1
        ]
        print("impasses dans le labyrinthe :", len(impasses))
        if impasses:
            ghost = GhostIA(field, impasses[0])
            ghost.step()
            ghost.step()
            print("depuis l'impasse", impasses[0], "-> apres 2 pas :",
                  (ghost.x, ghost.y), "(ne doit pas rester colle)")
