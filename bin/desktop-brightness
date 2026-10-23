#!/usr/bin/env bash
# Adjust brightness on all DDC/CI (external) monitors via ddcutil.
# Usage: brightness.sh +|-  [step%]
# Requires: i2c-dev module loaded + user in the 'i2c' group (see setup notes).
set -euo pipefail

op="${1:-+}"        # + or -
step="${2:-10}"     # percent

# VCP feature 0x10 = brightness. Apply to every detected I2C bus in parallel.
mapfile -t buses < <(ddcutil detect --terse 2>/dev/null \
    | grep -oP '/dev/i2c-\K[0-9]+')

if [ "${#buses[@]}" -eq 0 ]; then
    notify-send "Brightness" "No DDC/CI monitors detected" 2>/dev/null || true
    exit 1
fi

for bus in "${buses[@]}"; do
    ddcutil --bus "$bus" setvcp 10 "$op" "$step" --noverify >/dev/null 2>&1 &
done
wait
