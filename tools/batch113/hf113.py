"""Hand-set histories for batch 113 (Leyes 1843/2017, 1259/2008, 1918/2018), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None

L1259, T1259, S1259 = "ley_1259_2008", "Comparendo ambiental (Ley 1259 de 2008)", "comparendo-ambiental"
L1918, T1918, S1918 = "ley_1918_2018", "Inhabilidades por delitos sexuales contra menores (Ley 1918 de 2018)", \
    "inhabilidades-por-delitos-sexuales-contra-menores"
PH = H.PH


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


def fix_1259_7(act):
    """art. 7: Sentencia C-928-09 (10 December 2009) struck the last sentence of numeral 6 ('Si el desacato persiste en
    grado extremo, cometiéndose reiteradamente la falta, las sanciones antes enumeradas pueden convertirse en arresto'),
    which the page shows struck only inside the article's 'Texto original de la Ley 1259 de 2008' box (the article itself
    was repealed by Ley 1801 de 2016 art. 242 from 29 January 2017). As for Ley 793 de 2002 (hf93.fix_793_c740), the
    article reads as enacted (the box's words, the struck ones included) until the ruling, then without the struck words,
    until the repeal. The engine had put the placeholder in it from the ruling's day."""
    u = H.B23._unit(L1259, "7")
    _need("C-928-09 de 10 de diciembre de 2009" in H._jv(u) and "INEXEQUIBLE" in H._jv(u), "L1259 art. 7 JV")
    blk = _orig_block(u, "Texto original de la Ley 1259 de 2008")
    full, cut = _box_lines(blk["paras"], True), _box_lines(blk["paras"], False)
    _need(full != cut and len(full) == len(cut), "L1259 art. 7 strike")
    _need(any(l.endswith("pueden convertirse en arresto.") for l in full), "L1259 art. 7 struck words")
    key = "art-0007"
    h = H._hist(act, key)
    _need(len(h) == 3 and h[0][0] == "2008-12-19" and h[0][1] == full and h[1][0] == "2009-12-10"
          and h[1][2] == ["c-928-09"] and h[1][1] == [PH] and h[2][0] == "2017-01-29" and h[2][1] is None
          and h[2][2] == ["ley-1801-2016"], f"L1259 art. 7 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, full, None), ("2009-12-10", cut, "c-928-09"),
                                         ("2017-01-29", None, "ley-1801-2016")])
    H.B23._forget(L1259, key)
    H._done(T1259, fix_1259_7)


def fix_1918_2(act):
    """art. 2: Sentencia C-407-20 (16 September 2020) declared the original article INEXEQUIBLE ('Artículo original
    declarado INEXEQUIBLE', its Jurisprudencia Vigencia box); Ley 2375 de 2024 art. 3 then added a new article 2 (from 12
    July 2024, its note: 'Rige a partir de su publicación'). The article reads as the page's 'Texto original de la Ley 1918
    de 2018' box gives it until the ruling, is out from the ruling's day, and reads Ley 2375's text from 12 July 2024. The
    engine had kept the original text in force until 2024."""
    u = H.B23._unit(L1918, "2")
    jv = H._jv(u)
    _need("Artículo original declarado INEXEQUIBLE" in jv and "C-407-20 de 16 de septiembre de 2020" in jv,
          "L1918 art. 2 JV")
    blk = _orig_block(u, "Texto original de la Ley 1918 de 2018")
    orig = _box_lines(blk["paras"], True)
    key = "art-0002"
    h = H._hist(act, key)
    _need(len(h) == 2 and h[0][0] == "2018-07-12" and h[0][1] == orig and h[1][0] == "2024-07-12"
          and h[1][2] == ["ley-2375-2024"], f"L1918 art. 2 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, orig, None), ("2020-09-16", None, "c-407-20"),
                                         ("2024-07-12", h[1][1], "ley-2375-2024")])
    H.B23._forget(L1918, key)
    H._done(T1918, fix_1918_2)


def fix_1918_5(act):
    """art. 5: Ley 2375 de 2024 art. 4 rewrote it from 12 July 2024 (its note: 'Rige a partir de su publicación'); the new
    PARÁGRAFO TRANSITORIO gives the Ministerio de Defensa up to six months from the act's promulgation to update the
    register, 'Fecha en la cual empezará a regir lo dispuesto en el presente artículo'. That day is not a fixed date
    (it depends on the update) and changes no words: the text stands from 12 July 2024, as the note dates it, with
    Decreto 1110 de 2024 art. 2's correction ('Ley 1918 de 2019' -> 'Ley 1918 de 2018') from 30 August 2024."""
    u = H.B23._unit(L1918, "5")
    _need("Fecha en la cual empezará a regir lo dispuesto en el presente artículo" in " ".join(H._printed(u)),
          "L1918 art. 5 parágrafo transitorio")
    h = H._hist(act, "art-0005")
    _need([(d, c) for d, _, c in h] == [("2018-07-12", None), ("2024-07-12", ["ley-2375-2024"]),
                                         ("2024-08-30", ["dec-1110-2024"])], f"L1918 art. 5 {H._shape(h)}")
    _need("Ley 1918 de 2019" in " ".join(h[1][1]) and "Ley 1918 de 2018" in " ".join(h[2][1]), "L1918 art. 5 yerro")
    H._done(T1918, fix_1918_5)


H.FIXES[S1259] = [fix_1259_7]
H.FIXES[S1918] = [fix_1918_2, fix_1918_5]
