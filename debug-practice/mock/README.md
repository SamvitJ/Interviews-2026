# Mock interview sets

Two sealed sets of 4 bugs each, ordered easy → hard, sized for a 45-minute
run. **Do not browse these files before your mock.** They are the only bugs you
haven't seen, and they're worth far more as a cold run than as reading.

- `set-a/` — first mock
- `set-b/` — second mock
- `answers/INTERVIEWER.md` — protocol, hint ladders, answer key, scoring rubric.
  For whoever is running the mock. Not for you, until after.

## Running it with Claude

Open a fresh Claude Code session in this directory and paste:

> Run a mock debugging interview using `mock/set-a`. Read
> `mock/answers/INTERVIEWER.md` and follow the protocol there exactly. I'm the
> candidate — give me one bug at a time, stay in character, and don't reveal
> anything I haven't found myself.

Swap in `set-b` for the second run. A fresh session matters: a session that
watched these files get written already knows every answer.

## Running it with a person

`INTERVIEWER.md` is written so a friend who doesn't know Python can run it. The
hint ladders are scripted and the rubric is concrete.

## Running it solo

Set a 45-minute timer, open `set-a/m1` through `m4` in order, and record
yourself talking. It's a weaker rehearsal of the interpersonal part but a
perfectly good rehearsal of the debugging part. Score yourself against the
rubric afterward.
