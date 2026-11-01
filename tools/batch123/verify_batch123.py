"""Check corpus.d/99zzzzzzzz-103-bat.json against the text the Secretaría del Senado's basedoc pages still print
(batch4/verify_batch4.py's check, with this batch's page repairs, which parse_batch50 applies on import; staged-repeal
markers are taken out of the page text as the parse takes them out). Batch 28's check, for acts with or without stages.

Each article is checked against the version in force the day before the stage that took it out (articles in no stage:
against the last version). Each stage version must only take out its own articles.

Usage: python -X utf8 batch123/verify_batch123.py [part.json] [-v]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch68", "batch67", "batch66", "batch65", "batch64", "batch63", "batch62", "batch61", "batch60", "batch59", "batch58", "batch57", "batch56", "batch55", "batch54", "batch53", "batch52", "batch51", "batch50", "batch49", "batch48", "batch47", "batch46", "batch45", "batch44", "batch43", "batch42", "batch41", "batch40", "batch38",
           "batch37", "batch36", "batch35", "batch34", "batch33", "batch32", "batch31", "batch30", "batch29", "batch28", "batch27", "batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16",
           "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4",
           "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch123 as B  # noqa: E402  (its page repairs apply to the check too)
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
# (batch 87) Two headings E.label_num cannot read, so the page reading skipped them while the parse keeps them (by the
# anchor name): Ley 549 de 1999 'ARTíCULO 18.' (lower-case í) and 'ARTÍCULO TRANSITORIO 12C.' (the word before the
# number). The check reads their number too, so their words are compared like every other article's.
_label_num = E.label_num


def _label_num_87(label):
    n = _label_num(label)
    if n:
        return n
    m = re.match(r"\s*ART[IÍí]CULO\s+(?:TRANSITORIO\s+)?(\d+[A-Z]?)\.", label or "")
    return m.group(1) if m else None


_today_87 = V.today


def _today_read_all(name):
    E.label_num = _label_num_87
    try:
        return _today_87(name)
    finally:
        E.label_num = _label_num


V.today = _today_read_all
import verify_extra  # noqa: E402

verify_extra.REPEALED = B.B13.B10.REPEAL_MARK
verify_extra.install(V)


import hand_fixes as H  # noqa: E402  (batch123/hand_fixes.py)
import hf446  # noqa: E402
import hf123  # noqa: E402  (batch 91+: hf123.gone_evidence, articles out today whose words the page still prints)

# Articles the part has out today while the page still prints them under a deferred ruling's marker (hand_fixes).
GONE: dict = {}
# (batch 88) Ley 191 de 1995 art. 27: out since Ley 633 de 2000 art. 134; Ley 677 de 2001 revived nothing (Ley 153 de 1887,
# art. 14; hf88.fix_191_27). The page prints its words under that marker.
GONE[("ley_0191_1995", "art-0027")] = "Derogado por el Artículo 134 de la Ley 633 de 2000"
# Words a ruling struck with effect from an undated day: still in the part's text (hand_fixes).
KEEP: dict = {}
# Decreto Ley 262 de 2000 art. 28: the page prints the inciso Ley 2220 de 2022 repealed from 30 December 2022 under its
# 'Inciso derogado a partir del 30 de diciembre de 2022' marker (hf67.fix_262_28): today's text is the page without it.
KEEP[("decreto_0262_2000", "art-0028")] = lambda ls: [l for l in ls if not l.startswith(
    "Los Procuradores Delegados que intervengan como agentes del Ministerio Público ante la jurisdicción")]
# (batch 91) Ley 790 de 2002 art. 13: the check's page reading keeps the words the page shows struck as 'derogado
# tácitamente por ... la Ley 812 de 2003' (hf91.fix_790_13 takes them out from 2003-06-27): today's text is without them.
# (batch 98) Ley 488 de 1998 art. 121: the inciso Sentencia C-030-19 struck with effect deferred by two legislatures is out
# from 20 June 2021 (hf98.fix_488_121); the page still prints it under its marker: today's text is the heading without it.
KEEP[("ley_0488_1998", "art-0121")] = lambda ls: [("BASE GRAVABLE." if l.startswith("BASE GRAVABLE. Está constituida por el "
                                                  "valor de referencia") else l) for l in ls]
# (batch 98) Ley 488 de 1998 art. 80: repealed by Ley 633 de 2000 (hf98.fix_488_80); the page's marker holds a marker
# inside it ('<sic, 2000>'), so the check's reading keeps the marker's tail as words: today the article has none.
KEEP[("ley_0488_1998", "art-0080")] = lambda ls: [l for l in ls if not l.endswith(
    "según establece la Corte Constitucional en Sentencias C-1066-01>")]
KEEP[("ley_0790_2002", "art-0013")] = lambda ls: [l.replace(
    ", y hasta el vencimiento de las facultades extraordinarias que se confieren en la presente ley.", ",.") for l in ls]
# (batch 91) Ley 1444 de 2011 art. 17: the page's last item is '19. <struck words>. <unclosed note on Decreto 626 de 2026';
# today's text keeps the label '19.' only (hf91.fix_1444_17): the note is not law text.
KEEP[("ley_1444_2011", "art-0017")] = lambda ls: [
    "19." if l == "19.. <Ministerio liquidado mediante el Decreto 626 de 2026" else l for l in ls]

# (batch 95) Ley 141 de 1994 arts. 21 and 22: '<Artículo derogado, salvo el parágrafo ...>', '...', then the kept
# parágrafo: the check reads the article as wholly out; today's text is the parágrafo under its heading (hf95.fix_21_22).
KEEP[("ley_0141_1994", "art-0021")] = lambda ls: hf95.kept_paragraph(21)
KEEP[("ley_0141_1994", "art-0022")] = lambda ls: hf95.kept_paragraph(22)
# (batch 99) Ley 1101 de 2006 art. 8: the footnote mark '<1>' between the epigraph and '.Además' reads as two periods
# (hf99.fix_1101_8 writes one): today's text is the page with one.
KEEP[("ley_1101_2006", "art-0008")] = lambda ls: [l.replace(hf99.DOTS_8[0], hf99.DOTS_8[1], 1) for l in ls]
# (batch 104) Ley 1421 de 2010 art. 8: the two incisos Sentencia C-101-22 struck with effect deferred by two legislatures
# are out from 20 June 2024 (hf104.fix_1421_8); the page still prints them under its marker: today's text is without them.
KEEP[("ley_1421_2010", "art-0008")] = lambda ls: [l for l in ls if l not in (hf104.TASAS_8, hf104.PERM_8)]
# (batch 101) Ley 2388 de 2024 art. 3: the editor's mark '*' after 'artículo 5', and the bracket the page prints outside
# the struck 'o notario' (hf101.fix_2388_3): today's text is the page without them.
KEEP[("ley_2388_2024", "art-0003")] = lambda ls: [l.replace(*hf101.MARK_5).replace(*hf101.OPEN_3) for l in ls]
# (batch 107) Ley 179 de 1994 art. 12: Ley 1687 de 2013's text, struck by Sentencia C-052-15 with effect deferred to 31
# December 2015, is out from that day and Ley 225 de 1995's text is back (hf107.fix_12); the page still prints Ley 1687's
# under its marker: today's text is Ley 225's (the page's 'Texto modificado por la Ley 225 de 1995' box).
KEEP[("ley_0179_1994", "art-0012")] = lambda ls: hf107.text_225_12()
# (batch 112) Ley 6 de 1992 art. 124: the page's concordance line 'C_Comerc,+78+80+...' after the parágrafo is not law text
# (hf112.fix_6_124 leaves it out): today's text is the page without it.
KEEP[("ley_0006_1992", "art-0124")] = lambda ls: [l for l in ls if l != hf112.CONC_124]


def main(argv):
    part = next((a for a in argv if a.endswith(".json")), os.path.join(COUNTRY, "corpus.d", B.PART))
    c = json.load(open(part, encoding="utf-8"))
    total = 0
    for slug, page, *_ in B.ACTS:
        a = next(x for x in c["acts"] if x["slug"] == slug)
        vs = _full(a["versions"])
        if page in B.WHOLE_REPEAL or page in B.B24.REPEALS:
            # repealed as a whole (WHOLE_REPEAL, or batch 24's REPEALS with the page's repeal marker taken out): the last
            # version holds nothing (checked), the page's text is the version before it
            r = B.WHOLE_REPEAL.get(page) or B.B24.REPEALS[page]
            if vs[-1]["from"] != r["day"] or vs[-1]["units"] or set(vs[-1]["credits"]) != set(vs[-2]["units"]) or any(
                    c != [r["law"]] for c in vs[-1]["credits"].values()):
                print(f"{slug}: repeal version wrong")
                total += 1
            vs = vs[:-1]
        if page in B.PARTIAL_REPEAL or page in getattr(B, "PARTIAL_93", {}) or page in getattr(B, "PARTIAL_94", {}):
            # repealed save some articles: the last version keeps exactly those (as before) and the headings above them;
            # the page's text is checked against the version before it (batch 93: also PARTIAL_93, Ley 793 de 2002)
            r = B.PARTIAL_REPEAL.get(page) or B.PARTIAL_93.get(page) or B.PARTIAL_94[page]
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
            if hf123.gone_evidence(page, key) and mine is None:  # (batch 90 rule) out today; the page still prints them
                where, ev = hf123.gone_evidence(page, key)
                u_ = B.B23._unit(page, key[4:].lstrip("0"))
                text_ = H._nv(u_) if where == "nv" else B.E.plain(next(it[1] for it in u_["items"] if it[0] == "p"))
                if ev in text_:
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


# Repeals the page dates in the marker over words it still prints (Ley 1608 de 2013 art. 7; phase2/dated_repeal.py).
import dated_repeal  # noqa: E402

dated_repeal.install(V, B.E.RETRIEVED)

if __name__ == "__main__":
    main(sys.argv[1:])
