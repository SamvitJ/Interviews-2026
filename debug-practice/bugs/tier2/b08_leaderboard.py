"""Weekly leaderboard. Rows arrive already parsed out of the export CSV."""

ROWS = [
    {"name": "dana",  "score": "9"},
    {"name": "arjun", "score": "10"},
    {"name": "mei",   "score": "100"},
    {"name": "sam",   "score": "85"},
    {"name": "kira",  "score": "7"},
]


def top_scorers(rows, n):
    """Names of the `n` highest scorers, highest first."""
    ranked = sorted(rows, key=lambda row: int(row["score"]), reverse=True)
    return [row["name"] for row in ranked[:n]]


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("top 1", top_scorers(ROWS, 1), ["mei"]),
        _check("top 3", top_scorers(ROWS, 3), ["mei", "sam", "arjun"]),
        _check("all", top_scorers(ROWS, 5), ["mei", "sam", "arjun", "dana", "kira"]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
