"""Hand-set histories for batch 69, installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import hand_fixes as H  # noqa: F401

import re


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


D760, T760 = "decreto_0760_2005", "Procedimiento ante y por la Comisión Nacional del Servicio Civil (Decreto Ley 760 de 2005)"
D785, T785 = ("decreto_0785_2005", "Nomenclatura, clasificación, funciones y requisitos de los empleos de las entidades "
              "territoriales (Decreto Ley 785 de 2005)")


def fix_760_3(act):
    """art. 3: the words 'el Departamento Administrativo de la Función Pública' of the original text, which Sentencia
    C-1175-05 (17 November 2005) struck (Jurisprudencia Vigencia: 'Aparte tachado declarado INEXEQUIBLE'; the earlier-text
    box prints them struck), stand until that day and leave on it, credited to the ruling, as the page prints the text
    without them; the engine had kept them until Ley 1753 de 2015 replaced the article."""
    B23, E = H.B23, H.E
    u = B23._unit(D760, "3")
    B23._need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1175-05 de 17 de "
              "noviembre de 2005" in H._jv(u), "D760 art. 3 JV")
    bl = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])]
    B23._need(len(bl) == 1 and bl[0]["head"].startswith("Texto original del Decreto 760 de 2005"), "D760 art. 3 box")
    paras = bl[0]["paras"]
    B23._need(re.findall(r"<S>.*?</S>", paras[0]) == ["<S><span class='b_aj'>el Departamento Administrativo de la "
                                                      "Funci&oacute;n P&uacute;blica</span></S>"], "D760 art. 3 struck")
    first = E.tidy(E.ART_HEAD.sub("", E.tidy(E.to_text(paras[0], True)), count=1))
    after = E.tidy(E.ART_HEAD.sub("", E.tidy(E.to_text(paras[0], False)), count=1))
    key = "art-0003"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2005-03-19", None), ("2015-06-09", ["ley-1753-2015"]),
                                            ("2016-09-21", ["c-518-16"])] and h[0][1][0] == first, f"D760 art. 3 {H._shape(h)}")
    c = "c-1175-05"
    B23._need(c in E.LAWS, "C-1175-05 law")
    E.LAWS[c]["note"] = None  # it struck words here
    _units_on(act, "2005-11-17")
    H._set(act, key, H._label(act, key), [(None, h[0][1], None), ("2005-11-17", [after] + h[0][1][1:], c)]
           + [(d, b, cc[0]) for d, b, cc in h[1:]])
    B23._forget(D760, key)
    H._done(T760, fix_760_3)


def fix_785_18_19(act):
    """arts. 18 and 19: Ley 2492 de 2025 arts. 2 and 3 (23 July 2025) rewrote them, and the earlier-text boxes give no
    words for that text ('<Consultar directamente artículo 2 [3] de la Ley 2492 de 2025>'); the engine had read that as the articles'
    absence. They read '[La fuente no da el texto vigente en esta fecha.]' from that day until Ley 2611 de 2026 (28 July
    2026) gave the text the page prints."""
    B23 = H.B23
    for n, a in (("18", "2"), ("19", "3")):
        u = B23._unit(D785, n)
        box = " ".join(H.E.plain(b) for b in B23._boxes(u, "Legislación Anterior"))
        B23._need(f"Texto modificado por la Ley 2492 de 2025:ARTÍCULO {n}. <Consultar directamente artículo {a} de la Ley 2492 "
                  "de 2025>" in box, f"D785 art. {n} box")
        key = f"art-{int(n):04d}"
        h = H._hist(act, key)
        B23._need([(d, c, b is None) for d, b, c in h] == [("2005-03-19", None, False), ("2025-07-23", ["ley-2492-2025"], True),
                                                           ("2026-07-28", ["ley-2611-2026"], False)], f"D785 art. {n} {H._shape(h)}")
        H._set(act, key, H._label(act, key), [(None, h[0][1], None), ("2025-07-23", [H.PH], "ley-2492-2025"),
                                              ("2026-07-28", h[2][1], "ley-2611-2026")])
        B23._forget(D785, key)
    H._done(T785, fix_785_18_19)


H.FIXES.setdefault("procedimiento-comision-nacional-del-servicio-civil", []).append(fix_760_3)
H.FIXES.setdefault("nomenclatura-de-empleos-territoriales", []).append(fix_785_18_19)
