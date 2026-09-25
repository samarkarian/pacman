#!/bin/sh
# Double-clic (macOS) ou ./play.command : lance le jeu avec sa config
cd "$(dirname "$0")" && ./pac-man config.json
