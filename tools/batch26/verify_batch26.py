"""Check corpus.d/99r-batch26.json (Código del Menor, repealed in stages) against the text the Secretaría del Senado's
basedoc page still prints (batch4/verify_batch4.py's check, with this batch's page repairs, which parse_batch26 applies on
import; the stage markers are taken out of the page text as the parse takes them out).

Each article is checked against the version in force the day before the stage that took it out (articles in no stage:
against the last version). Each stage version must only take out its own articles.

Usage: python -X utf8 batch26/verify_batch26.py [part.json] [-v]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16",
           "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4",
           "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch26 as B  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
P = V.P
E = B.E
_full = P.full_versions
_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}
import verify_extra  # noqa: E402

verify_extra.install(V)


def main(argv):
    part = next((a for a in argv if a.endswith(".json")), os.path.join(COUNTRY, "corpus.d", B.PART))
    c = json.load(open(part, encoding="utf-8"))
    total = 0
    for slug, page, *_ in B.ACTS:
        a = next(x for x in c["acts"] if x["slug"] == slug)
        vs = _full(a["versions"])
        today = V.today(page)
        P.doc_units(page)
        stage_of = {}
        for k, (_, law, day, _, _) in enumerate(B.STAGES[page]):
            for n in B.STAGE_UNITS[page][k]:
                stage_of[E.unit_key(n)[0]] = (day, law)
            v = next(v for v in vs if v["from"] == day)
            prev = [w for w in vs if w["from"] < day][-1]
            gone = set(prev["units"]) - set(v["units"])
            keys = {E.unit_key(n)[0] for n in B.STAGE_UNITS[page][k]}
            changed = [u for u in v["units"] if prev["units"].get(u) != v["units"][u]]
            if gone != keys or changed:
                print(f"{slug}: stage {day} takes out {len(gone)} (expected {len(keys)}), changes {changed[:5]}")
                total += 1
        bad = []
        for key, lines in today.items():
            if key in stage_of:
                day = stage_of[key][0]
                state = [w for w in vs if w["from"] < day][-1]["units"]
            else:
                state = vs[-1]["units"]
            mine = state.get(key, {}).get("text")
            mine_lines = [l for l in (mine or "").split("\n")[1:] if l and re.search(r"\w", l)]
            if lines != mine_lines and not (not lines and mine is None):
                bad.append(key)
                if "-v" in argv:
                    import difflib
                    print("DIFF", key)
                    for d in difflib.unified_diff(mine_lines, lines, "corpus", "page", n=0, lineterm=""):
                        if not d.startswith(("@@", "---", "+++")):
                            print("   ", d[:300])
        extra = [k for k in vs[-1]["units"] if k not in today and k != "titulos"]
        total += len(bad) + len(extra)
        print(f"{slug}: {len(today)} articles, {len(bad)} differ{': ' + ' '.join(bad[:20]) if bad else ''}; "
              f"in force at the end: {sorted(k for k in vs[-1]['units'] if k != 'titulos')}; extra: {extra}")
    print("TOTAL differ:", total)


if __name__ == "__main__":
    main(sys.argv[1:])
