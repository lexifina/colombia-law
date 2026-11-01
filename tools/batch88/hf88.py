"""Hand-set histories for batch 88 (Leyes 643 de 2001, 191 de 1995), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L191, T191 = "ley_0191_1995", "Zonas de frontera (Ley 191 de 1995)"


def _u(name):
    return next(u for u in H.P.doc_units(L191)[1:] if u["name"] == name)


def _drop_empty(act, day):
    """Take out the version of `day` once the fixes above left it with no credit and no change (no decision line: the
    fix's own line says why)."""
    vs = act["versions"]
    i = next(i for i, v in enumerate(vs) if v["from"] == day)
    H.B23._need(not vs[i]["credits"] and vs[i]["units"] == vs[i - 1]["units"], f"L191 version {day} not empty")
    del vs[i]


def fix_191_40(act):
    """art. 40: the page heads it '<Artículo modificado por el Artículo 1o. del Decreto 1182 de 1999 ... El texto original
    es el siguiente:>' and prints the words as enacted. That decree (Diario Oficial No. 43.626 of 29 June 1999), as its
    Notas de Vigencia quote it, abolished the Consejería Presidencial de Fronteras the article created and gave its
    functions to the Ministerio de Relaciones Exteriores; it changed no words of the article. The article reads as enacted
    from the act's first day to today, and the decree is no version (the engine had put the placeholder before it)."""
    B23 = H.B23
    u = _u("40")
    nv = H._nv(u)
    B23._need("Suprímese en el Departamento Administrativo de la Presidencia de la República la Consejería Presidencial de "
              "Fronteras de que trata el artículo 40 de la Ley 191 de 1995" in nv, "L191 art. 40 NV")
    p0 = H.E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    B23._need("Artículo modificado por el Artículo 1o. del Decreto 1182 de 1999" in p0 and "El texto original es el siguiente" in p0,
              "L191 art. 40 marker")
    key = "art-0040"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1995-06-23", None), ("1999-06-29", ["dec-1182-1999"])] and h[0][1] == [H.PH],
              f"L191 art. 40 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, h[1][1], None)])
    B23._forget(L191, key)
    _drop_empty(act, "1999-06-29")
    H._done(T191, fix_191_40)


def fix_191_27(act):
    """art. 27 (IVA exemptions for goods from neighbouring countries, Amazonas): repealed by Ley 633 de 2000 art. 134 (29
    December 2000). Ley 677 de 2001 art. 29 (4 August 2001) took out the words of art. 134 that repealed it, but did not
    re-enact the article: a repealed provision does not revive because the law that repealed it is abolished, only by
    being reproduced in a new law (Ley 153 de 1887, art. 14). The article is out from 29 December 2000; the page still
    prints its words under its repeal marker; they are the words as enacted (the engine had put the placeholder before
    the repeal and brought the words back on 4 August 2001)."""
    B23 = H.B23
    u = _u("27")
    nv = H._nv(u)
    B23._need("El aparte del artículo 134 de la Ley 633 de 2000, que derogaba este artículo fue suprimido por el artículo 29 de "
              "la Ley 677 de 2001" in nv and "Artículo derogado por el artículo 134 de la Ley 633 de 2000" in nv, "L191 art. 27 NV")
    p0 = H.E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    B23._need("no obstante el texto original de este artículo no fue incluido en la Ley 677 de 2001" in p0, "L191 art. 27 marker")
    key = "art-0027"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1995-06-23", None), ("2000-12-29", ["ley-633-2000"]), ("2001-08-04", ["ley-677-2001"])]
              and h[0][1] == [H.PH] and h[1][1] is None and h[2][1], f"L191 art. 27 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, h[2][1], None), ("2000-12-29", None, "ley-633-2000")])
    B23._forget(L191, key)
    _drop_empty(act, "2001-08-04")
    H._done(T191, fix_191_27)


H.FIXES["zonas-de-frontera-1995"] = [fix_191_40, fix_191_27]
