"""Hand-set histories for batch 89 (Ley 643 de 2001), installed by hand_fixes.install(); each checks the page
first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L643, T643 = "ley_0643_2001", "Juegos de suerte y azar (Ley 643 de 2001)"
DEC, D0 = "dec-130-2010", "2010-01-21"   # Decreto 130 de 2010 (Diario Oficial No. 47.599 of 21 January 2010)
RUL0 = "2010-05-12"                       # Sentencia C-332-10, Comunicado de Prensa de la Sala Plena of 12 May 2010
JV332 = ("Decreto 130 de 2010 declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-332-10 según "
         "Comunicado de Prensa de la Sala Plena de 12 de mayo de 2010")
DONE130: list = []


def _u(name):
    return next(u for u in H.P.doc_units(L643)[1:] if u["name"] == name)


def _box(u, head, first=None, full=False):
    """The lines of the one earlier-text block headed `head` (whose first line starts with `first`), the publisher's
    leading '<...>' label out; full: the 'ARTÍCULO N.' heading of a whole-article block out too."""
    E = H.E
    out = []
    for b in H.B23._boxes(u, "Legislación Anterior"):
        for blk in E.la_blocks(b):
            if blk["head"].rstrip(" :.").startswith(head):
                ls = [E.tidy(re.sub(r"^<[^<>]*>\s*", "", x)) for x in E.block_text(blk["paras"], full)]
                ls = [x for x in ls if x]
                if ls and (first is None or ls[0].startswith(first)):
                    out.append(ls)
    H.B23._need(len(out) == 1, f"L643 art. {u['name']} box {head!r} {first!r}: {len(out)}")
    return out[0]


def _c332():
    law = H.E.add_court("C-332-10", RUL0, "c-332_2010.html")
    H.B23._need(law == "c-332-10" and H.E.LAWS[law]["enacted"] == RUL0, "C-332-10 day")
    return law


def _check(u, nv_words):
    H.B23._need(JV332 in H._jv(u), f"L643 art. {u['name']} JV C-332-10")
    nv = H._nv(u)
    for w in nv_words:
        H.B23._need(w in nv, f"L643 art. {u['name']} NV {w!r}")


def _idx(lines, start, what):
    k = [i for i, x in enumerate(lines) if x.startswith(start)]
    H.B23._need(len(k) == 1, f"L643 {what}: line {start!r} {len(k)}")
    return k[0]


def _hist_is(act, key, days):
    h = H._hist(act, key)
    H.B23._need([(d, c) for d, _, c in h] == days, f"L643 {key} {H._shape(h)}")
    return h


def _units_on(act, days):
    """A version on each of `days` that carries no units (it changed no words) gets a copy of the units before it, so a
    text set for that day lands on it (set_history skips versions without units)."""
    full = None
    for v in act["versions"]:
        if "units" in v:
            full = v["units"]
        elif v["from"] in days:
            v["units"] = dict(full)
            full = v["units"]


def _apply(act, key, tl, n):
    _units_on(act, {d for d, _, _ in tl[1:]})
    H._set(act, key, H._label(act, key), tl)
    H.B23._forget(L643, key)
    DONE130.append(n)


def fix_643_130(act):
    """Decreto 130 de 2010 (an emergency-social decree, Diario Oficial No. 47.599 of 21 January 2010, in force from its
    publication) rewrote or added words in arts. 3 (literals e and f), 5 (inciso 3 and parágrafo 2), 7 (a last inciso),
    9 (inciso 2 and a parágrafo), 11 (a parágrafo), 14 and 15 (whole articles), 32 (the end of inciso 1 and inciso 4), 37,
    42 and 44 (whole articles). The Constitutional Court struck the decree as a whole (Sentencia C-332-10, the press
    release of the Sala Plena of 12 May 2010; no deferral). Each changed article reads as the page's 'Texto adicionado/
    modificado por el Decreto 130 de 2010, INEXEQUIBLE' box gives it from 21 January 2010; on 12 May 2010 the words that
    stood before the decree return, credited to the ruling, and an added literal or parágrafo keeps only the label the
    page prints ('e) <Literal INEXEQUIBLE>' reads 'e)'). Where the page gives no earlier text, the article's printed
    words (unchanged by any later act) are its words from 2001 (arts. 9, 14, 15, 32, 42: the engine had read the decree's
    box as the last earlier text and put the placeholder before it, or credited today's revived words to the decree).
    Art. 9 also: Ley 715 de 2001 art. 106 gave inciso 2 the words of the page's 'Texto modificado por la Ley 715 de 2001,
    Inexequible' box from 21 December 2001 until Sentencia C-005-03 (21 January 2003) struck that article. Art. 42 also:
    parágrafo 4o., added by Ley 715 de 2001 art. 42, from 21 December 2001. Arts. 11, 37, 44: the Ley 1393 de 2010
    texts follow from 12 July 2010 as the engine read them. Art. 32: Sentencia C-1114-03 struck Ley 788 de 2002 art. 101,
    which only stated how inciso 4 is to be read; neither changed its words, so neither makes a version."""
    B23 = H.B23
    law = _c332()
    PH = H.PH

    # art. 3: literals e) and f) added (decree art. 16)
    u = _u("3")
    _check(u, ["Literal adicionado por el artículo 16 del Decreto 130 de 2010"])
    e = _box(u, "Texto adicionado por el Decreto 130 de 2010", "e) Conectividad y control.")
    f = _box(u, "Texto adicionado por el Decreto 130 de 2010", "f) Control al juego ilegal.")
    key = "art-0003"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])])
    B23._need(h[1][1] == h[0][1] + ["e)", "f)"], "L643 art. 3 stubs")
    _apply(act, key, [(None, h[0][1], None), (D0, h[0][1] + e + f, DEC), (RUL0, h[1][1], law)], "3")

    # art. 5: inciso 3 rewritten, parágrafo 2 added (decree art. 20); Ley 1753 de 2015 art. 94 inciso 3 later
    u = _u("5")
    _check(u, ["Inciso modificado por el artículo 20 del Decreto 130 de 2010",
               "Parágrafo adicionado por el artículo 20 del Decreto 130 de 2010"])
    orig = _box(u, "Texto original de la Ley 643 de 2001")
    dec = _box(u, "Texto modificado por el Decreto 130 de 2010")
    par = _box(u, "Texto adicionado por el Decreto 130 de 2010", "PARÁGRAFO 2.")
    key = "art-0005"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC]), ("2015-06-09", ["ley-1753-2015"])])
    p0 = h[0][1]
    i = _idx(p0, "Están excluidos del ámbito", "art. 5 inciso 3")
    B23._need(len(orig) == 1 and len(dec) == 1 and p0[i] == orig[0], "L643 art. 5 original inciso 3")
    B23._need(h[1][1] == p0[:i] + dec + p0[i + 1:] + ["PARÁGRAFO 2o."], "L643 art. 5 engine 2010")
    r = p0 + ["PARÁGRAFO 2o."]
    B23._need(h[2][1][:i] + h[2][1][i + 1:] == r[:i] + r[i + 1:], "L643 art. 5 2015 = ruling text but inciso 3")
    _apply(act, key, [(None, p0, None), (D0, p0[:i] + dec + p0[i + 1:] + par, DEC), (RUL0, r, law),
                      ("2015-06-09", h[2][1], "ley-1753-2015")], "5")

    # art. 7: a last inciso added (decree art. 9); the page prints '<Inciso INEXEQUIBLE>' (no words)
    u = _u("7")
    _check(u, ["Inciso adicionado por el artículo 9 del Decreto 130 de 2010"])
    add = _box(u, "Texto adicionado por el Decreto 130 de 2010")
    key = "art-0007"
    h = _hist_is(act, key, [("2001-01-17", None)])  # (the engine credited the decree with no change)
    B23._need(len(add) == 1, "L643 art. 7")
    _apply(act, key, [(None, h[0][1], None), (D0, h[0][1] + add, DEC), (RUL0, h[0][1], law)], "7")

    # art. 9: inciso 2 (Ley 715 de 2001 art. 106, struck by C-005-03; decree art. 3) and a parágrafo (decree art. 3)
    u = _u("9")
    _check(u, ["Inciso modificado por el artículo 3 del Decreto 130 de 2010",
               "Parágrafo adicionado por el artículo 3 del Decreto 130 de 2010",
               "Inciso 2o. modificado por el artículo 106 de la Ley 715 de 2001"])
    B23._need("El Artículo 106 de la Ley 715 de 2001 fue declarado INEXEQUIBLE por la Corte Constitucional mediante "
              "Sentencia C-005-03" in H._jv(u), "L643 art. 9 C-005-03")
    dec = _box(u, "Texto modificado por el Decreto 130 de 2010")
    par = _box(u, "Texto adicionado por el Decreto 130 de 2010")
    l715 = _box(u, "Texto modificado por la Ley 715 de 2001")
    key = "art-0009"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])])  # (Ley 715 and C-005-03 credited with no change)
    t = h[1][1]
    B23._need(h[0][1] == [PH] and len(t) == 3 and t[1].startswith("Sin perjuicio de los derechos de explotación")
              and t[2] == "PARÁGRAFO." and len(dec) == len(par) == len(l715) == 1, f"L643 art. 9 {H._shape(h)}")
    o = t[:2]
    _apply(act, key, [(None, o, None), ("2001-12-21", [t[0]] + l715, "ley-715-2001"), ("2003-01-21", o, "c-005-03"),
                      (D0, [t[0]] + dec + par, DEC), (RUL0, t, law)], "9")

    # art. 11: a parágrafo added (decree art. 10); Ley 1393 de 2010 art. 13 added today's parágrafo
    u = _u("11")
    _check(u, ["Parágrafo adicionado por el artículo 10 del Decreto 130 de 2010"])
    par = _box(u, "Texto adicionado por el Decreto 130 de 2010")
    key = "art-0011"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC]), ("2010-07-12", ["ley-1393-2010"])])
    B23._need(h[1][1] == h[0][1] + par and h[2][1][:-1] == h[0][1], "L643 art. 11")
    _apply(act, key, [(None, h[0][1], None), (D0, h[1][1], DEC), (RUL0, h[0][1], law),
                      ("2010-07-12", h[2][1], "ley-1393-2010")], "11")

    # arts. 14 and 15: whole articles (decree arts. 11, 12); the printed words are the 2001 words
    for n, art in (("14", 11), ("15", 12)):
        u = _u(n)
        _check(u, [f"Artículo modificado por el artículo {art} del Decreto 130 de 2010"])
        dec = _box(u, "Texto modificado por el Decreto 130 de 2010", full=True)
        key = f"art-{int(n):04d}"
        h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])])
        B23._need(h[0][1] == [PH] and h[1][1] == H._printed(u), f"L643 art. {n} {H._shape(h)}")
        _apply(act, key, [(None, h[1][1], None), (D0, dec, DEC), (RUL0, h[1][1], law)], n)

    # art. 32: end of inciso 1 and inciso 4 (decree art. 21); C-1114-03 struck Ley 788 de 2002 art. 101, which only
    # 'clarified' inciso 4 (no words of this article): no version
    u = _u("32")
    _check(u, ["Inciso, aparte final, modificado por el artículo 21 del Decreto 130",
               "Inciso modificado por el artículo 21 del Decreto 130 de 2010", "Inciso aclarado por el Artículo 101 de la Ley 788 de 2002"])
    d1 = _box(u, "Texto modificado por el Decreto 130 de 2010", "Son modalidades de juegos de suerte y azar")
    d4 = _box(u, "Texto modificado por el Decreto 130 de 2010", "El funcionamiento de los establecimientos")
    key = "art-0032"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])])  # (C-1114-03 credited with no change)
    t = h[1][1]
    i1 = _idx(t, "JUEGOS LOCALIZADOS. Son modalidades", "art. 32 inciso 1")
    i4 = _idx(t, "Los juegos localizados que a partir de la sanción", "art. 32 inciso 4")
    B23._need(h[0][1] == [PH] and t == H._printed(u) and len(d1) == len(d4) == 1, f"L643 art. 32 {H._shape(h)}")
    d = list(t)
    d[i1], d[i4] = "JUEGOS LOCALIZADOS. " + d1[0], d4[0]
    _apply(act, key, [(None, t, None), (D0, d, DEC), (RUL0, t, law)], "32")

    # arts. 37 and 44: whole articles (decree arts. 14, 24); the original words return until Ley 1393 de 2010
    for n, art, later in (("37", 14, [("2010-07-12", ["ley-1393-2010"])]),
                          ("44", 24, [("2010-07-12", ["ley-1393-2010"]), ("2011-11-03", ["dec-4142-2011"])])):
        u = _u(n)
        _check(u, [f"Artículo modificado por el artículo {art} del Decreto 130 de 2010"])
        orig = _box(u, "Texto original de la Ley 643 de 2001", full=True)
        dec = _box(u, "Texto modificado por el Decreto 130 de 2010", full=True)
        key = f"art-{int(n):04d}"
        h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])] + later)
        B23._need(h[0][1] == orig and h[1][1] == dec, f"L643 art. {n} {H._shape(h)}")
        _apply(act, key, [(None, orig, None), (D0, dec, DEC), (RUL0, orig, law)]
               + [(d_, b_, c_[0]) for d_, b_, c_ in h[2:]], n)

    # art. 42: whole article (decree art. 6); parágrafo 4o. added by Ley 715 de 2001 art. 42 (21 December 2001)
    u = _u("42")
    _check(u, ["Artículo modificado por el artículo 6 del Decreto 130 de 2010",
               "Parágrafo adicionado por el artículo 42 de la Ley 715 de 2001, publicada en el Diario Oficial No 44.654, "
               "de 21 de diciembre de 2001"])
    dec = _box(u, "Texto modificado por el Decreto 130 de 2010", full=True)
    key = "art-0042"
    h = _hist_is(act, key, [("2001-01-17", None), (D0, [DEC])])
    t = h[1][1]
    B23._need(h[0][1] == [PH] and t[-1].startswith("PARÁGRAFO 4o. Del 80% contemplado")
              and sum(x.startswith("PARÁGRAFO 4") for x in t) == 1, f"L643 art. 42 {H._shape(h)}")
    B23._need(H.E.law_day("ley-715-2001") == "2001-12-21", "Ley 715 de 2001 day")
    _apply(act, key, [(None, t[:-1], None), ("2001-12-21", t, "ley-715-2001"), (D0, dec, DEC), (RUL0, t, law)], "42")

    B23._need(DONE130 == ["3", "5", "7", "9", "11", "14", "15", "32", "37", "44", "42"], f"L643 130 {DONE130}")
    # C-1114-03's version (credited with no change of words) is left with nothing: it goes
    vs = act["versions"]
    i = next(i for i, v in enumerate(vs) if v["from"] == "2003-11-25")
    B23._need(not vs[i]["credits"] and "units" not in vs[i], "L643 version 2003-11-25 not empty")
    del vs[i]
    H._done(T643, fix_643_130)


def fix_643_39(act):
    """art. 39 (creates the Empresa Territorial para la Salud, Etesa): the page prints no words, only '<Mediante el
    Decreto 175 de 2010, se suprime la Empresa Territorial para la Salud, Etesa creada mediante este artículo>', and gives
    the article's words in its 'Texto original de la Ley 643 de 2001' box. Decreto 175 de 2010 (Diario Oficial No.
    47.604 of 26 January 2010, in force from its publication: its own last article) suppressed and ordered the
    liquidation of the entity. The original words stand from the act's first day; following the page, the article is out
    from 26 January 2010, credited to Decreto 175 de 2010 (the engine had the article in no version)."""
    B23, E = H.B23, H.E
    u = _u("39")
    p0 = E.plain(next(it[1] for it in u["items"] if it[0] == "p"))
    B23._need("Mediante el Decreto 175 de 2010, se suprime la Empresa Territorial para la Salud, Etesa creada mediante este "
              "artículo" in p0 and "Diario Oficial No. 47.604 de 26 de enero de 2010" in H._nv(u), "L643 art. 39 marker")
    orig = _box(u, "Texto original de la Ley 643 de 2001", full=True)
    B23._need(orig[0].startswith("Créase la Empresa Industrial y Comercial del Estado del orden nacional"), "L643 art. 39 box")
    key = "art-0039"
    B23._need(all(b is None for _, b, _ in H._hist(act, key)), "L643 art. 39 already there")
    k = "dec-175-2010"
    E.PUB[k] = "2010-01-26"
    E.TITLES.setdefault(k, "Decreto 175 de 2010")
    E.register(k)
    B23._need(E.law_day(k) == "2010-01-26", f"Decreto 175 de 2010 day {E.law_day(k)}")
    _units_on(act, {"2010-01-26"})
    H._set(act, key, "Art. 39", [(None, orig, None), ("2010-01-26", None, k)])
    B23._forget(L643, key)
    H._done(T643, fix_643_39)


def fix_643_notes(act):
    """readings that change no words. (1) art. 24: Decreto 127 de 2010 (emergency decree, 21 January 2010) gave it
    the words of the page's 'Texto modificado por el Decreto 127 de 2010' box; Sentencia C-253 de 2010 struck that decree
    but deferred its effects to 16 December 2010, and Ley 1393 de 2010 art. 23 replaced the words on 12 July 2010, before
    that day, so the ruling makes no version (as for the other parts with Decreto 127); the page gives no 2001 text of
    the article (placeholder until 2010). (2) arts. 46 and 47: Decreto 130 de 2010 art. 29 (struck with the whole decree
    by Sentencia C-332-10) only said that references to the Consejo Nacional de Juegos de Suerte y Azar were to be read
    as made to a new Comisión de Regulación; it changed no words of the articles: no version. (3) arts. 5, 24, 38 and 49:
    the changes made by the development-plan laws (Ley 1753 de 2015, Ley 1955 de 2019) stand to today; the page notes
    'No derogado expresamente por planes de desarrollo posteriores', and Ley 1955 de 2019 art. 336 and Ley 2294 de 2023
    art. 372 keep in force the articles of the earlier plans not expressly repealed; the editor's remark on the four-year
    term of the plans is not read as a lapse. (4) art. 53: the page notes that Decreto 126 de 2010 (struck by Sentencia
    C-302-10 of 28 April 2010) changed the act 'en lo relativo a multas'; it changed no words of the article. (5) arts. 32
    and 60: Ley 788 de 2002 art. 101 (struck by Sentencia C-1114-03 of 25 November 2003) only stated how the mayor's prior
    opinion in those articles is to be read; neither changed their words."""
    B23 = H.B23
    u = _u("24")
    B23._need(not any("Decreto 127" in x for x in [H._nv(u), H._jv(u)])
              and _box(u, "Texto modificado por el Decreto 127 de 2010", full=True)[0].startswith("PLAN DE PREMIOS."),
              "L643 art. 24 Decreto 127 box")
    B23._need("No derogado expresamente por planes de desarrollo posteriores" in H._nv(u), "L643 art. 24 PND note")
    h = _hist_is(act, "art-0024", [("2001-01-17", None), (D0, ["dec-127-2010"]), ("2010-07-12", ["ley-1393-2010"]),
                                   ("2019-05-25", ["ley-1955-2019"])])
    B23._need(h[0][1] == [H.PH], "L643 art. 24 first text")
    for n in ("46", "47"):
        B23._need("Mediante el artículo 29 del Decreto 130 de 2010" in H._nv(_u(n)), f"L643 art. {n} Decreto 130 art. 29")
    B23._need("No derogado expresamente por planes de desarrollo posteriores" in H._nv(_u("5")), "L643 art. 5 PND note")
    B23._need("Decreto 126 de 2010" in H._nv(_u("53")) and "Sentencia C-302-10" in H._jv(_u("53")), "L643 art. 53 Decreto 126")
    B23._need("Aclárese que el alcance del concepto previo del alcalde, de que tratan los artículos 32 y 60 de la Ley 643 de "
              "2001" in H._nv(_u("60")) and "Sentencia C-1114-03" in H._jv(_u("60")), "L643 art. 60 Ley 788 art. 101")
    H._done(T643, fix_643_notes)


H.FIXES["juegos-de-suerte-y-azar-2001"] = [fix_643_130, fix_643_39, fix_643_notes]
