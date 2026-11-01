"""Hand-set histories for batch 67 (Decretos Ley 262 y 267 de 2000), installed by hand_fixes.install(); each checks the
page first."""
from __future__ import annotations

import hand_fixes as H

D267, T267 = "decreto_0267_2000", ("Organización y funcionamiento de la Contraloría General de la República (Decreto Ley 267 "
                                   "de 2000)")
CONS = "con las modificaciones parciales introducidas con posterioridad"


def fix_267_11(act):
    """art. 11 (organización): its earlier-text box holds two texts, 'Texto original del Decreto 267 de 2000, con las
    modificaciones parciales introducidas con posterioridad' and 'Texto original del Decreto 267 de 2000'; the engine
    read the first as the act's first text, though it already holds later lines. Now: the original text from the act's
    first day; from 12 July 2011 the four units Ley 1474 de 2011 art. 128 created in the Contraloría's structure (Unidad
    de Investigaciones Especiales contra la Corrupción, de Cooperación Nacional e Internacional de Prevención,
    Investigación e Incautación de Bienes, de Apoyo Técnico al Congreso, de Seguridad y Aseguramiento Tecnológico e
    Informático; Decreto Ley 405 de 2020 art. 13 names art. 11 as 'modificado por el artículo 128 de la Ley 1474 de
    2011'); from 1 September 2016 numerals 1.7 and 1.8 added and numeral 2.2 repealed by Ley 1807 de 2016 arts. 11-12 (the
    article's Notas de Vigencia); from 27 May 2017 the Unidad Delegada para el Posconflicto that Decreto Ley 888 de 2017
    created (in force on its publication, Diario Oficial No. 50.246 of 27 May 2017). That last text is the box's text with
    the later partial changes, which Decreto Ley 2037 de 2019 replaced."""
    B23, E = H.B23, H.E
    u = B23._unit(D267, "11")
    B23._need("Numerales 1.7 y 1.8 adicionados por el artículo 11 y numeral 2.2 derogado por el artículo 12 de la Ley 1807 "
              "de 2016" in H._nv(u), "D267 art. 11 NV")
    a128 = " ".join(E.plain(it[1]) for it in B23._unit("ley_1474_2011", "128")["items"] if it[0] == "p")
    B23._need("créanse dentro de la estructura de la Contraloría General de la República la Unidad de Investigaciones "
              "Especiales contra la Corrupción, la Unidad de Cooperación Nacional e Internacional de Prevención, "
              "Investigación e Incautación de Bienes, la Unidad de Apoyo Técnico al Congreso y la Unidad de Seguridad y "
              "Aseguramiento Tecnológico e Informático" in a128, "Ley 1474 art. 128")
    d888 = " ".join(E.plain(E.html.unescape(E.read(E.BASE + "decreto_0888_2017.html") or "")).split())
    B23._need("se crea una Unidad Delegada para el Posconflicto en la Contraloría General de la República" in d888
              and "Diario Oficial No. 50.246 de 27 de mayo de 2017" in d888
              and "El presente decreto ley rige a partir de su publicación y modifica el Decreto-ley 267 de 2000" in d888,
              "Decreto Ley 888 de 2017 page")
    blocks = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])]
    cons = [b for b in blocks if CONS in b["head"]]
    orig = [b for b in blocks if b["head"].rstrip(" :") == "Texto original del Decreto 267 de 2000"]
    B23._need(len(cons) == 1 and len(orig) == 1, f"D267 art. 11 boxes {[b['head'] for b in blocks]}")
    orig_lines = E.block_text(orig[0]["paras"], True)
    cons_lines = E.block_text(cons[0]["paras"], True)
    key = "art-0011"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2000-02-22", None), ("2019-11-07", ["dec-2037-2019"]),
                                            ("2020-03-16", ["dec-405-2020"])], f"D267 art. 11 {H._shape(h)}")
    B23._need(h[0][1] == cons_lines, f"D267 art. 11 first text {h[0][1][:3]} {cons_lines[:3]}")
    units4 = ["Unidad de Investigaciones Especiales contra la Corrupción",
              "Unidad de Cooperación Nacional e Internacional de Prevención, Investigación e Incautación de Bienes",
              "Unidad de Apoyo Técnico al Congreso", "Unidad de Seguridad y Aseguramiento Tecnológico e Informático"]
    post = "Unidad Delegada para el Posconflicto"
    n16 = orig_lines.index("1.6. Oficina de Comunicaciones y Publicaciones.")
    n22 = orig_lines.index("2.2. Oficina de Capacitación, Producción de Tecnología y Cooperación Técnica Internacional.")
    B23._need(orig_lines[n16 + 1] == "2. Despacho del Vicecontralor." and n22 > n16, "D267 art. 11 original")
    v2011 = orig_lines[:n16 + 1] + units4 + orig_lines[n16 + 1:]
    c17, c18 = [l for l in cons_lines if l.startswith("1.7 ")], [l for l in cons_lines if l.startswith("1.8 ")]
    B23._need(len(c17) == 1 and len(c18) == 1 and cons_lines.count(post) == 1 and cons_lines.count("2.2") == 1, "cons")
    v2016 = [("2.2" if l == orig_lines[n22] else l) for l in v2011]
    v2016 = v2016[:n16 + 1] + c17 + c18 + v2016[n16 + 1:]
    v2017 = cons_lines
    B23._need([l for l in v2017 if l != post] == v2016, f"D267 art. 11 2016 text {v2016[:20]} {v2017[:20]}")
    k888, k1474 = E.register("dec-888-2017"), E.register("ley-1474-2011")
    B23._need(E.law_day(k888) == "2017-05-27" and E.law_day(k1474) == "2011-07-12",
              f"D267 art. 11 law days {E.law_day(k888)} {E.law_day(k1474)}")
    H._set(act, key, H._label(act, key), [(None, orig_lines, None), ("2011-07-12", v2011, "ley-1474-2011"),
                                          ("2016-09-01", v2016, "ley-1807-2016"), ("2017-05-27", v2017, k888)]
           + [(d, b, c[0]) for d, b, c in h[1:]])
    B23._forget(D267, key)
    H._done(T267, fix_267_11)


H.FIXES.setdefault("contraloria-general-de-la-republica", []).append(fix_267_11)


D262, T262 = "decreto_0262_2000", ("Estructura y organización de la Procuraduría General de la Nación (Decreto Ley 262 de "
                                   "2000)")
N38 = ("38. Organizar las dependencias de la Procuraduría General de la Nación para su adecuado funcionamiento conforme a "
       "las reglas y principios establecidos en este decreto y denominarlas, de acuerdo con")


def fix_262_7(act):
    """art. 7, numeral 38 of the original text: the words 'y denominarlas', struck by Sentencia C-429-01 (2 May 2001), as
    the numeral's Jurisprudencia Vigencia box gives it ('salvo el aparte tachado que se declara INEXEQUIBLE') and its
    earlier-text box prints them struck, stand until that day and leave on it, credited to the ruling; the engine had
    kept them until Decreto Ley 1851 de 2021 replaced the article."""
    B23, E = H.B23, H.E
    u = B23._unit(D262, "7")
    B23._need("Numeral 38 del texto original declarado EXEQUIBLE por la Corte Constitucional mediante Sentencia C-429-01 de "
              "2 de mayo de 2001" in H._jv(u) and "salvo el aparte tachado que se declara INEXEQUIBLE" in H._jv(u), "D262 art. 7 JV")
    raw = [it[2] for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" and "<p>38. &lt;Aparte tachado" in it[2]]
    B23._need(raw and all("este decreto <S><span class='b_aj'>y denominarlas</span></S>, de acuerdo" in r for r in raw),
              "D262 art. 7 box 38")
    key = "art-0007"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2000-03-03", None), ("2022-03-29", ["dec-1851-2021"])], f"D262 art. 7 {H._shape(h)}")
    first = h[0][1]
    k = [i for i, l in enumerate(first) if l.startswith(N38)]
    B23._need(len(k) == 1 and first[k[0]].count(" y denominarlas,") == 1, "D262 art. 7 numeral 38")
    after = first[:k[0]] + [first[k[0]].replace(" y denominarlas,", ",")] + first[k[0] + 1:]
    vs = act["versions"]  # the ruling's day has a credit-only version (no unit texts): it gets the texts before it
    for i, v in enumerate(vs):
        if v["from"] == "2001-05-02" and "units" not in v:
            v["units"] = dict(next(p for p in reversed(vs[:i]) if "units" in p)["units"])
    H._set(act, key, H._label(act, key), [(None, first, None), ("2001-05-02", after, "c-429-01"), ("2022-03-29", h[1][1], "dec-1851-2021")])
    B23._forget(D262, key)
    H._done(T262, fix_262_7)


H.FIXES.setdefault("procuraduria-general-de-la-nacion", []).append(fix_262_7)


INC28 = "Los Procuradores Delegados que intervengan como agentes del Ministerio Público ante la jurisdicción de lo contencioso"


def fix_262_28(act):
    """art. 28: the inciso that Ley 1367 de 2009 art. 2 added (Diario Oficial of 21 December 2009) and Ley 2220 de 2022
    art. 146 repealed from 30 December 2022 is printed on the page under both markers; the engine showed the placeholder
    for the whole article between those days and the inciso after its repeal. The article's first two paragraphs stand
    throughout; the printed inciso stands from 21 December 2009 and leaves on 30 December 2022, credited to Ley 2220."""
    B23, E = H.B23, H.E
    u = B23._unit(D262, "28")
    B23._need("Inciso derogado por el artículo 146 de la Ley 2220 de 2022" in H._nv(u) and "Rige a partir del 30 de "
              "diciembre de 2022" in H._nv(u) and "Inciso adicionado por el artículo 2 de la Ley 1367 de 2009, publicada en "
              "el Diario Oficial No. 47.570 de 21 de diciembre de 2009" in H._nv(u), "D262 art. 28 NV")
    ps = [E.tidy(E.to_text(it[1])) for it in u["items"] if it[0] == "p"]
    inc = [p for p in ps if p.startswith(INC28)]
    B23._need(len(inc) == 1, f"D262 art. 28 inciso {ps}")
    key = "art-0028"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2000-03-03", None), ("2009-12-21", ["ley-1367-2009"]),
                                            ("2022-12-30", ["ley-2220-2022"])]
              and h[1][1] == [H.PH] and h[2][1] == h[0][1] + inc, f"D262 art. 28 {H._shape(h)}")
    H._set(act, key, H._label(act, key), [(None, h[0][1], None), ("2009-12-21", h[0][1] + inc, "ley-1367-2009"),
                                          ("2022-12-30", h[0][1], "ley-2220-2022")])
    B23._forget(D262, key)
    H._done(T262, fix_262_28)


H.FIXES.setdefault("procuraduria-general-de-la-nacion", []).append(fix_262_28)
