"""Layers environment overrides on top of a shared base config."""

import copy

def with_overrides(base, overrides):
    """Return a NEW config with `overrides` layered on `base`.

    Nested dicts are merged key by key. `base` is shared across every
    environment, so it must come back unmodified.
    """
    result = base.copy()
    for key, value in overrides.items():
        current = result.get(key)
        if isinstance(value, dict) and isinstance(current, dict):
            result[key] = with_overrides(current, value)   # ← was current.update(value)
        else:
            result[key] = value
    return result


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    base = {"db": {"host": "localhost", "port": 5432}, "debug": False}

    staging = with_overrides(base, {"db": {"port": 6000}, "debug": True})
    prod = with_overrides(base, {"db": {"host": "prod.internal"}})

    r = [
        _check("staging merged", staging,
               {"db": {"host": "localhost", "port": 6000}, "debug": True}),
        _check("prod merged", prod,
               {"db": {"host": "prod.internal", "port": 5432}, "debug": False}),
        _check("base untouched", base,
               {"db": {"host": "localhost", "port": 5432}, "debug": False}),
    ]

    # --- nested overrides -------------------------------------------------
    # The docstring says nested dicts are merged key by key. These pin down
    # at what depth that actually holds.

    # Given: a config nested three levels deep
    nested = {
        "db": {
            "host": "localhost",
            "opts": {"ssl": True, "pool": 5,
                     "retry": {"attempts": 3, "backoff": "exp"}},
        },
        "debug": False,
    }
    nested_before = copy.deepcopy(nested)

    # When: we override at each depth, and in ways that should not merge
    at_depth_1 = with_overrides(nested, {"db": {"host": "prod"}})
    at_depth_2 = with_overrides(nested, {"db": {"opts": {"pool": 20}}})
    at_depth_3 = with_overrides(nested, {"db": {"opts": {"retry": {"attempts": 5}}}})
    shape_change = with_overrides(nested, {"db": "postgres://..."})
    added_key = with_overrides(nested, {"cache": {"ttl": 60}})

    # Then:
    r += [
        # controls -- true whether or not the merge recurses
        _check("[control] depth-1 override keeps its siblings",
               at_depth_1["db"]["opts"]["ssl"], True),
        _check("[control] shape change still replaces",
               shape_change["db"], "postgres://..."),
        _check("[control] new key still inserted",
               added_key["cache"], {"ttl": 60}),
        _check("[control] nested base untouched",
               nested, nested_before),

        # boundary -- the deepest level a one-level merge gets right
        _check("depth-2 override keeps depth-1 siblings",
               at_depth_2["db"]["host"], "localhost"),

        # discriminating -- these require the merge to recurse
        _check("depth-2 override keeps its siblings",
               at_depth_2["db"]["opts"],
               {"ssl": True, "pool": 20,
                "retry": {"attempts": 3, "backoff": "exp"}}),
        _check("depth-3 override keeps its siblings",
               at_depth_3["db"]["opts"]["retry"],
               {"attempts": 5, "backoff": "exp"}),
    ]

    print("\n%d/%d passing" % (sum(r), len(r)))
