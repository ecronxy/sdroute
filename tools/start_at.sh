#!/bin/sh
# usage: start_at.sh end15 | kf15_late | off   (список: см. README.md)
F="${GAME_DIR:-./game}/start_at.txt"
if [ "$1" = off ] || [ -z "$1" ]; then rm -f "$F"; echo "старт обычный"; else echo "$1" > "$F"; echo "«Новая игра» теперь стартует с точки $1"; fi
