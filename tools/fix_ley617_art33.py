"""Rebuild Ley 617 de 2000, art. 33 (inhabilidades de los diputados) in corpus.d/99c-batch11.json, without re-parsing.

The page prints the article's last words under the marker '<Derogado por el artículo 154 (ver sobre el tema el Art. 49)
de la Ley 2200 de 2022>', and numeral 5 under '<Aparte tachado INEXEQUIBLE, sustituido por el aparte entre <>>' with the
struck words 'segundo grado de consanguinidad' and the new words '<tercer grado de consanguinidad>'. The engine read the
printed words as the text Ley 2200 wrote (placeholder from the act's first day, the article in force from 2022 on) and
left the marker's tail ('> ') in numeral 5. As the page dates it:
  2000-10-09 (the act's first day in the part): the printed words, numeral 5 with 'segundo grado de consanguinidad';
  2009-05-13 Sentencia C-325 de 2009: 'tercer grado de consanguinidad' in its place;
  2022-02-08 Ley 2200 de 2022 (its day in the part), art. 154: the article is gone.
batch11/verify_batch11.py reads the article as not in force today. Idempotent.

Usage:  python -X utf8 fix_ley617_art33.py [corpus.d folder]
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

PART, SLUG, PAGE, KEY = "99c-batch11.json", "ley-617-2000", "ley_0617_2000", "art-0033"
START, RULING, RDAY, REPEAL, PDAY = "2000-10-09", "c-325-09", "2009-05-13", "ley-2200-2022", "2022-02-08"
REPEAL_MARK = re.compile(r"^\s*&lt;Derogado por el art&iacute;culo <A [^>]*>154</A> \(ver sobre el tema el Art\. <A [^>]*>49"
                         r"</A>\) de la Ley 2200 de 2022&gt;(?:&#160;|\s)*")
SUB_MARK = re.compile(r"&lt;Aparte tachado INEXEQUIBLE, sustituido por el aparte entre &lt;&gt;&gt;(?:&#160;|\s)*")
NEW_WORDS = "<U>&lt;tercer grado de consanguinidad&gt;</U>"
C325 = {"label": "Sentencia C-325 de 2009", "title": "Corte Constitucional, Sentencia C-325 de 2009", "kind": "court",
        "enacted": RDAY, "published": None, "url": E.BASE + "c-325_2009.html", "temporary_until": None,
        "restores": None, "note": None}
DECISION = ("Ley 617 de 2000, art. 33: the page prints its last words under '<Derogado por el artículo 154 ... de la Ley "
            "2200 de 2022>'; they are the article's text from the act's first day (numeral 5 with 'segundo grado de "
            "consanguinidad', which Sentencia C-325 de 2009 of 13 May 2009 replaced with 'tercer grado de "
            "consanguinidad', as the page shows), and the article is gone from Ley 2200 de 2022's day (fix_ley617_art33.py).")


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


def texts():
    u = next(x for x in E.doc_units(PAGE) if x["name"] == "33")
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    if len(ps) != 6 or not REPEAL_MARK.match(ps[0]) or not SUB_MARK.search(ps[5]) or NEW_WORDS not in ps[5]:
        raise SystemExit(f"{PAGE} art. 33: page changed")
    ps[0] = REPEAL_MARK.sub("", ps[0])
    ps[5] = SUB_MARK.sub("", ps[5])
    old = ps[:5] + [re.sub(r"\s*" + re.escape(NEW_WORDS), "", ps[5])]
    new = ps[:5] + [re.sub(r"<S>(?:(?!</S>).)*</S>\s*", "", ps[5], flags=re.S).replace(NEW_WORDS, "tercer grado de consanguinidad")]
    epi = E.tidy(re.sub(r"<[^>]*>?", "", E.tidy(E.ART_HEAD.sub("", u["label"], count=1))))
    out = []
    for ls in (old, new):
        lines = [E.tidy(E.to_text(p)) for p in ls]
        lines[0] = epi + " " + lines[0]
        if any(">" in l or "<" in l for l in lines):
            raise SystemExit("marker left in the text")
        out.append(lines)
    if "segundo grado de consanguinidad" not in out[0][5] or "tercer grado de consanguinidad" not in out[1][5]:
        raise SystemExit("numeral 5 words not found")
    return out


def main(argv):
    folder = argv[0] if argv else os.path.join(HERE, "corpus.d")
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    if DECISION in part["decisions"]:
        print(PART, "already fixed")
        return
    old, new = texts()
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    if vs[0]["from"] != START or not any(v["from"] == PDAY for v in vs):
        raise SystemExit("unexpected version days")
    if not any(v["from"] == RDAY for v in vs):
        j = next(i for i, v in enumerate(vs) if v["from"] > RDAY)
        vs.insert(j, {"from": RDAY, "credits": {}})
    sts = states(vs)
    label = next(s[KEY]["label"] for s in sts if KEY in s)
    mk = lambda ls: {"label": label, "kind": "art", "text": f"# {label}\n" + "".join(l + "\n" for l in ls)}  # noqa: E731
    for v, st in zip(vs, sts):
        if v["from"] < RDAY:
            st[KEY] = mk(old)
        elif v["from"] < PDAY:
            st[KEY] = mk(new)
        else:
            st.pop(KEY, None)
        v["credits"].pop(KEY, None)
        if v["from"] == RDAY:
            v["credits"][KEY] = [RULING]
        if v["from"] == PDAY:
            v["credits"][KEY] = [REPEAL]
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
    act["versions"] = [v for j, v in enumerate(vs) if j == 0 or v.get("changes") or v.get("credits")]
    part["laws"].setdefault(RULING, C325)
    if REPEAL not in part["laws"]:
        raise SystemExit(f"{REPEAL} missing")
    part["decisions"].append(DECISION)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed")


if __name__ == "__main__":
    main(sys.argv[1:])
