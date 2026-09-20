"""Reads per-tenant rate limits out of the operator-edited config file.

Operators type these by hand, so values show up as '1000', ' 1000 ',
or '1,000'. All three mean the same number.
"""


def load_limits(raw):
    """Map tenant name -> integer limit."""
    out = {}
    for name, value in raw.items():
        out[name] = int(value.replace(",", ""))
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
        _check("plain", load_limits({"acme": "10"}), {"acme": 10}),
        _check("padded", load_limits({"acme": "  250 "}), {"acme": 250}),
        _check("grouped", load_limits({"acme": "1,000"}), {"acme": 1000}),
        _check("mixed", load_limits({"a": "5", "b": "1,250", "c": " 42"}),
               {"a": 5, "b": 1250, "c": 42}),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
