"""Runs a migration plan and keeps a journal for the on-call runbook."""


class StepError(Exception):
    pass


def run_steps(steps, journal):
    """Runs each step in order. Returns the names of the steps that completed.

    The journal is flushed whether or not the run succeeds. If a step
    raises, the exception propagates to the caller: a failed migration
    must never look like a successful one.
    """
    done = []
    try:
        for name, fn in steps:
            fn()
            done.append(name)
    finally:
        journal.append("flushed")
    return done


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


def _ok():
    return None


def _boom():
    raise StepError("constraint violation")


def _propagates(steps, journal):
    """True when run_steps lets a StepError reach the caller."""
    try:
        run_steps(steps, journal)
    except StepError:
        return True
    return False


if __name__ == "__main__":
    good = [("create_table", _ok), ("backfill", _ok)]
    bad = [("create_table", _ok), ("add_constraint", _boom), ("backfill", _ok)]

    j1 = []
    j2 = []
    j3 = []

    r = [
        _check("clean run reports every step", run_steps(good, j1),
               ["create_table", "backfill"]),
        _check("journal flushed on success", j1, ["flushed"]),
        _check("journal flushed on failure", (_propagates(bad, j2), j2)[1], ["flushed"]),
        _check("a failing step propagates", _propagates(bad, j3), True),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
