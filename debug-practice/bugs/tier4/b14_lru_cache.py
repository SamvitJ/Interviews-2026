"""Bounded cache in front of the embedding service."""

from collections import OrderedDict


class LRUCache:
    """Evicts the least *recently used* entry once capacity is exceeded.

    Both get() and put() count as using an entry.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.data = OrderedDict()

    def get(self, key):
        if key not in self.data:
            return None
        return self.data[key]

    def put(self, key, value):
        if key in self.data:
            del self.data[key]
        self.data[key] = value
        if len(self.data) > self.capacity:
            self.data.popitem(last=False)

    def keys(self):
        """Keys from least to most recently used."""
        return list(self.data)


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    c = LRUCache(2)
    c.put("a", 1)
    c.put("b", 2)
    got_a = c.get("a")
    c.put("c", 3)

    d = LRUCache(2)
    d.put("a", 1)
    d.put("b", 2)
    d.put("a", 10)
    d.put("c", 3)

    r = [
        _check("get returns the value", got_a, 1),
        _check("get protects 'a' from eviction", c.keys(), ["a", "c"]),
        _check("evicted key is gone", c.get("b"), None),
        _check("re-put refreshes 'a'", d.keys(), ["a", "c"]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
