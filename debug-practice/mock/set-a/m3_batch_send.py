"""Ships a batch of records to a downstream sink, retrying on blips."""


class TransientError(Exception):
    pass


class Sink:
    """Test double. Fails the first time it is asked to send `fail_on`."""

    def __init__(self, fail_on=None):
        self.received = []
        self.fail_on = fail_on
        self._already_failed = False

    def send(self, record):
        if record == self.fail_on and not self._already_failed:
            self._already_failed = True
            raise TransientError("downstream hiccup on %r" % record)
        self.received.append(record)


def process_batch(records, sink, retries=2):
    """Send every record to `sink`.

    A TransientError means the downstream had a blip; retry so the batch
    still gets through. Every record must land in the sink exactly once.
    """
    for attempt in range(retries + 1):
        try:
            for record in records:
                sink.send(record)
            return
        except TransientError:
            continue
    raise TransientError("batch failed after %d attempts" % (retries + 1))


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    clean = Sink()
    process_batch(["a", "b", "c"], clean)

    flaky = Sink(fail_on="c")
    process_batch(["a", "b", "c", "d"], flaky)

    early = Sink(fail_on="a")
    process_batch(["a", "b"], early)

    r = [
        _check("clean run", clean.received, ["a", "b", "c"]),
        _check("failure mid-batch", flaky.received, ["a", "b", "c", "d"]),
        _check("failure on first record", early.received, ["a", "b"]),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
