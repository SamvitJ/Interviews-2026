"""Builds plain-text summary reports for the nightly job."""


def add_line(text, lines=None):
    if lines is None:
        lines = []
    lines.append(text)
    return lines


def build_report(title, rows):
    lines = add_line("== %s ==" % title)
    for row in rows:
        add_line(row, lines)
    return "\n".join(lines)


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    first = build_report("Monday", ["ok", "ok"])
    second = build_report("Tuesday", ["ok"])
    r = [
        _check("first report", first, "== Monday ==\nok\nok"),
        _check("second report", second, "== Tuesday ==\nok"),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
