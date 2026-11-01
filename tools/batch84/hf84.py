"""Hand-set histories for batch 84 (Leyes 905 de 2004, 1453 de 2011), installed by hand_fixes.install(); each checks
the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L905, T905 = "ley_0905_2004", "Reforma de la ley de micro, pequeñas y medianas empresas (Ley 905 de 2004)"
L1453, T1453 = "ley_1453_2011", "Seguridad ciudadana (Ley 1453 de 2011)"


def _orig_lines(u, start):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        try:
            ls = H.B23._box_lines(b, "Texto original", True)
        except StopIteration:
            continue
        if ls and ls[0].startswith(start):
            return ls
    H.B23._need(False, f"box starting {start!r}")


def fix_905_2(act):
    """art. 2 (Ley 590 de 2000 art. 2, quoted): numeral 1 literal b) reads as enacted ('Activos totales por valor entre
    cinco mil uno (5.001) a treinta mil (30.000) salarios mínimos mensuales legales vigentes.', the earlier-text box) until
    Ley 1111 de 2006 art. 51 restated amounts given in minimum wages in UVT (27 December 2006, the day the corpus gives Ley
    1111 de 2006); the UVT words the page prints from that day. The engine had used today's words from the act's first
    day (no earlier text read for a '<Ajuste ... en términos de UVT ...>' marker)."""
    B23, E = H.B23, H.E
    u = B23._unit(L905, "2")
    B23._need("El artículo 51 de la Ley 1111 de 2006, que modifica el artículo 868-1" in H._nv(u)
              and "ajusta los valores establecidos en salarios mínimos en términos de UVT" in H._nv(u), "L905 art. 2 note")
    old = _orig_lines(u, "b) Activos totales por valor entre cinco mil uno")
    B23._need(len(old) == 1, "L905 art. 2 box")
    key = "art-0002"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 1, f"L905 art. 2 {H._shape(h)}")
    today = h[0][1]
    k = [i for i, l in enumerate(today) if l == "b) Activos totales por valor entre 100.000 a 610.000 UVT."]
    B23._need(len(k) == 1, "L905 art. 2 literal b)")
    first = today[:k[0]] + old + today[k[0] + 1:]
    l1111 = E.register("ley-1111-2006")
    H._set(act, key, H._label(act, key), [(None, first, None), ("2006-12-27", today, l1111)])
    B23._forget(L905, key)
    H._done(T905, fix_905_2)


def fix_1453_41(act):
    """art. 41 (Código Penal art. 130, quoted): its second inciso ('Si el abandono se produce en sitios o circunstancias
    donde la supervivencia del recién nacido esté en peligro ...', the earlier-text box) stands from the act's first day
    until Sentencia C-093 de 2021 struck it (press release of 14 and 15 April 2021: 15 April, the day the Código Penal's
    history in this record gives the ruling); the page prints only '<Inciso INEXEQUIBLE>' for it. The engine had left the
    inciso out of every version."""
    B23, E = H.B23, H.E
    u = B23._unit(L1453, "41")
    B23._need("Inciso declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-093-21 según Comunicado de "
              "Prensa de 14 y 15 de abril de 2021" in H._jv(u), "L1453 art. 41 JV")
    inc = _orig_lines(u, "Si el abandono se produce en sitios o circunstancias")
    B23._need(len(inc) == 1, "L1453 art. 41 box")
    key = "art-0041"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 1, f"L1453 art. 41 {H._shape(h)}")
    today = h[0][1]
    B23._need(today[-1].startswith("Artículo 130. Circunstancias de agravación.") and today[-1].endswith("cuarta parte."),
              f"L1453 art. 41 today {today}")
    c = E.add_court("C-093-21", "2021-04-15", "c-093_2021.html")
    E.LAWS[c]["note"] = None
    H._set(act, key, H._label(act, key), [(None, today + inc, None), ("2021-04-15", today, c)])
    B23._forget(L1453, key)
    H._done(T1453, fix_1453_41)


H.FIXES["reforma-mipymes-2004"] = [fix_905_2]
H.FIXES["seguridad-ciudadana-2011"] = [fix_1453_41]
