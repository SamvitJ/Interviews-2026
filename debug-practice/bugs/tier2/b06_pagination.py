"""Pagination helper for the search results endpoint."""

ITEMS = ["a", "b", "c", "d", "e", "f", "g"]


def paginate(items, page, per_page):
    """Return one page of `items`.

    `page` is 1-indexed, as it appears in the query string (?page=1 is
    the first page). Pages past the end come back empty.

    Raises ValueError if `page` or `per_page` is less than 1 -- an empty
    list already means "valid request, past the end", so invalid input
    must not reuse it.
    """
    if page < 1 or per_page < 1:
        raise ValueError(
            "page and per_page must be >= 1, got page=%r per_page=%r" % (page, per_page))
    start = (page - 1) * per_page
    return items[start:start + per_page]


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


def _check_raises(name, fn, exc):
    """fn is a zero-arg callable so the call happens INSIDE the try."""
    try:
        got = fn()
    except exc:
        print("PASS  " + name)
        return True
    except Exception as e:
        print("FAIL  " + name)
        print("        raised %s: %s" % (type(e).__name__, e))
        print("        want:  %s" % exc.__name__)
        return False
    print("FAIL  " + name)
    print("        returned %r, expected %s" % (got, exc.__name__))
    return False


if __name__ == "__main__":
    r = [
        _check("first page", paginate(ITEMS, 1, 3), ["a", "b", "c"]),
        _check("second page", paginate(ITEMS, 2, 3), ["d", "e", "f"]),
        _check("partial last page", paginate(ITEMS, 3, 3), ["g"]),
        _check("past the end", paginate(ITEMS, 4, 3), []),
        _check_raises("page 0 rejected",
                      lambda: paginate(ITEMS, 0, 3), ValueError),
        _check_raises("negative page rejected, not served from the end",
                      lambda: paginate(ITEMS, -1, 3), ValueError),
        _check_raises("per_page 0 rejected",
                      lambda: paginate(ITEMS, 1, 0), ValueError),
        _check_raises("negative per_page rejected",
                      lambda: paginate(ITEMS, 1, -2), ValueError),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
