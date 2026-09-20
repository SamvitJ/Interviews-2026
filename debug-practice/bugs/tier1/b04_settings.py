"""Merges user-supplied overrides onto the built-in defaults."""

DEFAULTS = {"retries": 3, "timeout": 30, "verbose": True}


def resolve(overrides):
    """Return the effective config. Any key present in `overrides` wins,
    even when its value is falsy. Keys absent from `overrides` fall back
    to DEFAULTS."""
    out = {}
    for key, default in DEFAULTS.items():
        if key in overrides:
            out[key] = overrides[key]
        else:
            out[key] = default
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
        _check("empty overrides", resolve({}),
               {"retries": 3, "timeout": 30, "verbose": True}),
        _check("normal override", resolve({"timeout": 5}),
               {"retries": 3, "timeout": 5, "verbose": True}),
        _check("zero retries", resolve({"retries": 0}),
               {"retries": 0, "timeout": 30, "verbose": True}),
        _check("verbose off", resolve({"verbose": False}),
               {"retries": 3, "timeout": 30, "verbose": False}),
        _check("explicit None wins over the default", resolve({"timeout": None}),
               {"retries": 3, "timeout": None, "verbose": True}),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
