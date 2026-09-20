#!/bin/bash
# Graduated hints. ./hint.sh b07   -> next unseen rung
#                  ./hint.sh b07 3 -> that rung explicitly
cd "$(dirname "$0")" || exit 1
id="$1"; want="$2"
[ -z "$id" ] && { echo "usage: ./hint.sh <bug-id> [rung]"; exit 1; }
mkdir -p .drill
state=".drill/hint_$id"
if [ -z "$want" ]; then
  seen=$(cat "$state" 2>/dev/null || echo 0)
  want=$((seen + 1))
fi
if [ "$want" -gt 3 ]; then
  echo "No rung $want. Rung 3 names the bug outright; after that, read answers/ANSWERS.md."
  exit 0
fi
line=$(awk -v id="### $id" '$0==id{f=1;next} /^### /{f=0} f' answers/HINTS.md | grep "^$want\." )
[ -z "$line" ] && { echo "No hints for '$id'."; exit 1; }
if [ "$want" -gt 1 ]; then
  echo "── rung $want of 3 (rungs 1-$((want-1)) already shown) ──"
else
  echo "── rung 1 of 3 ──"
fi
[ "$want" = 3 ] && echo "── this one names the bug ──"
echo "$line"
echo "$want" > "$state"
