"""Finds which line items add up to a disputed invoice total."""


def subsets_summing_to(numbers, target):
    """Every subset of `numbers` that sums to `target`.

    Each subset keeps the original order of `numbers`. Subsets are
    returned in the order the search finds them (items taken before
    items skipped, left to right).

    subsets_summing_to([2, 3, 5], 5) -> [[2, 3], [5]]
    """
    out = []
    path = []

    def go(index, remaining):
        if remaining == 0:
            out.append(path)
            return
        if index >= len(numbers) or remaining < 0:
            return
        path.append(numbers[index])
        go(index + 1, remaining - numbers[index])
        path.pop()
        go(index + 1, remaining)

    go(0, target)
    return out


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("two ways", subsets_summing_to([2, 3, 5], 5), [[2, 3], [5]]),
        _check("whole list", subsets_summing_to([2, 3, 5], 10), [[2, 3, 5]]),
        _check("no solution", subsets_summing_to([2, 3, 5], 1), []),
        _check("repeats", subsets_summing_to([1, 1, 2], 2), [[1, 1], [2]]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
