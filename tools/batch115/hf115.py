"""Hand-set histories for batch 115 (Leyes 1060/2006, 2161/2021, 1381/2010), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


L2161, T2161, S2161 = "ley_2161_2021", "Medidas sobre el Seguro Obligatorio de Accidentes de Tránsito, SOAT (Ley 2161 de 2021)",     "soat-2021"
DEFER_11 = "Artículo INEXEQUIBLE. Fallo diferido hasta el 20 de junio de 2023"


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    if page == L2161 and key == "art-0011":
        return ("p0", DEFER_11)
    return None


def fix_2161_11(act):
    """art. 11 (suspension of the expiry of driving licences): the page prints it under '<Artículo INEXEQUIBLE. Fallo
    diferido hasta el 20 de junio de 2023>' (Sentencia C-261-22 of 13 July 2022 struck it with effect deferred to 20 June
    2023; C-396-22 'estarse a lo resuelto'). Deferred strike rule: the article stands as printed from the act's day and
    leaves on the deferral's stated day, 20 June 2023, credited to C-261-22. The engine had left it out of every version."""
    E = H.E
    u = H.B23._unit(L2161, "11")
    jv = " ".join(H._jv(u).split())
    p0 = E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    H.B23._need(DEFER_11 in p0 and "Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-261-22 "
                "de 13 de julio de 2022" in jv and "Fallo diferido hasta el 20 de junio de 2023" in jv, "L2161 art. 11 page")
    key = "art-0011"
    h = H._hist(act, key)
    H.B23._need(h == [(act["versions"][0]["from"], None, None)] or h == [], f"L2161 art. 11 shape {H._shape(h)}")
    lines = H._printed(u)
    H.B23._need(len(lines) == 2 and lines[0].startswith("SUSPENSIÓN DEL VENCIMIENTO DE LAS LICENCIAS DE CONDUCCIÓN. "
                "Suspéndase por el término"), f"L2161 art. 11 lines {lines}")
    c = E.add_court("C-261-22", "2022-07-13", "c-261_2022.html")
    H.B23._need(c == "c-261-22", f"C-261-22 key {c}")
    H._set(act, key, "Art. 11", [(None, lines, None), ("2023-06-20", None, c)])
    H.B23._forget(L2161, key)
    H._done(T2161, fix_2161_11)




H.FIXES[S2161] = [fix_2161_11]
