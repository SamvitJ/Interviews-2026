"""Finds where a new reading belongs in a sorted time series."""


def first_index_at_least(values, target):
    """Index of the first element of sorted `values` that is >= `target`.

    If every element is smaller than `target`, return len(values) --
    i.e. the position a new element would be inserted at.
    """
    lo, hi = 0, len(values)
    while lo < hi:
        mid = (lo + hi) // 2
        if values[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    v = [10, 20, 30, 40, 50]
    r = [
        _check("below all", first_index_at_least(v, 5), 0),
        _check("exact hit", first_index_at_least(v, 30), 2),
        _check("between", first_index_at_least(v, 35), 3),
        _check("last element", first_index_at_least(v, 50), 4),
        _check("above all", first_index_at_least(v, 99), 5),
        _check("empty list", first_index_at_least([], 1), 0),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
