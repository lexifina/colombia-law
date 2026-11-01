"""Hand-set histories for batch 98 (Leyes 633 de 2000 and 488 de 1998), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L488, T488, S488 = "ley_0488_1998", "Reforma tributaria (Ley 488 de 1998)", "reforma-tributaria-1998"
BRACED_488 = "{del año inmediatamente anterior}"


def fix_488_48_braces(act):
    """Ley 488 de 1998, art. 48 (Estatuto Tributario art. 476 as rewritten), numeral 21: the page writes 'a 31 de
    diciembre {del año inmediatamente anterior}', braces its 'Legislación Anterior' boxes explain as words the decrees
    that updated the absolute values for 2003-2006 left out of their tables ('textos entre corchetes {...} omitidos por
    el Decreto ...'). A decree that updates values does not change a law's words: the words stand in every version,
    without the braces (as in the Estatuto Tributario's own history)."""
    u = H.B23._unit(L488, "48")
    raw = " ".join(it[1] if it[0] == "p" else it[2] for it in u["items"])
    H.B23._need(raw.count("textos entre corchetes {...} omitidos por el Decreto") >= 4, "L488 art. 48 brace boxes")
    n = 0
    for v in act["versions"]:
        for us in (v.get("units") or {}, v.get("changes") or {}):
            x = us.get("art-0048")
            if x and BRACED_488 in (x.get("text") or ""):
                x["text"] = x["text"].replace(BRACED_488, BRACED_488[1:-1])
                n += 1
    H.B23._need(n >= 1, "L488 art. 48 braced versions")
    H._done(T488, fix_488_48_braces)


H.FIXES.setdefault(S488, []).append(fix_488_48_braces)


L633, T633, S633 = "ley_0633_2000", "Reforma tributaria (Ley 633 de 2000)", "reforma-tributaria-2000"


def _box_text(page, num, head):
    """The article's earlier text from its 'Legislación Anterior' box headed `head`, its 'ARTICULO N.' heading out."""
    E = H.E
    u = H.B23._unit(page, num)
    paras = [E.tidy(E.to_text(p, False)) for b in H.B23._boxes(u, "Legislación Anterior") for p in E.box_paras(b)]
    paras = [t for t in paras if re.search(r"\w", t)]
    k = [i for i, t in enumerate(paras) if t.startswith(head)]
    H.B23._need(len(k) == 1, f"{page} {num}: box '{head}'")
    first = re.sub(r"^" + re.escape(head) + r"\s*", "", paras[k[0]])
    out = ([first] if first else []) + paras[k[0] + 1:]
    out[0] = re.sub(r"^ART[ÍI]CULO " + num + r"o?\.\s*", "", out[0])
    H.B23._need(out and not any(t.startswith("Texto ") for t in out), f"{page} {num}: box lines")
    return out


# Whole articles the page marks '<Artículo declarado INEXEQUIBLE ...>' (phase2/engine.py reads only '<Artículo
# INEXEQUIBLE>' as a whole-article strike, so these articles were in no version): page, num, ruling, day, href, epigraph.
WHOLE = [
    (L633, "4", "C-992-01", "2001-09-19", "c-992_2001.html", "BENEFICIO ESPECIAL DE AUDITORIA."),
    (L488, "28", "C-740-99", "1999-10-06", "c-740_1999.html", "REGIMEN UNIFICADO DE IMPOSICION (RUI) PARA PEQUEÑOS CONTRIBUYENTES."),
    (L488, "96", "C-816-99", "1999-10-20", "c-816_1999.html", None),
]
GONE = {}


def _whole(page, num, rid, day, href, epi, title):
    def fix(act):
        """Whole article struck ('<Artículo declarado INEXEQUIBLE>')."""
        E = H.E
        u = H.B23._unit(page, num)
        p0 = E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
        H.B23._need(p0.strip() == "<Artículo declarado INEXEQUIBLE>", f"{page} {num}: marker")
        jv = H._jv(u)
        d = day.split("-")
        H.B23._need(f"Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia {rid}" in jv, f"{page} {num}: ruling")
        key = E.unit_key(num)[0]
        body = _box_text(page, num, "Texto original de la Ley " + ("633 de 2000:" if page == L633 else "488 de 1998:"))
        if epi:
            body = [epi] + ([body[0][len(epi):].strip()] if body[0].startswith(epi) else [body[0]]) + body[1:]
        c = E.add_court(rid, day, href)
        h = H._hist(act, key)
        if getattr(E, "DECL_WHOLE", False) and any(b is not None for _, b, _ in h):
            # (twenty-second session) with E.DECL_WHOLE on the engine reads the marker itself: its history must be the
            # box text (without the epigraph the page prints in the heading only) until the ruling; the epigraph is added
            bare = body[1:] if epi else body
            H.B23._need([(b, cr) for _, b, cr in h] == [(bare, None), (None, [c])] and h[1][0] == day,
                        f"{page} {num}: engine history {H._shape(h)}")
        else:
            H.B23._need(all(b is None for _, b, _ in h), f"{page} {num}: already there")
        H._set(act, key, f"Art. {num}", [(None, body, None), (day, None, c)])
        H.B23._forget(page, key)
        H.B29.HAND_DONE.append(f"{title}: art. {num}: the page marks the whole article '<Artículo declarado INEXEQUIBLE>' "
                               f"(struck by Sentencia {rid}). Its text as enacted (the page's 'Texto original' box"
                               + (", with the epigraph the page prints in the article's heading" if epi else "")
                               + f") stands from the act's first day until the ruling ({day}).")
    return fix


for _p, _n, _r, _d, _h, _e in WHOLE:
    H.FIXES.setdefault(S633 if _p == L633 else S488, []).append(_whole(_p, _n, _r, _d, _h, _e, T633 if _p == L633 else T488))


def fix_488_77(act):
    """Ley 488 de 1998, art. 77 (adds ET art. 657-1): the page marks it '<Artículo declarado INEXEQUIBLE con excepción
    del numeral 5o. declarado exequible>' (Sentencia C-674-99, 9 September 1999) and prints only numeral 5; the engine
    gave that one numeral from the act's first day. The text as enacted (the page's 'Texto original' box) now stands
    until the ruling; from 9 September 1999 the article keeps its heading lines and numeral 5, credited to the ruling."""
    E = H.E
    u = H.B23._unit(L488, "77")
    jv = H._jv(u)
    H.B23._need("Artículo declarado INEXEQUIBLE, con excepción del numeral 5o. declarado EXEQUIBLE, por la Corte "
                "Constitucional mediante Sentencia C-674-99" in jv.replace("  ", " "), "L488 art. 77 ruling")
    h = H._hist(act, "art-0077")
    H.B23._need(len(h) == 1 and h[0][1][-1].startswith("5. Las personas comisionadas"), "L488 art. 77 shape")
    body = _box_text(L488, "77", "Texto original de la Ley 488 de 1998:")
    epi = "RETENCION DE MERCANCIAS A QUIENES COMPREN SIN FACTURA."
    H.B23._need(body[0].startswith(epi + " Adiciónase"), "L488 art. 77 box")
    body = [epi, body[0][len(epi):].strip()] + body[1:]
    c = E.add_court("C-674-99", "1999-09-09", "c-674_1999.html")
    H._set(act, "art-0077", H._label(act, "art-0077"), [(None, body, None), ("1999-09-09", h[0][1], c)])
    H.B23._forget(L488, "art-0077")
    H._done(T488, fix_488_77)


H.FIXES[S488].append(fix_488_77)


def fix_488_145(act):
    """Ley 488 de 1998, art. 145 (impuesto sobre vehículos automotores, tarifas): the page's earlier-text boxes give the
    brackets each yearly decree set, the last for 2025 (Decreto 1493 de 2024: 'a) Hasta $55.679.000 1,5%'); today's
    brackets are those Decreto 1457 de 2025 set for 2026 (the page's marker '<Valores absolutos que regirán a partir del
    1o. de enero de 2026, reajustados por el el artículo 1 del Decreto 1457 de 2025 ...>'), which the engine credited to
    Decreto 1493 de 2024 from 1 January 2025. Now the 2025 brackets stand from 1 January 2025 (Decreto 1493 de 2024) and
    today's from 1 January 2026 (Decreto 1457 de 2025). The 2023 box (Decreto 2588 de 2022) prints the same values as
    the 2022 one; that version changes no words."""
    E = H.E
    key = "art-0145"
    u = H.B23._unit(L488, "145")
    blk = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])
           if b["head"].startswith("Texto original de la Ley 488 de 1998 con los valores absolutos establecidos para el año "
                                   "2025 por el Decreto 1493 de 2024")]
    H.B23._need(len(blk) == 1, "L488 art. 145: 2025 box")
    new = E.block_text(blk[0]["paras"], False)
    H.B23._need(len(new) == 4 and new[0] == "1. Vehículos particulares:" and new[1] == "a) Hasta $55.679.000 1,5%",
                f"L488 art. 145: 2025 lines {new}")
    h = H._hist(act, key)
    H.B23._need(h[-1][0] == "2025-01-01" and h[-1][2] == ["dec-1493-2024"] and all(len(c or [None]) == 1 for _, _, c in h),
                f"L488 art. 145 shape {H._shape(h)}")
    today = h[-1][1]
    k = today.index("1. Vehículos particulares:")
    H.B23._need(today[k + 1] == "a) Hasta $57.349.000 1,5%" and today[k + 4].startswith("2. Motos"), "L488 art. 145 today")
    y2025 = today[:k] + new + today[k + 4:]
    law = E.register("dec-1457-2025")
    H.B23._need(E.law_day(law) == "2026-01-01", f"dec-1457-2025 in force {E.law_day(law)}")
    tl = [(None if i == 0 else d, b, (c or [None])[0]) for i, (d, b, c) in enumerate(h)]
    tl[-1] = ("2025-01-01", y2025, "dec-1493-2024")
    tl.append(("2026-01-01", today, law))
    H._set(act, key, H._label(act, key), tl)
    H._done(T488, fix_488_145)


H.FIXES[S488].append(fix_488_145)


def fix_488_48_n21(act):
    """Ley 488 de 1998, art. 48 (Estatuto Tributario art. 476), numeral 21 (added by Ley 788 de 2002): the page's boxes
    give its values for each year from 2003 to 2006; the engine left out the last box (the values Decreto 4715 de 2005
    set for 2006, '$3.576.812.000' and '$596.135.000') and gave the numeral's UVT wording from 1 January 2006, though
    Ley 1111 de 2006 (27 December 2006) put the values in UVT ('ajusta los valores absolutos en términos de UVT', the
    page's note). The 2006 values now stand from 1 January 2006 (Decreto 4715 de 2005) and the UVT wording from 27
    December 2006 (Ley 1111 de 2006), as the page gives them."""
    E = H.E
    key = "art-0048"
    u = H.B23._unit(L488, "48")
    blk = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])
           if b["head"].startswith("Texto adicionado por la Ley 788 de 2002 con los valores absolutos establecidos para el "
                                   "año 2006 por el Decreto 4715 de 2005")]
    H.B23._need(len(blk) == 1, "L488 art. 48: 2006 box")
    new = [l.replace(BRACED_488, BRACED_488[1:-1]) for l in E.block_text(blk[0]["paras"], False)][:2]
    H.B23._need(new[0].endswith("inferiores a $3.576.812.000.") and "$596.135.000" in new[1], f"L488 art. 48 n21 {new}")
    h = H._hist(act, key)
    days = [d for d, _, _ in h]
    H.B23._need("2006-01-01" in days and "2006-12-27" in days and days.index("2006-12-27") == days.index("2006-01-01") + 1,
                f"L488 art. 48 shape {days}")
    i = days.index("2006-01-01")
    body = list(h[i][1])
    k = [j for j, l in enumerate(body) if l.startswith("21. Los servicios de publicidad en periódicos")]
    H.B23._need(len(k) == 1 and body[k[0]].endswith("inferiores a 180.000 UVT.")
                and body[k[0] + 1].startswith("La publicidad en las emisoras de radio cuyas ventas sean inferiores a 30.000 UVT")
                and all(l in h[i + 1][1] for l in body[k[0]:k[0] + 2]), "L488 art. 48 n21 lines")
    body[k[0]:k[0] + 2] = new
    tl = [(None if j == 0 else d, b, (c or [None])[0] if len(c or []) < 2 else c) for j, (d, b, c) in enumerate(h)]
    tl[i] = (tl[i][0], body, tl[i][2])
    multi = [(j, c) for j, (_, _, c) in enumerate(h) if len(c or []) > 1]
    H._set(act, key, H._label(act, key), [(d, b, c[0] if isinstance(c, list) else c) for d, b, c in tl])
    for j, c in multi:  # versions crediting two acts keep both
        for v in act["versions"]:
            if v["from"] == h[j][0]:
                v["credits"][key] = c
    H._done(T488, fix_488_48_n21)


H.FIXES[S488].append(fix_488_48_n21)


def fix_633_80(act):
    """Ley 633 de 2000, art. 80 (subsidio de energía para distritos de riego): each year's budget law rewrote it tacitly
    ('Para el año 2022 debe entenderse modificado tácitamente por el artículo 100 de la Ley 2159 de 2021 ...'). The
    page's last boxes head two texts 'Texto modificado tácitamente por la Ley 2063 de 2020': the one whose parágrafo 3o.
    says the subsidy runs from 1 January 2021 is Ley 2063 de 2020's; the other (parágrafo 3o. 'El Gobierno nacional
    deberá reglamentar ...') is the 2022 text, which the page's notes give to Ley 2159 de 2021. The engine read both as
    one and gave today's text (Ley 2276 de 2022, for 2023) from Ley 2063's day. Now: Ley 2063's text from its day, Ley
    2159's from its day, today's from Ley 2276's. The Ley 2008 de 2019 box prints the page's marker inside the text
    ('Para el año 2020 modificado tácitamente por el artículo 125 de la Ley 2008 de 2019. El nuevo texto es el
    siguiente:>'); those words are left out."""
    E = H.E
    key = "art-0080"
    u = H.B23._unit(L633, "80")
    nv = H._nv(u)
    H.B23._need("Para el año 2022 debe entenderse modificado tácitamente por el artículo 100 de la Ley 2159 de 2021" in nv
                and "Para el año 2023 debe entenderse modificado tácitamente por el artículo 90 de la Ley 2276 de 2022" in nv,
                "L633 art. 80 notes")
    blks = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])]

    def body(b):
        ls = E.block_text(b["paras"], False)
        ls = [re.sub(r"^ART[ÍI]CULO 80\.+\s*", "", ls[0])] + ls[1:]
        return [x for x in ls if x]
    b63 = [b for b in blks if b["head"] == "Texto modificado tácitamente por la Ley 2063 de 2020:"]
    H.B23._need(len(b63) == 2, "L633 art. 80: two Ley 2063 boxes")
    by = {("2021" if "1 de enero del año 2021" in " ".join(body(b)) else "2022"): body(b) for b in b63}
    H.B23._need(sorted(by) == ["2021", "2022"] and by["2022"][-1].startswith("PARÁGRAFO 3o. El Gobierno nacional deberá"),
                "L633 art. 80: 2021/2022 boxes")
    h = H._hist(act, key)
    days = [d for d, _, _ in h]
    H.B23._need(days[-2:] == ["2019-12-27", "2020-11-28"] and h[-1][2] == ["ley-2063-2020"] and h[-2][2] == ["ley-2008-2019"],
                f"L633 art. 80 shape {days[-3:]}")
    RES = "Para el año 2020 modificado tácitamente por el artículo 125 de la Ley 2008 de 2019. El nuevo texto es el siguiente:> "
    b19 = list(h[-2][1])
    H.B23._need(b19[0].startswith(RES), "L633 art. 80: Ley 2008 marker words")
    b19[0] = b19[0][len(RES):]
    l59, l76 = E.register("ley-2159-2021"), E.register("ley-2276-2022")
    d59, d76 = E.law_day(l59), E.law_day(l76)
    H.B23._need(d59 and d76 and "2020-11-28" < d59 < d76 <= E.RETRIEVED, f"L633 art. 80 days {d59} {d76}")
    tl = [(None if i == 0 else d, b, (c or [None])[0]) for i, (d, b, c) in enumerate(h)]
    tl[-2] = ("2019-12-27", b19, "ley-2008-2019")
    tl[-1] = ("2020-11-28", by["2021"], "ley-2063-2020")
    tl += [(d59, by["2022"], l59), (d76, h[-1][1], l76)]
    H._set(act, key, H._label(act, key), tl)
    H._done(T633, fix_633_80)


H.FIXES[S633].append(fix_633_80)


def fix_633_80_c175(act):
    """Ley 633 de 2000, art. 80, 2009 (coordinator decision): Ley 1152 de 2007 (Estatuto de Desarrollo Rural, art. 112)
    tacitly rewrote the article from 25 July 2007, and Sentencia C-175-09 (18 March 2009) struck Ley 1152 as a whole.
    Under the corpus's rule that a struck law's predecessor text does not revive by itself, from the ruling's day the
    article reads the placeholder '[La fuente no da el texto vigente en esta fecha.]', credited to the ruling, until Ley
    1365 de 2009 (art. 89) rewrote it again (21 December 2009); the page gives no text for those months (Ley 1260 de 2008,
    the 2009 budget, did not include it)."""
    E = H.E
    key = "art-0080"
    u = H.B23._unit(L633, "80")
    nv = " ".join(H._nv(u).split())
    H.B23._need("modificado tácitamente por el artículo 112 de la Ley 1152 de 2007" in nv
                and "Ley declarada INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-175-09 de 18 de marzo de 2009" in nv
                and "Texto no incluido en la Ley 1260 de 2008" in nv
                and "modificado tácitamente por el artículo 89 de la Ley 1365 de 2009" in nv, "L633 art. 80 C-175-09 notes")
    h = H._hist(act, key)
    days = [d for d, _, _ in h]
    i = days.index("2007-07-25")
    H.B23._need(h[i][2] == ["ley-1152-2007"] and days[i + 1] == "2009-12-21" and h[i + 1][2] == ["ley-1365-2009"]
                and H.PH not in h[i][1], f"L633 art. 80 2007-2009 shape {H._shape(h)}")
    c = E.add_court("C-175-09", "2009-03-18", "c-175_2009.html")
    H.B23._need(c == "c-175-09", f"C-175-09 key {c}")
    tl = [(None if j == 0 else d, b, (cr or [None])[0]) for j, (d, b, cr) in enumerate(h)]
    tl.insert(i + 1, ("2009-03-18", [H.PH], c))
    H._set(act, key, H._label(act, key), tl)
    H._done(T633, fix_633_80_c175)


H.FIXES[S633].append(fix_633_80_c175)


def fix_633_58(act):
    """Ley 633 de 2000, art. 58 (empresas asociativas de trabajo, Ley 10 de 1991 art. 16 as rewritten): the page's
    boxes give the amounts as enacted ($400.000.000 / $200.000.000), for 2002 (Decreto 2794 de 2001: $432.300.000 /
    $216.200.000) and for 2003 (Decreto 3257 de 2002: $458.300.000 / $229.100.000; a second box headed only 'Texto
    original de la Ley 633 de 2000' repeats them); today's text gives those for 2004 (Decreto 3804 de 2003). The engine
    gave each box's amounts to the decree before it (the 2003 amounts as enacted). Now each set stands from 1 January of
    its year, credited to its decree, in today's words (the boxes quote the rewritten article with single quotes and
    leave out its opening 'Modifícase el artículo 16 de la Ley 10 de 1991, el cual quedará así:')."""
    E = H.E
    key = "art-0058"
    u = H.B23._unit(L633, "58")
    blks = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in E.la_blocks(it[2])]
    AMT = re.compile(r"\(\$[\d.]+\)")
    sets = {}
    for b in blks:
        ls = E.block_text(b["paras"], False)
        sets.setdefault(b["head"], AMT.findall(ls[0]))
    want = {"Texto con los valores originales establecidos por la ley 633 de 2000:": ["($400.000.000.00)", "($200.000.000.00)"],
            "Texto original de la Ley 633 de 2000, con los valores absolutos que regirán para el año 2002 establecidos por el "
            "Decreto 2794 de 2001:": ["($432.300.000.00)", "($216.200.000.00)"],
            "Texto original de la Ley 633 de 2000 con los valores absolutos establecidos para el año 2003 por el Decreto 3257 de "
            "2002:": ["($458.300.000.00)", "($229.100.000.00)"]}
    H.B23._need(all(sets.get(k) == v for k, v in want.items()), f"L633 art. 58 boxes {sets}")
    h = H._hist(act, key)
    today = h[-1][1]
    k = [i for i, l in enumerate(today) if l.startswith('"Las empresas asociativas de trabajo')]
    H.B23._need(len(k) == 1 and AMT.findall(today[k[0]]) == ["($490.108.000)", "($245.054.000)"], "L633 art. 58 today")
    H.B23._need([d for d, _, _ in h][1:] == ["2002-01-01", "2003-01-01"], f"L633 art. 58 shape {H._shape(h)}")

    def with_amounts(a):
        b = list(today)
        line = today[k[0]]
        for old, new in zip(AMT.findall(line), a):
            line = line.replace(old, new, 1)
        b[k[0]] = line
        return b
    days = {"dec-2794-2001": "2002-01-01", "dec-3257-2002": "2003-01-01", "dec-3804-2003": "2004-01-01"}
    H.B23._need(all(E.law_day(E.register(l)) == d for l, d in days.items()), "L633 art. 58 decree days")
    tl = [(None, with_amounts(want["Texto con los valores originales establecidos por la ley 633 de 2000:"]), None),
          ("2002-01-01", with_amounts(sets[list(want)[1]]), "dec-2794-2001"),
          ("2003-01-01", with_amounts(sets[list(want)[2]]), "dec-3257-2002"),
          ("2004-01-01", today, "dec-3804-2003")]
    H._set(act, key, H._label(act, key), tl)
    H._done(T633, fix_633_58)


H.FIXES[S633].append(fix_633_58)


def _orig488(num):
    """The article's lines from the page's 'Texto original de la Ley 488 de 1998:' box (heading and markers out)."""
    E = H.E
    u = H.B23._unit(L488, num)
    paras = [E.tidy(E.to_text(p, False)) for b in H.B23._boxes(u, "Legislación Anterior") for p in E.box_paras(b)]
    paras = [t for t in paras if re.search(r"\w", t)]
    H.B23._need(paras and paras[0] == "Texto original de la Ley 488 de 1998:" and not any(t.startswith("Texto ") for t in paras[1:]),
                f"L488 art. {num}: box")
    return u, paras[1:]


def fix_488_80(act):
    """Ley 488 de 1998, art. 80 (creación de la policía fiscal y aduanera): the page's marker '<Artículo derogado por el
    artículo 53 la Ley 633 de 2001<sic, 2000>, según establece la Corte Constitucional en Sentencias C-1066-01>' holds a
    marker inside a marker, so its tail stood as the article's text in every version. The text as enacted (the page's
    'Texto original' box, whose heading misprints 'ARTÍCULO 81.' and whose last line ends in a stray quote) stands from
    the act's first day; Ley 633 de 2000 (art. 53, which the Court read as repealing it: C-1066-01) takes it out on its
    day, 29 December 2000."""
    E = H.E
    u, lines = _orig488("80")
    H.B23._need(lines[0].startswith("ARTÍCULO 81. Créase en la Dirección de Impuestos y Aduanas Nacionales")
                and lines[-1].endswith("Fiscalía General de la Nación.'."), "L488 art. 80 box lines")
    lines = [lines[0][len("ARTÍCULO 81. "):]] + lines[1:-1] + [lines[-1][:-3] + "."]
    H.B23._need("derogación de los artículos 71 y 80 de la Ley 488 de 1998 por los artículos 42 y 53 de la Ley 633 de 2000"
                in H._jv(u), "L488 art. 80 ruling note")
    h = H._hist(act, "art-0080")
    H.B23._need(len(h) == 1 and h[0][1][-1].endswith("según establece la Corte Constitucional en Sentencias C-1066-01>"),
                f"L488 art. 80 shape {H._shape(h)}")
    law = E.register("ley-633-2000")
    H.B23._need(E.law_day(law) == "2000-12-29", "Ley 633 day")
    H._set(act, "art-0080", H._label(act, "art-0080"),
           [(None, ["CREACION DE LA POLICIA FISCAL Y ADUANERA."] + lines, None), ("2000-12-29", None, law)])
    H.B23._forget(L488, "art-0080")
    H._done(T488, fix_488_80)


def fix_488_100(act):
    """Ley 488 de 1998, art. 100 (gasolina en zonas fronterizas): repealed by Ley 681 de 2001 (10 August 2001), so the
    page prints no current text and the act's first version had held a placeholder. The text as enacted (the page's
    'Texto original' box) stands from the act's first day; its parágrafo goes on 8 March 2000 (Sentencia C-269-00:
    'Artículo declarado EXEQUIBLE, excepto el parágrafo que fué declarado INEXEQUIBLE'); the article goes on 10 August
    2001 (Ley 681 de 2001)."""
    E = H.E
    u, lines = _orig488("100")
    H.B23._need(len(lines) == 3 and lines[2] == "PARAGRAFO. El Gobierno Nacional reglamentará la materia antes de noventa (90) días.",
                f"L488 art. 100 box lines {lines}")
    H.B23._need("excepto el parágrafo que fué declarado INEXEQUIBLE, por la Corte Constitucional mediante Sentencia C-269-00 "
                "del 8 de marzo de 2000" in H._jv(u), "L488 art. 100 ruling")
    h = H._hist(act, "art-0100")
    H.B23._need(len(h) == 2 and h[0][1] == [H.PH] and h[1][0] == "2001-08-10" and h[1][2] == ["ley-681-2001"],
                f"L488 art. 100 shape {H._shape(h)}")
    c = E.add_court("C-269-00", "2000-03-08", "c-269_2000.html")
    epi = "GASOLINA EN ZONAS FRONTERIZAS."
    H._set(act, "art-0100", H._label(act, "art-0100"),
           [(None, [epi] + lines, None), ("2000-03-08", [epi] + lines[:2], c), ("2001-08-10", None, "ley-681-2001")])
    H.B23._forget(L488, "art-0100")
    H._done(T488, fix_488_100)


H.FIXES[S488] += [fix_488_80, fix_488_100]


def fix_633_134(act):
    """Ley 633 de 2000, art. 134 (vigencia y derogatorias): the page strikes 'el artículo 27 de la Ley 191 de 1995' in
    the list of repealed provisions, with the marker '<Aparte tachado suprimido por el artículo 29 de la Ley 677 de
    2001>' (Diario Oficial No. 44.509 of 4 August 2001); the engine left the struck words out of every version. They
    stand from the act's first day until Ley 677 de 2001 takes them out, credited to it."""
    E = H.E
    u = H.B23._unit(L633, "134")
    H.B23._need("Aparte tachado suprimido por el artículo 29 de la Ley 677 de 2001" in H._nv(u), "L633 art. 134 note")
    old = H._printed(u, keep_struck=True)
    h = H._hist(act, "art-0134")
    H.B23._need(len(h) == 1 and len(old) == len(h[0][1]), f"L633 art. 134 shape {H._shape(h)}")
    diff = [(a, b) for a, b in zip(old, h[0][1]) if a != b]
    H.B23._need(len(diff) == 1 and diff[0][0].replace(" el artículo 27 de la Ley 191 de 1995", "", 1) == diff[0][1],
                "L633 art. 134 struck words")
    law = E.register("ley-677-2001")
    d = E.law_day(law)
    H.B23._need(d and "2000-12-29" < d < "2002-01-01", f"Ley 677 day {d}")
    H._set(act, "art-0134", H._label(act, "art-0134"), [(None, old, None), (d, h[0][1], law)])
    H._done(T633, fix_633_134)


H.FIXES[S633].append(fix_633_134)


def _full(act, day):
    """Give the version on `day` (a credit-only version, which holds no units at this stage) the units of the version
    before it, so a hand history can change a unit there."""
    vs = act["versions"]
    i = next(i for i, v in enumerate(vs) if v["from"] == day)
    if "units" not in vs[i]:
        vs[i]["units"] = dict(next(v for v in reversed(vs[:i]) if "units" in v)["units"])


def fix_633_91(act):
    """Ley 633 de 2000, art. 91 (páginas web): Sentencia C-1147-01 ('de octubre 31 de 2001', the month written first)
    upheld the article on a condition and struck the words the page shows struck; the engine left those words out of
    the 2000 version too (the ruling's day changed no words). They stand from the act's first day until the ruling."""
    E = H.E
    u = H.B23._unit(L633, "91")
    H.B23._need("Las expresiones tachadas fueron declaradas INEXEQUIBLES por la misma Sentencia C-1147-01" in H._jv(u),
                "L633 art. 91 ruling")
    old, new = H._printed(u, keep_struck=True), H._printed(u)
    h = H._hist(act, "art-0091")
    H.B23._need(old != new and h == [("2000-12-29", new, None)]
                and any(v["from"] == "2001-10-31" and v["credits"].get("art-0091") == ["c-1147-01"] for v in act["versions"]),
                f"L633 art. 91 shape {H._shape(h)}")
    _full(act, "2001-10-31")
    H._set(act, "art-0091", H._label(act, "art-0091"), [(None, old, None), ("2001-10-31", new, "c-1147-01")])
    H._done(T633, fix_633_91)


H.FIXES[S633].append(fix_633_91)


def fix_488_91(act):
    """Ley 488 de 1998, art. 91: Ley 633 de 2000 art. 99 rewrote it (29 December 2000) and Sentencia C-992-01 (19
    September 2001) struck parts of that wording; the 2000 version held a placeholder. The page prints the struck parts
    struck: the words from 29 December 2000 are the page's with them (as Ley 633 art. 99, in this part, prints them)."""
    u = H.B23._unit(L488, "91")
    then = H._printed(u, keep_struck=True)
    H.B23._need("Artículo 99 de la Ley 633 de 2000 declarado EXEQUIBLE, salvo los apartes tachados que fueron declarados "
                "INEXEQUIBLES, por la Corte Constitucional mediante Sentencia C-992-01" in H._jv(u), "L488 art. 91 ruling")
    h = H._hist(act, "art-0091")
    H.B23._need([d for d, _, _ in h] == ["1998-12-28", "2000-12-29", "2001-09-19"] and h[1][1] == [H.PH]
                and h[2][2] == ["c-992-01"], f"L488 art. 91 shape {H._shape(h)}")
    today = h[2][1]
    H.B23._need(len(then) == len(today) and then[0] == today[0] and today[1] == "." and then[1] != "."
                and then[2:] != today[2:] and then[3:] == today[3:], "L488 art. 91 struck lines")
    H._set(act, "art-0091", H._label(act, "art-0091"),
           [(None, h[0][1], None), ("2000-12-29", then, "ley-633-2000"), ("2001-09-19", today, "c-992-01")])
    H._done(T488, fix_488_91)


H.FIXES[S488].append(fix_488_91)


C030_END = "2021-06-20"


def fix_488_121(act):
    """Ley 488 de 1998, art. 121 (base gravable de la sobretasa): Sentencia C-030-19 (30 January 2019) struck the inciso
    with its effects 'diferidos por el término de dos legislaturas a partir de la fecha de notificación' (notified by
    edicto on 13 March 2019). The two legislatures after that day are 2019-2020 and 2020-2021; the second ends on 20 June
    2021 (Constitución art. 138), so the inciso goes on that day, credited to the ruling (as Sentencia C-161-24's
    deferral by two legislatures, batch 91). The page still prints it under its marker '<Inciso INEXEQUIBLE, efectos
    diferidos por dos legislaturas>'; Ley 2093 de 2021 (29 June 2021) then added art. 121A, a new base gravable."""
    E = H.E
    u = H.B23._unit(L488, "121")
    H.B23._need("'los efectos de la declaración de INEXEQUIBILIDAD quedan diferidos por el término de dos legislaturas a "
                "partir de la fecha de notificación de la presente sentencia" in H._jv(u)
                and "Esta sentencia se notifica mediante Edicto el 13 de marzo de 2019" in H._jv(u), "L488 art. 121 ruling")
    h = H._hist(act, "art-0121")
    H.B23._need([d for d, _, _ in h] == ["1998-12-28", "2003-12-29"] and h[1][1][0].startswith("BASE GRAVABLE. Está constituida")
                and h[1][1][1:] == ["PARÁGRAFO."], f"L488 art. 121 shape {H._shape(h)}")
    c = E.add_court("C-030-19", "2019-01-30", "c-030_2019.html")
    H._set(act, "art-0121", H._label(act, "art-0121"),
           [(None, h[0][1], None), ("2003-12-29", h[1][1], "ley-863-2003"), (C030_END, ["BASE GRAVABLE.", "PARÁGRAFO."], c)])
    H._done(T488, fix_488_121)


H.FIXES[S488].append(fix_488_121)
