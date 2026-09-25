# Planning

Order decided at the start of the project:

1. define the interfaces together (Maze, Config, rendering)
2. build the configuration and the maze first
3. each of us works on their own part in parallel
4. write the game rules (game.py) together
5. finish with cheat mode, highscores, packaging and documentation

What actually happened, from the commit history:

- Aug 28 to Sept 1: repository created, sprites, first pygame window, maze display
- Sept 2 to 7: config loading, Maze class, scene system, menu and resizing
- Sept 8 to 14: merge of both parts, player / ghost / pacgum classes, ghost states, smooth movement
- Sept 15 to 21: ghost AI, level progression, highscores and name entry, HUD
- Sept 22 to 25: score and instructions pages, pause, cheat mode, lint, README, packaging

The planned order was kept, but the game rules were finished in the 3rd
week instead of the 2nd. So the end screen, pause and cheat mode were
pushed to the last week, and packaging and documentation to the last day,
with little margin.
