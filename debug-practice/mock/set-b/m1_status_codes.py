"""Checks a response's status line against the codes we expect."""

EXPECTED = {"ok": 200, "created": 201, "teapot": 418, "gateway": 502}


def status_matches(code, name):
    """True when `code` is the status registered under `name`.

    `code` arrives already parsed out of the HTTP response line.
    """
    return code is EXPECTED[name]


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("200 is ok", status_matches(int("200"), "ok"), True),
        _check("404 is not ok", status_matches(int("404"), "ok"), False),
        _check("418 is teapot", status_matches(int("418"), "teapot"), True),
        _check("502 is gateway", status_matches(int("502"), "gateway"), True),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
