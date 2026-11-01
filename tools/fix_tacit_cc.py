"""Take out of the Código Civil (corpus.d/50-codes.json) the four articles the source shows with no current text because
it calls them derogated tacitly or 'orgánicamente', from the in-force day of the act the page names, without re-parsing.

The part kept their words in every version (no act or ruling removed them in express terms), so its last version
differed from the source's current text, which shows only the derogation marker:
  art. 50   'Derogado orgánicamente por la Ley 5a. de 1975, el Código del Menor y el Código de la Infancia y la
            Adolescencia, según lo analiza la Corte Constitucional en Sentencia C-336-16': out from Ley 5 de 1975
            (1975-01-28), the first of the acts named;
  art. 196, art. 208  'derogado tácitamente por la Ley 28 de 1932, según sostiene la Corte Constitucional en Sentencia
            C-379-98': out from Ley 28 de 1932 (1933-01-19, its art. 10);
  art. 636  'derogado tácitamente por los Artículos 40, 42 Y 43 del Decreto 2150 de 1995, según lo establece la Corte
            Constitucional en Sentencia C-670-05': out from Decreto 2150 de 1995 (1995-12-06, its art. 152).
For each, the script checks the marker in the cached page, removes the article from the version on that day on (adding
the version if none exists) and credits the removal to the act. It rewrites the part's decision on these four articles.
Idempotent.

Usage:  python -X utf8 fix_tacit_cc.py [corpus.d folder]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "codes"))
import parse_codes as P  # noqa: E402

PART, SLUG = "50-codes.json", "codigo-civil"
FIXES = [  # (unit key, article number, day, law key, words of the page's marker)
    ("art-0050", "50", "1975-01-28", "ley-5-1975", "Derogado orgánicamente por la Ley 5ª de 1975"),
    ("art-0196", "196", "1933-01-19", "ley-28-1932", "Artículo derogado tácitamente por la Ley 28 de 1932"),
    ("art-0208", "208", "1933-01-19", "ley-28-1932", "Artículo derogado tácitamente por la Ley 28 de 1932"),
    ("art-0636", "636", "1995-12-06", "dec-2150-1995", "Artículo derogado tácitamente por los Artículos 40, 42 Y 43 del Decreto 2150 de 1995"),
]
DEC_2150 = {"label": "Decreto 2150 de 1995", "title": "Decreto 2150 de 1995", "kind": "decree", "enacted": "1995-12-05",
            "published": "1995-12-06", "url": "http://www.secretariasenado.gov.co/senado/basedoc/decreto_2150_1995.html",
            "temporary_until": None, "restores": None, "note": None}
OLD = ("Articles the source calls derogated only tacitly or 'orgánicamente' by Court opinion (arts. 50, 196, 208, 636) keep "
       "their words in every version, since no act or ruling removed them; the page itself shows no current text for them.")
NEW = ("Articles the source shows with no current text because it calls them derogated tacitly or 'orgánicamente' leave "
       "on the in-force day of the act it names (fix_tacit_cc.py): art. 50 from Ley 5 de 1975 (1975-01-28, the first of "
       "Ley 5 de 1975, the Código del Menor and the Código de la Infancia y la Adolescencia, as Sentencia C-336 de 2016 "
       "analyses), arts. 196 and 208 from Ley 28 de 1932 (1933-01-19; Sentencia C-379 de 1998), art. 636 from Decreto "
       "2150 de 1995, arts. 40, 42 and 43 (1995-12-06; Sentencia C-670 de 2005).")
OLD_CHECK = ("all match except the four tacitly derogated articles above.")
NEW_CHECK = ("all match.")


def check_page():
    for key, num, _, _, words in FIXES:
        u = next((u for u in P.doc_units(P.CC)[1:] if re.match(rf"ART[IÍ]CULO\s+{num}\.", P.split_libro(u)[0]["label"])), None)
        if u is None:
            raise SystemExit(f"art. {num} not on the page")
        ps = [P.plain(it[1]) for it in u["items"] if it[0] == "p"]
        if not any(words in p for p in ps) or any(re.search(r"\w", P.tidy(P.to_text(it[1], False)))
                                                  for it in u["items"] if it[0] == "p"):
            raise SystemExit(f"art. {num}: marker changed or the page shows text again")


def full_states(versions):
    cur, out = {}, []
    for v in versions:
        if "units" in v:
            cur = dict(v["units"])
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
    if any(NEW in d for d in part["decisions"]):
        print(PART, "already fixed")
        return
    check_page()
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    last_before = full_states(vs)[-1]
    for key, _, day, law, _ in FIXES:
        if not any(v["from"] == day for v in vs):
            k = next(i for i, v in enumerate(vs) if v["from"] > day)
            vs.insert(k, {"from": day, "credits": {}})
    sts = full_states(vs)
    for key, _, day, law, _ in FIXES:
        for st, v in zip(sts, vs):
            if v["from"] >= day:
                st.pop(key, None)
            if v["from"] == day:
                v["credits"].setdefault(key, [])
                if law not in v["credits"][key]:
                    v["credits"][key].append(law)
    prev = None
    for i, (v, st) in enumerate(zip(vs, sts)):
        if i == 0:
            v["units"] = st
        else:
            ch = {k: u for k, u in st.items() if prev.get(k) != u}
            ch.update({k: None for k in prev if k not in st})
            if ch:
                v["changes"] = ch
            else:
                v.pop("changes", None)
        prev = st
    after = full_states(vs)[-1]
    if {k: u for k, u in last_before.items() if k not in {f[0] for f in FIXES}} != after:
        raise SystemExit("unexpected change to today's text")
    part["laws"].setdefault("dec-2150-1995", DEC_2150)
    part["decisions"] = [d.replace(OLD, NEW).replace(OLD_CHECK, NEW_CHECK) for d in part["decisions"]]
    if not any(NEW in d for d in part["decisions"]):
        raise SystemExit("decision text not found")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed")


if __name__ == "__main__":
    main(sys.argv[1:])
