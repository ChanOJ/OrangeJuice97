#!/usr/bin/env python3
"""Add the removal-request footer ("To be removed from this page, contact me.") to the pages of
`site/` that list or describe people. Idempotent: a page that already has it is left alone, the
other bytes of every page are untouched (pages are read and written as latin-1, byte for byte).

    python3 scripts/add_removal_note.py [--check]

--check changes nothing and exits 1 if a listed page lacks the footer or does not exist.
"""
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent / "site"
# Pages that list or describe people (relative to site/).
PAGES = [
    "handles.htm",
    "kloon.htm",
    "credits.htm",
]

import re

REMOVAL_MARK = 'id="removal-note"'
REMOVAL_NOTE = (
    '<div id="removal-note" style="clear:both;margin:28px auto 8px;padding:6px 8px 0;width:775px;max-width:96%;'
    'border-top:1px solid #808080;text-align:center;font:10px/14px Verdana,Arial,Helvetica,sans-serif;'
    'color:#808080;background:transparent">To be removed from this page, '
    '<a href="mailto:chandra_oj@pm.me" style="color:#808080;text-decoration:underline">contact me</a>.</div>'
)
_BODY_END = re.compile(r"(?is)</body\s*>(?!.*</body\s*>)")


def add_removal_note(text):
    if REMOVAL_MARK in text:
        return text
    m = _BODY_END.search(text)
    if m:
        return text[: m.start()] + REMOVAL_NOTE + "\n" + text[m.start():]
    return text + "\n" + REMOVAL_NOTE + "\n"


def main(argv):
    check = "--check" in argv
    bad = 0
    for rel in PAGES:
        p = SITE / rel
        if not p.is_file():
            print("missing: " + rel)
            bad += 1
            continue
        old = p.read_bytes().decode("latin-1")
        new = add_removal_note(old)
        if new != old:
            if check:
                print("no footer: " + rel)
                bad += 1
            else:
                p.write_bytes(new.encode("latin-1"))
                print("added: " + rel)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
