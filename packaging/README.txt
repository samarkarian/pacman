PAC-MAN - 42 project by samarkar and rschimme
=============================================

LAUNCH
  - itch.io app: click "Launch" (it runs: pac-man config.json)
  - macOS: double-click play.command
  - Terminal: ./pac-man config.json

CONTROLS
  Arrows ............ move Pac-Man
  Esc ............... pause (Resume / back to main menu)
  Up / Down + Enter . choose in the menus
  Esc in a menu ..... go back (quits from the main menu)

RULES
  Eat every pac-gum to clear the level, before the timer runs out.
  A ghost touching you costs a life. Super pac-gums (corners) make the
  ghosts blue for a few seconds: eat them for bonus points.
  Clear the 10 levels to win. At the end, type your name for the top 10.

CHEAT MODE (for evaluation)
  C ..... cheat mode on / off (shown in the HUD)
  N ..... skip level (wins the game on the last level)
  I ..... invincible
  F ..... freeze the ghosts
  L ..... +1 life

OPTIONS / CONFIGURATION
  Resize (main menu): small (750x750) or medium (1500x1500) window.
  Edit config.json (next to the game) to change the levels, lives,
  points, seed and time per level. Lines starting with # are comments.
  Invalid values are replaced by safe defaults, with a message.
  Highscores are saved in _internal/scores.json.
