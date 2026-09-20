"""Work items for the scheduler queue."""


class Job:
    """A unit of work. `tags` are per-job routing labels."""

    tags = []

    def __init__(self, name, priority=0):
        self.name = name
        self.priority = priority

    def add_tag(self, tag):
        self.tags.append(tag)

    def replace_tags(self, tags):
        self.tags = list(tags)


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    replaced = Job("indexer")
    replaced.replace_tags(["nightly", "io"])

    first = Job("mailer")
    first.add_tag("urgent")
    second = Job("cleanup")
    second.add_tag("batch")

    r = [
        _check("replace_tags sets tags", replaced.tags, ["nightly", "io"]),
        _check("first job keeps its own tag", first.tags, ["urgent"]),
        _check("second job keeps its own tag", second.tags, ["batch"]),
        _check("a fresh job starts untagged", Job("fresh").tags, []),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
