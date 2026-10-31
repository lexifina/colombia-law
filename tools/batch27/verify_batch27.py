"""Check corpus.d/99s-batch27.json (codes repealed as a whole) against the text the Secretaría del Senado's basedoc pages
still print for them (batch4/verify_batch4.py's check, with this batch's page repairs, which parse_batch24 applies on
import; the repeal markers are taken out of the page text as the parse takes them out).

For each code the version in force the day before its repeal is checked against that text. Then: every later version
holds only provisions whose repeal the page dates later (with the text checked), and the last version holds none.

Usage: python -X utf8 batch27/verify_batch27.py [part.json] [-v]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16", "batch15", "batch14",
           "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch27 as B  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
P = V.P
V.ACTS = tuple((slug, page) for slug, page, *_ in B.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", B.PART)
_full = P.full_versions
_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}

# Fallback audit (2026-10-31): two CPC articles whose page text is a publisher's note, not the article. Art. 101 shows only
# '<Artículo incorporado en el artículo 23 del Decreto 1818 de 1998>' (a compilation that repealed nothing: the part keeps
# its last text, as Decreto 2651 de 1991 left it, until the code's repeal); art. 104 shows the broken marker '<Artículo
# derogado por el artículo 1, numeral 54 del Decreto 2282 de 1989.' (the part has it absent from that decree's day).
NOT_TEXT = {"codigo_procedimiento_civil": {"art-0101", "art-0104"}}
_today_subst = V.today
V.today = lambda name: {k: ls for k, ls in _today_subst(name).items() if k not in NOT_TEXT.get(name, set())}

import verify_extra  # noqa: E402

verify_extra.install(V)


def main(argv):
    part = next((a for a in argv if a.endswith(".json")), V.P.OUT)
    c = json.load(open(part, encoding="utf-8"))
    bad = 0
    first_repeal = {}
    for slug, page, *_ in B.ACTS:
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
    laws = {B.B24.REPEALS[pg]["law"] for _, pg, *_ in B.ACTS}
    days = {B.B24.REPEALS[pg]["day"] for _, pg, *_ in B.ACTS}

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
