"""Check corpus.d/99zzh-batch68.json against the text the Secretaría del Senado's basedoc pages still print
(batch4/verify_batch4.py's check, with this batch's page repairs, which parse_batch50 applies on import; staged-repeal
markers are taken out of the page text as the parse takes them out). Batch 28's check, for acts with or without stages.

Each article is checked against the version in force the day before the stage that took it out (articles in no stage:
against the last version). Each stage version must only take out its own articles.

Usage: python -X utf8 batch68/verify_batch68.py [part.json] [-v]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch67", "batch66", "batch65", "batch64", "batch63", "batch62", "batch61", "batch60", "batch59", "batch58", "batch57", "batch56", "batch55", "batch54", "batch53", "batch52", "batch51", "batch50", "batch49", "batch48", "batch47", "batch46", "batch45", "batch44", "batch43", "batch42", "batch41", "batch40", "batch38",
           "batch37", "batch36", "batch35", "batch34", "batch33", "batch32", "batch31", "batch30", "batch29", "batch28", "batch27", "batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16",
           "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4",
           "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch68 as B  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
P = V.P
E = B.E
_full_all = P.full_versions


def _full(versions):
    """The versions in force on the retrieval day (a version on the future branch is not today's text)."""
    return [v for v in _full_all(versions) if v["from"] <= B.E.RETRIEVED]


_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}
import verify_extra  # noqa: E402

verify_extra.REPEALED = B.B13.B10.REPEAL_MARK
verify_extra.install(V)


import hand_fixes as H  # noqa: E402  (batch68/hand_fixes.py)
import hf446  # noqa: E402

# Articles the part has out today while the page still prints them under a deferred ruling's marker (hand_fixes).
GONE: dict = {}
# Words a ruling struck with effect from an undated day: still in the part's text (hand_fixes).
KEEP: dict = {}
# Decreto Ley 262 de 2000 art. 28: the page prints the inciso Ley 2220 de 2022 repealed from 30 December 2022 under its
# 'Inciso derogado a partir del 30 de diciembre de 2022' marker (hf67.fix_262_28): today's text is the page without it.
KEEP[("decreto_0262_2000", "art-0028")] = lambda ls: [l for l in ls if not l.startswith(
    "Los Procuradores Delegados que intervengan como agentes del Ministerio Público ante la jurisdicción")]


def main(argv):
    part = next((a for a in argv if a.endswith(".json")), os.path.join(COUNTRY, "corpus.d", B.PART))
    c = json.load(open(part, encoding="utf-8"))
    total = 0
    for slug, page, *_ in B.ACTS:
        a = next(x for x in c["acts"] if x["slug"] == slug)
        vs = _full(a["versions"])
        if page in B.WHOLE_REPEAL:
            # repealed as a whole: the last version holds nothing (checked), the page's text is the version before it
            r = B.WHOLE_REPEAL[page]
            if vs[-1]["from"] != r["day"] or vs[-1]["units"] or set(vs[-1]["credits"]) != set(vs[-2]["units"]) or any(
                    c != [r["law"]] for c in vs[-1]["credits"].values()):
                print(f"{slug}: repeal version wrong")
                total += 1
            vs = vs[:-1]
        if page in B.PARTIAL_REPEAL:
            # repealed save some articles: the last version keeps exactly those (as before) and the headings above them;
            # the page's text is checked against the version before it
            r = B.PARTIAL_REPEAL[page]
            keep = {E.unit_key(n)[0] for n in r["kept"]}
            last, prev = vs[-1], vs[-2]["units"]
            gone = set(prev) - keep - {"titulos"}
            if (last["from"] != r["day"] or set(last["units"]) != keep | {"titulos"}
                    or any(last["units"][k] != prev[k] for k in keep) or set(last["credits"]) != gone | {"titulos"}
                    or any(c != [r["law"]] for c in last["credits"].values())
                    or [l for l in last["units"]["titulos"]["text"].split(chr(10)) if l]
                    != [l for l in prev["titulos"]["text"].split(chr(10)) if any(l.startswith(h) for h in r["heads"])]):
                print(f"{slug}: partial repeal version wrong")
                total += 1
            vs = vs[:-1]
        P.doc_units(page)
        today = V.today(page)
        stage_of = {}
        for k, (_, law, day, _, _) in enumerate(B.B26.STAGES.get(page, [])):
            for n in B.B26.STAGE_UNITS[page][k]:
                stage_of[E.unit_key(n)[0]] = (day, law)
            v = next(v for v in vs if v["from"] == day)
            prev = [w for w in vs if w["from"] < day][-1]
            gone = set(prev["units"]) - set(v["units"])
            keys = {E.unit_key(n)[0] for n in B.B26.STAGE_UNITS[page][k]}
            changed = [u for u in v["units"] if prev["units"].get(u) != v["units"][u]]
            if page in B.TITLE_GONE and "titulos" in changed:  # the title's headings leave with its articles
                a_, b_ = prev["units"]["titulos"]["text"].splitlines(), v["units"]["titulos"]["text"].splitlines()
                i_ = a_.index(next(x for x in a_ if x.startswith(B.TITLE_GONE[page][0])))
                j_ = a_.index(next(x for x in a_ if x.startswith(B.TITLE_GONE[page][1])))
                if b_ == a_[:i_] + a_[j_:]:
                    changed.remove("titulos")
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
            if page in H.PRINTED and mine is None:  # printed repeal (hand_fixes.PRINTED): out on the day its marker gives
                p0 = next(it[1] for it in B.B23._unit(page, key[4:].lstrip("0")).get("items") if it[0] == "p")
                if any(m.startswith(st) and day <= B.E.RETRIEVED for m in B.E.markers(p0) for st, _, day in H.PRINTED[page]):
                    continue
            if page == hf446.L446 and not lines and mine and (
                    key in {f"art-{int(n):04d}" for n in hf446.INCORPORATED} | {"art-0148"}
                    or (key == "art-0146" and "[La fuente no da" in mine)):
                continue  # coordinator decision: incorporated articles keep their box words (art. 146: placeholder)
            if (page, key) in GONE and mine is None:  # out by a dated deferred ruling the page still prints under its marker
                p0 = next(it[1] for it in B.B23._unit(page, key[4:].lstrip("0")).get("items") if it[0] == "p")
                if GONE[(page, key)] in B.E.plain(p0):
                    continue
            if (page, key) in KEEP:
                lines = KEEP[(page, key)](lines)
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
