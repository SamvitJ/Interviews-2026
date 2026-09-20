#!/bin/bash
# Copy a bug file to the clipboard for pasting into CoderPad, and start its timer.
#   ./pad.sh b01
# Deliberately does NOT print the source — read it cold in the pad.
cd "$(dirname "$0")" || exit 1
id="$1"
[ -z "$id" ] && { echo "usage: ./pad.sh <bug-id>"; exit 1; }
case "$id" in
  */*)  # a mock bug, e.g. ./pad.sh set-a/m1 -- copy only, the interviewer keeps the clock
    file=$(ls mock/"$id"_*.py 2>/dev/null | head -1)
    [ -z "$file" ] && { echo "No mock bug '$id'. Try set-a/m1 .. set-b/m4."; exit 1; }
    pbcopy < "$file"
    echo "$id copied to clipboard — $(wc -l < "$file" | tr -d ' ') lines, self-contained."
    echo "Paste into your Python 3 pad and hit Run. Do NOT read it here first."
    echo "No timer started: the interviewer session runs the 45-minute clock."
    exit 0 ;;
esac
file=$(ls bugs/tier*/"$id"_*.py 2>/dev/null | head -1)
[ -z "$file" ] && { echo "No bug '$id'."; exit 1; }
case "$file" in
  *tier1*) box=4 ;; *tier2*) box=6 ;; *tier3*) box=8 ;; *) box=10 ;;
esac
pbcopy < "$file"
mkdir -p .drill
[ -f ".drill/start_$id" ] || date +%s > ".drill/start_$id"
echo "$id copied to clipboard — $(wc -l < "$file" | tr -d ' ') lines, no imports, self-contained."
echo "Paste into a Python 3 pad and hit Run. Timebox: ${box} min. Timer started."
echo "Stuck: ./hint.sh $id     Done: paste your fix back and ./drill.sh $id"
