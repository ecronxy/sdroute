#!/bin/sh
# usage: runplan.sh tag display timeout   (изолированный Xvfb, окно владельца не трогаем)
W=${SDRF_WORK:-$(cd "$(dirname "$0")" && pwd)/work}
D=$2
rm -f $W/run_$1.log
Xvfb :$D -screen 0 1280x720x24 >/dev/null 2>&1 &
XP=$!
sleep 2
env -u WAYLAND_DISPLAY DISPLAY=:$D SDL_VIDEODRIVER=x11 ZPLAN=$W/plan_$1.json ZLOG=$W/run_$1.log SDL_AUDIODRIVER=dummy RENPY_RENDERER=sw timeout ${3:-900} ${RENPY_SH:-renpy.sh} $W/proj < /dev/null > $W/run_$1.out 2>&1
echo rc=$?
kill $XP
