"""Código de Procedimiento Civil art. 91 and Sentencia C-662-04 (coordinator decision, 2026-11-01, twenty-eighth session).

Ley 794 de 2003 art. 11 rewrote CPC art. 91 (in force 9 April 2003). Sentencia C-662-04 (8 July 2004) declared its
numeral 2 INEXEQUIBLE only 'en cuanto se refiere' to the exceptions of falta de jurisdicción (art. 97 num. 1) and of
compromiso o cláusula compromisoria (art. 97 num. 3): an integrating ruling that limited the numeral's application and
struck no words (the CPC page and Ley 794's page both still print the numeral). The engine read it as a strike of the
whole Ley 794 text and gave the article the text before 2003 (four numerals, 'perención') again from the ruling's day,
credited to the ruling. Here that change goes: C-662-04 makes no version, and the article keeps Ley 794's text from 9
April 2003 until Ley 1564 de 2012 took it out (1 October 2012). If the ruling is then credited nowhere in the part, its
law entry leaves the part.

Checks before any change: the CPC page's note on art. 91 (numeral 2, C-662-04 of 8 July 2004, 'en cuanto se refiere a
la excepción de falta de jurisdicción'); the 8 July 2004 version changes art. 91 alone, credited to c-662-04 alone, and
its text is the article's text before Ley 794 (the 1989 text); the text before it is Ley 794's.

Idempotent (no such version and the decision line once: nothing written). RE-RUN ORDER: after fix_ley794_start.py,
before fix_conditional_notes.py, after any re-parse of 99s-batch27.

Usage: python -X utf8 fix_c662_cpc91.py [corpus.d folder]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_c253_deferral as C253  # noqa: E402  (page_text)

PART, SLUG, KEY, DAY, LAW = "99s-batch27.json", "codigo-de-procedimiento-civil-1970", "art-0091", "2004-07-08", "c-662-04"
MARK = "CPC art. 91, Sentencia C-662-04 (2026-11-01)"
PAGE_NOTE = ("Numeral 2o. declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-662-04 de 8 de julio de "
             "2004, Magistrado Ponente Dr. Rodrigo Uprimny Yepes, '...en cuanto se refiere a la excepción de falta de "
             "jurisdicción prevista en el numeral 1 del artículo 97 del Código de Procedimiento Civil.")
DECISION = (f"{MARK}: Sentencia C-662-04 (8 July 2004) declared numeral 2 of art. 91, as Ley 794 de 2003 art. 11 wrote "
            "it, INEXEQUIBLE only 'en cuanto se refiere' to the exceptions of falta de jurisdicción (art. 97, numeral 1) "
            "and of compromiso o cláusula compromisoria (art. 97, numeral 3). The ruling limited the numeral's "
            "application and struck no words (the source still prints the numeral), so it makes no version: the article "
            "keeps Ley 794's text from 9 April 2003 until Ley 1564 de 2012 took it out (1 October 2012). The text before "
            "Ley 794 does not return on the ruling's day.")


def states(act):
    out, cur = [], None
    for v in act["versions"]:
        if "units" in v:
            cur = (v["units"].get(KEY) or {}).get("text")
        if KEY in (v.get("changes") or {}):
            u = v["changes"][KEY]
            cur = u and u.get("text")
        out.append((v["from"], cur, v["credits"].get(KEY)))
    return out


def credited(part, law):
    return any(law in c for a in part["acts"] for v in a["versions"] for c in v["credits"].values())


def main(argv):
    folder = argv[0] if argv else os.path.join(HERE, "corpus.d")
    page = C253.page_text("codigo_procedimiento_civil")
    if PAGE_NOTE not in page:
        raise SystemExit("codigo_procedimiento_civil: C-662-04 note on art. 91 not found")
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    days = [v["from"] for v in act["versions"]]
    if DAY not in days:
        if part["decisions"].count(DECISION) != 1 or credited(part, LAW) or LAW in part["laws"]:
            raise SystemExit(f"{PART}: no {DAY} version but the fix is not complete")
        print(PART, "already applied")
        return
    k = days.index(DAY)
    v = act["versions"][k]
    if "units" in v or set(v.get("changes") or {}) != {KEY} or v["credits"] != {KEY: [LAW]} or v.get("note"):
        raise SystemExit(f"{PART} {DAY}: not a change of {KEY} alone credited to {LAW} alone: {v['credits']}")
    st = states(act)
    hist = [(d, t, c) for i, (d, t, c) in enumerate(st) if i == 0 or t != st[i - 1][1]]
    hdays = [d for d, _, _ in hist]
    j = hdays.index(DAY)
    if j < 2 or hist[j - 1][2] != ["ley-794-2003"] or hist[j][1] != hist[j - 2][1] or hist[j][1] == hist[j - 1][1]:
        raise SystemExit(f"{PART} {KEY}: shape {[(d, c) for d, _, c in hist]}")
    del act["versions"][k]
    after = states(act)
    want = [s for i, s in enumerate(st) if i != k]
    want = [(d, (hist[j - 1][1] if d >= DAY and t == hist[j][1] else t), c) for d, t, c in want]
    if after != want:
        raise SystemExit(f"{PART} {KEY}: states do not come out as wanted")
    if not credited(part, LAW):
        part["laws"].pop(LAW, None)
    part["decisions"] = [d for d in part["decisions"] if d != DECISION] + [DECISION]
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, f"applied: the {DAY} change of {KEY} credited to {LAW} is gone; law entry kept: {LAW in part['laws']}")


if __name__ == "__main__":
    main(sys.argv[1:])
