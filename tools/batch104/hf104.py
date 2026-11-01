"""Hand-set histories for batch 104 (Leyes 1421 de 2010 and 1738 de 2014), installed by hand_fixes.install(); each
checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L1421, S1421 = "ley_1421_2010", "prorroga-de-la-ley-418-2010"
T1421 = "Prórroga y reforma de la Ley 418 de 1997 (Ley 1421 de 2010)"
SUJETOS_8 = "El carácter de los sujetos pasivos y la base impositiva del tributo serán reglamentados por el Ministerio del Interior y de Justicia."
TASAS_8 = "Los departamentos y municipios podrán imponer tasas o sobretasas especiales destinadas a financiar los fondos-cuenta territoriales de seguridad para fomentar la seguridad ciudadana."
PERM_8 = "El inciso segundo del presente artículo no estará sometido a la vigencia de la prórroga establecida mediante la presente ley, sino que conservará un carácter permanente."
C101_END = "2024-06-20"


def fix_1421_8(act):
    """Ley 1421 de 2010, art. 8 (aportes voluntarios a los fondos-cuenta territoriales). (a) Sentencia C-891-12 (31
    October 2012) struck the last inciso ('El carácter de los sujetos pasivos y la base impositiva del tributo serán
    reglamentados por el Ministerio del Interior y de Justicia.'), which the page gives only in its Legislación Anterior
    box under an empty '<Inciso INEXEQUIBLE>' marker: out from that day, credited to C-891-12 (the engine had taken it out
    on the day of Sentencia C-101-22, whose version is gone). (b) Sentencia C-101-22 (17 March 2022) struck the second inciso ('Los
    departamentos y municipios podrán imponer tasas o sobretasas especiales ...') and the third inciso of the parágrafo
    ('El inciso segundo del presente artículo no estará sometido a la vigencia de la prórroga ...') with its effects
    deferred by two legislatures from its notification (Edicto No. 48 of 1 June 2022); the second of those legislatures
    ends on 20 June 2024 (Constitución art. 138; the page's own note '<hasta 20 de junio de 2024>'), so both go on that
    day, credited to the ruling (as Sentencia C-030-19's deferral, batch 98). The page still prints both under the marker
    '<Inciso INEXEQUIBLE. Fallo diferido ...>'. Ley 2272 de 2022 art. 12 (Diario Oficial No. 52.208 of 4 November 2022),
    'in compliance with' C-101-22, lets territories already collecting the tax go on doing so: a rule of its own that
    changes none of Ley 1421's words. No version. Sentencia C-045-18 (inhibited) changes nothing."""
    E = H.E
    u = H.B23._unit(L1421, "8")
    jv = H._jv(u)
    legi = " ".join(E.plain(b) for b in H.B23._boxes(u, "Legislación Anterior"))
    H.B23._need("Sentencia C-891-12 de 31 de octubre de 2012" in jv and SUJETOS_8 in legi
                and jv.count("SE DIFIEREN por el término de dos legislaturas") == 2
                and "Notificada mediante Edicto No. 48 de 1 de junio de 2022" in jv and "hasta 20 de junio de 2024" in jv
                and "ARTÍCULO 12. CUMPLIMIENTO DE LA SENTENCIA C-101 DE 2022" in H._nv(u), "L1421 art. 8 page")
    h = H._hist(act, "art-0008")
    b0 = h[0][1]
    H.B23._need([d for d, _, _ in h] == ["2010-12-21", "2022-03-17"] and b0[-1] == SUJETOS_8 and b0[1] == TASAS_8
                and b0[4] == PERM_8 and h[1][1] == b0[:-1], f"L1421 art. 8 shape {H._shape(h)}")
    c891 = E.add_court("C-891-12", "2012-10-31", "c-891_2012.html")
    c101 = E.add_court("C-101-22", "2022-03-17", "c-101_2022.html")
    b1 = b0[:-1]
    b2 = [l for l in b1 if l not in (TASAS_8, PERM_8)]
    H._set(act, "art-0008", H._label(act, "art-0008"), [(None, b0, None), ("2012-10-31", b1, c891), (C101_END, b2, c101)])
    vs = act["versions"]  # the engine's 2022-03-17 version (C-101-22's day) now changes and credits nothing: gone
    i = next(i for i, v in enumerate(vs) if v["from"] == "2022-03-17")
    prev = next(v for v in reversed(vs[:i]) if "units" in v)
    H.B23._need(not vs[i]["credits"] and vs[i].get("units", prev["units"]) == prev["units"], f"2022-03-17 version {vs[i]['credits']}")
    del vs[i]
    H.B23._forget(L1421, "art-0008")
    H._done(T1421, fix_1421_8)


H.FIXES[S1421] = [fix_1421_8]
