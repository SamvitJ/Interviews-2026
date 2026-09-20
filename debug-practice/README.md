# Debugging practice — Factory, Monday

16 buggy Python files, four difficulty tiers, one bug each. Every file runs
standalone and prints PASS/FAIL per case plus a score:

    python3 bugs/tier1/b01_report_builder.py

`./score.sh` prints the scoreboard for all 16.

`mock/` holds two additional sealed 4-bug sets for timed mock interviews.
Leave those alone until Sunday.

The answer key is in `answers/ANSWERS.md`. Each entry gives the root cause, the
minimal fix, the archetype, and the symptom-shape that should have tipped you
off. **Don't open it until you've fixed the bug or burned your full timebox.**

## Rules while practicing

These matter more than the bugs do — they're what makes practice transfer:

1. **Turn off Copilot / Cursor / any AI autocomplete.** CoderPad has none. If
   you practice with completion on, you're rehearsing a skill you won't have.
2. **No internet.** Standard library only, from memory.
3. **Run a timer** and keep it visible.
4. **Talk out loud the entire time.** Record yourself on Sunday. The silences
   are the thing you're trying to eliminate, and you cannot hear them live.
5. **Run the file before you read it.** Every time. Let the failure tell you
   where to look instead of scanning for something that looks off.
6. **Say your hypothesis before you test it**, in this shape: *"I think X, so
   if I print Y I should see Z."* If you can't fill in the blanks, you don't
   have a hypothesis yet — you're about to guess.
7. **Fix minimally.** No refactoring, no renaming, no cleanup. The interviewer
   is reading your diff.
8. **Re-run after the fix**, and check you didn't break a passing case.

## Timeboxes

Real pace is ~8-10 minutes per bug including reading, talking and fixing.
Practice tighter than that:

| Tier | Files | Target |
|---|---|---|
| 1 | b01-b04 | 4 min each |
| 2 | b05-b08 | 6 min each |
| 3 | b09-b12 | 8 min each |
| 4 | b13-b16 | 10 min each |

When the timer goes off, stop and read the answer. Going 25 minutes over on one
bug teaches you nothing you can use on Monday — the interview will cut you off
too, and the skill you actually need is noticing you're stuck and saying so.

## Passing tests are not evidence

Several of these files — among the numbered bugs and the mock sets both — have
tests that pass **by coincidence**. The code is broken and the green line next
to it is luck: an input that happens to agree with the wrong behavior.

You are not told which ones. That is the point.

The habit it trains: when you suspect a function, don't let a nearby passing
test talk you out of it. Probe the "working" behavior yourself with an input of
your own choosing — a throwaway `print(f(...))` on a case the harness didn't
cover. Most of fast debugging is constructing one cheap probe to check one
specific belief.

## Schedule — interview is Monday, it's Saturday midday

**Saturday afternoon/evening (~2 hrs).** Tiers 1-3, timed, out loud. That's 12
bugs at 4/6/8 minutes, so about 80 minutes of clock plus reading the answers.
Finish by re-deriving the symptom-shape table at the bottom of `ANSWERS.md`
from memory — cover it and reconstruct the rows.

**Sunday (~2.5 hrs).** Mock `set-a` in the morning, cold, 45 minutes. Review
against the rubric. Then tier 4 (the four hardest standalone bugs) in the
afternoon. Then mock `set-b` in the evening if you have the appetite — if you
only do one mock, do it Sunday morning while you're fresh, not at night.

**Monday — warm-up only.** One tier-1 file to get your hands moving. Nothing
new. Re-read the symptom-shape table once. Then stop.

If you're short on time, the highest-value 90 minutes is: `set-a` as a cold
timed mock, then tier 4. The mock is worth more than any amount of reading.

## Running a mock interview

Two sealed 4-bug sets live in `mock/`, ordered easy to hard and sized for 45
minutes. **Don't open them before you sit down for the mock** — they're the
only bugs you haven't seen, and a cold run is the entire point.

See `mock/README.md`. Short version: open a **fresh** Claude Code session in
this directory and say:

> Run a mock debugging interview using `mock/set-a`. Read
> `mock/answers/INTERVIEWER.md` and follow the protocol there exactly. I'm the
> candidate — give me one bug at a time, stay in character, and don't reveal
> anything I haven't found myself.

A fresh session matters. Any session that watched these files get written
already knows every answer and can't run the mock honestly.

`mock/answers/INTERVIEWER.md` has the protocol, a graduated hint ladder per bug
(so a friend who doesn't know Python can run it), the answer key, and a scoring
rubric across localization, hypothesis quality, communication, and fix quality.

## Clarifying questions to actually ask on Monday

The recruiter flagged that asking these is part of the evaluation. Good ones:

- What's the expected output for this input?
- Is there a failing test or repro I should start from?
- Can I add print statements and modify the code freely?
- Is there anything I should preserve — API shape, performance, a caller I
  can't see?
- Should I optimize for speed or thoroughness here?

## When you get stuck

Say this out loud, because it's a positive signal rather than a concession:

> "Here's what I've ruled out: [X, Y]. My next hypothesis is [Z], and I'd check
> it by [W]. I'd also like to timebox this and come back if it's not the fix."

Ruling things out *is* progress, and stating it is how you get credit for it.
