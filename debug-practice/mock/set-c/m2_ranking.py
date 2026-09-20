"""Orders search results for the results page."""


def rank(results):
    """Highest score first. Ties broken by title, A to Z.

    Each result is a dict with "title" and "score".
    """
    return sorted(results, key=lambda r: (-r["score"], r["title"]))


def _titles(results):
    return [r["title"] for r in results]


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    distinct = [
        {"title": "cherry", "score": 3},
        {"title": "apple", "score": 9},
        {"title": "banana", "score": 5},
    ]
    tied = [
        {"title": "zebra", "score": 4},
        {"title": "apple", "score": 4},
        {"title": "mango", "score": 4},
    ]
    mixed = [
        {"title": "widget", "score": 7},
        {"title": "anvil", "score": 7},
        {"title": "rope", "score": 2},
    ]

    r = [
        _check("distinct scores", _titles(rank(distinct)), ["apple", "banana", "cherry"]),
        _check("single result", _titles(rank([{"title": "solo", "score": 1}])), ["solo"]),
        _check("all tied, titles A-Z", _titles(rank(tied)), ["apple", "mango", "zebra"]),
        _check("tie at the top", _titles(rank(mixed)), ["anvil", "widget", "rope"]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
