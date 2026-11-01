"""Hand-set histories for batch 85 (Ley 938 de 2004), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L938, T938 = "ley_0938_2004", "Estatuto Orgánico de la Fiscalía General de la Nación (Ley 938 de 2004)"
ORIG = "Texto original de la Ley 938 de"   # art. 78's box is headed '... de 2008' (a slip; see HEADING_FIXES_58)
# A row of the staffing tables the earlier-text boxes type out as bold paragraphs ('ASESOR I<tabs>3', 'TOTAL 17.928',
# 'Propuesta de nominaciones Planta 2006'); tables are left out everywhere in this record.
ROW = re.compile(r"^\s*<span class='b_aj'>[^<]*</span>\s*$|\t")


def _orig_block(u):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        for blk in H.E.la_blocks(b):
            if blk["head"].startswith(ORIG):
                return blk
    H.B23._need(False, f"art. {u['label']}: no '{ORIG} ...' box")


def _lines(paras, keep_struck):
    """block_text with or without the struck words; table rows left out."""
    E, out = H.E, []
    for i, ph in enumerate(paras):
        if ROW.search(ph):
            continue
        t = E.tidy(E.to_text(ph, keep_struck))
        if i == 0:
            t = E.tidy(E.ART_HEAD.sub("", t, count=1))
        if t and not re.fullmatch(r"\(?\.\.\.\)?", t):
            out.append(t)
    return out


def fix_938_c878(act):
    """arts. 56, 60, 62, 65, 66 and 71: Sentencia C-878 de 2008 (10 September 2008) struck words the page shows only inside
    the articles' earlier-text boxes ('<Aparte tachado INEXEQUIBLE>', the words struck through), as the Jurisprudencia
    Vigencia box of each says. Each article reads as enacted (the box's words, the struck ones included) until the ruling,
    then without the struck words, until Decreto 20 de 2014 repealed it (9 January 2014). The engine had put the
    placeholder line after the ruling."""
    B23 = H.B23
    for n in ("56", "60", "62", "65", "66", "71"):
        u = B23._unit(L938, n)
        jv = H._jv(u)
        B23._need("Sentencia C-878-08 de 10 de septiembre de 2008" in jv and "INEXEQUIBLE" in jv, f"L938 art. {n} JV")
        blk = _orig_block(u)
        B23._need(blk["head"].startswith("Texto original de la Ley 938 de 2004"), f"L938 art. {n} box head")
        B23._need(any(re.search(r"<s\b", p, re.I) for p in blk["paras"]), f"L938 art. {n} struck words")
        full, cut = _lines(blk["paras"], True), _lines(blk["paras"], False)
        B23._need(full != cut, f"L938 art. {n} strike")
        key = f"art-{int(n):04d}"
        h = H._hist(act, key)
        B23._need([(d, c) for d, _, c in h] == [("2004-12-31", None), ("2008-09-10", ["c-878-08"]),
                                                   ("2014-01-09", ["dec-20-2014"])], f"L938 art. {n} {H._shape(h)}")
        B23._need(h[0][1] == full and h[1][1] == [H.PH], f"L938 art. {n} texts")
        H._set(act, key, H._label(act, key), [(None, full, None), ("2008-09-10", cut, "c-878-08"),
                                              ("2014-01-09", None, "dec-20-2014")])
        B23._forget(L938, key)
    H._done(T938, fix_938_c878)


def fix_938_9(act):
    """art. 9: its earlier-text box shows the word 'institucional' struck ('<Aparte tachado INEXEQUIBLE>'), but the only
    ruling its Jurisprudencia Vigencia box names on this act is Sentencia C-166 de 2014 (19 March 2014, 'estarse a lo
    resuelto en la Sentencia C-037-96'; C-037 de 1996 reviewed the bill of Ley 270 de 1996, before this act existed). The
    article was repealed by Decreto 16 de 2014 on 9 January 2014, before that ruling, so its enacted words, the struck
    word included, stand for its whole life; the ruling changes no words in this record."""
    B23 = H.B23
    u = B23._unit(L938, "9")
    jv = H._jv(u)
    B23._need("mediante Sentencia C-166-14 de 19 de marzo de 2014" in jv and "Sentencia C-037-96 de 5 de febrero de 1996" in jv
              and "Proyecto de Ley 58/94 Senado" in jv, "L938 art. 9 JV")
    blk = _orig_block(u)
    full, cut = _lines(blk["paras"], True), _lines(blk["paras"], False)
    B23._need(full == ["El Fiscal General de la Nación es elegido para un período institucional de cuatro (4) años."]
              and cut == ["El Fiscal General de la Nación es elegido para un período de cuatro (4) años."], "L938 art. 9 box")
    key = "art-0009"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2004-12-31", None), ("2014-01-09", ["dec-16-2014"])], f"L938 art. 9 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, full, None), ("2014-01-09", None, "dec-16-2014")])
    B23._forget(L938, key)
    H._done(T938, fix_938_9)


def fix_938_78(act):
    """art. 78 and art. transitorio 1 (staffing plans): art. 78 reads as enacted ('Establece la siguiente planta de cargos
    ... a partir del primero (1) de enero de 2009:', the earlier-text box; the table of posts left out, as tables are
    everywhere) until Decreto 122 de 2008 art. 5 repealed it (18 January 2008). Art. transitorio 1 reads as enacted (today's
    words plus the box's sentences for the plans of 2006, 2007 and 2008, tables left out) until the same article repealed
    those plans; today's words from that day. Ley 1024 de 2006 art. 7 suspended arts. 78 and transitorios 1 and 2 for five
    years from its promulgation (20 May 2006), which changed no words: the version of that day says so in its note. Decreto
    122 de 2008 also repealed that art. 7."""
    B23 = H.B23
    u = B23._unit(L938, "78")
    nv = H._nv(u)
    B23._need("Artículo derogado por el artículo 5 del Decreto 122 de 2008" in nv and "Suspéndase por el término de cinco (5) "
              "años, contados a partir de la promulgación de la presente ley, la aplicación de los artículos 78 y los "
              "transitorios 1o y 2o de la Ley 938 de 2004" in nv, "L938 art. 78 NV")
    blk = _orig_block(u)
    old78 = _lines(blk["paras"], True)
    B23._need(old78 == ["Establece la siguiente planta de cargos para la Fiscalía General de la Nación a partir del primero "
                        "(1) de enero de 2009:"], f"L938 art. 78 box {old78[:3]}")
    key = "art-0078"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2004-12-31", None), ("2008-01-18", ["dec-122-2008"])], f"L938 art. 78 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, old78, None), ("2008-01-18", None, "dec-122-2008")])
    B23._forget(L938, key)

    t = next(x for x in H.P.doc_units(L938)[1:] if (x["label"] or "").startswith("ARTÍCULO TRANSITORIO 1."))
    nv = H._nv(t)
    B23._need("Referencias a la disminución gradual de la planta de personal años 206, 207, 2008 derogados por el artículo "
              "5 del Decreto 122 de 2008" in nv, "L938 art. T1 NV")
    blk = _orig_block(t)
    add = _lines(blk["paras"], True)
    B23._need(add == ["A partir del 1o de enero de 2006, se tendrá la siguiente planta de cargos en el año 2006.",
                      "A partir del 1o de enero de 2007, se tendrá la siguiente planta de cargos.",
                      "La siguiente planta de cargos se establece para la Fiscalía General de la Nación a partir del 1o de "
                      "enero de 2008."], f"L938 art. T1 box {add}")
    key = "art-transitorio-1"
    h = H._hist(act, key)
    B23._need(len(h) == 1, f"L938 art. T1 {H._shape(h)}")
    today = h[0][1]
    B23._need(today[-1] == "A partir del primero de enero de 2005 se tendrá la siguiente planta de cargos:", f"L938 T1 {today}")
    H._set(act, key, H._label(act, key), [(None, today + add, None), ("2008-01-18", today, "dec-122-2008")])
    B23._forget(L938, key)
    H.E.REPORT[:] = [r for r in H.E.REPORT if not r.startswith(f"{L938} {key}:")]

    v = [x for x in act["versions"] if x["from"] == "2006-05-20"]
    B23._need(len(v) == 1, "L938 Ley 1024 version")
    v[0]["note"] = ("Ley 1024 de 2006, art. 7, suspended articles 78 and transitorios 1 and 2 for five years from its "
                    "promulgation (20 May 2006); their words stay in the text. Decreto 122 de 2008 repealed that art. 7, "
                    "art. 78 and the 2006-2008 plans of art. transitorio 1.")
    H._done(T938, fix_938_78)


def fix_938_dec16(act):
    """arts. 1 to 32: Decreto 16 de 2014 art. 51 repealed them from its publication (9 January 2014) but kept the
    functions they gave the Fiscalía's offices 'hasta tanto se adopte la nueva planta de personal' (the Notas de Vigencia
    quote it); that keeps functions, not the articles' words, so they leave the text on 9 January 2014. No change."""
    B23 = H.B23
    for n in ("1", "9", "32"):
        nv = H._nv(B23._unit(L938, n))
        B23._need("derogado por el artículo 51 del Decreto 16 de 2014" in nv and "continuarán vigentes hasta tanto se adopte "
                  "la nueva planta de personal" in nv, f"L938 art. {n} NV")
    h = H._hist(act, "art-0001")
    B23._need([(d, c) for d, _, c in h][-1] == ("2014-01-09", ["dec-16-2014"]), "L938 art. 1 repeal day")
    H._done(T938, fix_938_dec16)


H.FIXES["estatuto-organico-fiscalia-2004"] = [fix_938_c878, fix_938_9, fix_938_78, fix_938_dec16]
