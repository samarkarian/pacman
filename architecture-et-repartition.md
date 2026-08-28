# Pac-Man (42) — Architecture & Répartition

Projet Pac-Man en **Python**, en binôme. Ce doc fige nos choix techniques, le découpage des modules et qui fait quoi. À lire avant de coder.

---

## 1. Stack technique

- **Python 3.10+**, conforme **flake8**, passe **mypy** (type hints partout), docstrings.
- **Lib graphique : Pygame**, mais restreinte au **sous-ensemble « équivalent MLX »** (fenêtre, chargement d'images, blit, pixel, texte, clavier, boucle). On s'interdit : `pygame.mixer` (son), `pygame.sprite`/`pygame.mask` (collisions auto), `pygame.transform` (rotation/scale). → on code ces choses nous-mêmes.
- **Labyrinthes : package `mazegenerator` imposé** (on n'écrit PAS notre générateur). On adapte notre code à SON interface : `MazeGenerator(size=(w,h), perfect=False, seed=…)`, grille en `.maze` (murs encodés en bits : N=1, E=2, S=4, W=8), `seed=42` fixe pour le niveau 1.
- **Jamais de crash / jamais de traceback** affiché : tout géré proprement (`try/except`, context managers).

## 2. Règle d'or

> **La logique du jeu ne connaît JAMAIS Pygame.** Seul le module `Renderer` importe Pygame.

Tout le reste (config, maze, joueur, fantômes, score…) manipule des positions et des grilles → **testable sans fenêtre** (avec `pytest`). C'est ce qui prouve notre conformité MLX et rend l'étape « recode » de la soutenance triviale.

## 3. Architecture des modules

```
pac-man.py                  # Entrée : lit argv, charge config, lance Game (nom imposé)
pacman/
├── config/
│   ├── loader.py           # Parse JSON + commentaires, défauts, clamping
│   └── defaults.py         # Valeurs par défaut (lives, points, seed, temps…)
├── maze/
│   ├── loader.py           # Adapte le package mazegenerator → modèle interne
│   └── maze.py             # Modèle Maze : décodage bits, can_move(), coins, centre
├── entities/
│   ├── entity.py           # Base commune : position grille, direction, déplacement
│   ├── player.py           # Pac-Man
│   ├── ghost.py            # Fantôme (états)
│   └── collectibles.py     # Pacgums & super-pacgums
├── ai/
│   └── ghost_ai.py         # Comportements : poursuite / fuite
├── game/
│   ├── game.py             # Machine à états + boucle + timer  ← ZONE PARTAGÉE
│   ├── level.py            # Un niveau : maze + entités + compteur pacgums
│   ├── scoring.py          # Règles de score (ne décroît jamais)
│   └── cheat.py            # Cheat mode (invincible, skip, freeze, +vies, +vitesse)
├── render/
│   ├── renderer.py         # ⭐ LE wrapper Pygame (seule brique qui importe Pygame)
│   ├── assets.py           # Chargement des sprites/images
│   └── hud.py              # Score / vies / niveau / temps
├── ui/
│   ├── main_menu.py        # Start / Highscores / Instructions / Exit
│   ├── pause_menu.py       # Resume / Retour menu
│   └── end_screens.py      # Game over + Victory (saisie du nom)
├── highscore/
│   └── highscore.py        # Persistance JSON, top 10, validation des noms
└── input/
    └── controls.py         # Flèches / WASD → actions

tests/  ·  assets/  ·  config.json
packaging/  (spec PyInstaller + build Itch.io)
project-management/  (Gantt, Kanban, risques, plan de tests)
Makefile  ·  README.md  ·  .gitignore
```

## 4. Les 3 contrats à figer ENSEMBLE (avant de se séparer)

On se met d'accord sur ces 3 interfaces + on écrit des stubs vides. Ensuite chacun code de son côté **sans se bloquer** :

1. **`Renderer`** → `load_image`, `draw_image`, `put_pixel`, `put_string`, `clear`, `on_key`, `run_loop`.
2. **`Maze`** → `can_move(x, y, dir)`, `is_walkable(x, y)`, `corners()`, `center()`, `neighbors(x, y)`.
3. **`Config`** → la liste des clés + types + valeurs par défaut.

## 5. Répartition des tâches

Chacun a une grosse pièce algorithmique (A = le joueur, B = l'IA des fantômes). Ils partagent la même mécanique de base (déplacement sur grille + `can_move`) via une classe `Entity` commune ; seule diffère la façon de **choisir sa direction** (A : clavier — B : calcul).

### 👤 Sacha (A) — Moteur, Rendu & Joueur

- **Renderer** (wrapper Pygame) + **assets** → la seule brique qui importe Pygame ; il définit l'API que les deux utilisent.
- **Boucle de jeu + machine à états** (menu → jeu → pause → fin) + **timer** de niveau.
- **Input** clavier (flèches/WASD).
- **Joueur** ⭐ : déplacement sur grille, collisions murs, direction bufferisée (virage fluide), respawn au centre.
- **Collectibles** : consommation des pacgums/super-pacgums, condition de victoire (tout mangé).
- **Rendu en jeu** : labyrinthe (à partir des bits), entités, **HUD**, menu pause.

### 👤 [Ami] (B) — Monde, Systèmes & Fantômes

- **Config loader** : JSON + commentaires, valeurs par défaut, clamping (robuste, jamais de crash).
- **Maze loader + modèle `Maze`** : adapter le package `mazegenerator`, décoder les murs en bits, exposer `can_move`/`is_walkable`/`corners`/`center`.
- **Fantômes + IA** ⭐ : états chase / flee / eaten, choix de direction (viser ou fuir le joueur), respawn au coin après 5–10 s.
- **Highscore** (JSON, top 10, noms ≤ 10 caractères alphanum) + **scoring** + **cheat mode**.
- **Écrans data-driven** : menu principal (affiche les highscores), instructions, game over / victory (saisie du nom).

### 🤝 En binôme (pair programming)

- `game/game.py` (la « colle » entre les deux mondes).
- Les **3 contrats** ci-dessus.
- **La collision joueur ↔ fantôme** — l'unique point de rencontre entre nos deux tranches :
  - si le fantôme est effrayé → fantôme mangé (+points, état EATEN, respawn différé) ;
  - sinon → le joueur perd une vie / respawn (ou game over).

## 6. Livrables non-code (notés par le sujet)

| Livrable | Responsable |
|---|---|
| Packaging PyInstaller + déploiement **Itch.io** | Sacha (A) |
| Docs gestion de projet (Gantt, Kanban, risques, plan de tests) | [Ami] (B), alimenté par les deux |
| README (anglais, sections imposées) | Chacun rédige les sections de ses modules |

## 7. Ordre de démarrage conseillé

1. **Ensemble** : figer les 3 contrats + stubs.
2. **B** : config loader + maze loader → livrer le modèle `Maze` tôt (ça débloque A).
3. **A** : Renderer + une scène de debug qui affiche le maze → débloque le visuel pour B.
4. **Chacun sa tranche** en parallèle.
5. **Ensemble** : `game.py` (collisions, transitions d'états).
6. **Fin** : cheat, highscore, polish, packaging, docs.
