"""Turns the rich-text comment body into a plain-text preview."""

import re


def strip_tags(html):
    """Remove every HTML tag, keeping the text between them.

    '<b>hi</b>' -> 'hi'
    """
    return re.sub(r"<.*>", "", html)


def _check(name, got, want):
    ok = got == want
    print(("PASS  " if ok else "FAIL  ") + name)
    if not ok:
        print("        got:  %r" % (got,))
        print("        want: %r" % (want,))
    return ok


if __name__ == "__main__":
    r = [
        _check("no markup", strip_tags("plain text"), "plain text"),
        _check("one tag pair", strip_tags("<b>hi</b>"), "hi"),
        _check("two paragraphs", strip_tags("<p>a</p><p>b</p>"), "ab"),
        _check("text around tags", strip_tags("before <i>mid</i> after"),
               "before mid after"),
    ]
    print("\n%d/%d passing" % (sum(r), len(r)))
