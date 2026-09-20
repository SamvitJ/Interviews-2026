#!/bin/bash
# Scoreboard across every practice file. Usage: ./score.sh
cd "$(dirname "$0")/bugs" || exit 1
for f in tier*/b*.py; do
  printf '%-36s %s\n' "$f" "$(python3 "$f" 2>&1 | tail -1)"
done
