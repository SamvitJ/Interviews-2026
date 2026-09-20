"""Quote engine. Pricing lookups are slow, so results are memoized."""

BASE = {"widget": 100.0, "gadget": 250.0}
REGION_MULTIPLIER = {"us": 1.0, "eu": 1.2, "apac": 1.5}

_cache = {}


def price_for(sku, quantity, region):
    """Total price for `quantity` units of `sku` delivered to `region`."""
    key = (sku, quantity, region)
    if key in _cache:
        return _cache[key]
    price = BASE[sku] * quantity * REGION_MULTIPLIER[region]
    _cache[key] = price
    return price


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("widget x2 us", price_for("widget", 2, "us"), 200.0),
        _check("gadget x1 us", price_for("gadget", 1, "us"), 250.0),
        _check("widget x2 eu", price_for("widget", 2, "eu"), 240.0),
        _check("widget x2 apac", price_for("widget", 2, "apac"), 300.0),
        _check("widget x2 us again", price_for("widget", 2, "us"), 200.0),

        # gadgets across every region
        _check("gadget x1 eu", price_for("gadget", 1, "eu"), 300.0),
        _check("gadget x1 apac", price_for("gadget", 1, "apac"), 375.0),
        _check("gadget x3 us", price_for("gadget", 3, "us"), 750.0),
        _check("gadget x3 eu", price_for("gadget", 3, "eu"), 900.0),
        _check("gadget x3 apac", price_for("gadget", 3, "apac"), 1125.0),

        # same sku and quantity, every region -- prices must differ
        _check("widget x1 us", price_for("widget", 1, "us"), 100.0),
        _check("widget x1 eu", price_for("widget", 1, "eu"), 120.0),
        _check("widget x1 apac", price_for("widget", 1, "apac"), 150.0),

        # repeats must return the same answer as the first call
        _check("gadget x1 us again", price_for("gadget", 1, "us"), 250.0),
        _check("gadget x1 eu again", price_for("gadget", 1, "eu"), 300.0),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
