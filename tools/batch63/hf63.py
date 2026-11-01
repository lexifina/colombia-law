"""Hand-set histories for batch 63 (Leyes 1739 de 2014, 788 de 2002, 863 de 2003), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import hand_fixes as H

L1739, T1739 = "ley_1739_2014", "Reforma tributaria (Ley 1739 de 2014)"
L788, T788 = "ley_0788_2002", "Reforma tributaria (Ley 788 de 2002)"
L863, T863 = "ley_0863_2003", "Reforma tributaria (Ley 863 de 2003)"


def _errata(key, label, day, title):
    H.E.LAWS.setdefault(key, {"label": label, "title": title, "kind": "publisher", "enacted": day, "published": day,
                              "url": None, "temporary_until": None, "restores": None,
                              "note": "A correction of a printing error in the act as first published (fe de erratas); "
                                      "the corrected words are the act's own."})
    return key


def _orig_lines(u, start):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        try:
            ls = H.B23._box_lines(b, "Texto original", True)
        except StopIteration:
            continue
        if ls and ls[0].startswith(start):
            return ls
    H.B23._need(False, f"box starting {start!r}")


def fix_1739_29(act):
    """art. 29 (Estatuto Tributario art. 254, quoted): literal d) as first published ('... hayan estado gravado ... por la
    proposición de que trata el literal h) ...', the earlier-text box) until the fe de erratas published in Diario
    Oficial No. 49.977 of 26 August 2016 corrected it ('gravados', 'proporción'); the corrected words from that day."""
    B23, E = H.B23, H.E
    u = B23._unit(L1739, "29")
    B23._need("Literal corregido mediante Fe de Erratas publicada en el Diario Oficial No. 49.977 de 26 de agosto de 2016"
              in H._nv(u), "L1739 art. 29 note")
    old = _orig_lines(u, "d) Cuando los dividendos")
    B23._need(len(old) == 1, "L1739 art. 29 box")
    key = "art-0029"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 1, f"L1739 art. 29 {H._shape(h)}")
    today = h[0][1]
    k = [i for i, l in enumerate(today) if l.startswith("d) Cuando los dividendos")]
    B23._need(len(k) == 1 and today[k[0]] != old[0], "L1739 art. 29 literal d)")
    first = today[:k[0]] + old + today[k[0] + 1:]
    law = _errata("fe-de-erratas-2016-08-26", "Fe de erratas, Diario Oficial No. 49.977 de 26 de agosto de 2016",
                  "2016-08-26", "Fe de erratas de la Ley 1739 de 2014, Diario Oficial No. 49.977")
    H._set(act, key, H._label(act, key), [(None, first, None), ("2016-08-26", today, law)])
    B23._forget(L1739, key)
    H._done(T1739, fix_1739_29)


def fix_788_28(act):
    """art. 28 (Capítulo XI of the Estatuto Tributario's Título I, quoted): the quoted arts. 260-6 (Jurisdicción de menor
    imposición fiscal) and 260-9 (Interpretación), which the page gives only in their earlier-text boxes, stand with their
    words until Sentencia C-690-03 (12 August 2003) struck them; from that day each keeps only its heading line, as the
    page prints it. The engine had left their words out of every version."""
    B23, E = H.B23, H.E
    key = "art-0028"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 1, f"L788 art. 28 {H._shape(h)}")
    today = h[0][1]
    u = B23._unit(L788, "28")
    jv = H._jv(u)
    first = list(today)
    for n, head, start in (("260-6", "Artículo 260-6. Jurisdicción de menor imposición fiscal.", "Salvo prueba en contrario"),
                           ("260-9", "Artículo 260-9. Interpretación.", "Para la interpretación")):
        B23._need(f"Artículo {n} declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-690-03 de 12 de "
                  "agosto de 2003" in jv, f"L788 art. 28 {n} JV")
        box = _orig_lines(u, start)
        k = [i for i, l in enumerate(first) if l == head]
        B23._need(len(k) == 1, f"L788 art. 28 {n} heading")
        first = first[:k[0]] + [head + " " + box[0]] + box[1:] + first[k[0] + 1:]
    c = E.add_court("C-690-03", "2003-08-12", "c-690_2003.html")
    E.LAWS[c]["note"] = None
    H._set(act, key, H._label(act, key), [(None, first, None), ("2003-08-12", today, c)])
    B23._forget(L788, key)
    H._done(T788, fix_788_28)


CAP5 = "### CAPITULO V. IMPUESTOS TERRITORIALES. IMPUESTO AL CONSUMO DE LICORES, VINOS, APERITIVOS, Y SIMILARES"
GASOLINA = "### SOBRETASA A LA GASOLINA"


def fix_788_54(act):
    """art. 54 (Cesión del IVA): the words as enacted (the earlier-text box) until Ley 1111 de 2006 art. 78 repealed the
    inciso 'El impuesto liquidado en ningún caso podrá ser afectado con impuestos descontables, salvo el correspondiente a
    los productores oficiales ...' (27 December 2006; Ley 1151 de 2007's later repeal of that inciso of art. 78 revived
    nothing, Ley 153 de 1887 art. 14, as the page's editor notes); the whole article out on 1 January 2017 (Ley 1816 de
    2016 art. 42). 'SOBRETASA A LA GASOLINA', which the page prints after the repeal marker, is the heading of the next
    articles, not words of art. 54: it stands in titulos.md under Capítulo V from the act's first day."""
    B23, E = H.B23, H.E
    u = B23._unit(L788, "54")
    nv = H._nv(u)
    B23._need("Aparte tachado derogado por el artículo 78 de la Ley 1111 de 2006" in nv
              and "Artículo derogado por el artículo 42 de la Ley 1816 de 2016" in nv, "L788 art. 54 notes")
    key = "art-0054"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 2 and h[1][0] == "2017-01-01" and h[1][2] == "ley-1816-2016", f"L788 art. 54 {H._shape(h)}")
    first = h[0][1]
    gone = [l for l in first if l.startswith("El impuesto liquidado en ningún caso podrá ser afectado")]
    B23._need(len(gone) == 1, "L788 art. 54 inciso")
    mid = [l for l in first if l not in gone]
    l1111 = E.register("ley-1111-2006")
    H._set(act, key, H._label(act, key), [(None, first, None), ("2006-12-27", mid, l1111),
                                          ("2017-01-01", None, "ley-1816-2016")])
    B23._forget(L788, key)
    n = 0
    for v in act["versions"]:
        t = ((v.get("units") or {}).get("titulos") or {}).get("text")
        if t is None:
            continue
        ls = t.split("\n")
        B23._need(ls.count(CAP5) == 1 and GASOLINA not in ls, "L788 titulos")
        i = ls.index(CAP5)
        ls = ls[:i + 1] + [GASOLINA] + ls[i + 1:]
        v["units"] = dict(v["units"], titulos=dict(v["units"]["titulos"], text="\n".join(ls)))
        n += 1
    B23._need(n >= 1, "L788 titulos versions")
    H._done(T788, fix_788_54)


def fix_863_14(act):
    """art. 14 (Estatuto Tributario art. 499, quoted): numeral 3 ('Que su establecimiento de comercio ... no se encuentre
    ubicado en un centro comercial o dentro de almacenes de cadena ...'), which the page gives only in its earlier-text
    box, stands until Sentencia C-1114-04 (9 November 2004) struck it; from that day the line reads '3.', as the page
    prints it. The engine had left its words out of every version."""
    B23, E = H.B23, H.E
    u = B23._unit(L863, "14")
    B23._need("Numeral 3. declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1114-04 de 9 de noviembre "
              "de 2004" in H._jv(u), "L863 art. 14 JV")
    box = _orig_lines(u, "3. Que su establecimiento")
    key = "art-0014"
    h = H._one(H._hist(act, key), key)
    B23._need(len(h) == 1, f"L863 art. 14 {H._shape(h)}")
    today = h[0][1]
    k = [i for i, l in enumerate(today) if l == "3."]
    B23._need(len(k) == 1 and today[k[0] + 1].startswith("4. Que en el establecimiento") and len(box) == 1,
              "L863 art. 14 numerals")
    first = today[:k[0]] + box + today[k[0] + 1:]
    c = E.add_court("C-1114-04", "2004-11-09", "c-1114_2004.html")
    E.LAWS[c]["note"] = None
    H._set(act, key, H._label(act, key), [(None, first, None), ("2004-11-09", today, c)])
    B23._forget(L863, key)
    H._done(T863, fix_863_14)


H.FIXES["reforma-tributaria-2014"] = [fix_1739_29]
H.FIXES["reforma-tributaria-2002"] = [fix_788_28, fix_788_54]
H.FIXES["reforma-tributaria-2003"] = [fix_863_14]
