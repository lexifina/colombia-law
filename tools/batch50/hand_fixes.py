"""Hand-set histories for batch 50 (bound by parse_batch50.py through install(); each checks the page first)."""
from __future__ import annotations

import re

D = B23 = B29 = B13 = E = P = None
L222 = "ley_0222_1995"
T222 = "Régimen de sociedades (Ley 222 de 1995)"
FIXES: dict = {}


def _done(title, fn):
    B29.HAND_DONE.append(f"{title}: " + " ".join(fn.__doc__.split()))


def _hist(act, key):
    out, last = [], object()
    for v in act["versions"]:
        if "units" in v:
            t = (v["units"].get(key) or {}).get("text")
            if t != last:
                out.append((v["from"], t, v["credits"].get(key)))
                last = t
    return out


def fix_222_44(act):
    """Ley 222 de 1995, art. 44: Sentencia C-290-97 (16 June 1997) struck the article 'salvo los apartes no tachados' and
    set out how it reads from then on (the page prints that reading under '<Artículo INEXEQUIBLE, salvo los apartes no
    tachados ...>'); the engine had read the marker as the whole article struck. The original text until the ruling,
    the remaining words from its day, credited to it."""
    u = B23._unit(L222, "44")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("Artículo declarado INEXEQUIBLE por la Corte Constitucional, mediante Sentencia C-290-97 del 16 de junio de "
              "1997, salvo los apartes no tachados" in jv, "Ley 222 art. 44 C-290-97")
    ps = [E.tidy(E.plain(it[1])) for it in u["items"] if it[0] == "p"]
    m = re.match(r"<Artículo INEXEQUIBLE, salvo los apartes no tachados, ver Legislación Anterior\. La Corte Constitucional "
                 r"en la sentencia C-290-97 deja establecido el nuevo texto de este artículo así:>\s*(.*)", ps[0])
    B23._need(m and len(ps) == 3, f"Ley 222 art. 44 text {ps[:1]}")
    h = _hist(act, "art-0044")
    B23._need([(d, c) for d, _, c in h] == [("1996-06-20", None), ("1997-06-16", ["c-290-97"])] and h[1][1] is None,
              f"Ley 222 art. 44 history {[(d, c) for d, _, c in h]}")
    first = h[0][1].split("\n")[1:-1]
    B23._need(first[0].startswith("EXPEDICION DE REGLAMENTOS. Corresponde al Gobierno Nacional"), "Ley 222 art. 44 first")
    new = ["EXPEDICION DE REGLAMENTOS. " + m.group(1)] + ps[1:]
    B13.B6.set_history(act, "art-0044", "Art. 44", [(None, "\n".join(first), None),
                                                     ("1997-06-16", "\n".join(new), "c-290-97")])
    B23._forget(L222, "art-0044")
    _done(T222, fix_222_44)


FIXES["regimen-de-sociedades-1995"] = [fix_222_44]


L550 = "ley_0550_1999"
T550 = "Reestructuración empresarial (Ley 550 de 1999)"


def fix_550_61(act):
    """Ley 550 de 1999, art. 61: its Notas de Vigencia read 'Artículo derogado en cuanto a "lista a cargo de la
    Superintendencia de Industria y Comercio", por el artículo 39 de la Ley 1673 de 2013' and the page prints the
    article's words with no part struck and no earlier text; the engine had put the placeholder before Ley 1673 de 2013
    and the printed words after it. The printed words stand from the act's first day; Ley 1673's partial repeal names no
    words of the article, so it changes none here."""
    u = B23._unit(L550, "61")
    nv = " ".join(E.plain(b) for b in B23._boxes(u, "Notas de Vigencia"))
    B23._need(nv.strip().startswith("- Artículo derogado en cuento a 'lista a cargo de la Superintendencia de Industria y "
                                    "Comercio', por el artículo 39 de la Ley 1673 de 2013")
              and not B23._boxes(u, "Legislación Anterior"), "Ley 550 art. 61 notes")
    h = _hist(act, "art-0061")
    B23._need([(d, c) for d, _, c in h] == [("1999-12-30", None), ("2014-01-19", ["ley-1673-2013"])]
              and "[La fuente no da" in h[0][1], f"Ley 550 art. 61 history {[(d, c) for d, _, c in h]}")
    lines = h[1][1].split("\n")
    B13.B6.set_history(act, "art-0061", lines[0][2:], [(None, "\n".join(lines[1:-1]), None)])
    B23._forget(L550, "art-0061")
    _done(T550, fix_550_61)


FIXES["reestructuracion-empresarial-1999"] = [fix_550_61]


def run(slug):
    def go(act):
        for f in FIXES.get(slug, []):
            f(act)
    return go


def install(driver):
    global D, B23, B29, B13, E, P
    D = driver
    B23, B29, B13, E, P = D.B23, D.B29, D.B13, D.E, D.P
    B29.HAND_FIXES.update({s: run(s) for s in FIXES})
