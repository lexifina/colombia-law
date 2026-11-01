"""Hand-set histories for batch 99 (Leyes 1101 de 2006 and 1558 de 2012), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L1101, T1101, S1101 = ("ley_1101_2006", "Reforma de la Ley General de Turismo (Ley 1101 de 2006)",
                       "reforma-de-la-ley-general-de-turismo-2006")
L1558, T1558, S1558 = ("ley_1558_2012", "Reforma de la Ley General de Turismo (Ley 1558 de 2012)",
                       "reforma-de-la-ley-general-de-turismo-2012")
M372 = "Artículo derogado por el artículo 372 de la Ley 2294 de 2023"
M158 = "Artículo derogado por el artículo 158 del Decreto Ley 2106 de 2019"
NUEVO = "ley_1101_2006:NUEVO:5:1"
# Ley 1101 de 2006 art. 8: the page prints the footnote mark '<1>' after the epigraph, then '.Además ...': the engine
# joins them as 'TURÍSTICA..Además'; the act's words are 'TURÍSTICA. Además'.
DOTS_8 = ("RECURSOS DEL FONDO DE PROMOCIÓN TURÍSTICA..Además", "RECURSOS DEL FONDO DE PROMOCIÓN TURÍSTICA. Además")


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    if page == L1101 and key == "art-0009":
        return ("p0", M372)
    if page == L1558 and key == "art-0019":
        return ("p0", M158)
    return None


def _p0(u):
    return H.E.plain(next(it[1] for it in u["items"] if it[0] == "p"))


def fix_1101_3(act):
    """Ley 1101 de 2006, art. 3 (aportantes de la contribución parafiscal): Ley 1558 de 2012 art. 16 rewrote it (10 July
    2012) and Sentencia C-678-13 (25 September 2013) struck that art. 16 as a whole ('por vicios de trámite'). The page
    does not say the 2006 text revived, and a struck law's predecessor text does not revive by itself (the corpus's
    rule, as for Ley 633 de 2000 art. 80 after C-175-09): from the ruling's day the article reads '[La fuente no da el
    texto vigente en esta fecha.]', credited to the ruling, until Ley 2068 de 2020 art. 37 rewrote it (31 December
    2020). The engine had put the 2006 text back on the ruling's day."""
    key = "art-0003"
    u = H.B23._unit(L1101, "3")
    jv = " ".join(H._jv(u).split())
    H.B23._need("Artículo 16 de la Ley 1558 de 2012 declarado INEXEQUIBLE, por vicios de trámite, por la Corte Constitucional "
                "mediante Sentencia C-678-13 de 25 de septiembre de 2013" in jv
                and "reviv" not in jv.lower() and "reviv" not in H._nv(u).lower(), "L1101 art. 3 C-678-13 note")
    h = H._hist(act, key)
    H.B23._need([d for d, _, _ in h] == ["2006-11-23", "2012-07-10", "2013-09-25", "2020-12-31"]
                and [c for _, _, c in h[1:]] == [["ley-1558-2012"], ["c-678-13"], ["ley-2068-2020"]]
                and h[2][1] == h[0][1], f"L1101 art. 3 shape {H._shape(h)}")
    tl = [(None if j == 0 else d, b, (c or [None])[0]) for j, (d, b, c) in enumerate(h)]
    tl[2] = ("2013-09-25", [H.PH], "c-678-13")
    H._set(act, key, H._label(act, key), tl)
    H._done(T1101, fix_1101_3)


def fix_1101_nuevo(act):
    """Ley 1101 de 2006, the article Ley 1450 de 2011 art. 41 added after art. 5 (constitución de fiducias para la
    ejecución de proyectos del Fondo de Promoción Turística): the page prints its epigraph and its two parágrafos under
    the marker '<Artículo derogado por el artículo 372 de la Ley 2294 de 2023>' and its first inciso in the box 'Texto
    adicionado por la Ley 1450 de 2011'. The whole article (epigraph, inciso, parágrafos 1o. and 2o.) stands from Ley
    1450's day (16 June 2011) and goes on Ley 2294 de 2023's (19 May 2023); the engine had kept only the inciso until
    2023 and then the epigraph and parágrafos alone to today."""
    key = "art-0005-nuevo-1"
    u = next(x for x in H.P.doc_units(L1101) if x["name"] == NUEVO)
    H.B23._need(M372 in _p0(u) and "Artículo adicionado por el artículo 41 de la Ley 1450 de 2011" in H._nv(u)
                and "Artículo 41 de la Ley 1450 de 2011 derogado por el artículo 372 de la Ley 2294 de 2023" in H._nv(u),
                "L1101 nuevo art. notes")
    h = H._hist(act, key)
    H.B23._need([d for d, _, _ in h] == ["2006-11-23", "2011-06-16", "2023-05-19"] and h[0][1] is None
                and h[1][2] == ["ley-1450-2011"] and h[2][2] == ["ley-2294-2023"] and len(h[1][1]) == 1
                and h[2][1][0] == "CONSTITUCIÓN DE FIDUCIAS PARA LA EJECUCIÓN DE PROYECTOS DEL FONDO DE PROMOCIÓN TURÍSTICA."
                and [x[:14] for x in h[2][1][1:]] == ["PARÁGRAFO 1o. ", "PARÁGRAFO 2o. "]
                and h[1][1][0].startswith("El Ministerio de Comercio, Industria y Turismo como titular"),
                f"L1101 nuevo art. shape {H._shape(h)}")
    body = [h[2][1][0] + " " + h[1][1][0]] + h[2][1][1:]
    H._set(act, key, H._label(act, key), [(None, None, None), ("2011-06-16", body, "ley-1450-2011"),
                                          ("2023-05-19", None, "ley-2294-2023")])
    H._done(T1101, fix_1101_nuevo)


def fix_1101_8(act):
    """Ley 1101 de 2006, art. 8: the page prints the footnote mark '<1>' between the epigraph and '.Además ...', which
    read as 'TURÍSTICA..Además'; the words are 'RECURSOS DEL FONDO DE PROMOCIÓN TURÍSTICA. Además ...' in every
    version."""
    key = "art-0008"
    h = H._hist(act, key)
    H.B23._need(len(h) == 1 and h[0][1][0].startswith(DOTS_8[0]), f"L1101 art. 8 shape {H._shape(h)}")
    body = [DOTS_8[1] + h[0][1][0][len(DOTS_8[0]):]] + h[0][1][1:]
    H._set(act, key, H._label(act, key), [(None, body, None)])
    H._done(T1101, fix_1101_8)


def fix_1101_9(act):
    """Ley 1101 de 2006, art. 9 (new text of Ley 300 de 1996 art. 45, administración del Fondo de Promoción
    Turística): the page prints the words as enacted under the marker '<Artículo derogado por el artículo 372 de la Ley
    2294 de 2023>'. They stand from the act's first day and go on Ley 2294 de 2023's day (19 May 2023); the engine had
    held a placeholder until then and the words after it."""
    key = "art-0009"
    u = H.B23._unit(L1101, "9")
    H.B23._need(_p0(u).startswith("<" + M372 + ">") or _p0(u).startswith(M372), f"L1101 art. 9 marker {_p0(u)[:90]}")
    h = H._hist(act, key)
    H.B23._need([d for d, _, _ in h] == ["2006-11-23", "2023-05-19"] and h[0][1] == [H.PH] and h[1][2] == ["ley-2294-2023"]
                and h[1][1][0] == "El artículo 45 de la Ley 300 de 1996, quedará así:", f"L1101 art. 9 shape {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, h[1][1], None), ("2023-05-19", None, "ley-2294-2023")])
    H._done(T1101, fix_1101_9)


H.FIXES[S1101] = [fix_1101_3, fix_1101_nuevo, fix_1101_8, fix_1101_9]


def fix_1558_19(act):
    """Ley 1558 de 2012, art. 19 (procedimiento para acceder a los recursos del Programa Nacional de Inversiones
    Turísticas): the page prints the first word 'Todos' before the marker '<Artículo derogado por el artículo 158 del
    Decreto Ley 2106 de 2019>' and the rest in the box 'Texto original de la Ley 1558 de 2018' (a slip for 2012:
    the act is of 2012). The text as enacted (epigraph, 'Todos' and the box's words) stands from the act's first day
    and goes on Decreto Ley 2106 de 2019's day (22 November 2019); the engine had held a placeholder until then and
    the word 'Todos' alone after it."""
    key = "art-0019"
    u = H.B23._unit(L1558, "19")
    p0 = _p0(u)
    H.B23._need(p0.startswith("Todos") and M158 in p0, f"L1558 art. 19 p0 {p0[:90]}")
    blks = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in H.E.la_blocks(it[2])]
    H.B23._need(len(blks) == 1 and blks[0]["head"] == "Texto original de la Ley 1558 de 2018:", "L1558 art. 19 box")
    ls = H.E.block_text(blks[0]["paras"], False)
    ls = [re.sub(r"^ART[ÍI]CULO 19\.\s*", "", ls[0])] + ls[1:]
    H.B23._need(len(ls) == 1 and ls[0].startswith("los proyectos de infraestructura turística presentados por los entes"),
                f"L1558 art. 19 box text {ls}")
    h = H._hist(act, key)
    epi = "PROCEDIMIENTO PARA ACCEDER A LOS RECURSOS DEL PROGRAMA NACIONAL DE INVERSIONES TURÍSTICAS."
    H.B23._need([d for d, _, _ in h] == ["2012-07-10", "2019-11-22"] and h[0][1] == [H.PH]
                and h[1][2] == ["dec-2106-2019"] and h[1][1] == [epi + " Todos"], f"L1558 art. 19 shape {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, [f"{epi} Todos {ls[0]}"], None), ("2019-11-22", None, "dec-2106-2019")])
    # the engine's 'today's text used from the latest act's day' report for this unit no longer holds
    gone = [r for r in H.E.REPORT if r.startswith(f"{L1558} {key}: latest earlier text differs")]
    H.B23._need(len(gone) == 1, f"L1558 art. 19 report {gone}")
    H.E.REPORT.remove(gone[0])
    H._done(T1558, fix_1558_19)


H.FIXES[S1558] = [fix_1558_19]
