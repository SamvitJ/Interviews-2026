"""Reserves inventory for the checkout flow. Stock lives behind a slow store."""

import asyncio

INVENTORY = {}


async def _read_stock(sku):
    await asyncio.sleep(0.01)          # network round trip to the store
    return INVENTORY[sku]


async def _write_stock(sku, value):
    await asyncio.sleep(0.01)
    INVENTORY[sku] = value


async def reserve(sku, count):
    """Take `count` units of `sku` out of stock."""
    current = await _read_stock(sku)
    await _write_stock(sku, current - count)


async def reserve_all(sku, counts):
    """Apply several reservations for the same sku concurrently.
    Returns the remaining stock."""
    await asyncio.gather(*(reserve(sku, count) for count in counts))
    return INVENTORY[sku]


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


async def _run(start, counts):
    INVENTORY.clear()
    INVENTORY["widget"] = start
    return await reserve_all("widget", counts)


async def _main():
    return [
        _check("single reservation", await _run(100, [10]), 90),
        _check("three reservations", await _run(100, [10, 10, 10]), 70),
        _check("mixed sizes", await _run(50, [5, 20, 1]), 24),
    ]


if __name__ == "__main__":
    r = asyncio.run(_main())
    print("\n%d/%d passing" % (sum(r), len(r)))
