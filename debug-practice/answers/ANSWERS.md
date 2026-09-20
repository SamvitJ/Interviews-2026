# Answer key

**Don't open this until you've either fixed the bug or spent your full timebox on it.**

Format: symptom you see → root cause → minimal fix → the archetype it belongs to.

---

## Tier 1

### b01 — build_report
- **Symptom:** the first report is right; the second contains the first's contents too.
- **Cause:** `def add_line(text, lines=[])` — the default list is created once at function-definition time and shared by every call that omits the argument. `build_report` omits it on the first line of each report.
- **Fix:** `def add_line(text, lines=None):` then `if lines is None: lines = []`
- **Archetype:** mutable default argument.
- **Tell:** state leaking *between* top-level calls. When call N is fine and call N+1 is polluted, look for something that outlives the call: a default arg, a module global, a class attribute.

### b02 — group_runs
- **Symptom:** the right *number* of runs, but every run holds the last value: `[[3], [3], [3]]`.
- **Cause:** `current.clear()` empties the very list object that was just appended to `runs`. `runs` holds a reference, not a copy, so all entries alias one list.
- **Fix:** rebind instead of mutating — `current = []`. (Or append a copy: `runs.append(list(current))`.)
- **Archetype:** aliasing — mutating an object you've already handed to someone else.
- **Tell:** N results that are all *identical* and all equal to the final state. That signature means one shared object, not N objects.

### b03 — moving_average
- **Symptom:** every result is missing its final window; `window == len(values)` returns `[]`.
- **Cause:** `range(len(values) - window)` produces one fewer start index than there are windows. For 4 values and window 2 there are 3 windows but `range(2)` gives 2.
- **Fix:** `range(len(values) - window + 1)`
- **Archetype:** off-by-one on a computed loop bound.
- **Tell:** the first test's `got` is a strict prefix of `want`. A prefix/suffix truncation almost always means a bound, not a calculation.

### b04 — resolve
- **Symptom:** `{"retries": 0}` and `{"verbose": False}` are ignored; defaults win.
- **Cause:** `if value:` tests truthiness, but `0` and `False` are legitimate override values that are falsy. It also can't distinguish "absent" from "present but falsy", since `.get` returns `None` for both.
- **Fix:** `if key in overrides: out[key] = overrides[key]` (or `value = overrides.get(key, _MISSING)` and compare against a sentinel).
- **Archetype:** truthiness used where presence was meant.
- **Tell:** the failures are exactly the falsy values. Any time the failing inputs are `0`, `""`, `[]`, `False`, or `None`, suspect a truthiness test.

---

## Tier 2

### b05 — load_limits
- **Symptom:** `"1,000"` silently becomes `0` rather than `1000`.
- **Cause:** two-part. `int("1,000")` raises `ValueError` because the function never strips the thousands separator; the bare `except:` then swallows that error and substitutes a `0` that reads downstream as a real limit.
- **Fix:** normalize before parsing — `int(str(value).replace(",", "").strip())` — and let a genuinely malformed value raise rather than becoming `0`. At minimum narrow to `except ValueError` and re-raise with context.
- **Archetype:** swallowed exception hiding the real failure.
- **Tell:** a suspiciously round default value appearing where real data should be. **The move here is to delete the `except` and re-run** — the traceback hands you the bug. Do that out loud in the interview; it's exactly the instinct they're grading.

### b06 — paginate
- **Symptom:** page 1 returns the second page; the last page is unreachable.
- **Cause:** `page` is 1-indexed per the docstring, but the offset is computed as if it were 0-indexed.
- **Fix:** `start = (page - 1) * per_page`
- **Archetype:** index-base mismatch (1-indexed vs 0-indexed).
- **Tell:** results are correct in shape but shifted by exactly one unit of stride. Off-by-one-*page*, not off-by-one-element.

### b07 — drop_expired
- **Symptom:** one expired session is removed correctly, but two adjacent expired ones leave a survivor.
- **Cause:** removing from a list while iterating it. The iterator holds an index; deleting the item at index i shifts the next item into slot i, and the iterator then moves to i+1, skipping it.
- **Fix:** `sessions[:] = [s for s in sessions if s["expires"] > now]` — slice assignment keeps the caller's list object identity, which the docstring requires. (`sessions = [...]` would rebind a local and silently do nothing to the caller.)
- **Archetype:** mutation during iteration.
- **Tell:** *every other* element is mishandled. Alternating or "skipped one" patterns point at index drift.

### b08 — top_scorers
- **Symptom:** ranking is nonsense: "9" beats "100".
- **Cause:** `score` is a string from the CSV, so `sorted` compares lexicographically. `"9" > "85" > "7" > "100" > "10"`.
- **Fix:** `key=lambda row: int(row["score"])`
- **Archetype:** type confusion at a data boundary.
- **Tell:** the ordering is consistent but wrong, and it's alphabetical. Print the key values with `repr()`, not `str()` — `repr` shows quotes and would have made this instant.

---

## Tier 3

### b09 — with_overrides
- **Symptom:** `base` is modified, and the two derived configs bleed into each other.
- **Cause:** `dict.copy()` is shallow. `result["db"]` is the *same* dict object as `base["db"]`, so `result[key].update(value)` writes straight through into the shared base.
- **Fix:** copy the nested dict before merging:
  ```python
  merged = dict(result[key])
  merged.update(value)
  result[key] = merged
  ```
  (`copy.deepcopy(base)` also works and is more obviously correct, at a cost.)
- **Archetype:** shallow copy of a nested structure.
- **Tell:** an input the function promised not to touch has changed. Check object identity, not equality: `base["db"] is result["db"]` returning True is the whole diagnosis.

### b10 — first_index_at_least
- **Symptom:** five of six tests pass. Only "target above every element" is wrong — returns 4 instead of 5.
- **Cause:** `hi = len(values) - 1` makes the searchable range `[0, len-1]`, so `len(values)` — the documented "insert at the end" answer — is not a representable result.
- **Fix:** `hi = len(values)`. The rest of the loop is already correct for a half-open range.
- **Archetype:** search interval that can't represent a valid answer.
- **Tell:** a single failing case at a boundary, with the answer clamped to the maximum representable value. When only the extreme case fails, check whether your bounds can even *express* the expected output before you touch the loop body.

### b11 — build_validators
- **Symptom:** only one test fails (`bio` rejects a 20-char string). The others pass by coincidence.
- **Cause:** classic late binding. The lambda closes over the *variable* `limit`, not its value. After the loop finishes, `limit` is `3` (the last entry, `code`), so every validator enforces 3. `username`'s tests happen to agree with a limit of 3.
- **Fix:** bind at definition time — `lambda value, limit=limit: len(value) <= limit`. (Or `functools.partial`, or a factory function.)
- **Archetype:** closure over a loop variable.
- **Tell:** **the coincidental passes are the real lesson.** Three green tests here are worthless. When a bug makes functions behave identically, verify by probing the ones that "pass" — `v["username"]("abcd")` returns False, which is wrong for a limit of 8. Never trust a passing test to exonerate code; construct your own probe.

### b12 — price_for
- **Symptom:** the first region queried for a given (sku, quantity) is correct; every other region returns that first region's price.
- **Cause:** the memo key is `(sku, quantity)` but the result also depends on `region`. Different inputs collide on the same cache entry.
- **Fix:** `key = (sku, quantity, region)`
- **Archetype:** cache key omitting part of the input.
- **Tell:** wrong answers that are *right for a different input*, and order-dependence — run the `eu` case first and it passes while `us` then fails. If reordering tests changes which ones fail, you have shared state.

---

## Tier 4

### b13 — Scheduler.tick
- **Symptom:** catch-up is broken (only one missed run fires), and the schedule drifts off its grid — `next_run` lands at 00:03:30 instead of 00:03:00.
- **Cause:** `self.next_run = now + self.interval` advances from the *observation time* rather than from the scheduled time. Every tick bakes the caller's lateness permanently into the cadence, and the loop exits after one iteration because `now + interval` is always `> now`.
- **Fix:** `self.next_run = self.next_run + self.interval`
- **Archetype:** accumulating drift from measuring relative to "now" instead of the fixed grid.
- **Tell:** two symptoms from one cause — this is why you fix the cause, not the symptoms. Someone patching "only one run fires" separately from "the time is 30s off" writes two wrong fixes. **When several failures share a single line, say so out loud before fixing.** Also: the off-by-30-seconds exactly equals the caller's lateness, which names the bug for you.

### b14 — LRUCache
- **Symptom:** `get("a")` returns the right value, but `a` is evicted anyway when `c` is inserted.
- **Cause:** `get` reads without recording the access, so the recency order only ever reflects writes. `put` correctly refreshes (delete-then-reinsert moves the key to the end), which is why the "re-put refreshes" test passes and masks the asymmetry.
- **Fix:** `self.data.move_to_end(key)` before returning in `get`.
- **Archetype:** two code paths that must maintain the same invariant, where only one does.
- **Tell:** the passing test is the clue. `put` refreshes and `get` doesn't — when a class has several methods touching one invariant, **diff them against each other**. The one that's missing a step usually stands out immediately once you line them up.

### b15 — reserve / reserve_all
- **Symptom:** one reservation works. Three concurrent reservations of 10 remove only 10 total (100 → 90 instead of 70).
- **Cause:** read-modify-write straddling an `await`. Each `reserve` reads stock (100), suspends at the `await`, and while suspended the other two coroutines also read 100. All three then write `100 - count`, and the last write wins. This is a real race even though asyncio is single-threaded — `await` is a yield point, and any invariant you were holding across it is not protected.
- **Fix:** serialize the critical section with an `asyncio.Lock`:
  ```python
  _lock = asyncio.Lock()

  async def reserve(sku, count):
      async with _lock:
          current = await _read_stock(sku)
          await _write_stock(sku, current - count)
  ```
  The better production fix pushes atomicity into the store (an atomic decrement), so no caller can get this wrong.
- **Archetype:** check-then-act race across an await point.
- **Tell:** the answer is wrong by exactly the amount of the lost updates, and it's correct with concurrency of 1. **"Correct when serial, wrong when concurrent" is the signature of a race.** Scan for shared state read on one side of an `await` and written on the other.

### b16 — subsets_summing_to
- **Symptom:** the correct *number* of solutions, but every one is `[]`.
- **Cause:** `out.append(path)` appends a reference to the single working list. By the time the search unwinds, `path` has been popped back to empty, and every entry in `out` points at that same now-empty list.
- **Fix:** `out.append(list(path))` — snapshot the path at the moment you record it.
- **Archetype:** aliasing in backtracking (same family as b02, worth recognizing as one class).
- **Tell:** identical to b02's — N identical results matching the data structure's *final* state. The count being right tells you the search logic is fine and only the recording is broken, which halves the code you need to read.

---

## The archetypes, consolidated

If you only retain one thing, retain the mapping from *symptom shape* to *bug family*:

| What you see | Look for |
|---|---|
| Result is a prefix/suffix of expected | Loop bound, off-by-one |
| N identical results equal to final state | Aliasing — appended a reference, not a copy |
| Correct call, then a polluted second call | State outliving the call: default arg, global, class attr |
| Failing inputs are exactly `0`/`""`/`False`/`[]` | Truthiness where presence/identity was meant |
| Every other element skipped | Mutation during iteration |
| Ordering wrong but alphabetical | Type confusion, string vs number |
| Suspiciously round default in real data | Swallowed exception |
| Right answer for a *different* input | Cache key missing a parameter |
| Reordering tests changes what fails | Shared mutable state |
| Correct serial, wrong concurrent | Race across an await/yield point |
| Input you promised not to touch changed | Shallow copy |
| Only the extreme case fails | Bounds can't represent the answer |
| Several failures, one line | Fix the cause, not each symptom |
| One method right, its sibling wrong | Diff the two paths |
