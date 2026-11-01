"""Hand-set histories for batch 108 (Ley 794 de 2003), installed by hand_fixes.install(); each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L794, S794 = "ley_0794_2003", "reforma-del-procedimiento-civil-2003"
T794 = "Reforma del Código de Procedimiento Civil (Ley 794 de 2003)"
LAW794 = "ley-794-2003"
EARLY = {"41": ("El artículo 388 del Código de Procedimiento Civil, quedará así:",
                "Cuando haya lugar a remuneración o reembolso de honorarios por concepto de un dictamen pericial, en ningún "
                "caso se podrán exceder las tarifas señaladas por el Consejo Superior de la Judicatura, las cuales deberán "
                "ser fijadas dentro de los tres (3) meses siguientes a la promulgación de la presente ley."),
         "58": ("El artículo 528 del Código de Procedimiento Civil, quedará así:",
                "PARÁGRAFO 2o. La Superintendencia de Notariado y Registro fijará las tarifas de los derechos notariales que "
                "se cobrarán por la realización de las diligencias de remate. Las tarifas de las Cámaras de Comercio y "
                "Martillos serán fijadas por el Gobierno Nacional. Para estos efectos, las entidades dispondrán de un "
                "término de tres (3) meses contados a partir de la promulgación de la presente ley.\"")}


def fix_44(act):
    """Ley 794 de 2003, art. 44 (CPC art. 424, restitución del inmueble arrendado): the page prints parágrafo 5o.'s first
    inciso as '<Inciso INEXEQUIBLE>' and gives its words in the 'Texto original de la Ley 794 de 2003' box; Sentencia
    C-503-05 (17 May 2005) held it struck, as res judicata of C-798-03 (which had struck the same words in CPC art. 31,
    written by this act's art. 8). The engine had dropped the words from every version (no dated ruling). Now the inciso
    reads the box's words (the editor's closing quote mark out) from the act's start to 17 May 2005, then goes, credited
    to the ruling, as the Código de Procedimiento Civil part has it for art. 424."""
    E = H.E
    u = H.B23._unit(L794, "44")
    jv = H._jv(u)
    H.B23._need("mediante Sentencia C-503-05 de 17 de mayo de 2005" in jv and "cosa juzgada material" in jv
                and "PARÁGRAFO 5o." in H._printed(u), "L794 art. 44 page")
    box = H.B23._boxes(u, "Legislación Anterior")
    H.B23._need(len(box) == 1, "L794 art. 44 box")
    old = H.B23._box_lines(box[0], "Texto original de la Ley 794 de 2003", True)
    H.B23._need(len(old) == 1 and old[0].startswith("PARÁGRAFO 5. Cumplimiento de la sentencia.")
                and old[0].endswith("del juez'."), f"L794 art. 44 box {old}")
    line = old[0][:-2] + "."
    h = H._hist(act, "art-0044")
    H.B23._need(len(h) == 1, f"L794 art. 44 shape {H._shape(h)}")
    now = h[0][1]
    k = [i for i, x in enumerate(now) if x == "PARÁGRAFO 5o."]
    H.B23._need(len(k) == 1, "L794 art. 44 PARÁGRAFO 5o. line")
    before = now[:k[0]] + [line] + now[k[0] + 1:]
    c503 = E.add_court("C-503-05", "2005-05-17", "c-503_2005.html")
    H._set(act, "art-0044", H._label(act, "art-0044"), [(None, before, None), ("2005-05-17", now, c503)])
    H.B23._forget(L794, "art-0044")
    H._done(T794, fix_44)


def fix_start(act):
    """Ley 794 de 2003, art. 70 (coordinator decision, twenty-seventh session): 'La presente ley entrará a regir tres (3)
    meses después de su promulgación, salvo lo que se dispone para los artículos 388 inciso final y parágrafo 2o del
    artículo 528, los cuales entrarán a regir a partir de la promulgación de esta ley.' Promulgated in Diario Oficial No.
    45.058 of 9 January 2003: the first version, of 9 January 2003, holds only art. 41's opening words and the last
    inciso of CPC art. 388 as it writes it, and art. 58's opening words and parágrafo 2o of CPC art. 528 as it writes
    it; on 9 April 2003 the rest of those two articles and every other article (art. 70 included) are added, credited
    to the act (phase2/late.py, as for Ley 640 de 2001), as the Código de Procedimiento Civil part dates them."""
    import late
    E, P, B23 = H.E, H.P, H.B23
    pub = act["versions"][0]["from"]
    later = E.add_months(pub, 3)
    B23._need((pub, later) == ("2003-01-09", "2003-04-09"), f"L794 days {pub} {later}")
    nums = [E.label_num(u["label"] or "") for u in P.doc_units(L794)[1:]]
    nums = [n for n in nums if n]
    B23._need(nums == [str(i) for i in range(1, 71)], f"L794 articles {nums}")
    hs = {}
    for n, (intro, last) in EARLY.items():
        key = E.unit_key(n)[0]
        h = H._hist(act, key)
        full = h[0][1]
        B23._need(full[0] == intro and full[-1] == last and full.count(last) == 1, f"L794 art. {n} lines")
        hs[n] = (key, h)
    late.late_start(act, [n for n in nums if n not in EARLY], later, LAW794, L794, P, E, B23)
    late.FOLDED.clear()
    for n, (key, h) in hs.items():
        intro, last = EARLY[n]
        full = h[0][1]
        tl = [(None, [intro, last], None), (later, full, LAW794)]
        # events after the start that changed no words keep their day and credit (C-798-03's condition on art. 58)
        B23._need(len(h) == 1, f"L794 art. {n}: words changed {H._shape(h)}")
        for v in act["versions"]:
            c = v["credits"].get(key)
            if c and v["from"] > later:
                B23._need(len(c) == 1 and c[0] != LAW794, f"L794 art. {n}: {v['from']} {c}")
                tl.append((v["from"], full, c[0]))
        H._set(act, key, H._label(act, key), sorted(tl, key=lambda x: x[0] or ""))
        B23._forget(L794, key)
    H._done(T794, fix_start)


def note_11(act):
    """Ley 794 de 2003, art. 11 (CPC art. 91), numeral 2: Sentencia C-662-04 (8 July 2004) declared it INEXEQUIBLE only
    'en cuanto se refiere' to the exceptions of lack of jurisdiction and of arbitration agreement (CPC art. 97 nums. 1 and
    3), with an integrating rule in their place; the page still prints the numeral's words, under a marker. No words of
    the article changed on that day, so the ruling makes no version (as for other rulings that leave the words)."""
    u = H.B23._unit(L794, "11")
    H.B23._need("Numeral declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-662-04 de 8 de julio de 2004"
                in H._jv(u) and "en cuanto se refiere a la excepción de falta de jurisdicción" in H._jv(u), "L794 art. 11 page")
    h = H._hist(act, "art-0011")
    H.B23._need(len(h) == 1 and any(x.startswith("2. Cuando el proceso termine") for x in h[0][1]), "L794 art. 11 shape")
    H._done(T794, note_11)


H.FIXES[S794] = [fix_44, note_11, fix_start]
