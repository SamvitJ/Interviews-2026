"""Rolling averages for a metrics dashboard."""


def moving_average(values, window):
    """Average of every consecutive `window`-sized slice of `values`.

    moving_average([1, 2, 3, 4], 2) -> [1.5, 2.5, 3.5]
    If `window` is larger than `values`, returns [].
    """
    out = []
    for i in range(len(values) - window + 1):
        chunk = values[i:i + window]
        out.append(sum(chunk) / window)
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
        _check("pairs", moving_average([1, 2, 3, 4], 2), [1.5, 2.5, 3.5]),
        _check("triples", moving_average([2, 4, 6, 8, 10], 3), [4.0, 6.0, 8.0]),
        _check("window == len", moving_average([5, 7], 2), [6.0]),
        _check("window > len", moving_average([5], 3), []),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
