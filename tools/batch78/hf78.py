"""Hand-set histories for batch 78 (Leyes 1575 de 2012, 678 de 2001, 258 de 1996), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L678, T678 = "ley_0678_2001", "Acción de repetición y llamamiento en garantía con fines de repetición (Ley 678 de 2001)"
JV678_6 = ("Mediante Sentencia C-455-02 de 12 de junio de 2002, Magistrado Ponente Dr. Marco Gerardo Monroy Cabra, la Corte "
           "Constitucional declaró estese a lo resuelto en la Sentencia C-374-02, en relación con los cargos de la demanda."
           "Esta misma sentencia declaró EXEQUIBLES, por los cargos analizados, los numerales 1, 2, 3 y 4, excepto el aparte "
           "tachado del numeral 4. que se declara INEXEQUIBLE")
STRUCK_678_6 = "manifiesta e inexcusablemente"


def fix_678_6(act):
    """art. 6: the original text's numeral 4 reads 'Violar manifiesta e inexcusablemente el debido proceso ...' from the
    act's first day; the words 'manifiesta e inexcusablemente', which the earlier-text box shows struck, go on 12 June
    2002, credited to Sentencia C-455 de 2002 (its Jurisprudencia Vigencia box: 'Esta misma sentencia declaró EXEQUIBLES
    ... los numerales 1, 2, 3 y 4, excepto el aparte tachado del numeral 4. que se declara INEXEQUIBLE'; the engine found
    no dated ruling for the struck words and had kept them until Ley 2195 de 2022 rewrote the article)."""
    u = H.B23._unit(L678, "6")
    jv = re.sub(r"\s+", " ", H._jv(u))
    H.B23._need(JV678_6 in jv, f"{L678} art. 6: C-455-02 line")
    la = " ".join(H.E.plain(b) for b in H.B23._boxes(u, "Legislación Anterior"))
    H.B23._need("4. <Aparte tachado INEXEQUIBLE> Violar manifiesta e inexcusablemente el debido proceso" in re.sub(r"\s+", " ", la), f"{L678} art. 6: box")
    key = "art-0006"
    h = H._hist(act, key)
    H.B23._need([(d, c) for d, _, c in h] == [("2001-08-04", None), ("2022-01-18", ["ley-2195-2022"])],
                f"{L678} {key}: {H._shape(h)}")
    before = h[0][1]
    i = next(i for i, l in enumerate(before) if l.startswith("4. Violar "))
    H.B23._need(STRUCK_678_6 in before[i], f"{L678} {key}: numeral 4")
    after = list(before)
    after[i] = H.E.tidy(before[i].replace(STRUCK_678_6, " "))
    c = H.E.add_court("C-455-02", "2002-06-12", "c-455_2002.html")
    H.E.LAWS[c]["note"] = None
    H._set(act, key, "Art. 6", [(None, before, None), ("2002-06-12", after, c), ("2022-01-18", h[1][1], "ley-2195-2022")])
    H.B23._forget(L678, key)
    H._done(T678, fix_678_6)


H.FIXES.setdefault("accion-de-repeticion", []).append(fix_678_6)
