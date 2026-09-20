"""Builds per-field length validators from a schema."""



def build_validators(limits):
    """limits: field name -> maximum allowed length.

    Returns field name -> predicate that is True when a value fits.
    """
    def make(lim):
        return lambda x: len(x) <= lim

    validators = {}
    for field, limit in limits.items():
        validators[field] = make(limit)
    return validators


def _sealed(fn, value):
    """True if a caller cannot defeat the validator by supplying lim itself."""
    try:
        fn(value, lim=99)
    except TypeError:
        return True
    return False


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    v = build_validators({"username": 8, "bio": 40, "code": 3})
    r = [
        _check("short username ok", v["username"]("sam"), True),
        _check("long username rejected", v["username"]("samvitjain12"), False),
        _check("bio of 20 ok", v["bio"]("x" * 20), True),
        _check("code of 4 rejected", v["code"]("abcd"), False),
        _check("code of 3 ok", v["code"]("abc"), True),

        # each validator must enforce ITS OWN limit at the boundary --
        # this is what a late-binding bug fails and the passing tests above hide
        _check("username boundary", (v["username"]("x" * 8), v["username"]("x" * 9)),
               (True, False)),
        _check("bio boundary", (v["bio"]("x" * 40), v["bio"]("x" * 41)),
               (True, False)),
        _check("code boundary", (v["code"]("x" * 3), v["code"]("x" * 4)),
               (True, False)),

        # the limit must not be reachable from the call site
        _check("limit sealed against keyword override",
               _sealed(v["code"], "abcd"), True),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
