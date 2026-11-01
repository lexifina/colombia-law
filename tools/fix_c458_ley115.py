"""Repair the words Sentencia C-458 de 2015 (22 July 2015) put into Ley 115 de 1994 (Ley General de Educación), arts. 1 and
46, in corpus.d/99-batch8.json, without re-parsing the part.

The page marks them '<Texto(s) entre <> corregido(s) en los términos de la Sentencia C-458-15>' and gives the new words in
angle brackets ('<personas en situación de discapacidad física, sensorial y psíquica>'). The engine's marker reading
stopped at the inner '<>': the marker's tail ('corregido en los términos de la Sentencia C-458-15>') stood in the text
and the new words were dropped as an editor's note ('dirigida ... a grupos étnicos, a, con capacidades excepcionales').
phase2/nested_lt.py reads the page right; the check (batch8/verify_batch8.py) reads it through the same module.

For both articles the script reads the page through phase2/nested_lt.py and, in every version from the ruling's day on,
puts the page's lines in place of the lines that differ. The text before the ruling (the original wording, set by the
fallback audit) is not touched. Idempotent.

Usage:  python -X utf8 fix_c458_ley115.py [corpus.d folder]
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ("batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(HERE, _d))

PART, SLUG, PAGE, DAY = "99-batch8.json", "ley-general-de-educacion", "ley_0115_1994", "2015-07-22"
KEYS = ("art-0001", "art-0046")
DECISION = ("Ley General de Educación (Ley 115 de 1994), arts. 1 and 46: the words Sentencia C-458 de 2015 ordered read "
            "('personas en situación de discapacidad física, sensorial y psíquica'), which the page gives in angle brackets "
            "under the marker '<Texto(s) entre <> corregido(s) en los términos de la Sentencia C-458-15>', are the text from "
            "22 July 2015; the marker is the publisher's (fix_c458_ley115.py, phase2/nested_lt.py).")


def states(vs):
    cur, out = {}, []
    for v in vs:
        if "units" in v:
            cur = copy.deepcopy(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append(dict(cur))
    return out


def main(argv):
    folder = argv[0] if argv else os.path.join(HERE, "corpus.d")
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    if DECISION in part["decisions"]:
        print(PART, "already fixed")
        return
    import verify_batch4 as V4  # noqa: E402  (today's text as the checks read it)
    V = V4.V
    old_today = V.today(PAGE)
    import nested_lt  # noqa: E402
    nested_lt.install(V.E, {PAGE})
    new_today = V.today(PAGE)
    if nested_lt.SEEN.get(PAGE) != 4:
        raise SystemExit(f"{PAGE}: expected 4 bracketed C-458-15 phrases, found {nested_lt.SEEN.get(PAGE)}")
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    sts = states(vs)
    for key in KEYS:
        o, n = old_today[key], new_today[key]
        if len(o) != len(n):
            raise SystemExit(f"{key}: line counts differ")
        repl = {a: b for a, b in zip(o, n) if a != b}
        if not repl or any("C-458" in b or "&lt;" in b for b in repl.values()):
            raise SystemExit(f"{key}: unexpected lines")
        for v, st in zip(vs, sts):
            if v["from"] < DAY or key not in st:
                continue
            lines = st[key]["text"].split("\n")
            new = [repl.get(l, l) for l in lines]
            if new == lines:
                raise SystemExit(f"{key} {v['from']}: the old lines are not there")
            st[key] = dict(st[key], text="\n".join(new))
        last = [l for l in sts[-1][key]["text"].split("\n")[1:] if l]
        if last != n:
            raise SystemExit(f"{key}: last version does not equal the page")
    prev = None
    for j, (v, st) in enumerate(zip(vs, sts)):
        if j == 0:
            v["units"] = st
        else:
            ch = {k: u for k, u in st.items() if prev.get(k) != u}
            ch.update({k: None for k in prev if k not in st})
            if ch:
                v["changes"] = ch
            else:
                v.pop("changes", None)
        prev = st
    if any(re.search(r"C-458-15>", u["text"]) for st in sts for k, u in st.items() if k in KEYS):
        raise SystemExit("marker tail left")
    part["decisions"].append(DECISION)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed")


if __name__ == "__main__":
    main(sys.argv[1:])
