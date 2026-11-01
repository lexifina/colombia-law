"""Hand-set histories for batch 65 (Leyes 2272 de 2022, 1530 de 2012), installed by hand_fixes.install(); each checks the
page first."""
from __future__ import annotations

import hand_fixes as H

L1530, T1530 = "ley_1530_2012", "Sistema General de Regalías (Ley 1530 de 2012)"


def fix_1530_150(act):
    """art. 150: its Notas de Vigencia say 'Artículo modificado por el artículo 7 de la Ley 1608 de 2013', with no
    earlier-text box, so the engine gave it the placeholder before that act. Ley 1608 de 2013's own page shows that its
    art. 6 ('Adiciónese el artículo 150 de la Ley 1530 de 2012') only added the parágrafo the page marks '<Parágrafo
    adicionado por el artículo 6 de la Ley 1608 de 2013>' (its art. 7 rewrites Ley 1438 de 2011 art. 50). The article
    reads as printed without that parágrafo from the act's first day; the parágrafo arrives on 2 January 2013, credited
    to Ley 1608 de 2013."""
    B23, E = H.B23, H.E
    u = B23._unit(L1530, "150")
    B23._need("Artículo modificado por el artículo 7 de la Ley 1608 de 2013" in H._nv(u)
              and not B23._boxes(u, "Legislación Anterior"), "L1530 art. 150 note")
    a6 = E.plain(" ".join(it[1] for it in B23._unit("ley_1608_2013", "6")["items"] if it[0] == "p"))
    B23._need("Se adiciona el siguiente parágrafo al artículo 150 de la Ley 1530 de 2012" in a6, "Ley 1608 art. 6")
    ps = [E.plain(it[1]) for it in u["items"] if it[0] == "p"]
    B23._need(sum("Parágrafo adicionado por el artículo 6 de la Ley 1608 de 2013" in p for p in ps) == 1, "L1530 art. 150 marker")
    key = "art-0150"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2012-05-17", None), ("2013-01-02", ["ley-1608-2013"])]
              and h[0][1] == [H.PH], f"L1530 art. 150 {H._shape(h)}")
    today = h[1][1]
    k = [i for i, l in enumerate(today) if l.startswith("PARÁGRAFO.")]
    B23._need(len(k) == 1 and k[0] == len(today) - 1, "L1530 art. 150 parágrafo")
    H._set(act, key, H._label(act, key), [(None, today[:k[0]], None), ("2013-01-02", today, "ley-1608-2013")])
    B23._forget(L1530, key)
    H._done(T1530, fix_1530_150)


H.FIXES.setdefault("sistema-general-de-regalias-2012", []).append(fix_1530_150)


L2272, T2272 = "ley_2272_2022", "Política de paz de Estado y prórroga de la Ley 418 de 1997 (Ley 2272 de 2022)"
JUICIO = "serán los que a juicio del Gobierno nacional sean necesarios para pacificar"
LIBERTAD = "a la conflictividad social, y se encuentren en privación de libertad."
DIH = ("hostilidades, hacen parte del DIH, conforme a lo dispuesto en los artículos 93 y 94 de la Constitución Política, en "
       "consecuencia,] serán vinculantes")


def fix_2272_5(act):
    """art. 5 (Ley 418 de 1997 art. 8 as rewritten, quoted): the expressions 'a juicio del Gobierno nacional' and 'y se
    encuentren en privación de libertad' were struck by Sentencia C-525-23 (29 November 2023) and the words 'hacen parte
    del DIH, conforme a lo dispuesto en los artículos 93 y 94 de la Constitución Política, en consecuencia,' by Sentencia
    C-036-25 (5 February 2025), as the article's Jurisprudencia Vigencia boxes give them; the engine had taken all three out
    on the later day. Each now leaves on its own ruling's day, leaving the punctuation the page prints around it (', .',
    ', ] serán'); the bracket ']' the page prints after the words C-036-25 struck is shown only from that ruling."""
    B23, E = H.B23, H.E
    u = B23._unit(L2272, "5")
    jv = H._jv(u)
    B23._need('Declarar INEXEQUIBLE, por el cargo analizado, la expresión "a juicio del gobierno nacional"' in jv
              and 'Expresión tachada "y se encuentren en privación de libertad" declarada INEXEQUIBLE' in jv
              and "Sentencia C-525-23 de 29 de noviembre de 2023" in jv
              and "Aparte tachado 'hacen parte del DIH, conforme a lo dispuesto en los artículos 93 y 94 de la Constitución "
                  "Política, en consecuencia,' declarado INEXEQUIBLE" in jv and "Sentencia C-036-25 de 5 de febrero" in jv,
              "L2272 art. 5 JV")
    key = "art-0005"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [("2022-11-04", None), ("2025-02-05", ["c-036-25"])], f"L2272 art. 5 {H._shape(h)}")
    first, today = h[0][1], h[1][1]

    def sub(lines, old, new):
        k = [i for i, l in enumerate(lines) if old in l]
        B23._need(len(k) == 1 and lines[k[0]].count(old) == 1, f"L2272 art. 5: {old[:40]}")
        return lines[:k[0]] + [lines[k[0]].replace(old, new)] + lines[k[0] + 1:]

    v0 = sub(first, DIH, DIH.replace(",] ", ", "))
    v1 = sub(sub(v0, JUICIO, JUICIO.replace("a juicio del Gobierno nacional ", "")), LIBERTAD, "a la conflictividad social,.")
    B23._need(sub(v1, DIH.replace(",] ", ", "), "hostilidades, ] serán vinculantes") == today, "L2272 art. 5 today")
    H._set(act, key, H._label(act, key), [(None, v0, None), ("2023-11-29", v1, "c-525-23"), ("2025-02-05", today, "c-036-25")])
    B23._forget(L2272, key)
    H._done(T2272, fix_2272_5)


H.FIXES.setdefault("paz-total", []).append(fix_2272_5)
