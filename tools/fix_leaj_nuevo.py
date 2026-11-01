"""Add to the Ley Estatutaria de la Administración de Justicia (Ley 270 de 1996), in corpus.d/99-batch8.json, the article
without a number that Ley 1285 de 2009, art. 25, added after art. 209B ('ARTÍCULO NUEVO. Agotada cada etapa del proceso,
el Juez ejercerá el control de legalidad ...'), without re-parsing the part. The batch 8 driver did not read the page's
unnumbered 'ARTÍCULO NUEVO' blocks (phase2/stray.py new_articles, used from batch 10 on); the article is the file
art-0209-nuevo-1 ('Art. nuevo 1 (después del art. 209)', the later batches' naming), in force from Ley 1285 de 2009's
day (2009-01-22, its publication, as the part dates it) to today; the page marks no change to it since. Idempotent.

Usage:  python -X utf8 fix_leaj_nuevo.py [corpus.d folder]
"""
from __future__ import annotations

import copy
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "phase2"))
import engine as E  # noqa: E402

PART, SLUG, PAGE, LAW, DAY = "99-batch8.json", "ley-estatutaria-de-la-administracion-de-justicia", "ley_0270_1996", \
    "ley-1285-2009", "2009-01-22"
KEY, LABEL = "art-0209-nuevo-1", "Art. nuevo 1 (después del art. 209)"
MARK = "Artículo adicionado por el artículo 25 de la Ley 1285 de 2009"
DECISION = ("Ley Estatutaria de la Administración de Justicia (Ley 270 de 1996): the article without a number that Ley 1285 "
            "de 2009, art. 25, added after art. 209B (the page heads it 'ARTÍCULO NUEVO.') is the file art-0209-nuevo-1, "
            "in force from 2009-01-22 (fix_leaj_nuevo.py).")


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
    us = E.doc_units(PAGE)
    i = next(i for i, u in enumerate(us) if u["name"] == "NUEVO")
    if us[i - 1]["name"] != "209B":
        raise SystemExit("the unnumbered article does not follow art. 209B")
    u = us[i]
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    if len(ps) != 1 or MARK not in E.plain(ps[0]):
        raise SystemExit(f"{PAGE}: 'ARTÍCULO NUEVO' block changed")
    if any(re.search(r"derogad|INEXEQUIBLE|modificad", E.plain(it[2])) for it in u["items"]
           if it[0] == "box" and it[1] == "Notas de Vigencia"):
        raise SystemExit("a later change is noted")
    line = re.sub(r"^ART[ÍI]CULO NUEVO\.\s*", "", E.tidy(E.to_text(ps[0])))
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    sts = states(vs)
    if not any(v["from"] == DAY for v in vs):
        raise SystemExit(f"no version on {DAY}")
    unit = {"label": LABEL, "kind": "art", "text": f"# {LABEL}\n{line}\n"}
    for v, st in zip(vs, sts):
        if v["from"] >= DAY:
            st[KEY] = unit
            if v["from"] == DAY:
                v["credits"][KEY] = [LAW]
    prev = None
    for j, (v, st) in enumerate(zip(vs, sts)):
        if j == 0:
            v["units"] = st
        else:
            ch = {k: x for k, x in st.items() if prev.get(k) != x}
            ch.update({k: None for k in prev if k not in st})
            if ch:
                v["changes"] = ch
            else:
                v.pop("changes", None)
        prev = st
    part["decisions"].append(DECISION)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed")


if __name__ == "__main__":
    main(sys.argv[1:])
