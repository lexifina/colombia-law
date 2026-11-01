"""Editor footnote marks left inside the law text (2026-11-01, twenty-fifth session).

The basedoc prints an editor's footnote mark '*' after a cross-reference and explains it in a 'Notas del Editor' box
starting '* ...'. The mark is the editor's, not the act's. Ley 294 de 1996 art. 5 (99f-batch14, violencia-intrafamiliar)
kept it in three versions: 'artículo 18 * de la presente ley' (Ley 1257 de 2008, Ley 2126 de 2021 texts, from the page's
earlier-text boxes) and 'artículo 18* de la presente ley' (Ley 2197 de 2022 text, today's). Each now reads 'artículo 18
de la presente ley' (batch 101 did the same for Ley 2388 de 2024 art. 3 in its driver, hf101.fix_2388_3).

Checks, from the cached page (engine reader): the unit's Notas del Editor box starts with the mark and names the
reference; every replaced text must hold the mark exactly once; no change may become empty (each changed version must
still differ from the one before it). Text only: no credit or day changes.

Idempotent: a part whose decision line lists the unit already is left alone (a re-parse writes no such line and brings
the mark back, so the fixer applies after one).
Usage: python -X utf8 fix_editor_marks.py [--dry] [--to DIR] [corpus.d folder]
Re-run order: after fix_ley294_arts456.py (after any re-parse of 99f-batch14); text only, no credits.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DECISION = ("Editor marks (2026-11-01): the page prints the editor's footnote mark '*' after a cross-reference (explained "
            "in its Notas del Editor); the mark is not the act's words and is left out of every version: ")

ENTRIES = [
    {"part": "99f-batch14.json", "slug": "violencia-intrafamiliar", "page": "ley_0294_1996", "num": "5",
     "key": "art-0005",
     "marks": [("artículo 18 * de la presente ley", "artículo 18 de la presente ley"),
               ("artículo 18* de la presente ley", "artículo 18 de la presente ley")],
     "note": "criterio del editor la referencia al 'artículo 18 de la presente ley'",
     "why": "Ley 294 de 1996 art. 5, 'artículo 18 de la presente ley'"},
]


def _engine():
    sys.path.insert(0, os.path.join(HERE, "phase2"))
    import engine as E  # noqa: E402
    import parse_phase2 as P  # noqa: E402
    return E, P


def page_check(e) -> None:
    E, P = _engine()
    u = next(u for u in P.doc_units(e["page"]) if u["name"] == e["num"])
    notes = [E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas del Editor"]
    p0 = E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    if not any(n.lstrip().startswith("*") and e["note"] in n for n in notes):
        raise SystemExit(f"{e['page']} art. {e['num']}: no editor note '* ... {e['note']}'")
    if not any(old in p0 for old, _ in e["marks"]):
        raise SystemExit(f"{e['page']} art. {e['num']}: the page's text has no mark")


def apply(part: dict, e: dict) -> int:
    line = DECISION + e["why"] + "."
    if line in part.get("decisions", []):
        return 0
    act = next(a for a in part["acts"] if a["slug"] == e["slug"])
    n, prev = 0, None
    for v in act["versions"]:
        for field in ("units", "changes"):
            u = (v.get(field) or {}).get(e["key"])
            if not u:
                continue
            t = u["text"]
            hits = [(o, w) for o, w in e["marks"] if o in t]
            if hits:
                if len(hits) != 1 or t.count(hits[0][0]) != 1:
                    raise SystemExit(f"{e['slug']} {e['key']} {v['from']}: mark not found exactly once")
                t = t.replace(*hits[0])
                if field == "changes" and t == prev:
                    raise SystemExit(f"{e['slug']} {e['key']} {v['from']}: the change would become empty")
                u["text"] = t
                n += 1
            prev = u["text"]
    if not n:
        raise SystemExit(f"{e['slug']} {e['key']}: no version holds the mark")
    part.setdefault("decisions", []).append(line)
    return n


def main(argv: list[str]) -> None:
    dry = "--dry" in argv
    argv = [a for a in argv if a != "--dry"]
    to = None
    if "--to" in argv:
        i = argv.index("--to")
        to = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    src = argv[0] if argv else os.path.join(HERE, "corpus.d")
    out = to or src
    for e in ENTRIES:
        p = os.path.join(src, e["part"])
        if not os.path.exists(p):
            print("missing", e["part"])
            continue
        raw = open(p, encoding="utf-8").read()
        part = json.loads(raw)
        if (DECISION + e["why"] + ".") in part.get("decisions", []):
            print("already applied", e["part"], e["key"])
            continue
        page_check(e)
        n = apply(part, e)
        print(f"APPLIED {e['part']} {e['slug']} {e['key']}: {n} versions")
        if dry:
            continue
        os.makedirs(out, exist_ok=True)
        q = os.path.join(out, e["part"])
        s = json.dumps(part, ensure_ascii=False, separators=(",", ":"))
        open(q + ".tmp", "w", encoding="utf-8", newline="\n").write(s + ("\n" if raw.endswith("\n") else ""))
        os.replace(q + ".tmp", q)


if __name__ == "__main__":
    main(sys.argv[1:])
