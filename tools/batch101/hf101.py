"""Hand-set histories for batch 101 (Leyes 2388 de 2024 and 548 de 1999), installed by hand_fixes.install(); each
checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L2388, S2388 = "ley_2388_2024", "familia-de-crianza"
T2388 = "Familia de crianza (Ley 2388 de 2024)"
MARK_5 = ("artículo 5* de la presente ley", "artículo 5 de la presente ley")
OPEN_3 = ("juez de familia [ del domicilio", "juez de familia del domicilio")


def _hist_cr(act, key):
    """H._hist, also listing a day that credits the unit without changing its words (a conditional ruling's note)."""
    out, last = [], object()
    for v in act["versions"]:
        if "units" in v or key in v["credits"]:  # a version without units reads as the one before it
            t = (v["units"].get(key) or {}).get("text") if "units" in v else last
            if t != last or key in v["credits"]:
                out.append((v["from"], None if t is None else t.split("\n")[1:-1], v["credits"].get(key)))
                last = t
    return out


def fix_2388_3(act):
    """Ley 2388 de 2024, art. 3: (a) the page prints the editor's footnote mark '*' after 'artículo 5' (its Notas del
    Editor quote Sentencia C-506-25 on the reference); the mark is not the act's: 'artículo 5 de la presente ley' in every
    version. (b) Sentencia C-506-25 (11 December 2025) struck 'o notario', which the page prints with the opening
    bracket outside the struck span ('[<S>o notario]</S>'): the bracket goes with the struck words, so from the ruling the
    inciso reads 'ante juez de familia del domicilio ...' (the engine had left 'juez de familia [ del domicilio')."""
    key = "art-0003"
    u = H.B23._unit(L2388, "3")
    raw = " ".join(it[1] for it in u["items"] if it[0] == "p")
    H.B23._need("[<S>o notario]</S>" in raw and "Sentencia C-506-25" in H._jv(u) and "artículo 5' la Corte" in
                " ".join(H.E.plain(it[2]) for it in u["items"] if it[0] == "box"), "L2388 art. 3 page")
    h = _hist_cr(act, key)
    H.B23._need(len(h) >= 2 and h[1][2] == ["c-506-25"] and all(MARK_5[0] in b[1] for _, b, _ in h)
                and all((OPEN_3[0] in b[0]) == (i > 0) for i, (_, b, _) in enumerate(h)), f"L2388 art. 3 shape {H._shape(h)}")
    tl = []
    for i, (d, b, c) in enumerate(h):
        b = [l.replace(MARK_5[0], MARK_5[1]).replace(OPEN_3[0], OPEN_3[1]) for l in b]
        tl.append((None if i == 0 else d, b, None if i == 0 else c[0]))
    H._set(act, key, H._label(act, key), tl)
    H.B23._forget(L2388, key)
    H._done(T2388, fix_2388_3)


H.FIXES[S2388] = [fix_2388_3]


L548, S548 = "ley_0548_1999", "prorroga-de-la-ley-418-1999"
T548 = "Prórroga y reforma de la Ley 418 de 1997 (Ley 548 de 1999)"


def note_642(act):
    """Ley 548 de 1999, art. 2 (new text of Ley 418 de 1997 art. 13): art. 1 of Ley 642 de 2001 (Diario Oficial No.
    44.282 of 5 January 2001) 'clarified' the second inciso ('Aclarase el articulo 2o. de la Ley 548 de 1999 en el
    sentido de que la opción prevista en el inciso segundo de este artículo se aplicará también a quienes cumplan los
    dieciocho (18) años mientras cursan sus estudios de bachillerato'): a rule of its own on how the inciso applies, which
    changes none of its words; the page prints the inciso as enacted. No version."""
    u = H.B23._unit(L548, "2")
    H.B23._need("Inciso 2o. aclarado por el artículo 1 de la Ley 642 de 2001" in H._nv(u)
                and "se aplicará también a quienes cumplan los dieciocho (18) años" in H._nv(u), "L548 art. 2 NV")
    h = _hist_cr(act, "art-0002")
    H.B23._need(len(h) == 1, f"L548 art. 2 shape {H._shape(h)}")
    H._done(T548, note_642)


H.FIXES[S548] = [note_642]
