# Interviewer guide

**Candidate: stop reading. This has every answer in it.**

You are running a 45-minute debugging interview. Four bugs, increasing
difficulty, one at a time. This mirrors Factory's format.

Three sets are available: `set-a`, `set-b`, `set-c`. Run one per session.

---

## Protocol

**Setup (2 min).** Tell the candidate: four bugs, increasing difficulty, 45
minutes total, roughly 10 minutes each. They may run the file, add prints, and
change anything. Encourage clarifying questions and thinking out loud.

**Per bug:** reveal only the next file. Never mention the bug's location, the
archetype, or how many tests should pass. Start a per-bug timer.

**Answer clarifying questions in character** — you're the engineer who owns
this code. Good answers to expect:
- *"What's the expected behavior?"* → point at the docstring, read it aloud.
- *"Can I add prints / change the code?"* → yes, freely.
- *"Is there a test?"* → yes, run the file.
- *"Is anything else calling this?"* → assume only what's in the file, unless
  the docstring says otherwise (m3 in set A and b07 do constrain this).

**One question at a time.** Ask it, then stop and wait. Never send a numbered
list of questions, and don't append a follow-up to a question you haven't had
answered yet — a real interviewer speaks one thought and goes quiet. A
candidate reading the bug in a separate pad re-enters this conversation after a
context switch, so anything bundled below your actual question gets missed.
Bundled questions also corrupt the scoring: an unanswered sub-question looks
like evasion when it was never seen. If you want two things, ask for the first,
wait, then ask for the second.

**When they go quiet for more than ~20 seconds,** prompt once: *"What are you
thinking?"* or *"What's your current hypothesis?"* Note that you had to.

**Hints.** Use the ladder below. Each rung costs them on the rubric, but a
stuck candidate learns nothing — give a rung roughly every 2 minutes of no
progress. Never skip to the bottom rung.

**At 10 minutes on a bug, move on** even if unsolved. Say: *"Let's come back to
this if there's time."* Running out of time on one bug is itself a realistic
thing to handle well.

**Watch for the two big anti-patterns** and note them:
1. Editing code before running it or forming a hypothesis (shotgun debugging).
2. Special-casing the failing input rather than fixing the cause.

---

## Set A

### m1 — strip_extension *(easy, target 4 min)*
- **Bug:** `str.strip(".txt")` treats its argument as a **set of characters** to
  remove from both ends, not as a suffix. `"report.txt"` loses the trailing `t`
  of `report` too, giving `"repor"`.
- **Fix:** `filename.removesuffix(".txt")` (3.9+). Manual equivalent:
  `filename[:-4] if filename.endswith(".txt") else filename`.
- **Note:** `"notes.txt"` passes by luck — `s` isn't in the strip set. The
  passing test is a coincidence, and a candidate who notices that unprompted is
  doing well.
- **Hints:**
  1. "Look at the two that fail versus the one that passes. What's different
     about the words themselves?"
  2. "What exactly does the argument to `.strip()` mean?"
  3. "`.strip()` takes a set of characters, not a suffix."

### m2 — strip_tags *(medium, target 6 min)*
- **Bug:** `<.*>` is greedy — `.*` matches as much as possible, so it spans from
  the first `<` to the *last* `>`, swallowing the text between tags.
- **Fix:** `<[^>]*>` (preferred — can't cross a `>`), or the lazy `<.*?>`.
- **Hints:**
  1. "The whole string disappeared, not just the tags. What did the pattern
     actually match?"
  2. "Try `re.findall(r'<.*>', '<p>a</p><p>b</p>')` and look at what comes back."
  3. "`.*` is greedy."

### m3 — process_batch *(hard, target 10 min)*
- **Bug:** the retry re-sends the **whole batch**, so records that already
  landed before the failure get sent twice. `['a','b','a','b','c','d']`. The
  docstring's "exactly once" is the contract being violated.
- **Fix:** retry at record granularity rather than batch granularity:
  ```python
  for record in records:
      for attempt in range(retries + 1):
          try:
              sink.send(record)
              break
          except TransientError:
              if attempt == retries:
                  raise
  ```
- **Note:** this is the most realistic bug in the set — at-least-once delivery
  masquerading as exactly-once. A strong candidate names that tradeoff.
- **Hints:**
  1. "Read the `got` list carefully. Is anything missing, or is something
     there twice?"
  2. "Where does control go when `sink.send` raises on the third record?"
  3. "The retry restarts the loop from the beginning of the batch."

### m4 — summarize *(hardest, target 10 min)*
- **Bug:** `big` is a **generator**, not a list. `sum(1 for _ in big)` consumes
  it; the second `sum` sees an exhausted generator and returns 0. The count is
  right, the total is always 0.
- **Fix:** `big = [r for r in records if ...]` — square brackets, one character.
- **Note:** hardest because the code looks completely ordinary and the fix is
  invisible in a diff unless you know to look. The "nothing qualifies" test
  passes because `(0, 0)` is right by accident.
- **Hints:**
  1. "Count is right, total is zero. What's different between how the two are
     computed?"
  2. "Add `print(list(big))` right after `big` is created, then run it. Now move
     that same print to after the `count` line."
  3. "`big` is a generator expression, and it's being iterated twice."

---

## Set B

### m1 — status_matches *(easy, target 4 min)*
- **Bug:** `is` compares **object identity**, not value. CPython caches small
  integers (-5 to 256), so `int("200") is 200` happens to be True, while
  `int("418") is 418` is False — different objects with the same value.
- **Fix:** `code == EXPECTED[name]`.
- **Note:** the two passing tests are the whole lesson. 200 and 404 are both
  inside the interning range, so the broken comparison looks correct.
- **Hints:**
  1. "200 and 404 work, 418 and 502 don't. What's special about the numbers
     that work?"
  2. "Try `int('418') is 418` and `int('200') is 200` in isolation."
  3. "`is` is identity, not equality."

### m2 — days_until *(medium, target 6 min)*
- **Bug:** `timedelta.days` **truncates toward zero**. 23 hours is 0 days, 25
  hours is 1 day, and -1 hour is -1. The docstring asks for a ceiling.
- **Fix:** `math.ceil((deadline - now).total_seconds() / 86400)`.
- **Hints:**
  1. "Every wrong answer is one less than expected. What's dropping the
     remainder?"
  2. "Print the raw timedelta for the 23-hour case, then print its `.days`."
  3. "`.days` is the whole-days component, and it truncates."

### m3 — Job.tags *(hard, target 8 min)*
- **Bug:** `tags = []` is a **class attribute**, shared by every instance.
  `add_tag` calls `self.tags.append(...)`, mutating the shared list.
  `replace_tags` does `self.tags = list(tags)`, which *creates an instance
  attribute* and so appears to work — which is why one test passes.
- **Fix:** initialize per instance — delete the class attribute and add
  `self.tags = []` in `__init__`.
- **Note:** same "two paths, one right" shape as the LRU cache in b14. The
  passing `replace_tags` test is what makes this hard: it looks like tags work.
- **Hints:**
  1. "`replace_tags` works and `add_tag` doesn't. What do those two lines do
     differently?"
  2. "One assigns to `self.tags`; the other mutates it in place. Where does the
     list being mutated actually live?"
  3. "`tags = []` sits at class scope, so all instances share one list."

### m4 — Stats.record *(hardest, target 10 min)*
- **Bug:** read-modify-write race. `record` reads `counts`, calls `_audit`
  (which sleeps, releasing the GIL), then writes back a value computed *before*
  the yield. Four threads read the same number and all write the same result.
  The GIL does **not** make `current = ...; ...; counts[key] = current + 1`
  atomic.
- **Fix:** guard the critical section with a `threading.Lock` held across the
  whole read-modify-write.
- **Note:** the hidden yield point inside `_audit` is what makes this hard —
  `record` looks like straight-line code. The audit-trail test passing (all 100
  calls arrived) proves every call ran, isolating the bug to the counter.
- **Hints:**
  1. "Serial counting works, threaded doesn't, and the audit trail shows all
     100 calls arrived. So what's getting lost?"
  2. "Walk through `record` for two threads running at once. Where can one be
     interrupted?"
  3. "`_audit` sleeps, which lets another thread run between the read of
     `counts` and the write."

---

## Set C

### m1 — bucket_index *(easy, target 4 min)*
- **Bug:** `int()` **truncates toward zero**, it does not floor. `int(-5 / 10)`
  is `int(-0.5)` which is `0`, but `-5` belongs in bucket `-1`. Positive
  readings are unaffected because truncation and flooring agree above zero.
- **Fix:** `skew_ms // width`. Python's `//` floors, which is exactly the
  tiling the docstring describes.
- **Note:** the two passing tests are both positive, so they can't distinguish
  truncation from flooring — the bug is invisible until skew goes negative, and
  in production most nodes drift one direction. A candidate who notices that
  every passing case is positive, *before* theorizing, is doing well. Watch for
  the special-case fix (`if skew_ms < 0: ... - 1`), which is a 0 on fix quality.
- **Related:** set B m2 is also a rounding bug, but the other direction — there
  the candidate needs a ceiling and `.days` floors. Here they need a floor and
  `int()` truncates. Worth pairing in a debrief.
- **Hints:**
  1. "Which two pass and which two fail? What do the passing inputs have in
     common?"
  2. "Print `skew_ms / width` before the `int()` for the -5 case, and say out
     loud which bucket -0.5 should land in."
  3. "`int()` truncates toward zero. Flooring and truncating disagree below
     zero."

### m2 — rank *(medium, target 6 min)*
- **Bug:** `reverse=True` reverses the **entire tuple key**, not just the first
  element. Scores come out correctly descending, but the title tiebreak is
  reversed too — Z to A instead of A to Z.
- **Fix:** `key=lambda r: (-r["score"], r["title"])` with no `reverse`.
- **Note:** negating works only because the score is numeric. Ask what they'd do
  if the primary key were a string — the answer is two stable sorts, least
  significant first: sort by title, then sort by score with `reverse=True`.
  Python's sort is stable, which is what makes that work. A candidate who
  reaches for that unprompted is strong.
- **Hints:**
  1. "Which two tests fail? What do those inputs have that the passing ones
     don't?"
  2. "The scores come out in the right order. Look only at the titles within a
     single score."
  3. "`reverse=True` applies to the whole key, not just the first element."

### m3 — dedupe *(hard, target 8 min)*
- **Bug:** the record is added to `seen`, then mutated by `normalize()`. A set
  stores each entry under the hash it had **at insertion time**. Changing `key`
  changes the hash, so the stored record now sits in the wrong bucket and can
  never be found again — including by a later record that should match it.
- **Fix:** move `record.normalize()` above the `if record in seen` check. Deeper
  fix: don't put mutable objects in sets — key on an immutable tuple, or make
  `Record` frozen.
- **Note:** the `mixed batch` failure prints two identical-looking
  `('api', 'delta')` entries — a dedupe function returning visible duplicates.
  Strong candidates seize on that immediately. The exact-duplicate test passes
  because `"beta"` normalizes to itself, so its hash never changes. Same "two
  paths, one right" shape as set B m3.
- **Hints:**
  1. "Exact duplicates collapse, but the ones needing normalization don't.
     What's different about the records in the failing cases?"
  2. "Print `record.key` immediately before and immediately after
     `seen.add(record)`, and print `len(seen)` at the end."
  3. "A set records an object's hash when you insert it. `normalize()` changes
     the key *after* insertion."

### m4 — run_steps *(hardest, target 10 min)*
- **Bug:** `return done` sits inside the `finally` block. A `return` in a
  `finally` **discards any exception still propagating**. `StepError` is raised,
  the `finally` runs, and the return swallows it — the caller receives a partial
  list that is indistinguishable from a short but successful run.
- **Fix:** move the `return` outside the `try`/`finally`. The `finally` keeps
  only `journal.append("flushed")`.
- **Note:** hardest because the code reads as *careful* — someone deliberately
  added cleanup. All three passing tests confirm the cleanup works, which is
  exactly what hides the bug: the defensive machinery functions correctly, it
  just eats the error. Real-world shape: a migration that fails silently and
  reports partial success to the runbook.
- **The tradeoff to name:** even once it raises, the caller can't see which
  steps completed. Any partial-success contract has to carry the failure *and*
  the progress — which is an argument about the return type, not the
  `try` block.
- **Hints:**
  1. "Three tests pass and they all confirm the cleanup works. What's the one
     thing the failing test checks that the others don't?"
  2. "Add a print inside `_boom` to confirm it raises. It does. So where does
     the exception go?"
  3. "A `return` inside `finally` discards an exception that is still
     propagating."

## Scoring rubric

Score each bug 0-3 on four axes, then read the totals as a whole.

**1. Localization** — how fast they got to the right few lines.
- 3: ran it first, used the failure output to narrow, found the region in under
  half the timebox.
- 2: got there, but by reading rather than by evidence.
- 1: needed a hint to reach the right area.
- 0: never localized it.

**2. Hypothesis quality** — did they predict before they tested?
- 3: stated hypotheses in testable form ("if X, then printing Y shows Z") and
  updated cleanly when wrong.
- 2: formed hypotheses but tested them loosely.
- 1: mostly guessed, with occasional reasoning.
- 0: shotgun — changed code to see what happened.

**3. Communication** — could you follow their thinking without asking?
- 3: continuous, and you always knew what they were testing and why.
- 2: mostly narrated, with a few silent stretches.
- 1: you prompted more than twice.
- 0: silent.

**4. Fix quality** — minimal, correct, cause not symptom.
- 3: smallest correct change, re-ran, checked nothing else broke, and named the
  tradeoff where one existed (m3 in set A, m4 in set B).
- 2: correct and minimal, didn't re-verify.
- 1: works but over-broad — refactored, or patched the symptom.
- 0: special-cased the test input, or the fix is wrong.

### Reading the result

- **Communication is the axis that generalizes.** A candidate scoring 3s on
  localization and 1s on communication fails interviews they should pass. It's
  also the fastest thing to fix — it's a habit, not a skill.
- **Check whether axis 2 dropped as difficulty rose.** Almost everyone reverts
  to guessing under pressure on bug 4. Noticing your own reversion is the point
  of the exercise.
- **Any 0 on fix quality is the most serious signal here**, even alongside fast
  localization. Special-casing the input is the one thing that reliably fails a
  debugging round: it says you'll ship a patch you don't understand.
