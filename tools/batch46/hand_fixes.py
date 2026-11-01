"""Hand-set histories for batch 46 (imported by parse_batch46.py; each checks the page before it changes anything)."""
from __future__ import annotations

D = B23 = B29 = B13 = B7 = E = P = struck = L2150 = L43 = None


def _timeline(act, key):
    """The unit's history as set_history's timeline [(day or None, text or None, law)] (one law per change)."""
    out = []
    for i, (day, u, cr) in enumerate(struck.history(act, key)):
        B23._need(cr is None or len(cr) == 1, f"{act['slug']} {key} credits {cr}")
        text = None if u is None else "\n".join(u["text"].split("\n")[1:-1])
        out.append((None if i == 0 else day, text, cr[0] if cr else None))
    return out


def _done(title, fn):
    B29.HAND_DONE.append(f"{title}: " + " ".join(fn.__doc__.split()))


T2150 = "Supresión y reforma de regulaciones, procedimientos o trámites innecesarios (Decreto Ley 2150 de 1995)"
T43 = "Nacionalidad colombiana (Ley 43 de 1993)"


def fix_43_38(act):
    """Ley 43 de 1993, art. 38: Decreto 286 de 1993 (Diario Oficial No. 40.745 of 10 February 1993, in force on
    publication, its art. 3), art. 2, corrected the article 'en el sentido de que la ley que deroga es la Ley 145 de 1888 y
    no la Ley 145 de 1988, como allí aparece'. The page prints the corrected words; until the decree's day the article
    reads 'las Leyes 145 de 1988 y 22 Bis de 1936', as the decree says it appeared (the engine had a placeholder)."""
    B23._need(B7.B3.article_text(P.doc_units("decreto_0286_1993"), "2").startswith(
        "Corrígese el artículo 38 de la Ley 43 de 1993 en el sentido de que la ley que deroga es la Ley 145 de 1888 y no la "
        "Ley 145 de 1988, como allí aparece"), "Decreto 286 de 1993 art. 2")
    t = _timeline(act, "art-0038")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("1993-02-10", "dec-286-1993")]
              and t[0][1] == E.MISSING_LINE and t[1][1].count("Leyes 145 de 1888 ") == 1, f"Ley 43 art. 38 {t}")
    t[0] = (None, t[1][1].replace("Leyes 145 de 1888 ", "Leyes 145 de 1988 "), None)
    B13.B6.set_history(act, "art-0038", "Art. 38", t)
    B23._forget(L43, "art-0038")
    _done(T43, fix_43_38)


def fix_2150_82(act):
    """Decreto Ley 2150 de 1995, art. 82: the page gives the article's original text and the text after Ley 962 de 2005
    art. 36 rewrote its parágrafo, both without the epigraph the page's heading gives ('EXPEDICIÓN DEL CERTIFICADO.', put
    back in both); Decreto 19 de 2012 art. 92 repealed it. History: the original text from the decree's first day (the
    engine had a placeholder), Ley 962's text from 2005-07-08, gone from 2012-01-10."""
    u = B23._unit(L2150, "82")
    box = B23._boxes(u, "Legislación Anterior")[0]
    blk = [b for b in E.la_blocks(box) if b["head"].rstrip(" :") == "Texto original del Decreto 2150 de 1995"]
    B23._need(len(blk) == 1, "D2150 art. 82 original block")
    orig = E.block_text(blk[0]["paras"], True)
    B23._need(orig[0].startswith("El Certificado de Carencia de Informes") and orig[-1].startswith(
        "PARÁGRAFO. En ningún caso se solicitará"), f"D2150 art. 82 box {orig[:1]}")
    t = _timeline(act, "art-0082")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("2005-07-08", "ley-962-2005"), ("2012-01-10", "dec-19-2012")]
              and t[0][1] == E.MISSING_LINE, f"D2150 art. 82 {[(d, l) for d, _, l in t]}")
    epi = "EXPEDICIÓN DEL CERTIFICADO. "
    B23._need(t[1][1].startswith("El Certificado de Carencia de Informes"), "D2150 art. 82 Ley 962 text")
    t[0] = (None, "\n".join([epi + orig[0]] + orig[1:]), None)
    t[1] = (t[1][0], epi + t[1][1], t[1][2])
    B13.B6.set_history(act, "art-0082", "Art. 82", t)
    B23._forget(L2150, "art-0082")
    _done(T2150, fix_2150_82)


def fix_2150_102(act):
    """Decreto Ley 2150 de 1995, art. 102: Ley 964 de 2005 art. 75 repealed 'el inciso primero del artículo 102'; the page
    prints the whole article with the marker '<Inciso 1o. derogado por el Artículo 75 de la Ley 964 de 2005, el texto
    original del inciso es el siguiente:>' at the start of its first paragraph ('Sustituir los artículos 3o. y 4o. del
    Decreto 1169 de 1980 por el siguiente texto:'). History: the whole text from the decree's first day (the engine had a
    placeholder); that first paragraph, where the page puts the marker, gone from Ley 964's promulgation (2005-07-08,
    its art. 86)."""
    t = _timeline(act, "art-0102")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("2005-07-08", "ley-964-2005")] and t[0][1] == E.MISSING_LINE,
              f"D2150 art. 102 {[(d, l) for d, _, l in t]}")
    whole = t[1][1].split("\n")
    epi = "FACULTADES DE SALA GENERAL. "
    B23._need(whole[0] == epi + "Sustituir los artículos 3o. y 4o. del Decreto 1169 de 1980 por el siguiente texto:"
              and len(whole) == 3, f"D2150 art. 102 text {whole}")
    B13.B6.set_history(act, "art-0102", "Art. 102", [(None, "\n".join(whole), None),
                                                     ("2005-07-08", "\n".join([epi + whole[1]] + whole[2:]), "ley-964-2005")])
    B23._forget(L2150, "art-0102")
    _done(T2150, fix_2150_102)


LATE_2150 = [str(n) for n in list(range(40, 46)) + list(range(143, 149))]


def late_2150(act):
    """Decreto Ley 2150 de 1995, art. 152: Título I Capítulo II (arts. 40-45) and Título II Capítulo XV (arts. 143-148)
    took effect three months after publication: those articles are absent before that day and added on it, credited to
    the decree."""
    units = P.doc_units(L2150)
    names = [u["name"] for u in units[1:]]
    labels = {u["name"]: (u["label"] or "") for u in units[1:]}
    for first, last, head, cap in (("40", "45", "Nivel003", "CAPÍTULO II"), ("143", "148", "Nivel023", "CAPÍTULO XV")):
        i = names.index(head)
        B23._need(labels[head].startswith(cap + ".") and names[i + 1] == first
                  and names[names.index(last) + 1].startswith("Nivel"), f"D2150 chapter {head} {labels[head]}")
    day = E.add_months(act["versions"][0]["from"], 3)
    vs = act["versions"]
    if not any(v["from"] == day for v in vs):
        k = next(i for i, v in enumerate(vs) if v["from"] > day)
        prev = next(v for v in reversed(vs[:k]) if "units" in v)
        vs.insert(k, {"from": day, "units": dict(prev["units"]), "credits": {}, "source_url": prev["source_url"],
                      "sha256": prev["sha256"]})
    for num in LATE_2150:
        key = E.unit_key(num)[0]
        B23._need(all(not v["credits"].get(key) for v in vs if v["from"] <= day), f"D2150 {key} change before {day}")
        for v in vs:
            if v["from"] < day and "units" in v:
                B23._need(key in v["units"], f"D2150 {key} missing")
                v["units"] = {k: x for k, x in v["units"].items() if k != key}
            elif v["from"] == day:
                v["credits"][key] = ["dec-2150-1995"]
    B29.HAND_DONE.append(f"{T2150}: " + " ".join(late_2150.__doc__.split()) + f" ({day}).")


def note_2150_97(act):
    """Decreto Ley 2150 de 1995, art. 97: Sentencia C-847-99 (27 October 1999) declared the words 'y 11 de la Ley 57 de
    1985' (the repeal of that article) partly INEXEQUIBLE: the repeal stands only for one segment of art. 11 of Ley 57 de
    1985. The words stay in the text, so no version changes them."""
    u = B23._unit(L2150, "97")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("parcialmente INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-847-99 del 27 de octubre de 1999"
              in jv, "D2150 art. 97 ruling")
    B23._need(all(cr is None for _, _, cr in struck.history(act, "art-0097")), "D2150 art. 97 history")
    B23._forget(L2150, "art-0097")
    _done(T2150, note_2150_97)


def note_43_28(act):
    """Ley 43 de 1993, art. 28: Decreto 286 de 1993, art. 1, corrected the Constitution's article numbers cited in
    numerals 1, 4 and 6 ('son el 191, el 249 y el 267'); the page prints the numbers as first published (numeral 1 cites
    two articles, 192 and 204) with the correction only in notes, so the correction is not applied to the words."""
    B23._need(B7.B3.article_text(P.doc_units("decreto_0286_1993"), "1").startswith(
        "Corrígese el artículo 28 de la Ley 43 de 1993 en el sentido de que los artículos citados en los numerales 1, 4 y 6 "
        "son el 191, el 249 y el 267"), "Decreto 286 de 1993 art. 1")
    B23._need(all(not cr or cr == ["ley-2332-2023"] for _, _, cr in struck.history(act, "art-0028")), "Ley 43 art. 28")
    _done(T43, note_43_28)


def fix_43(act):
    D.fix_43_struck(act)
    fix_43_38(act)
    note_43_28(act)


def fix_2150(act):
    fix_2150_82(act)
    fix_2150_102(act)
    late_2150(act)
    note_2150_97(act)


def install(driver):
    """Bind the driver's modules and register the fixes (called once by parse_batch46.py)."""
    global D, B23, B29, B13, B7, E, P, struck, L2150, L43
    D = driver
    B23, B29, B13, B7, E, P, struck = D.B23, D.B29, D.B13, D.B7, D.E, D.P, D.struck
    L2150, L43 = D.L2150, D.L43
    E.HAND_RULES["ley-964-2005"] = ("pub", "Ley 964 de 2005, art. 86: 'La presente ley entrará a regir a partir de su "
                                           "promulgación, con excepción de ...' (the exceptions do not cover art. 75's "
                                           "repeals other than inciso 1 of its parágrafo 5)")
    B29.HAND_FIXES.update({"nacionalidad-1993": fix_43, "supresion-de-tramites-1995": fix_2150})
