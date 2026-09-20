# Hint ladders

Read these through `./hint.sh`, one rung at a time. Don't open this file.

Rung 1 points at evidence you already have. Rung 2 names an experiment to run.
Rung 3 names the bug. Take rung 3 only when the timebox is up.

### b01
1. The first report is right and the second is polluted. What can survive between two separate top-level calls?
2. Where does `lines` come from on the first `add_line` of each report?
3. A default argument is created once, when the function is defined, and shared by every call that omits it.

### b02
1. The number of runs is right but the contents aren't. What is every run equal to?
2. After `runs.append(current)` runs, how many distinct list objects exist?
3. `.clear()` empties the very object you just appended to `runs`.

### b03
1. Compare `got` to `want` on the first test. Is a value wrong, or is one just missing?
2. How many 2-element windows does a 4-element list have? How many does the loop produce?
3. The loop bound is one too small.

### b04
1. Which two inputs fail? What do `0` and `False` have in common?
2. `overrides.get(key)` returns `None` for a missing key. What does it return for a key explicitly set to `False`?
3. `if value:` tests truthiness where the docstring asks whether the key was provided.

### b05
1. Which input fails? What would `int()` do with that exact string?
2. Delete the `try`/`except` entirely and run it again.
3. The bare `except` is swallowing a real error and substituting a plausible-looking `0`.

### b06
1. Page 1 returns what page 2 should. By exactly how much is it shifted?
2. What is `start` when `page` is 1?
3. The docstring says `page` is 1-indexed; the offset math assumes 0-indexed.

### b07
1. One expired session is handled fine; two adjacent ones aren't. What happens to the positions of later items when you remove one?
2. Print the list and the current item at the top of each iteration.
3. You're removing from the list you're iterating over.

### b08
1. Print each row's sort key with `repr()`, not `str()`.
2. Is `"9"` greater than `"100"`?
3. The scores are strings, so the comparison is lexicographic.

### b09
1. Evaluate `base["db"] is staging["db"]`.
2. What does `dict.copy()` do with a value that is itself a dict?
3. The copy is shallow, so `result[key].update(...)` writes straight into `base`.

### b10
1. Only the "above all" case fails. What should it return, and can this function ever return that?
2. What is the largest value `lo` can possibly hold when the loop exits?
3. `hi` starts at `len - 1`, so `len` is not a reachable answer.

### b11
1. Four tests pass. Don't trust them — check `v["username"]("abcd")` by hand. Is that answer right?
2. Print the limit each validator actually enforces.
3. The lambda closes over the variable `limit`, not over its value at the time the lambda was created.

### b12
1. Move the `eu` test above the `us` test and re-run. Does the failure move with it?
2. What does the computed price depend on that the cache key doesn't include?
3. The memo key omits `region`.

### b13
1. `next_run` should be 00:03:00 but is 00:03:30. Where could 30 seconds come from?
2. What was `now` in that call, and what is `next_run` being computed from?
3. The next run is measured from the observation time instead of from the previous scheduled time.

### b14
1. `put` maintains recency correctly and `get` doesn't. Put the two methods side by side.
2. What does the order of an `OrderedDict` mean here, and which operations change it?
3. `get` never moves the key it just read to the end.

### b15
1. One reservation is correct; three aren't. By how much is the final answer off, and what does that number correspond to?
2. Trace two concurrent calls to `reserve` side by side. What does each one read before either writes?
3. The read and the write straddle an `await`, so both coroutines read the same starting stock.

### b16
1. The number of solutions is right; the contents aren't. What is every solution equal to?
2. What is `path` by the time the function returns?
3. You appended a reference to the live `path` list rather than a snapshot of it.
