"""Hand-set histories for batch 114 (Leyes 721/2001, 979/2005, 2089/2021), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None

L721, T721, S721 = "ley_0721_2001", "Pruebas de ADN en los procesos de filiación (Ley 721 de 2001)", "pruebas-de-adn-en-filiacion"
L979, T979, S979 = "ley_0979_2005", "Reforma de la unión marital de hecho (Ley 979 de 2005)", "union-marital-de-hecho-2005"
PH = H.PH
COND = ("A Constitutional Court ruling that upheld this text on a condition of interpretation (exequibilidad "
        "condicionada). It did not change the words.")


def _need(c, what):
    H.B23._need(c, what)


def _orig_block(u, head):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        for blk in H.E.la_blocks(b):
            if blk["head"].startswith(head):
                return blk
    _need(False, f"art. {u['label']}: no '{head} ...' box")


def _box_lines(paras, keep_struck):
    """An earlier-text block's lines with or without the struck words (hf93._box_lines), the 'ARTÍCULO N.' head cut."""
    E, out = H.E, []
    for i, ph in enumerate(paras):
        t = E.tidy(E.to_text(ph, keep_struck))
        if i == 0:
            t = E.tidy(E.ART_HEAD.sub("", t, count=1))
        if t and re.search(r"\w", t):
            out.append(t)
    return out


def fix_721_4(act):
    """art. 4: Sentencia C-807-02 (3 October 2002) struck the words 'en caso de no asumirlo no se decretará la prueba'
    of the second inciso (the rest of that inciso upheld on a condition), which the page shows struck only inside the
    article's 'Texto original de la Ley 721 de 2001' box (Ley 1395 de 2010 art. 44 repealed the article on 12 July 2010).
    As for Ley 793 de 2002 (hf93.fix_793_c740), the article reads as enacted until the ruling, then without the struck
    words until the repeal. The engine had put the placeholder in it from the ruling's day."""
    u = H.B23._unit(L721, "4")
    _need("C-807-02 de 3 de octubre de 2002" in H._jv(u) and "INEXEQUIBLE" in H._jv(u), "L721 art. 4 JV")
    blk = _orig_block(u, "Texto original de la Ley 721 de 2001")
    full, cut = _box_lines(blk["paras"], True), _box_lines(blk["paras"], False)
    _need(full != cut and len(full) == len(cut) and any("en caso de no asumirlo" in l for l in full), "L721 art. 4 strike")
    key = "art-0004"
    h = H._hist(act, key)
    _need(len(h) == 3 and h[0][0] == "2001-12-29" and h[0][1] == full and h[1][0] == "2002-10-03"
          and h[1][2] == ["c-807-02"] and h[1][1] == [PH] and h[2][0] == "2010-07-12" and h[2][1] is None
          and h[2][2] == ["ley-1395-2010"], f"L721 art. 4 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, full, None), ("2002-10-03", cut, "c-807-02"),
                                         ("2010-07-12", None, "ley-1395-2010")])
    H.B23._forget(L721, key)
    H._done(T721, fix_721_4)


def fix_721_8(act):
    """art. 8 (art. 14 de la Ley 75 de 1968 as rewritten): the page prints the article repealed by Ley 1564 de 2012 art.
    626 lit. c) from 1 January 2014 and gives its earlier text in a 'Texto original de la Ley 721 de 2001' box, where
    incisos 1 and 2 and parágrafo 3 carry '<Inciso/Parágrafo derogado por el artículo 44 de la Ley 1395 de 2010>' (the
    Notas de Vigencia box says the same; Ley 1395 de 2010 in force 12 July 2010). Those three leave on 12 July 2010,
    credited to Ley 1395 de 2010; the rest stands until 1 January 2014. Inciso 2 also carries '<Inciso CONDICIONALMENTE
    exequible>' (Sentencia C-476-05 of 10 May 2005, in a rulings paragraph with C-808-02, so the engine skipped it): it is
    credited on its day as a conditional ruling that changed no words. The engine had kept all six paragraphs to 2014."""
    u = H.B23._unit(L721, "8")
    nv, jv = " ".join(H._nv(u).split()), " ".join(H._jv(u).split())
    _need("Incisos 1o. y 2o. y parágrafo 3o. derogados por el artículo 44 de la Ley 1395 de 2010" in nv, "L721 art. 8 NV")
    _need("Inciso 2o. declarado EXEQUIBLE, en los términos expuestos en el numeral 5 de la parte motiva de la sentencia, por "
          "la Corte Constitucional mediante Sentencia C-476-05 de 10 de mayo de 2005" in jv, "L721 art. 8 JV")
    blk = _orig_block(u, "Texto original de la Ley 721 de 2001")
    raw = [H.E.plain(p) for p in blk["paras"]]
    _need(len(raw) == 6 and "Inciso derogado por el artículo 44 de la Ley 1395" in raw[1]
          and "Inciso derogado por el artículo 44 de la Ley 1395" in raw[2] and "CONDICIONALMENTE" in raw[2]
          and "Parágrafo derogado por el artículo 44 de la Ley 1395" in raw[5], "L721 art. 8 box markers")
    full = _box_lines(blk["paras"], True)
    key = "art-0008"
    h = H._hist(act, key)
    _need(len(h) == 2 and h[0][0] == "2001-12-29" and h[0][1] == full and len(full) == 6 and h[1][0] == "2014-01-01"
          and h[1][1] is None and h[1][2] == ["ley-1564-2012"], f"L721 art. 8 {H._shape(h)}")
    c = H.E.add_court("C-476-05", "2005-05-10", "c-476_2005.html", COND)
    _need(c == "c-476-05", f"C-476-05 key {c}")
    H._set(act, key, H._label(act, key), [(None, full, None), ("2005-05-10", full, c),
                                         ("2010-07-12", [full[0], full[3], full[4]], "ley-1395-2010"),
                                         ("2014-01-01", None, "ley-1564-2012")])
    H.B23._forget(L721, key)
    H._done(T721, fix_721_8)


def fix_979_1(act):
    """art. 1 (art. 2 de la Ley 54 de 1990 as rewritten), literal b): the page shows two struck asides in one paragraph,
    'y liquidadas' (Sentencia C-700-13 of 16 October 2013) and 'por lo menos un año' (Sentencia C-193-16 of 20 April
    2016), each dated in the Jurisprudencia Vigencia box; the engine credited both to the later ruling. Each leaves on its
    own ruling's day (struck words stand until the dated ruling)."""
    u = H.B23._unit(L979, "1")
    jv = " ".join(H._jv(u).split())
    _need("Aparte tachado 'y liquidadas' declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-700-13 de "
          "16 de octubre de 2013" in jv and "Aparte tachado 'por lo menos un año' declarado INEXEQUIBLE" in jv
          and "C-193-16 de 20 de abril de 2016" in jv, "L979 art. 1 JV")
    key = "art-0001"
    h = H._hist(act, key)
    _need([(d, c) for d, _, c in h] == [("2005-07-27", None), ("2016-04-20", ["c-193-16"])], f"L979 art. 1 {H._shape(h)}")
    a, b = h[0][1], h[1][1]
    OLD = "hayan sido disueltas y liquidadas por lo menos un año antes de la fecha"
    _need(sum(OLD in l for l in a) == 1 and sum("hayan sido disueltas antes de la fecha" in l for l in b) == 1, "L979 b)")
    mid = [l.replace(OLD, "hayan sido disueltas por lo menos un año antes de la fecha") for l in a]
    _need([l.replace(" por lo menos un año", "") for l in mid] == b, "L979 art. 1 mid")
    # C-075-07 (conditional, all of Ley 54 as amended) is a version of its own the engine made: keep it.
    vs = [v["from"] for v in act["versions"] if v["credits"].get(key)]
    _need(vs == ["2007-02-07", "2016-04-20"], f"L979 art. 1 credits {vs}")
    c = H.E.add_court("C-700-13", "2013-10-16", "c-700_2013.html")
    _need(c == "c-700-13", f"C-700-13 key {c}")
    H._set(act, key, H._label(act, key), [(None, a, None), ("2007-02-07", a, "c-075-07"), ("2013-10-16", mid, c),
                                         ("2016-04-20", b, "c-193-16")])
    H.B23._forget(L979, key)
    H._done(T979, fix_979_1)


H.FIXES[S721] = [fix_721_4, fix_721_8]
H.FIXES[S979] = [fix_979_1]
