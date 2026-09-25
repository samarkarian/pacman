# Tests and risks

Besides playing the game, we tested it with scripts that run it without
a window (pygame in dummy mode).

Tests done:

- launch: no argument, wrong file, invalid configuration
  (comments, wrong types, out of range values). Clear message, no traceback
- pause, resume and back to the menu
- cheat mode
- pause on death and last life
- highscores: top 10, rejected names, missing or corrupted file
- every screen at both sizes (64 px and 32 px sprites)
- make lint: 0 errors

Bugs found and fixed:

- a level lasted about 450 s instead of 90
- Pac-Man could spawn inside the "42" pattern
- crash with an out of range config value
- frozen ghosts did not turn blue
- Esc on the end screen closed the game
