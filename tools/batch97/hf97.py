"""Hand-set histories for batch 97 (Leyes 890 de 2004 and 1285 de 2009), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L1285, T1285, S1285 = ("ley_1285_2009", "Reforma de la Ley Estatutaria de la Administración de Justicia (Ley 1285 de 2009)",
                       "reforma-de-la-administracion-de-justicia-2009")
M626 = "Artículo derogado por el literal c) del artículo 626 de la Ley 1564 de 2012. Rige a partir del 1o. de enero de 2014"


def _gone(page, key):
    if page == L1285 and key == "art-0025":
        return ("p0", M626)
    return None


gone_evidence = _gone  # noqa: F811  (replaces the stub above)


def fix_1285_25(act):
    """Ley 1285 de 2009, art. 25 (a new article for the Ley 270 de 1996): the page marks it '<Artículo derogado por el
    literal c) del artículo 626 de la Ley 1564 de 2012. Rige a partir del 1o. de enero de 2014 ...>' and gives its
    text in 'Legislación Anterior'; the engine had kept the words 'Artículo Nuevo.' (printed before the marker) as the
    article after 2014. The article now leaves on 1 January 2014, credited to Ley 1564 de 2012."""
    E = H.E
    u = H.B23._unit(L1285, "25")
    p0 = E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    H.B23._need(M626 in p0, "L1285 art. 25 marker")
    h = H._hist(act, "art-0025")
    H.B23._need([(d, c) for d, _, c in h] == [("2009-01-22", None), ("2014-01-01", ["ley-1564-2012"])]
                and h[0][1] and h[0][1][0].startswith("Agotada cada etapa del proceso") and h[1][1] == ["Artículo Nuevo."],
                "L1285 art. 25 shape")
    H._set(act, "art-0025", H._label(act, "art-0025"), [(None, h[0][1], None), ("2014-01-01", None, "ley-1564-2012")])
    H.B23._forget(L1285, "art-0025")
    H._done(T1285, fix_1285_25)


H.FIXES.setdefault(S1285, []).append(fix_1285_25)


def fix_1285_prior(act):
    """Ley 1285 de 2009: the Constitutional Court reviewed the bill before it was signed (Sentencia C-713-08 of 15 July
    2008, prior review of a statutory bill; it struck words of the bill and upheld others on conditions). The text
    given is the act as promulgated on 22 January 2009, after that review, so the ruling makes no version of the act
    (Ley 1581 de 2012's rule, 50-codes)."""
    u = H.P.doc_units(L1285)[0]
    jv = " ".join(H.E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")
    H.B23._need("Revisión Previa efectuada por la Corte Constitucional mediante la Sentencia C-713-08 de 15 de julio de "
                "2008" in jv, "L1285 prior review")
    H._done(T1285, fix_1285_prior)


H.FIXES[S1285].append(fix_1285_prior)
