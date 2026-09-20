"""Collapses a sorted event stream into runs of identical values."""


def group_runs(values):
    """Split `values` into runs of consecutive equal items.

    group_runs([1, 1, 2, 2, 2, 3]) -> [[1, 1], [2, 2, 2], [3]]
    """
    runs = []
    current = []
    for value in values:
        if current and (value != current[-1]):
            runs.append(current)
            current = []
        current.append(value)
    if current:
        runs.append(current)
    return runs


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("mixed runs", group_runs([1, 1, 2, 2, 2, 3]), [[1, 1], [2, 2, 2], [3]]),
        _check("all distinct", group_runs(["a", "b", "c"]), [["a"], ["b"], ["c"]]),
        _check("single run", group_runs([7, 7, 7]), [[7, 7, 7]]),
        _check("empty", group_runs([]), []),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
