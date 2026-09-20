"""Fixed-interval scheduler for the metrics rollup job."""

from datetime import datetime, timedelta


class Scheduler:
    def __init__(self, first_run, interval):
        self.next_run = first_run
        self.interval = interval

    def tick(self, now):
        """Return every run time that is due at or before `now`, oldest
        first, and advance the schedule to the first run after `now`.

        The cadence is fixed: runs land on first_run, first_run +
        interval, first_run + 2*interval, ... regardless of when tick()
        happens to be called.
        """
        fired = []
        while self.next_run <= now:
            fired.append(self.next_run)
            self.next_run = now + self.interval
        return fired


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    t0 = datetime(2026, 1, 1, 0, 0, 0)
    minute = timedelta(minutes=1)

    s = Scheduler(t0, minute)
    first = s.tick(t0 + timedelta(seconds=150))
    after_first = s.next_run
    second = s.tick(t0 + timedelta(seconds=200))

    quiet = Scheduler(t0, minute)
    none_yet = quiet.tick(t0 - timedelta(seconds=1))

    r = [
        _check("catches up on missed runs", first,
               [t0, t0 + minute, t0 + 2 * minute]),
        _check("schedule stays on the grid", after_first, t0 + 3 * minute),
        _check("next tick fires the 3-minute mark", second, [t0 + 3 * minute]),
        _check("nothing due yet", none_yet, []),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
