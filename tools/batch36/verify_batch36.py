"""Check corpus.d/99zb-batch36.json against the text the Secretaría del Senado's basedoc pages
still print for them (batch4/verify_batch4.py's check, with this batch's page repairs, which parse_batch24 applies on
import; the repeal markers are taken out of the page text as the parse takes them out).

For each code the version in force the day before its repeal is checked against that text. Then: every later version
holds only provisions whose repeal the page dates later (with the text checked), and the last version holds none.

Usage: python -X utf8 batch36/verify_batch36.py [part.json] [-v]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch35", "batch34", "batch33", "batch32", "batch31", "batch30", "batch29", "batch27", "batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16", "batch15", "batch14",
           "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch36 as B  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
P = V.P
V.ACTS = tuple((slug, page) for slug, page, *_ in B.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", B.PART)
_full_all = P.full_versions


def _full(versions):
    """The versions in force on the retrieval day (a version on the future branch is not today's text)."""
    return [v for v in _full_all(versions) if v["from"] <= B.E.RETRIEVED]


_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}

import verify_extra  # noqa: E402

# The printed-repeal marker as parse_batch36 reads it (also 'del Decreto N de AAAA' with no link to the article).
verify_extra.REPEALED = B.B13.B10.REPEAL_MARK

verify_extra.install(V)

# Ley 962 de 2005, art. 9: '<Artículo derogado por el artículo 309 de la Ley 1437 de 2011. Rige a partir del dos (2) de
# julio del año 2012. El texto vigente hasta esta fecha es el siguiente:>' + the words until then: gone today.
_today_d = V.today


def today_dated_repeal(name):
    out = _today_d(name)
    if name == "ley_0962_2005":
        u = next(x for x in V.P.doc_units(name)[1:] if V.E.label_num(x["label"] or "") == "9")
        p0 = next(it[1] for it in u["items"] if it[0] == "p")
        if "Rige a partir del dos (2) de julio del a&ntilde;o 2012.</U> El texto vigente hasta esta fecha es el siguiente:"                 not in p0:
            raise SystemExit("Ley 962 art. 9 marker changed")
        out["art-0009"] = []
    return out


V.today = today_dated_repeal



def main(argv):
    part = next((a for a in argv if a.endswith(".json")), V.P.OUT)
    c = json.load(open(part, encoding="utf-8"))
    bad = 0
    first_repeal = {}
    for slug, page, *_ in B.ACTS:
        if page not in B.B24.REPEALS:
            continue
        r = B.B24.REPEALS[page]
        a = next((x for x in c["acts"] if x["slug"] == slug), None)
        if a is None:
            continue
        vs = _full(a["versions"])
        days = [r["day"]] + ([r["deferred"][1]] if "deferred" in r else [])
        tail = [v for v in vs if v["from"] >= r["day"]]
        if [v["from"] for v in tail] != days or tail[-1]["units"]:
            print(f"{slug}: versions from the repeal day {[(v['from'], len(v['units'])) for v in tail]}, expected {days} "
                  f"ending with none")
            bad += 1
            continue
        before = [v for v in vs if v["from"] < r["day"]][-1]
        for v in tail[:-1]:
            wrong = [k for k, u in v["units"].items() if before["units"].get(k) != u]
            if wrong:
                print(f"{slug}: {v['from']} changes the text of {wrong[:10]}")
                bad += 1
        print(f"{slug}: repealed on {days}; the last version holds no provisions; the version of {before['from']} is "
              f"checked below")
        first_repeal[slug] = r["day"]
    # full_versions(...)[-1] is what verify_phase2 checks: the version in force the day before the (first) repeal.
    laws = {B.B24.REPEALS[pg]["law"] for _, pg, *_ in B.ACTS if pg in B.B24.REPEALS}
    days = {B.B24.REPEALS[pg]["day"] for _, pg, *_ in B.ACTS if pg in B.B24.REPEALS}

    def before_repeal(versions):
        vs = _full(versions)
        for i, v in enumerate(vs):
            if i and v["from"] in days and all(ls and set(ls) <= laws for ls in v["credits"].values()) \
                    and len(v["units"]) < len(vs[i - 1]["units"]):
                return vs[:i]
        return vs

    P.full_versions = before_repeal
    V.main(argv)
    if bad:
        print("REPEAL CHECK FAILED:", bad)


if __name__ == "__main__":
    main(sys.argv[1:])
