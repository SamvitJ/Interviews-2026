"""Background job that drops expired sessions from the in-memory store."""


def drop_expired(sessions, now):
    """Remove every session whose `expires` is at or before `now`.

    Mutates and returns the same list object (callers hold a reference).
    """
    sessions[:] = [s for s in sessions if s["expires"] > now]
    return sessions


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


def _sessions(*pairs):
    return [{"id": i, "expires": e} for i, e in pairs]


if __name__ == "__main__":
    r = [
        _check("one expired",
               drop_expired(_sessions(("a", 10), ("b", 100)), 50),
               _sessions(("b", 100))),
        _check("two adjacent expired",
               drop_expired(_sessions(("a", 10), ("b", 20), ("c", 100)), 50),
               _sessions(("c", 100))),
        _check("all expired",
               drop_expired(_sessions(("a", 1), ("b", 2), ("c", 3)), 50),
               []),
        _check("none expired",
               drop_expired(_sessions(("a", 90), ("b", 99)), 50),
               _sessions(("a", 90), ("b", 99))),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
