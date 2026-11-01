"""Hand-set histories for batch 68, installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import hand_fixes as H  # noqa: F401

L35, T35 = "ley_0035_1993", "Ley marco de las actividades financiera, bursátil y aseguradora (Ley 35 de 1993)"


def _units_on(act, day):
    """A credit-only version (no unit texts) on `day` gets the texts of the version before it, so a hand-set change can
    land on it."""
    vs = act["versions"]
    for i, v in enumerate(vs):
        if v["from"] == day and "units" not in v:
            v["units"] = dict(next(p for p in reversed(vs[:i]) if "units" in p)["units"])


def _box_lines(u, head):
    E = H.E
    bl = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])
          if b["head"].rstrip(" :") == head]
    H.B23._need(len(bl) == 1, f"box {head}")
    return E.block_text(bl[0]["paras"], True)


def _c675():
    E = H.E
    if "c-675-98" not in E.LAWS:
        E.add_court("C-675-98", "1998-11-18", "c-675_1998.html")
    E.LAWS["c-675-98"]["note"] = None  # it struck words of arts. 8 and 37 (fix_35_8, fix_35_37)
    return "c-675-98"


def fix_35_4(act):
    """art. 4 (repealed by Ley 964 de 2005): the page prints its last text, and its earlier-text box headed 'Texto original'
    holds the same text, with literals l) to o); its Notas de Vigencia say 'Literales l), m), n) y o) adicionados por el
    artículo 57 de la Ley 510 de 1999' (Diario Oficial of 4 August 1999). The article now reads without those four
    literals from the act's first day; they arrive on 4 August 1999, credited to Ley 510 de 1999."""
    B23, E = H.B23, H.E
    u = B23._unit(L35, "4")
    B23._need("Literales l), m), n) y o) adicionados por el artículo 57 de la Ley 510 de 1999, publicada en Diario Oficial "
              "No. 43.654 de 4 de agosto de 1999" in H._nv(u), "L35 art. 4 NV")
    key = "art-0004"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1993-01-05", None), ("2006-01-08", ["ley-964-2005"])] and h[1][1] is None
              and h[0][1] == _box_lines(u, "Texto original de la Ley 35 de 1993"), f"L35 art. 4 {H._shape(h)}")
    lit = [l for l in h[0][1] if l[:3] in ("l) ", "m) ", "n) ", "o) ")]
    B23._need(len(lit) == 4, "L35 art. 4 literals")
    k510 = E.register("ley-510-1999")
    B23._need(E.law_day(k510) == "1999-08-04", f"Ley 510 day {E.law_day(k510)}")
    H._set(act, key, H._label(act, key), [(None, [l for l in h[0][1] if l not in lit], None), ("1999-08-04", h[0][1], k510),
                                          ("2006-01-08", None, "ley-964-2005")])
    B23._forget(L35, key)
    H._done(T35, fix_35_4)


def fix_35_8(act):
    """art. 8: the references to arts. 5, 6 and 7, which Sentencia C-675-98 (18 November 1998) struck (its Jurisprudencia
    Vigencia box: 'la referencia en este artículo a los artículos 5o., 6o. y 7o., tachada, fue declarada INEXEQUIBLE'),
    stand until that day and leave on it, credited to the ruling; the engine had dropped them from every version."""
    B23, E = H.B23, H.E
    u = B23._unit(L35, "8")
    B23._need("la referencia en este artículo a los artículos 5o., 6o. y 7o., tachada, fue declarada INEXEQUIBLE" in H._jv(u)
              and "Sentencia C-675-98 de 18 de noviembre de 1998" in H._jv(u), "L35 art. 8 JV")
    key = "art-0008"
    h = H._hist(act, key)
    after, before = H._printed(u), H._printed(u, keep_struck=True)
    B23._need([(d, c) for d, _, c in h] == [("1993-01-05", None)] and h[0][1] == after, f"L35 art. 8 {H._shape(h)} {after}")
    B23._need(before[0].count("artículos 3o., 5o., 6o. y 7o. serán") == 1 and before[1:] == after[1:], f"L35 art. 8 {before}")
    c = _c675()
    _units_on(act, "1998-11-18")
    H._set(act, key, H._label(act, key), [(None, before, None), ("1998-11-18", after, c)])
    B23._forget(L35, key)
    H._done(T35, fix_35_8)


def fix_35_35(act):
    """art. 35 (repealed by Decreto 1133 de 1999): its earlier-text box gives the original text under a heading printed
    'ARTÍCULO35.' (no space), which the engine did not read, so the article had the placeholder; the box text now stands
    from the act's first day until the repeal (29 June 1999)."""
    B23 = H.B23
    u = B23._unit(L35, "35")
    lines = _box_lines(u, "Texto original de la Ley 35 de 1993")
    B23._need(lines[0].startswith("ARTÍCULO35. FUNCIONES. Corresponde al Viceministerio Técnico"), "L35 art. 35 box")
    lines = [lines[0][len("ARTÍCULO35. "):]] + lines[1:]
    key = "art-0035"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1993-01-05", None), ("1999-06-29", ["dec-1133-1999"])] and h[0][1] == [H.PH]
              and h[1][1] is None, f"L35 art. 35 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, lines, None), ("1999-06-29", None, "dec-1133-1999")])
    B23._forget(L35, key)
    H._done(T35, fix_35_35)


def fix_35_37(act):
    """art. 37: its second inciso, which the page gives only in the earlier-text box ('<INCISO 2o.> En el evento de que
    deban producirse retiros de personal ...'), stands from the act's first day until Sentencia C-675-98 (18 November
    1998) struck it (Jurisprudencia Vigencia: 'INEXEQUIBLE el 2o. inciso de acuerdo al punto 6o. de la misma
    sentencia'); the engine had left it out of every version."""
    B23 = H.B23
    u = B23._unit(L35, "37")
    B23._need("INEXEQUIBLE el 2o. inciso de acuerdo al punto 6o. de la misma sentencia" in H._jv(u), "L35 art. 37 JV")
    inc2 = _box_lines(u, "Texto original de la Ley 35 de 1993")
    B23._need(len(inc2) == 1 and inc2[0].startswith("En el evento de que deban producirse retiros de personal"), "L35 art. 37 box")
    key = "art-0037"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1993-01-05", None)] and len(h[0][1]) == 1, f"L35 art. 37 {H._shape(h)}")
    c = _c675()
    _units_on(act, "1998-11-18")
    H._set(act, key, H._label(act, key), [(None, h[0][1] + inc2, None), ("1998-11-18", h[0][1], c)])
    B23._forget(L35, key)
    H._done(T35, fix_35_37)


H.FIXES.setdefault("marco-del-sector-financiero", []).extend([fix_35_4, fix_35_8, fix_35_35, fix_35_37])
