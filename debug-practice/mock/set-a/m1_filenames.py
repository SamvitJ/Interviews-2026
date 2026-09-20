"""Normalizes uploaded attachment names before they hit the store."""


def strip_extension(filename):
    """Remove a trailing '.txt' extension, if present.

    'report.txt' -> 'report'
    'report'     -> 'report'
    """
    return filename.strip(".txt")


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("simple", strip_extension("notes.txt"), "notes"),
        _check("word ending in t", strip_extension("report.txt"), "report"),
        _check("word ending in x", strip_extension("matrix.txt"), "matrix"),
        _check("no extension", strip_extension("README"), "README"),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
