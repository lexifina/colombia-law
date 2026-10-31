"""Which audited fallbacks took effect in the published parts: today's words T on the last named act's day D (or, where
today the text is gone, the text gone from D). A fallback whose result a later step replaced (the published unit on D
does not hold T) changed nothing there.

Usage:  python -X utf8 fallback/census.py [-v]     writes fallback/.tmp/census.json
"""
import glob
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply as AP  # noqa: E402
import audit as A  # noqa: E402
import triage as T  # noqa: E402


def published():
    out = {}
    for f in glob.glob(os.path.join(AP.COUNTRY, "corpus.d", "*.json")):
        tag = os.path.basename(f).split("-")[0]
        part = json.load(open(f, encoding="utf-8"))
        for a in part["acts"]:
            page = a["url"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
            out.setdefault((tag, page), a)
    return out


def effect(a, ukey, x):
    vs = a["versions"]
    sts = AP.states(vs)
    dn = x["events"][-1][0]
    idx = [i for i, v in enumerate(vs) if v["from"] <= dn]
    if not idx:
        return "no-version"
    i = idx[-1]
    u = sts[i].get(ukey)
    bl = AP.body_lines(u)
    real = [l for l in bl if re.search(r"[a-záéíóúñ]", l)]
    Tl, Kl = x["today"] or [], x["known_last"] or []
    tb = A.body(Tl)
    if tb:
        return "effective" if AP.find_run(bl, Tl) is not None else "replaced"
    # today gone
    if not real:
        return "effective"
    return "effective" if Kl and AP.find_run(bl, Kl) is None else "replaced"


def main(argv):
    pub = published()
    rows = json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))
    out, cnt = [], Counter()
    for r in rows:
        page, ukey = r["unit"].split(" ", 1)
        a = pub.get((r["tag"], page))
        for i, x in enumerate(r.get("records", [])):
            kind = T.kind(x)
            if kind == "heading":
                e = "heading"
            else:
                e = effect(a, ukey, x) if a else "no-act"
            out.append({"tag": r["tag"], "unit": r["unit"], "rec": i, "kind": kind, "effect": e})
            cnt[(kind, e)] += 1
    json.dump(out, open(os.path.join(A.TMP, "census.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    for k, n in sorted(cnt.items()):
        print(k, n)
    units = Counter()
    for (t, u), g in __import__("itertools").groupby(out, key=lambda o: (o["tag"], o["unit"])):
        g = list(g)
        units["effective" if any(o["effect"] == "effective" and o["kind"] not in ("punct",) for o in g) else "no effect"] += 1
    print(dict(units))
    if "-v" in argv:
        for o in out:
            if o["effect"] not in ("effective", "heading", "replaced"):
                print(o)


if __name__ == "__main__":
    main(sys.argv[1:])
