"""Take the publisher's page links out of titulos.md in the parts written before the engine learnt to drop them.

At a page break the basedoc prints its links 'Anterior | Siguiente' after the last heading of the page; the engine read
them as words of that heading ('### CAPÍTULO VII. DE LA USURPACIÓN Anterior | Siguiente Anterior | Siguiente').
phase2/engine.py now leaves them out (PAGE_NAV); batches 7 to 15 were parsed with it. This script cleans the other parts
in place, without re-parsing them: in every titulos.md text it removes the links at the end of a heading line (a line
left with no words is dropped), then removes titulos changes that no longer change anything, and versions left with no
change and no credit. Idempotent.

Usage:  python -X utf8 fix_nav_titulos.py [country folder]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILES = ["corpus.json", "corpus.d/50-codes.json", "corpus.d/60-phase2.json", "corpus.d/70-cst.json",
         "corpus.d/80-batch3.json", "corpus.d/90-batch4.json", "corpus.d/95-batch5.json", "corpus.d/97-batch6.json"]
NAV = re.compile(r"(?:\s+(?:Anterior|Siguiente)(?:\s*\|\s*(?:Anterior|Siguiente))*)+\s*$")
DECISION = ("Headings (titulos.md): the publisher's page links 'Anterior | Siguiente' that the basedoc prints after the last "
            "heading of a page are not words of that heading and are left out (fix_nav_titulos.py).")


def clean(text: str) -> str:
    out = []
    for line in text.split("\n")[:-1]:
        line = NAV.sub("", line)
        if re.fullmatch(r"#*\s*", line):
            continue
        out.append(line)
    return "".join(l + "\n" for l in out)


def fix_act(act: dict) -> int:
    vs = act["versions"]
    n = 0
    prev = None  # cleaned titulos in force before the version
    prev_units = None  # the last full version kept (cleaned)
    keep = []
    for v in vs:
        if "units" in v:
            t = v["units"].get("titulos")
            if t is not None:
                c = clean(t["text"])
                if c != t["text"]:
                    v["units"]["titulos"] = dict(t, text=c)
                    n += 1
                if keep and prev == c and "titulos" in v["credits"]:
                    v["credits"].pop("titulos")
                    n += 1
                prev = c
            if keep and prev_units is not None and v["units"] == prev_units and not v["credits"]:
                n += 1
                continue  # a full version that no longer changes anything
            prev_units = v["units"]
            keep.append(v)
            continue
        ch = v.get("changes")
        if ch and "titulos" in ch and ch["titulos"] is not None:
            c = clean(ch["titulos"]["text"])
            if c != ch["titulos"]["text"]:
                ch["titulos"] = dict(ch["titulos"], text=c)
                n += 1
            if c == prev:
                del ch["titulos"]
                v["credits"].pop("titulos", None)
                n += 1
            prev = c
        elif ch and "titulos" in ch:
            prev = None
        if "changes" in v and not v["changes"] and not v["credits"]:
            n += 1
            continue  # a version that no longer changes anything
        keep.append(v)
    act["versions"] = keep
    return n


def main(folder: str) -> None:
    for rel in FILES:
        path = os.path.join(folder, rel)
        with open(path, encoding="utf-8") as f:
            c = json.load(f)
        n = sum(fix_act(a) for a in c["acts"])
        if n and DECISION not in c.get("decisions", []):
            c.setdefault("decisions", []).append(DECISION)
        if n:
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                if rel == "corpus.json":  # written by parse.py with indent=1
                    json.dump(c, f, ensure_ascii=False, indent=1)
                else:
                    json.dump(c, f, ensure_ascii=False, separators=(",", ":"))
                f.write("\n")
            os.replace(tmp, path)
        print(rel, n, "changes")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else HERE)
