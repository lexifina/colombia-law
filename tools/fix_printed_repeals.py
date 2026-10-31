"""Repair articles of corpus.d/60-phase2.json that an act repealed as a whole but whose last words the page still prints
after the marker '<Artículo derogado por el artículo N de la Ley X>' (with no earlier-text box), without re-parsing the part.

The engine read the printed words as the text the repealing act wrote, with no text before it: the article showed the
placeholder line from the code's first day and the printed words from the repeal on, still in force today. It is the
other way round: the printed words are the text from the first day until the repeal, and from the repeal's day the
article is gone. batch10/parse_batch10.py (REPEALED_PRINTED) does the same when it parses later batches; the check
(phase2/verify_extra.py) reads such articles as not in force today.

For each article this script checks the marker on the page in the cache, then puts the printed words into the first
version in place of the placeholder line and turns the repeal's change into a removal. Idempotent.

Usage:  python -X utf8 fix_printed_repeals.py [corpus.d folder]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import engine as E  # noqa: E402

MISSING = "[La fuente no da el texto vigente en esta fecha.]"
FIXES = [  # (part, act slug, page, unit name, unit key, repealing law, its marker on the page)
    ("60-phase2.json", "codigo-general-del-proceso", "ley_1564_2012", "612", "art-0612", "ley-2080-2021",
     "Artículo derogado por el artículo 87 de la Ley 2080 de 2021"),
    ("60-phase2.json", "codigo-general-del-proceso", "ley_1564_2012", "616", "art-0616", "ley-2080-2021",
     "Artículo derogado por el artículo 87 de la Ley 2080 de 2021"),
]


def check_page(page: str, name: str, marker: str) -> None:
    u = next((x for x in E.doc_units(page) if x["name"] == name), None)
    ps = [it for it in (u or {"items": []})["items"] if it[0] == "p"]
    if not ps or not E.plain(ps[0][1]).strip().startswith("<" + marker + ">") or \
            any(it[0] == "box" and it[1] == "Legislación Anterior" for it in u["items"]):
        raise SystemExit(f"{page} art. {name}: marker '{marker}' not found as expected")


def fix(path: str, slug: str, key: str, law: str) -> bool:
    with open(path, encoding="utf-8") as f:
        part = json.load(f)
    act = next(a for a in part["acts"] if a["slug"] == slug)
    vs = act["versions"]
    first = vs[0]["units"].get(key)
    rep = [v for v in vs[1:] if key in (v.get("changes") or {}) or key in v["credits"]]
    if len(rep) != 1 or rep[0]["credits"].get(key) != [law] or "changes" not in rep[0]:
        raise SystemExit(f"{slug} {key}: expected one change by {law}, found {[(v['from'], v['credits'].get(key)) for v in rep]}")
    v = rep[0]
    printed = v["changes"][key]
    if printed is None and first and MISSING not in first["text"]:
        return False  # already fixed
    if not first or first["text"] != f"# {first['label']}\n{MISSING}\n" or printed is None:
        raise SystemExit(f"{slug} {key}: unexpected texts")
    vs[0]["units"][key] = dict(first, text=printed["text"])
    v["changes"][key] = None
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    return True


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d")
    notes = {}
    for part, slug, page, name, key, law, marker in FIXES:
        check_page(page, name, marker)
        print(part, key, "changed" if fix(os.path.join(out, part), slug, key, law) else "unchanged")
        notes.setdefault(part, []).append(f"art. {name}")
    for part, arts in notes.items():
        path = os.path.join(out, part)
        with open(path, encoding="utf-8") as f:
            c = json.load(f)
        d = ("Código General del Proceso (Ley 1564 de 2012): articles Ley 2080 de 2021 (art. 87) repealed as a whole, whose "
             "last words the page still prints after the marker '<Artículo derogado por el artículo 87 de la Ley 2080 de "
             "2021>', read those words from the code's first day until the repeal (25 January 2021), and are gone from it: "
             + ", ".join(arts) + ".")
        if d not in c["decisions"]:
            c["decisions"].append(d)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                json.dump(c, f, ensure_ascii=False, separators=(",", ":"))
                f.write("\n")
            os.replace(tmp, path)
