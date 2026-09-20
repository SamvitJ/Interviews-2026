"""Countdown shown on the billing reminder banner."""

from datetime import datetime, timedelta


def days_until(deadline, now):
    """Whole days remaining, rounded UP.

    1 hour from now      -> 1
    exactly 2 days away  -> 2
    25 hours away        -> 2
    1 hour ago           -> 0
    """
    return (deadline - now).days


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    now = datetime(2026, 9, 21, 9, 0, 0)
    r = [
        _check("exactly two days", days_until(now + timedelta(days=2), now), 2),
        _check("23 hours away", days_until(now + timedelta(hours=23), now), 1),
        _check("25 hours away", days_until(now + timedelta(hours=25), now), 2),
        _check("just passed", days_until(now - timedelta(hours=1), now), 0),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
