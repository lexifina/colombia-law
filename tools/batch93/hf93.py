"""Hand-set histories for batch 93 (Leyes 793 de 2002 y 60 de 1993), installed by hand_fixes.install(); each checks
the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L793, T793, S793 = "ley_0793_2002", "Extinción de dominio (Ley 793 de 2002)", "extincion-de-dominio-2002"
L60, T60, S60 = "ley_0060_1993", "Distribución de competencias y recursos (Ley 60 de 1993)", "competencias-y-recursos-1993"
PH = "[La fuente no da el texto vigente en esta fecha.]"


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


def _need(c, what):
    H.B23._need(c, what)


def _orig_block(u, head):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        for blk in H.E.la_blocks(b):
            if blk["head"].startswith(head):
                return blk
    _need(False, f"art. {u['label']}: no '{head} ...' box")


def _box_lines(paras, keep_struck):
    """An earlier-text block's lines with or without the struck words (hf85._lines), the 'ARTÍCULO N.' head cut."""
    E, out = H.E, []
    for i, ph in enumerate(paras):
        t = E.tidy(E.to_text(ph, keep_struck))
        if i == 0:
            t = E.tidy(E.ART_HEAD.sub("", t, count=1))
        if t and re.search(r"\w", t):
            out.append(t)
    return out


# ------------------------------------------------------------------------------------------------- Ley 793 de 2002

def fix_793_c740(act):
    """arts. 2, 13 and 16: Sentencia C-740-03 (26 August 2003) struck words the page shows only inside the articles'
    'Texto original de la Ley 793 de 2002' boxes ('<Aparte tachado INEXEQUIBLE>': in art. 2 numeral 7 the word 'ilícito';
    in art. 13 numeral 1 'Contra esta resolución no procederá recurso alguno'; in art. 16 numeral 3 'sin causa que lo
    justifique'), as each Jurisprudencia Vigencia box says. As for Ley 938 de 2004 (hf85.fix_938_c878), each article reads
    as enacted (the box's words, the struck ones included) until the ruling, then without the struck words, until the
    later acts the engine read (Leyes 1395 de 2010 and 1453 de 2011). The engine had taken arts. 2 and 16 out of the
    record and put the placeholder in art. 13 from the ruling's day."""
    for n, after in (("2", None), ("13", "PH"), ("16", None)):
        u = H.B23._unit(L793, n)
        _need("C-740-03 de 26 de agosto de 2003" in H._jv(u) and "INEXEQUIBLE" in H._jv(u), f"L793 art. {n} JV")
        blk = _orig_block(u, "Texto original de la Ley 793 de 2002")
        full, cut = _box_lines(blk["paras"], True), _box_lines(blk["paras"], False)
        _need(full != cut and len(full) == len(cut), f"L793 art. {n} strike")
        key = f"art-{int(n):04d}"
        h = H._hist(act, key)
        _need(h[0][0] == "2002-12-27" and h[0][1] == full and h[1][0] == "2003-08-26" and h[1][2] == ["c-740-03"]
              and h[1][1] == (None if after is None else [PH]) and all(x[2] and len(x[2]) == 1 for x in h[2:]),
              f"L793 art. {n} {H._shape(h)}")
        H._set(act, key, H._label(act, key), [(None, full, None), ("2003-08-26", cut, "c-740-03")]
               + [(d, b, c[0]) for d, b, c in h[2:]])
        H.B23._forget(L793, key)
    H._done(T793, fix_793_c740)


# -------------------------------------------------------------------------------------------------- Ley 60 de 1993

def fix_60_18(act):
    """art. 18 (budget procedure of the situado fiscal): Decreto 1122 de 1999 art. 117 (29 June 1999) rewrote numeral 1
    (the page's earlier-text box gives the decree's numeral 1); Sentencia C-923-99 (18 November 1999) struck the decree as
    a whole; Decreto 266 de 2000 art. 61 (22 February 2000) changed the numeral again, giving no text on this page;
    Sentencia C-1316-00 (26 September 2000) struck that decree as a whole (the box writes 'El Decreto 266 fue 1999': read
    as Decreto 266 de 2000, as for Ley 43 de 1993 in 99zl-batch46). The page prints the act's own words as today's. As for
    the Código de Régimen Municipal's art. 25 (99h-batch16): the printed words from the act's first day, the decree's
    numeral 1 from 29 June 1999, the printed words again from 18 November 1999, the placeholder from 22 February 2000 (no
    text given), the printed words again from 26 September 2000 (C-1316-00's effect from the decree's promulgation is
    recorded here; the decree stood for those months). The engine had the placeholder from 1993 to 1999."""
    E = H.E
    u = H.B23._unit(L60, "18")
    nv, jv = H._nv(u), H._jv(u)
    _need("Numeral modificado por el artículo 61 del Decreto 266 de 2000, publicado en el Diario Oficial No. 43.906 del 22 de "
          "febrero de 2000" in nv and "Artículo subrogado por el artículo 117 del Decreto 1122 de 1999" in nv, "L60 art. 18 NV")
    _need("El Decreto 266 fue 1999 fue declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1316-00 del 26 "
          "de septiembre de 2000" in jv and "El Decreto 1122 de 1999 fue declarado INEXEQUIBLE por la Corte Constitucional "
          "mediante Sentencia C-923-99 del 18 de noviembre de 1999" in jv, "L60 art. 18 JV")
    printed = H._printed(u)
    h = H._hist(act, "art-0018")
    _need([(d, c) for d, _, c in h][:2] == [("1993-08-12", None), ("1999-06-29", ["dec-1122-1999"])] and h[0][1] == [PH]
          and len(h[1][1]) == len(printed) and h[1][1][0] == printed[0] and h[1][1][2:] == printed[2:]
          and h[1][1][1] != printed[1] and h[1][1][1].startswith("1. El Ministerio de Hacienda y Crédito Público comunicará"),
          f"L60 art. 18 {H._shape(h)}")
    k266 = E.register("dec-266-2000")
    _need(E.law_day(k266) == "2000-02-22", f"Decreto 266 de 2000 day {E.law_day(k266)}")
    k1316 = E.add_court("C-1316-00", "2000-09-26", "c-1316_2000.html")
    k923 = E.add_court("C-923-99", "1999-11-18", "c-923_1999.html")
    H._set(act, "art-0018", H._label(act, "art-0018"),
           [(None, printed, None), ("1999-06-29", h[1][1], "dec-1122-1999"), ("1999-11-18", printed, k923),
            ("2000-02-22", [PH], k266), ("2000-09-26", printed, k1316)])
    H.B23._forget(L60, "art-0018")
    H._done(T60, fix_60_18)


def fix_60_21(act):
    """art. 21 numeral 1: the page shows struck the words 'financiación de becas,' ('<Aparte tachado declarado
    INEXEQUIBLE>'), which Sentencia C-520-94 (21 November 1994) struck, as its Jurisprudencia Vigencia box says. The words
    stand from the act's first day and go on the ruling's day, credited to it (the engine had kept them until Sentencia
    C-1146-01 of 31 October 2001, which struck words of numeral 13 only)."""
    E = H.E
    u = H.B23._unit(L60, "21")
    _need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-520-94 de 21 de noviembre "
          "de 1994" in H._jv(u), "L60 art. 21 JV")
    h = H._hist(act, "art-0021")
    _need([(d, c) for d, _, c in h] == [("1993-08-12", None), ("1999-12-30", ["ley-549-1999"]), ("2001-10-31", ["c-1146-01"])],
          f"L60 art. 21 {H._shape(h)}")
    with_w = "de educación formal y no formal, financiación de becas, pago de personal docente,"
    without = "de educación formal y no formal, pago de personal docente,"
    k = [i for i, x in enumerate(h[0][1]) if with_w in x]
    _need(len(k) == 1 and h[0][1][k[0]].startswith("1.. En educación:") and with_w in h[1][1][k[0]]
          and h[2][1][k[0]] == h[1][1][k[0]].replace(with_w, without), "L60 art. 21 numeral 1")

    def cut(t):
        t = list(t)
        t[k[0]] = t[k[0]].replace(with_w, without)
        return t
    k520 = E.add_court("C-520-94", "1994-11-21", "c-520_1994.html")
    H._set(act, "art-0021", H._label(act, "art-0021"),
           [(None, h[0][1], None), ("1994-11-21", cut(h[0][1]), k520), ("1999-12-30", cut(h[1][1]), "ley-549-1999"),
            ("2001-10-31", cut(h[2][1]), "c-1146-01")])
    H.B23._forget(L60, "art-0021")
    H._done(T60, fix_60_21)


H.FIXES[S793] = [fix_793_c740]
H.FIXES[S60] = [fix_60_18, fix_60_21]
