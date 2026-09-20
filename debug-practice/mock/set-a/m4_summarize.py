"""Summary line for the transactions panel."""


def summarize(records, threshold=100):
    """Return (count, total) across records whose amount exceeds `threshold`."""
    big = [r for r in records if r["amount"] > threshold]
    count = sum(1 for _ in big)
    total = sum(r["amount"] for r in big)
    return count, total


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


def _rows(*amounts):
    return [{"id": i, "amount": a} for i, a in enumerate(amounts)]


if __name__ == "__main__":
    r = [
        _check("nothing qualifies", summarize(_rows(5, 20, 99)), (0, 0)),
        _check("two qualify", summarize(_rows(5, 200, 300)), (2, 500)),
        _check("all qualify", summarize(_rows(150, 150)), (2, 300)),
        _check("custom threshold", summarize(_rows(5, 20, 99), threshold=10),
               (2, 119)),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
