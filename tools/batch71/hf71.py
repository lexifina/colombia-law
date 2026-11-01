"""Hand-set histories for batch 71 (Leyes 335 de 1996, 680 de 2001, 1273 de 2009), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L335, T335 = "ley_0335_1996", "Modificación de las Leyes 14 de 1991 y 182 de 1995 y televisión privada (Ley 335 de 1996)"
L680, T680 = "ley_0680_2001", "Reforma de las Leyes 14 de 1991, 182 de 1995 y 335 de 1996 en materia de televisión (Ley 680 de 2001)"


def _la(u, head, first=None):
    """The lines of the earlier-text block headed `head` (the only one whose first line starts with `first`), the
    publisher's leading '<Inciso N.>' label out."""
    B23, E = H.B23, H.E
    out = []
    for b in B23._boxes(u, "Legislación Anterior"):
        for blk in E.la_blocks(b):
            if blk["head"].rstrip(" :").startswith(head):
                ls = [E.tidy(re.sub(r"^<[^<>]*>\s*", "", x)) for x in E.block_text(blk["paras"], False)]
                ls = [x for x in ls if x]
                if ls and (first is None or ls[0].startswith(first)):
                    out.append(ls)
    B23._need(len(out) == 1, f"box {head!r} {first!r}: {len(out)}")
    return out[0]


def _one_line(lines, start):
    k = [i for i, x in enumerate(lines) if x.startswith(start)]
    H.B23._need(len(k) == 1, f"line {start!r}")
    return k[0]


def fix_335_25(act):
    """art. 25: the page gives the original incisos 1 to 4 and the parágrafo's first inciso in an earlier-text box headed
    'Texto original de los incisos 1o., 2o., 3o., 4o. y parágrafo inciso 1o. ...' (its tail printed after the box, joined
    by BOX_TAIL), which the engine did not read. From the act's first day the article reads that text followed by the
    parágrafo's last inciso ('La actividad periodística gozará de protección ...'); Sentencia C-350 de 1997 (29 July 1997)
    struck all of it except that inciso, which alone stands from that day, as the page prints it."""
    B23, E = H.B23, H.E
    u = B23._unit(L335, "25")
    B23._need("mediante Sentencia C-350-97 de 29 de julio de 1997" in H._jv(u) and "salvo el último inciso del parágrafo que fue "
              "declarado EXEQUIBLE" in H._jv(u), "L335 art. 25 JV")
    box = _la(u, "Texto original de los incisos 1o., 2o., 3o., 4o. y parágrafo inciso 1o. de la Ley 335 de 1996")
    B23._need(len(box) == 10 and box[-1].startswith("PARÁGRAFO. En los contratos"), "L335 art. 25 box")
    box = [E.tidy(E.ART_HEAD.sub("", box[0], count=1))] + box[1:]
    key = "art-0025"
    h = H._hist(act, key)
    B23._need(len(h) == 1 and h[0][1] == ["La actividad periodística gozará de protección para garantizar su libertad e "
                                          "independencia profesional."], f"L335 art. 25 {H._shape(h)}")
    B23._need("c-350-97" in E.LAWS, "C-350-97 law")
    H._set(act, key, H._label(act, key), [(None, box + h[0][1], None), ("1997-07-29", h[0][1], "c-350-97")])
    B23._forget(L335, key)
    H._done(T335, fix_335_25)


def fix_335_16(act):
    """art. 16 (Ley 182 de 1995 art. 62, quoted): the page prints its text after the marker '<Artículo derogado por el
    artículo 51 de la Ley 1978 de 2019>' and other notes, which the engine read as an article first in force on the
    repeal's day (25 July 2019), with the placeholder before. It reads as printed from the act's first day, with the words
    'previo el visto bueno del Ministerio de Comunicaciones' that Sentencia C-445 de 1997 (18 September 1997) struck
    standing until that day; Sentencia C-350 de 1997 (29 July 1997) upheld it on a condition (a credit, no words); it
    leaves on 25 July 2019, credited to Ley 1978 de 2019."""
    B23, E = H.B23, H.E
    u = B23._unit(L335, "16")
    jv = H._jv(u)
    B23._need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional, mediante Sentencia C-445-97 de 18 de "
              "septiembre de 1997" in jv, "L335 art. 16 JV")
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    B23._need(E.plain(ps[0]).startswith("<Artículo derogado por el artículo 51 de la Ley 1978 de 2019>"), "L335 art. 16 marker")
    struck = [x for x in ps if "<S>" in x.upper()]
    B23._need(len(struck) == 1 and re.findall(r"<S>.*?</S>", struck[0], re.S | re.I) == [
        '<S><span class="b_aj">previo el visto bueno del Ministerio de Comunicaciones</span></S>'], "L335 art. 16 struck")
    key = "art-0016"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1996-12-24", None), ("2019-07-25", ["ley-1978-2019"])] and h[0][1] == [H.PH],
              f"L335 art. 16 {H._shape(h)}")
    after = h[1][1]
    k = _one_line(after, "Previo otorgamiento de las frecuencias")
    s = "previo el visto bueno del Ministerio de Comunicaciones"
    B23._need(after[k].endswith("operadores públicos de televisión a la vigencia de la presente ley,.") and s not in after[k],
              "L335 art. 16 last line")
    first = list(after)
    first[k] = after[k][:-2] + ", " + s + "."
    B23._need(E.tidy(E.to_text(struck[0], True)).endswith(first[k]), "L335 art. 16 struck line")
    law = E.add_court("C-445-97", "1997-09-18", "c-445_1997.html")
    B23._need("c-350-97" in E.LAWS and E.LAWS[law]["enacted"] == "1997-09-18", "L335 art. 16 laws")
    _units_on_day(act, "1997-07-29")
    H._set(act, key, H._label(act, key), [(None, first, None), ("1997-07-29", first, "c-350-97"),
                                          ("1997-09-18", after, law), ("2019-07-25", None, "ley-1978-2019")])
    B23._forget(L335, key)
    H._done(T335, fix_335_16)


def _units_on_day(act, day):
    vs = act["versions"]
    for i, v in enumerate(vs):
        if v["from"] == day and "units" not in v:
            v["units"] = dict(next(p for p in reversed(vs[:i]) if "units" in p)["units"])


def fix_680_6(act):
    """art. 6: Sentencia C-351 de 2004 (20 April 2004) struck the first sentence of the parágrafo's last inciso ('En los
    contratos de concesión del servicio público de televisión por suscripción, se aplicarán ... sin sus excepciones y
    diferencias.', printed struck in the earlier-text box); from that day the inciso reads 'Cuando se den disminuciones en
    los costos ...' until Ley 1978 de 2019 repealed the article (25 July 2019). The engine had the placeholder from 2004."""
    B23, E = H.B23, H.E
    u = B23._unit(L680, "6")
    B23._need("salvo el aparte tachado que declara INEXEQUIBLE, por la Corte Constitucional mediante Sentencia C-351-04 de 20 "
              "de abril de 2004" in H._jv(u), "L680 art. 6 JV")
    key = "art-0006"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2001-08-11", None), ("2004-04-20", ["c-351-04"]), ("2019-07-25", ["ley-1978-2019"])]
              and h[1][1] == [H.PH], f"L680 art. 6 {H._shape(h)}")
    o = h[0][1]
    s = ("En los contratos de concesión del servicio público de televisión por suscripción, se aplicarán en lo pertinente las "
         "disposiciones que rigen en materia de tarifas, derechos, compensaciones y tasas, para los servicios de "
         "telecomunicaciones, establecidas en el Régimen Unificado para la Fijación de Contraprestaciones a favor del Estado "
         "para los servicios de difusión sin sus excepciones y diferencias. ")
    B23._need(o[-1].startswith(s) and o[-1][len(s):].startswith("Cuando se den disminuciones"), "L680 art. 6 last inciso")
    H._set(act, key, H._label(act, key), [(None, o, None), ("2004-04-20", o[:-1] + [o[-1][len(s):]], "c-351-04"),
                                          ("2019-07-25", None, "ley-1978-2019")])
    B23._forget(L680, key)
    H._done(T680, fix_680_6)


def fix_335_1(act):
    """art. 1 (Ley 182 de 1995 art. 6, quoted): the word 'reglamentará' in the two sentences 'La Registraduría Nacional del
    Estado Civil reglamentará y vigilará la elección nacional del respectivo representante', struck by Sentencia C-350 de
    1997 (29 July 1997; the page prints it struck), stands until that day and goes on it, credited to the ruling; the
    engine had left it out of every version. The article leaves on 25 July 2019 (Ley 1978 de 2019), as before."""
    B23, E = H.B23, H.E
    u = B23._unit(L335, "1")
    B23._need(H._jv(u).count("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional, mediante Sentencia C-350-97 de 29 "
                             "de julio de 1997") == 2, "L335 art. 1 JV")
    raws = [it[1] for it in u["items"] if it[0] == "p" and "<S>" in it[1].upper()]
    B23._need(len(raws) == 2 and all([H.E.plain(x).strip() for x in re.findall(r"<S>.*?</S>", r, re.S | re.I)] == ["reglamentará"] for r in raws),
              "L335 art. 1 struck")
    key = "art-0001"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("1996-12-24", None), ("2019-07-25", ["ley-1978-2019"])] and h[1][1] is None,
              f"L335 art. 1 {H._shape(h)}")
    after = h[0][1]
    old = "La Registraduría Nacional del Estado Civil y vigilará"
    ks = [i for i, x in enumerate(after) if x.startswith(old)]
    B23._need(len(ks) == 2, "L335 art. 1 lines")
    first = [x.replace(old, "La Registraduría Nacional del Estado Civil reglamentará y vigilará", 1) if i in ks else x
             for i, x in enumerate(after)]
    B23._need("c-350-97" in E.LAWS, "C-350-97 law")
    E.LAWS["c-350-97"]["note"] = None  # it struck words here (and in art. 25)
    _units_on_day(act, "1997-07-29")
    H._set(act, key, H._label(act, key), [(None, first, None), ("1997-07-29", after, "c-350-97"),
                                          ("2019-07-25", None, "ley-1978-2019")])
    B23._forget(L335, key)
    H._done(T335, fix_335_1)


H.FIXES.setdefault("television-privada-1996", []).extend([fix_335_1, fix_335_25, fix_335_16])
H.FIXES.setdefault("reforma-de-la-television-2001", []).append(fix_680_6)
