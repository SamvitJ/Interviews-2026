#!/bin/bash
# Timed drill runner.
#   ./drill.sh            status of every bug
#   ./drill.sh b01        start the timer (first call), run the tests, show elapsed
#   ./drill.sh b01 done   log it as solved in CoderPad (no local edit needed)
#   ./drill.sh reset b01  clear timer + hint state for one bug
cd "$(dirname "$0")" || exit 1
mkdir -p .drill

timebox_for() {  # minutes, by tier
  case "$1" in
    *tier1*) echo 4 ;; *tier2*) echo 6 ;; *tier3*) echo 8 ;; *tier4*) echo 10 ;;
    *) echo 10 ;;
  esac
}

find_file() { ls bugs/tier*/"$1"_*.py 2>/dev/null | head -1; }

fmt() { printf '%dm%02ds' $(( $1 / 60 )) $(( $1 % 60 )); }

if [ "$1" = "reset" ]; then
  rm -f ".drill/start_$2" ".drill/hint_$2"; echo "reset $2"; exit 0
fi

if [ -z "$1" ]; then
  printf '%-6s %-28s %-9s %s\n' ID FILE STATUS TIME
  for f in bugs/tier*/b*.py; do
    id=$(basename "$f" | cut -d_ -f1)
    start=$(cat ".drill/start_$id" 2>/dev/null)
    score=$(python3 "$f" 2>&1 | grep -o '[0-9]*/[0-9]* passing' | tail -1)
    n=${score%%/*}; m=${score#*/}; m=${m%% *}
    if [ -z "$start" ]; then st="untouched"; el="-"
    elif [ "$n" = "$m" ]; then st="SOLVED"; el="$(( ($(date +%s) - start) / 60 ))m"
    else st="in progress"; el="$(( ($(date +%s) - start) / 60 ))m"; fi
    printf '%-6s %-28s %-9s %s\n' "$id" "$(basename "$f")" "$st" "$el"
  done
  exit 0
fi

id="$1"; file=$(find_file "$id")
if [ "$2" = "done" ]; then
  start=$(cat ".drill/start_$id" 2>/dev/null)
  [ -z "$start" ] && { echo "No timer running for $id."; exit 1; }
  secs=$(( $(date +%s) - start )); elapsed=$(( secs / 60 ))
  box=$(timebox_for "$(find_file "$id")")
  if grep -q "^$id " progress.log 2>/dev/null; then
    echo "· $id already logged at $(grep "^$id " progress.log | awk '{print $2}') — not overwriting."
    echo "  (clock still running: $(fmt $secs). To redo: ./drill.sh reset $id and delete its row.)"
  else
    printf '%-6s %7s  (box %2dm)  hints:%s  [pad]\n' "$id" "$(fmt $secs)" "$box" \
      "$(cat ".drill/hint_$id" 2>/dev/null || echo 0)" >> progress.log
    echo "✓ $id logged: $(fmt $secs) (timebox ${box}m), hints used: $(cat ".drill/hint_$id" 2>/dev/null || echo 0)"
  fi
  exit 0
fi
[ -z "$file" ] && { echo "No bug '$id'."; exit 1; }
box=$(timebox_for "$file"); state=".drill/start_$id"

if [ ! -f "$state" ]; then
  date +%s > "$state"
  echo "══ $id — $file"
  echo "══ timebox: ${box} minutes. Timer started. Run './drill.sh $id' again to check."
  echo
fi

start=$(cat "$state"); secs=$(( $(date +%s) - start )); elapsed=$(( secs / 60 ))
python3 "$file" 2>&1 | tail -20
score=$(python3 "$file" 2>&1 | grep -o '[0-9]*/[0-9]* passing' | tail -1)
n=${score%%/*}; m=${score#*/}; m=${m%% *}
echo
if [ -n "$n" ] && [ "$n" = "$m" ]; then
  echo "✓ SOLVED in $(fmt $secs)  (timebox ${box}m)"
  grep -q "^$id " progress.log 2>/dev/null || \
    printf '%-6s %7s  (box %2dm)  hints:%s\n' "$id" "$(fmt $secs)" "$box" \
      "$(cat ".drill/hint_$id" 2>/dev/null || echo 0)" >> progress.log
elif [ "$elapsed" -ge "$box" ]; then
  echo "⏰ $(fmt $secs) elapsed — past the ${box}m timebox. Stop and read the answer."
else
  echo "   $(fmt $secs) elapsed of ${box}m00s. Stuck? ./hint.sh $id"
fi
