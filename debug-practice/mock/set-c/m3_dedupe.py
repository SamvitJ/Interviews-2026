"""Drops duplicate records before they reach the warehouse loader."""


class Record:
    """One inbound row. Identity is (source, key) after normalization."""

    def __init__(self, source, key):
        self.source = source
        self.key = key

    def normalize(self):
        """Canonical form: surrounding space trimmed, key lowercased."""
        self.key = self.key.strip().lower()

    def __eq__(self, other):
        return (self.source, self.key) == (other.source, other.key)

    def __hash__(self):
        return hash((self.source, self.key))

    def __repr__(self):
        return "Record(%r, %r)" % (self.source, self.key)


def dedupe(records):
    """Records with duplicates removed, in first-seen order.

    Two records are duplicates when they have the same source and the
    same key once normalized. Returned records are normalized.
    """
    seen = set()
    out = []
    for record in records:
        if record in seen:
            continue
        seen.add(record)
        record.normalize()
        out.append(record)
    return out


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    exact = [Record("api", "beta"), Record("api", "beta")]
    distinct = [Record("api", "beta"), Record("api", "gamma"), Record("web", "beta")]
    messy = [Record("api", " Alpha "), Record("api", "alpha")]
    batch = [
        Record("api", "Delta"),
        Record("api", "delta"),
        Record("api", "delta"),
        Record("web", " Delta"),
    ]

    r = [
        _check("exact duplicates collapse", len(dedupe(exact)), 1),
        _check("distinct records all kept", len(dedupe(distinct)), 3),
        _check("case and spacing duplicates collapse", len(dedupe(messy)), 1),
        _check("mixed batch", [(x.source, x.key) for x in dedupe(batch)],
               [("api", "delta"), ("web", "delta")]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
