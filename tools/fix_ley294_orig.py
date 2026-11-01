"""Ley 294 de 1996 (99f-batch14, violencia-intrafamiliar): original texts of arts. 7, 9, 11, 12, 14-18, in place.

Ley 575 de 2000 (Diario Oficial 43.889 of 11 February 2000) rewrote these articles. The page gives each one's original
words in an earlier-text box headed 'El texto original de la Ley 294 de 1996:', a heading the engine does not read (it
reads only headings starting 'Texto'), so the articles were absent from 22 July 1996 to 11 February 2000. As for art. 30
(fix_ley2126_term.py), each article now reads as its box from the act's first version (1996-07-22); Ley 575's text from
2000-02-11 is unchanged (now a change, no longer an insertion).

Art. 15: the box prints struck words, and its Jurisprudencia Vigencia box says 'Apartes subrayados del texto original
declarados INEXEQUIBLES por la Corte Constitucional, mediante Sentencia C-273-98 del 3 de junio de 1998 ... Los demas apartes
fueron declarados EXEQUIBLES, en el entendido de que ...': the full original text from 1996-07-22, without the struck words
from 1998-06-03, credited to Sentencia C-273 de 1998 (a new court law, no note: it struck words). Art. 9's ruling on its
original text (C-652-97) is a plain EXEQUIBLE and changes nothing. The words are read with the engine's own paragraph
reader (box_paras, block_text, to_text/tidy for the struck words).

Checks the page first; each article's history must still be the one insertion by Ley 575. Idempotent (decision line).
RE-RUN after any re-parse of batch 14 (after fix_ley2126_term.py).

Usage: python -X utf8 fix_ley294_orig.py [corpus.d folder]
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
for _d in ("batch14", "batch13", "batch12", "batch11", "batch10", "batch9", "batch8", "batch7", "batch6", "batch5", "batch4",
           "batch3", "phase2"):
    sys.path.insert(0, os.path.join(HERE, _d))
_argv, sys.argv = sys.argv, sys.argv[:1]
import parse_batch14 as B  # noqa: E402
sys.argv = _argv
P, E = B.P, B.E

PART, SLUG, PAGE = "99f-batch14.json", "violencia-intrafamiliar", "ley_0294_1996"
ARTS = (7, 9, 11, 12, 14, 15, 16, 17, 18)
L575, START, CHANGE = "ley-575-2000", "1996-07-22", "2000-02-11"
RULING, RDAY = "c-273-98", "1998-06-03"
HEAD = re.compile(r"El texto original de la Ley 294 de 1996\s*:?$")
SPAN = re.compile(r"(?:\s|&#160;|&nbsp;)*<span class='b_aj'>(.*?)</span>(?:\s|&#160;|&nbsp;)*:?(?:\s|&#160;|&nbsp;)*$", re.S)
JV15 = ("Apartes subrayados del texto original declarados INEXEQUIBLES por la Corte Constitucional, mediante Sentencia "
        "C-273-98 del 3 de junio de 1998")
MARK = "Ley 294 de 1996 original texts (2026-11-01)"


def page_blocks():
    """name -> (paragraphs of the original-text block, plain text of the unit's other boxes)."""
    out = {}
    for u in P.doc_units(PAGE):
        if u["name"] not in {str(n) for n in ARTS}:
            continue
        paras, other = None, []
        for it in u["items"]:
            if it[0] != "box":
                continue
            if "Legislaci" not in it[1]:
                other.append(E.plain(it[2]))
                continue
            ps = E.box_paras(it[2])
            heads = [i for i, ph in enumerate(ps) if SPAN.match(ph)]
            for i in heads:
                if HEAD.match(E.plain(SPAN.match(ps[i]).group(1)).strip()):
                    if paras is not None:
                        raise SystemExit(f"art. {u['name']}: two original-text blocks")
                    paras = ps[i + 1:next((h for h in heads if h > i), len(ps))]
        if not paras:
            raise SystemExit(f"art. {u['name']}: no 'El texto original de la Ley 294 de 1996' block")
        notes = " ".join(other)
        if "de la Ley 575 de 2000, publicada en el Diario Oficial No 43.889, de 11 de febrero de 2000" not in notes:
            raise SystemExit(f"art. {u['name']}: Ley 575 note not found")
        if "INEXEQUIBLE" in notes and u["name"] != "15":
            raise SystemExit(f"art. {u['name']}: a ruling struck words (not handled)")
        out[int(u["name"])] = (paras, notes)
    if sorted(out) != list(ARTS):
        raise SystemExit(f"articles found: {sorted(out)}")
    if JV15 not in out[15][1]:
        raise SystemExit("art. 15: C-273-98 line not found")
    return out


def texts(n, paras):
    lines = E.block_text(paras, True)
    if not lines or E.ART_HEAD.match(lines[0]):
        raise SystemExit(f"art. {n}: unexpected block {lines[:1]}")
    full = f"# Art. {n}\n" + "\n".join(lines) + "\n"
    if n != 15:
        if "<s" in "".join(paras).lower():
            raise SystemExit(f"art. {n}: struck words in the box")
        return full, None
    post = []
    for i, ph in enumerate(paras):
        t = E.tidy(E.to_text(ph, keep_struck=False))
        t = E.tidy(E.ART_HEAD.sub("", t, count=1)) if i == 0 else t
        if t:
            post.append(t)
    after = f"# Art. {n}\n" + "\n".join(post) + "\n"
    if after == full:
        raise SystemExit("art. 15: no struck words")
    return full, after


def touched(v, key):
    return key in (v.get("changes") or {}) or key in v["credits"] or key in (v.get("units") or {})


def main(folder):
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    if any(MARK in d for d in part["decisions"]):
        print(PART, "already applied")
        return
    blocks = page_blocks()
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    if vs[0]["from"] != START or "units" not in vs[0]:
        raise SystemExit("unexpected first version")
    i575 = next(i for i, v in enumerate(vs) if v["from"] == CHANGE)
    u0 = dict(vs[0]["units"])
    after15 = None
    for n in ARTS:
        key = f"art-{n:04d}"
        hist = [(v["from"], v["credits"].get(key)) for v in vs if touched(v, key)]
        if hist != [(CHANGE, [L575])] or vs[i575]["changes"][key] is None:
            raise SystemExit(f"art. {n}: unexpected history {hist}")
        full, after = texts(n, blocks[n][0])
        if full == vs[i575]["changes"][key]["text"]:
            raise SystemExit(f"art. {n}: original equals Ley 575's text")
        u0[key] = {"label": f"Art. {n}", "kind": "art", "text": full}
        if after:
            after15 = (key, after)
    tit = [kv for kv in u0.items() if kv[0] == "titulos"]
    vs[0]["units"] = dict(sorted(kv for kv in u0.items() if kv[0] != "titulos") + tit)
    # C-273-98: a version of its own between the last version before it and Ley 575's.
    j = next(i for i, v in enumerate(vs) if v["from"] > RDAY)
    if vs[j - 1]["from"] == RDAY or vs[j]["from"] != CHANGE:
        raise SystemExit("unexpected versions around 1998-06-03")
    ref = vs[j - 1]
    key, after = after15
    vs.insert(j, {"from": RDAY, "credits": {key: [RULING]}, "source_url": ref["source_url"], "sha256": ref["sha256"],
                  "changes": {key: {"label": "Art. 15", "kind": "art", "text": after}}})
    if RULING in part["laws"]:
        raise SystemExit(f"{RULING} already a law of the part")
    part["laws"][RULING] = {"label": "Sentencia C-273 de 1998", "title": "Corte Constitucional, Sentencia C-273 de 1998",
                            "kind": "court", "enacted": RDAY, "published": None, "url": E.BASE + "c-273_1998.html",
                            "temporary_until": None, "restores": None, "note": None}
    part["decisions"].append(
        f"Violencia intrafamiliar (Ley 294 de 1996), {MARK}: arts. 7, 9, 11, 12 and 14-18 read as their earlier-text boxes "
        "'El texto original de la Ley 294 de 1996' give them from 22 July 1996, until Ley 575 de 2000 (arts. 4-12) rewrote "
        "them on 11 February 2000 (the engine reads only box headings that start 'Texto', so these articles had been absent "
        "before 2000). Art. 15 without the words its box shows struck from 3 June 1998, credited to Sentencia C-273 de 1998 "
        "('Apartes subrayados del texto original declarados INEXEQUIBLES ...'; the rest upheld on a condition), as the box "
        "prints it: the word 'excepto' is not struck there, so it stays. Art. 9's original words were upheld by C-652-97 "
        "(plain EXEQUIBLE, no change). Arts. 5 and 6's original texts are left as they were (art. 5 placeholder before 2000; "
        "art. 6, which the page prints only inside art. 5's box, is in no version).")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "applied:", ", ".join(str(n) for n in ARTS), f"+ {RULING} version {RDAY}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "corpus.d"))
