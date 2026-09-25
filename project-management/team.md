# Team

Sacha (samarkar) and Robin (rschimme).

The initial split gave the engine, the rendering and the player to Sacha,
and the configuration, the maze and the ghosts to Robin. In the end it
was reversed:

- Robin: sprites and tileset, rendering classes, game loop and scenes,
  menus, window resizing, HUD, player and ghost display
  (interpolation, states), game over page

- Sacha: configuration (JSON + pydantic), Maze class, PlayField and pacgums,
  ghost AI, levels, highscores and name entry, score and instructions
  pages, pause, cheat mode

Organisation:

- an architecture document written on the first day (modules, interfaces, split)
- a GitHub repository with one branch per person (Robin_dev, Sash_dev), merged into main
- handover notes kept in the repository (removed from the final version)
- a shared Makefile so that we both use the same commands

Difficulties:

- on Sept 2, two entry points (main) written separately had to be merged
- on Sept 3, the game loop was restructured into scenes before adding the menus
- game_scene.py and config.json were edited by both of us, which brought
  test values and debug code onto main. We now tell each other before
  editing a file owned by the other
- when a life was lost, the ghost did not seem to be on the same cell as
  Pac-Man: the animation was behind the game logic. A 0.5 s pause before
  putting everyone back in place solved it
