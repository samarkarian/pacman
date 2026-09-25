*This project has been created as part of the 42 curriculum by samarkar, rschimme*

# Pac-Man

## Description

A complete, playable Pac-Man clone written in Python with pygame.
The goal of the project is to rebuild the 1980 arcade classic with a clean,
object-oriented and typed code base, mazes produced by another group's
A-Maze-ing package, a persistent highscore table, a cheat mode for the peer
review, and a build that can be downloaded and launched from itch.io.

What the game offers:

- 10 levels (configurable). The first maze always uses the same seed, the
  following ones are random.
- Pac-Man moves with the arrow keys and slides smoothly from cell to cell.
- 4 ghosts with different behaviours (chase, random, copy the player), who
  run away when a super pac-gum makes them blue, and come back to their
  corner 5 seconds after being eaten.
- A HUD with score, time left, level and lives, a pause menu, a Game Over /
  Victory screen with name entry, and a top 10 highscore page.
- Two window sizes: 1500×1500 (64 px sprites) or 750×750 (32 px sprites).

## Instructions

### Requirements

- Python 3.13 and [uv](https://docs.astral.sh/uv/) (it installs pygame,
  pydantic, the maze generator wheel and the dev tools).

### Install and run

```bash
make install        # uv sync: creates .venv and installs the dependencies
make run            # uv run python3 pac-man.py config.json
```

The program takes exactly one argument, a JSON configuration file:

```bash
python3 pac-man.py config.json
```

Other Makefile rules:

| Rule | Action |
|---|---|
| `make debug` | runs the game under `pdb` |
| `make lint` | `flake8` + `mypy` with the flags required by the subject |
| `make clean` | removes caches, `build/` and `dist/` |
| `make package` | builds the standalone game in `dist/pac-man/` and `dist/pac-man.zip` |

### Controls

| Key | Action |
|---|---|
| Arrows | move Pac-Man (the turn is remembered until it is possible) |
| Esc | pause / resume. The pause menu offers Resume or back to the main menu |
| Up / Down, Enter or Space | navigate and validate in every menu |
| Esc in a menu | previous page (on the main menu: quit; on the end screen: main menu without saving) |

### Cheat mode (for the evaluation)

Press **C** during a game to toggle the cheat mode. The HUD then shows
`CHEAT` and the active effects. While it is on:

| Key | Effect |
|---|---|
| N | skip level (on the last level: immediate victory) |
| I | invincibility on / off (blue ghosts can still be eaten) |
| F | freeze the ghosts on / off (their colour still follows the super pac-gums) |
| L | +1 life (the HUD shows "♥ x10" when the hearts do not fit) |

The cheat mode is reset when a new game starts.

### Packaging and itch.io

`make package` runs PyInstaller with the spec file at the root of the
repository (`pac-man.spec`) and produces a folder build for the current
operating system:

```
dist/pac-man/
├── pac-man          # executable
├── config.json      # editable configuration
├── README.txt       # in-package instructions (controls, options, configuration)
├── play.command     # double-click launcher (macOS)
├── .itch.toml       # itch.io app manifest: launches "pac-man config.json"
└── _internal/       # Python runtime, libraries and sprites
```

`dist/pac-man.zip` is the archive uploaded to itch.io as a free,
restricted (unlisted) project.

## Configuration

The configuration is a JSON file. Lines starting with `#` are comments and
are removed before parsing. Unknown keys are ignored. A missing key, a value
with the wrong type or out of range is replaced by a safe value, with a
warning in the terminal, and the game continues. Only a file that is not a
valid JSON object makes the game use the whole default configuration, with
a message.

| Key | Default | Accepted values |
|---|---|---|
| `highscore_filename` | `"scores.json"` | non-empty string (relative to the game folder) |
| `level` | 10 levels of 15×11 | non-empty list of `{"width", "height"}` (an item that is not an object becomes a 15×11 level; fewer than 10 levels are completed with 15×11 levels, as the game needs at least 10) |
| `level[].width` | 15 | 14 to 23 |
| `level[].height` | 11 | 10 to 21 |
| `lives` | 3 | at least 1 |
| `pacgum` | 42 | at least 0 (validated but not used: every free cell gets a pac-gum) |
| `points_per_pacgum` | 10 | at least 0 |
| `points_per_super_pacgum` | 50 | at least 0 |
| `points_per_ghost` | 200 | at least 0 |
| `seed` | 42 | seed of the first maze (a seed of 0 or less gives a random maze) |
| `level_max_time` | 90 | seconds per level, at least 10 |

The size limits come from the window (a 23×21 maze still fits next to the
HUD) and from the generator, which needs at least 14×10 cells to draw its
"42" pattern.

## Highscore

- Stored in a JSON file in the game folder (`scores.json` by default), as a
  list of `{"name": ..., "score": ...}` objects.
- Loaded when the game starts, saved when the player validates their name
  on the Game Over / Victory screen.
- Only the top 10 is kept, sorted from the best score.
- Names: 1 to 10 characters, letters, digits and spaces only. Scores:
  non-negative integers. Invalid entries in the file are skipped.
- Robust to file errors: a missing file gives an empty table; an unreadable
  file or invalid JSON prints a warning and gives an empty table; a failed
  save shows an error on the name screen instead of crashing.

Why JSON: it is human-readable (easy to check during the evaluation), needs
no extra dependency, and the table is tiny. Validation happens both when
loading and before saving, so a hand-edited file cannot break the game.

## Maze Generation

The mazes come from the A-Maze-ing package of another group, installed as
is from `mazegenerator-2.1.0-py3-none-any.whl`:

```python
MazeGenerator(size=(width, height), perfect=False, seed=seed).maze
```

- `perfect=False` produces loops, so the corridors are playable for a
  Pac-Man (several ways around a ghost).
- The result is a grid of integers. Each cell stores its closed walls as
  bits: North = 1, East = 2, South = 4, West = 8. A value of 15 is a closed
  cell (the "42" drawn in the middle of the maze).
- `maze.py` wraps this grid in a `Maze` class: `can_move(x, y, direction)`
  checks the wall bit and that the next cell is walkable, `neighbors()`
  lists the reachable cells, `corners()` gives the ghost spawns and
  `center()` the nearest walkable cell to the middle (the player spawn).
- Level 1 uses the configured seed; the next levels use seed 0, which the
  package turns into a random maze.
- If the generator raises an error, it is caught and a clear message is
  printed; if it happens for the first level, the program exits cleanly.

## Implementation

- **Game loop** (`game_loop.py`): 60 frames per second. Each frame reads the
  keyboard, updates the current scene and draws it. Scenes are the menu
  scene (a stack of pages) and the game scene.
- **Logic and display are separated.** `Game` (in `game.py`) holds the
  rules and never draws. Each character has a logic part (`PlayerController`,
  `GhostAI`) and a display part (`PlayerRenderer`, `GhostRenderer`).
- **Time-based movement.** `Game.update(dt)` receives the elapsed time
  (capped at 100 ms) and moves Pac-Man every 150 ms and the ghosts every
  200 ms. On screen, sprites slide between two cells (linear
  interpolation).
- **Ghost AI.** Two ghosts chase Pac-Man (closest cell by Manhattan
  distance), one moves randomly, one copies the player's direction. When
  blue, they pick the farthest cell. A ghost never turns back unless it is
  in a dead end. The blue state lasts 6 s and blinks during the last third.
- **Collisions.** Compared on grid cells after every step. After a lost
  life, the game waits 0.5 s so the sprites visibly meet before everybody is
  sent back to the spawn points.
- **Pause** freezes the game timer and all movement without leaving the
  game scene, so the game is resumed exactly where it stopped.
- **Robustness.** The configuration is validated with pydantic. File, image
  and font loading errors are caught. The main loop is wrapped so an
  unexpected error prints a message instead of a traceback.
- **Graphics.** pygame is limited to features that have an MLX equivalent:
  a window, image loading, blitting, filled surfaces, text and keyboard
  events. The sprites were drawn by the team; the font is KG Perfect
  Penmanship by Kimberly Geswein.
- **Quality.** The code passes `flake8` and `mypy` (flags of the subject),
  with type hints and docstrings everywhere.

## General Software Architecture

`pac-man.py`, the packaging spec, the config and the sprites stay at the
root of the repository. Every other module is in `src/` and is imported as
`src.<module>` (for example `from src.game import Game`).

```
pac-man.py            entry point: reads the config file, starts GameLoop
game_loop.py          GameLoop: window, main loop, switches between scenes
scene.py              Scene (abstract), SceneID
│
├── menu_scene.py     MenuScene: stack of MenuPage, Esc = back
│   ├── menu_classes.py   UIButton, UISprite, MenuPage (abstract)
│   └── menu_pages.py     MainMenuPage, ResolutionPage, HighscorePage,
│                         InstructionsPages, NameEntry (end screen)
│
└── game_scene.py     GameScene: keys, pause menu, cheat keys, drawing
    ├── game.py           Game: levels, score, lives, timer, collisions, cheats
    │   ├── field.py          PlayField: Maze + pac-gums + spawn points
    │   │   ├── maze.py           Maze, generate_maze (A-Maze-ing adapter)
    │   │   └── pacgums.py        Pacgum
    │   ├── player.py         Player = PlayerController + PlayerRenderer
    │   ├── ghost.py          Ghost = GhostAI + GhostRenderer
    │   └── high_score.py     load / validate / add / save the top 10
    ├── maze_display.py   MazeDisplayer: walls and pac-gums
    └── hud_container.py  HUDContainer → hud_render.py (score, time, level,
                          lives, cheat)

json_loader.py        Config / Level (pydantic models), json_load()
display_abstractmethods.py   Renderer, Entity: base classes of everything drawn
sprite_cache.py       load_image(): each image is loaded once
```

Relationships: `GameLoop` owns one `Game` for the whole session and creates
the scenes. `GameScene` asks `Game` to update, then draws `Game`'s objects
through the renderers. Pages of the menu read `Game` (highscores, final
score) through the `MenuScene` they belong to.

## Project Management

The project was split between the two members from the start (engine,
display and menus on one side, game logic and data on the other), with
shared work on the game rules and the collision. We used Git with personal
branches merged into `main`, a written architecture document, and headless
test scripts to check the features.

The documents (planning, team and blocking points, tests and risks) are
in the [`project-management/`](project-management/) directory.

## Resources

- [pygame documentation](https://www.pygame.org/docs/)
- [pydantic documentation](https://docs.pydantic.dev/)
- [The Pac-Man Dossier](https://pacman.holenet.info/) by Jamey Pittman,
  the reference on the original game rules
- [Understanding Pac-Man Ghost Behavior](https://gameinternals.com/understanding-pac-man-ghost-behavior)
  by Chad Birch
- [PyInstaller manual](https://pyinstaller.org/) and the
  [itch.io app manifest](https://itch.io/docs/itch/integrating/manifest.html)

### Use of AI

Explanation of the various concepts, debugging, and code review.

Every AI suggestion was read, tested in the game and is understood by the
team; nothing was kept without being able to explain it.
