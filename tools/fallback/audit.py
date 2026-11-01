"""Fallback audit: for every article a part lists under 'Articles where that happened', compare the engine's latest
earlier text (the state the source's own earlier-text box gives after the last named act) with today's text.

Reads fallback/.tmp/rec-<tag>.json (written by fallback/hook.py) and the parts' decisions. Writes
fallback/.tmp/audit.json and prints one line per article: harmless (same words but the heading line) or DIFFERS.

Usage:  python -X utf8 fallback/audit.py [-v]
"""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
TMP = os.path.join(HERE, "data")  # the audit's records and decisions (rec-*.json, the raw runs, stay in .tmp)
REC_DIR = os.path.join(HERE, ".tmp")


def listed() -> dict[str, list[str]]:
    """part tag -> the units its decisions list."""
    out = {}
    for f in sorted(glob.glob(os.path.join(COUNTRY, "corpus.d", "*.json"))):
        tag = os.path.basename(f).split("-")[0]
        for d in json.load(open(f, encoding="utf-8")).get("decisions", []):
            for m in re.finditer(r"Articles where that happened: (.*?)\.(?:$| [A-Z])", d):
                if m.group(1) != "none":
                    out.setdefault(tag, []).extend(m.group(1).split(", "))
    return out


def norm(s: str) -> str:
    s = unicodedata.normalize("NFC", s).lower()
    s = re.sub(r"[“”\"'‘’«»]", "", s)
    s = re.sub(r"\s+", " ", s)
    return re.sub(r"\s*([.,;:()])\s*", r"\1", s).strip()


EPI = re.compile(r"^(?:art[íi]culo\s+[\w-]+\.?\s*)?(?:[A-ZÁÉÍÓÚÑÜ0-9 ,;:()/\-–\"“”]{3,}?\.)\s+")


def strip_epi(line: str) -> str:
    """The first line without a leading capitals-only epigraph ('FUNCIONES. ...') or 'ARTÍCULO 5o.'."""
    line = re.sub(r"^ART[IÍ]CULO\s+[\w-]+\.?\s*", "", line.strip(), flags=re.I)
    m = EPI.match(line)
    return line[m.end():] if m else line


def body(lines) -> list[str]:
    if not lines:
        return []
    ls = [l for l in lines if re.search(r"\w", l)]
    if not ls or all(not re.search(r"[a-zñáéíóú]", l) for l in ls):
        return []  # nothing, or only the epigraph left (an article repealed today shows its epigraph alone)
    first = strip_epi(ls[0])
    # a first line that is only the epigraph ('CAMBIO DE LA NATURALEZA JURÍDICA DE INRAVISIÓN.') goes too
    if not first.strip() or (ls[0].isupper() and len(ls) > 1):
        ls = ls[1:]
    else:
        ls = [first] + ls[1:]
    return [norm(l) for l in ls if norm(l)]


def classify(known, today) -> str:
    if known in (None, []) and today in (None, []):
        return "harmless"
    if known in (None, []) or today in (None, []):
        return "differs"
    return "harmless" if body(known) == body(today) else "differs"


def main(argv):
    lst = listed()
    rows = []
    for tag, units in lst.items():
        path = os.path.join(REC_DIR, f"rec-{tag}.json")
        recs = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else None
        for unit in units:
            if recs is None:
                rows.append({"tag": tag, "unit": unit, "class": "no-record"})
                continue
            rs = [r for r in recs if r["unit"] == unit]
            if not rs:
                rows.append({"tag": tag, "unit": unit, "class": "no-record"})
                continue
            cls = ["harmless" if classify(r["known_last"], r["today"]) == "harmless" else "differs" for r in rs]
            rows.append({"tag": tag, "unit": unit, "class": "differs" if "differs" in cls else "harmless",
                         "records": rs})
    with open(os.path.join(TMP, "audit.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump(rows, f, ensure_ascii=False, indent=1)
    from collections import Counter
    print(Counter(r["class"] for r in rows), len(rows))
    by = Counter((r["tag"], r["class"]) for r in rows)
    for tag in lst:
        print(tag, {c: by[(tag, c)] for c in ("harmless", "differs", "no-record") if by[(tag, c)]})
    if "-v" in argv:
        for r in rows:
            if r["class"] != "harmless":
                print(r["class"], r["tag"], r["unit"])


if __name__ == "__main__":
    main(sys.argv[1:])
