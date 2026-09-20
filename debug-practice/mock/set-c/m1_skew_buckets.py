"""Buckets clock-skew readings for the drift histogram."""

WIDTH_MS = 10


def bucket_index(skew_ms, width=WIDTH_MS):
    """Index of the fixed-width bucket containing `skew_ms`.

    Buckets tile the number line: bucket 0 is [0, width), bucket 1 is
    [width, 2*width), and they continue into the negatives, so bucket -1
    is [-width, 0). A reading always lands in the bucket that contains it.

    Skew is signed: a positive reading means the node's clock is ahead,
    a negative one means it is behind.
    """
    return skew_ms // width


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("clock ahead, first bucket", bucket_index(5), 0),
        _check("clock ahead, third bucket", bucket_index(25), 2),
        _check("clock behind, just under zero", bucket_index(-5), -1),
        _check("clock behind, well under zero", bucket_index(-25), -3),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
