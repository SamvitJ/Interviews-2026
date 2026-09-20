"""Request counters for the metrics endpoint. Worker threads share one Stats."""

import threading
import time


class Stats:
    def __init__(self):
        self.counts = {}
        self.audit_trail = []
        self._lock = threading.Lock()

    def record(self, key):
        """Count one occurrence of `key`."""
        self._audit(key)
        with self._lock:
            current = self.counts.get(key, 0)
            self.counts[key] = current + 1

    def _audit(self, key):
        self.audit_trail.append(key)
        time.sleep(0.001)          # the audit trail is flushed to disk


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


def _run_threaded(thread_count, per_thread):
    stats = Stats()

    def worker():
        for _ in range(per_thread):
            stats.record("hit")

    threads = [threading.Thread(target=worker) for _ in range(thread_count)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return stats


if __name__ == "__main__":
    serial = Stats()
    for _ in range(5):
        serial.record("hit")

    threaded = _run_threaded(4, 25)

    r = [
        _check("serial counting", serial.counts, {"hit": 5}),
        _check("every call reached the audit trail",
               len(threaded.audit_trail), 100),
        _check("threaded counting", threaded.counts, {"hit": 100}),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
