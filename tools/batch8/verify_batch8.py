"""Check corpus.d/99-batch8.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch8 applies on import).

The Código Disciplinario Único (Ley 734 de 2002) was repealed as a whole from 29 March 2022; the page still prints its
last text (parse_batch8 takes out the repeal marker). For it, the version before the repeal is checked against that
text, and the last version must hold no provisions.

Usage: python -X utf8 batch8/verify_batch8.py [part.json] [-v]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch8  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
P = V.P
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch8.ACTS if slug in parse_batch8.BUILDERS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch8.PART)
import nested_lt  # noqa: E402  (Ley 115 arts. 1 and 46: C-458-15's words under a marker holding '<>'; ../fix_c458_ley115.py)
nested_lt.install(V.E, {"ley_0115_1994"})
_today = V4.V.today
V4.V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}  # replaced words: the new ones
REPEALED = {"codigo-disciplinario-unico": "2022-03-29"}
_full = P.full_versions


def main(argv):
    part = next((a for a in argv if a.endswith(".json")), V.P.OUT)
    c = json.load(open(part, encoding="utf-8"))
    bad = 0
    for slug, day in REPEALED.items():
        a = next(x for x in c["acts"] if x["slug"] == slug)
        vs = _full(a["versions"])
        if vs[-1]["from"] < day or vs[-1]["units"] or vs[-2]["from"] < day or any(v["units"] for v in vs if v["from"] >= day and v is not vs[-2]):
            print(f"{slug}: last version {vs[-1]['from']} holds {len(vs[-1]['units'])} units (expected none on {day})")
            bad += 1
        else:
            print(f"{slug}: last version {day} holds no provisions; the version before it is checked below")
    def last_texts(versions):
        """For a repealed act, each provision's last text before it left (the Código Disciplinario Único's art. 30 left
        after the rest), as one version to check against the page; other acts as they are."""
        vs = _full(versions)
        if not vs or vs[-1]["units"]:
            return vs
        day = min(REPEALED.values())
        before = [v for v in vs if v["from"] < day]
        merged = dict(before[-1]["units"])
        for v in vs[len(before):-1]:
            merged.update(v["units"])
        return vs[:-1] + [dict(vs[-2], units=merged)]
    P.full_versions = last_texts
    V.main(argv)
    if bad:
        print("REPEAL CHECK FAILED:", bad)


if __name__ == "__main__":
    main(sys.argv[1:])
