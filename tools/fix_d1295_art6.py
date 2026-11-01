"""Patch corpus.d/99z-batch34.json in place: Decreto Ley 1295 de 1994 art. 6 read with phase2/struck.py.

The page prints the article's original 1994 text as today's (it revived when Sentencia C-1316-00 struck Decreto 266 de
2000 as a whole on 26 September 2000), notes that Decreto 266 de 2000 art. 99 rewrote it, and gives that decree's article
in its earlier-text box ('Modifícase el artículo 6o. ... el cual quedará así: 'Artículo 6. ...''). The part had a
placeholder from 1994 and the today's text credited to Decreto 266 from 2000-02-22. History now: the original text from
the decree's first day; the wording Decreto 266 quoted, from 2000-02-22; the original again from 2000-09-26, credited to
C-1316-00. Idempotent (does nothing once the decision line is there); checks the page first.
RE-RUN after any re-parse of batch 34 that does not apply it.
Usage: python -X utf8 fix_d1295_art6.py
"""
import json
import os
import sys

C = os.path.dirname(os.path.abspath(__file__))
PART = os.path.join(C, "corpus.d", "99z-batch34.json")
SLUG, KEY = "sistema-general-de-riesgos-profesionales", "art-0006"
TITLE = "Sistema General de Riesgos Profesionales (Decreto Ley 1295 de 1994)"
MARK = "art. 6 (struck-decree reading, 2026-10-31)"
DECISION = (f"{TITLE}, {MARK}: the page prints the article's original 1994 text as today's (it revived when Sentencia "
            "C-1316-00 of 26 September 2000 struck Decreto 266 de 2000 as a whole) and gives in its earlier-text box the "
            "decree's art. 99, which rewrote the article ('Modifícase el artículo 6o. ... el cual quedará así: ...'). "
            "History: the original text from the decree's first day; the wording Decreto 266 quoted from 2000-02-22; the "
            "original again from 2000-09-26, credited to C-1316-00 (that ruling gave its effect from the decree's "
            "promulgation; the wording is still shown for the months it was applied).")
OLD = f"{TITLE}, art. 6: the page prints as today's text the wording Decreto 266 de 2000"
# the same record as the other parts give this ruling (97-batch6, 99c, 99h, 99o)
C1316 = {"label": "Sentencia C-1316 de 2000", "title": "Corte Constitucional, Sentencia C-1316 de 2000", "kind": "court",
         "enacted": "2000-09-26", "published": None, "url": "http://www.secretariasenado.gov.co/senado/basedoc/c-1316_2000.html",
         "temporary_until": None, "restores": None, "note": None}


def main():
    part = json.load(open(PART, encoding="utf-8"))
    if any(MARK in d for d in part["decisions"]):
        print("already applied")
        return
    sys.argv = [sys.argv[0], "x", "x"]
    exec(open(os.path.join(C, "batch45", "show.py"), encoding="utf-8").read().split("page, name")[0], globals())
    import parse_phase2 as P2
    import struck
    u = next(x for x in P.doc_units("decreto_1295_1994")[1:] if E.label_num(x["label"] or "") == "6")  # noqa: F821
    nv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas de Vigencia")  # noqa: F821
    jv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")  # noqa: F821
    assert "Artículo modificado por el artículo 99 del Decreto 266 de 2000" in nv, nv
    assert struck.DECREES["Decreto 266 de 2000"].search(jv), jv
    box = next(it[2] for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior")
    blk = [b for b in E.la_blocks(box) if b["head"].startswith("Texto del Decreto 266 de 2000")]  # noqa: F821
    assert len(blk) == 1
    lines = E.block_text(blk[0]["paras"], True)  # noqa: F821
    head = "RECLAMACIONES. Modifícase el artículo 6o. del Decreto Ley 1295 de 1994, el cual quedará así:"
    assert lines[0] == head and lines[1].startswith("'Artículo 6. Prestación de los servicios de salud.") \
        and lines[-1].endswith("'"), lines[:2]
    new = [lines[1][len("'Artículo 6. "):]] + lines[2:-1] + [lines[-1][:-1]]
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = P2.full_versions(act["versions"])
    hist = [(v["from"], v["units"].get(KEY), v["credits"].get(KEY)) for v in vs]
    changes = [(d, cr) for d, u, cr in hist if cr]
    assert changes == [("2000-02-22", ["dec-266-2000"])], changes
    today = vs[-1]["units"][KEY]
    assert "[La fuente no da" in vs[0]["units"][KEY]["text"] and "Corresponde a las Administradoras" not in today["text"]
    for v in vs:
        if v["from"] < "2000-02-22":
            v["units"] = dict(v["units"], **{KEY: today})
    for v in vs:
        if v["from"] == "2000-02-22":
            v["credits"].pop(KEY)
    act["versions"] = vs
    part["laws"].setdefault("c-1316-00", C1316)
    sys.path.insert(0, os.path.join(C, "phase2"))
    struck.respan(act, KEY, [("dec-266-2000", "2000-02-22", "c-1316-00", "2000-09-26", new)],
                  "[La fuente no da el texto vigente en esta fecha.]")
    # versions that changed no words keep no units (to_deltas keeps the first full and writes changes after it)
    act["versions"] = P2.to_deltas(act["versions"])
    part["decisions"] = [DECISION if d.startswith(OLD) else d for d in part["decisions"]]
    if DECISION not in part["decisions"]:
        part["decisions"].append(DECISION)
    with open(PART + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(PART + ".tmp", PART)
    print("patched", PART)


if __name__ == "__main__":
    main()
