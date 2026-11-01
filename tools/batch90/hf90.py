"""Hand-set histories for batch 90 (Leyes 1151 de 2007 and 812 de 2003), installed by hand_fixes.install(); each
checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L1151, T1151, S1151 = ("ley_1151_2007", "Plan Nacional de Desarrollo 2006-2010 (Ley 1151 de 2007)",
                       "plan-nacional-de-desarrollo-2006-2010")
L812, T812, S812 = ("ley_0812_2003", "Plan Nacional de Desarrollo 2003-2006 (Ley 812 de 2003)",
                    "plan-nacional-de-desarrollo-2003-2006")
L1450, D1450 = "ley-1450-2011", "2011-06-16"   # Ley 1450 de 2011 art. 276 (Diario Oficial No. 48.102, 16 June 2011)
K1151, D1151 = "ley-1151-2007", "2007-07-25"   # Ley 1151 de 2007 art. 160 (Diario Oficial No. 46.700, 25 July 2007)
LAPSE160 = "La vigencia de este artículo no fue prorrogada por el artículo 160 de la Ley 1151 de 2007"
NV276 = "no haber sido prorrogada su vigencia por el artículo 276 de la Ley 1450 de 2011"
# (page, key) -> evidence on the page (first paragraph or Notas de Vigencia) that the article is out today; read by
# verify_batch90 (the page still prints the words of these articles).
GONE: dict = {}   # (filled by the fixes as they run)
M276 = "el artículo 276 de la Ley 1450 de 2011"


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): the page evidence that an article of this part is out today,
    as (where, words): 'p0' the first paragraph, 'nv' the Notas de Vigencia. None: no such rule here."""
    n = key[4:].lstrip("0")
    if page == L1151:
        if n == "92":
            return ("nv", "Artículo derogado al no haber sido prorrogada su vigencia por el artículo 276")
        if n in ("6", "63", "65", "77", "101", "120"):
            return ("p0", "Artículo derogado por el artículo 276 de la Ley 1450 de 2011")
    if page == L812:
        if n == "63":
            return ("p0", "Artículo, salvo el parágrafo, derogado al no ser prorrogada su vigencia, según lo dispuesto por "
                          "el artículo 160 de la Ley 1151 de 2007")
        if n in ("13", "14", "21", "38", "43", "51", "69", "71", "75", "82", "83", "86", "92", "103", "110"):
            return ("p0", M276)
        return ("p0", LAPSE160)
    return None


def _need(c, what):
    H.B23._need(c, what)


def _u(page, num):
    return H.B23._unit(page, num)


def _p0(u):
    return H.E.plain(next(it[1] for it in u["items"] if it[0] == "p"))


def _key(num):
    return H.E.unit_key(num)[0]


def _units_on(act, days):
    """A version on one of `days` that carries no units (it changed no words) gets a copy of the units before it, so a
    text set for that day lands on it (set_history skips versions without units)."""
    full = None
    for v in act["versions"]:
        if "units" in v:
            full = v["units"]
        elif v["from"] in days:
            v["units"] = dict(full)
            full = v["units"]


def _apply(act, page, key, tl):
    _units_on(act, {d for d, _, _ in tl[1:]})
    H._set(act, key, H._label(act, key), tl)
    H.B23._forget(page, key)


def _lines(u, keep=(), subst=None):
    """The article's lines as _printed gives them, with the struck words of the paragraphs (item indexes) in `keep`
    kept and the paragraphs in `subst` read as the text given there."""
    subst = subst or {}
    E = H.E
    out = []
    for i, it in enumerate(u["items"]):
        if it[0] != "p":
            continue
        t = subst[i] if i in subst else E.tidy(E.to_text(it[1], i in keep))
        if re.search(r"\w", t):
            out.append(t)
    epi = E.tidy(E.ART_HEAD.sub("", u["label"], count=1))
    return ([f"{epi} {out[0]}"] if epi else [out[0]]) + out[1:]


# ------------------------------------------------------------------------------------------------ Ley 1151 de 2007

def fix_1151_276(act):
    """Ley 1450 de 2011 art. 276 (16 June 2011) kept in force only the articles of Ley 1151 de 2007 it lists and repealed
    the rest. Arts. 63, 65, 77, 101 and 120 (page marker 'Artículo derogado por el artículo 276 de la Ley 1450 de 2011')
    and art. 92 (no marker; its Notas de Vigencia say its force was not extended by that article) are not in the list.
    The page prints their words; those words stand from the act's first day and the articles leave on 16 June 2011,
    credited to Ley 1450 de 2011 (the engine had the placeholder up to 2011 and the words from then to today). Art.
    120: Ley 1753 de 2015 art. 267 repealed it again (9 June 2015), when it was already out: no version."""
    done = []
    for num in ("63", "65", "77", "92", "101", "120"):
        u = _u(L1151, num)
        p0, nv = _p0(u), H._nv(u)
        if num == "92":
            _need("Artículo derogado al no haber sido prorrogada su vigencia por el artículo 276 de la Ley 1450 de 2011" in nv
                  and "<" not in p0, "L1151 art. 92 NV")
            GONE[(L1151, _key(num))] = ("nv", "Artículo derogado al no haber sido prorrogada su vigencia por el artículo 276")
        else:
            _need("<Artículo derogado por el artículo 276 de la Ley 1450 de 2011" in p0, f"L1151 art. {num} marker")
            GONE[(L1151, _key(num))] = ("p0", "Artículo derogado por el artículo 276 de la Ley 1450 de 2011")
        if num == "101":
            _need("no prorroga expresamente la vigencia de este artículo" in nv, "L1151 art. 101 NV")
        printed = H._printed(u)
        key = _key(num)
        h = H._hist(act, key)
        if num == "120":
            _need([(d, c) for d, _, c in h] == [(D1151, None), (D1450, [L1450]), ("2015-06-09", ["ley-1753-2015"])]
                  and h[0][1] == [H.PH] and h[1][1] is None and h[2][1] == printed, f"L1151 art. 120 {H._shape(h)}")
            _need("Artículo derogado expresamente por el artículo 267 de la Ley 1753 de 2015" in nv, "L1151 art. 120 NV")
        else:
            _need([(d, c) for d, _, c in h] == [(D1151, None), (D1450, [L1450])] and h[0][1] == [H.PH]
                  and h[1][1] == printed, f"L1151 art. {num} {H._shape(h)}")
        _apply(act, L1151, key, [(None, printed, None), (D1450, None, L1450)])
        done.append(num)
    _need(done == ["63", "65", "77", "92", "101", "120"], f"L1151 276 {done}")
    H._done(T1151, fix_1151_276)


def fix_1151_6(act):
    """art. 6 (the description of the main investment programmes): the page prints it under 'Artículo derogado por el
    artículo 276 de la Ley 1450 de 2011' (it is not among the articles Ley 1450 de 2011 art. 276 kept) and shows struck
    words the Constitutional Court struck: numeral 4.2, the three incisos 'En aras de un desarrollo regional ...', 'El
    DNP será el organismo encargado ...' and 'Mientras se cumple el término ...' (Sentencia C-535-08, 28 May 2008);
    numeral 3.3.1, the first and last sentences of the inciso 'La entidad que agremia nacionalmente ...' (Sentencia
    C-978-10, 1 December 2010); numeral 3.3, inciso 23 'Para garantizar lo establecido en el parágrafo 2o del artículo
    26 de la Ley 1122 de 2007 ...', which the page gives only in its 'Texto original de la Ley 1151 de 2007' box
    (Sentencia C-979-10, 1 December 2010). The act's words, all of these included, stand from 25 July 2007; the C-535-08
    incisos go on 28 May 2008, the C-978-10 and C-979-10 words on 1 December 2010, credited to the rulings; the article
    leaves on 16 June 2011, credited to Ley 1450 de 2011 (the engine had the placeholder up to 2011 and the words from
    then to today). Sentencia C-714-08 (9 July 2008) upheld numeral 3.3.1 on a condition and changes no words;
    Sentencias C-1059-08 and C-078-11 were inhibitions or 'estarse a lo resuelto': no versions."""
    E = H.E
    u = _u(L1151, "6")
    _need("<Artículo derogado por el artículo 276 de la Ley 1450 de 2011" in _p0(u), "L1151 art. 6 marker")
    GONE[(L1151, "art-0006")] = ("p0", "Artículo derogado por el artículo 276 de la Ley 1450 de 2011")
    jv = H._jv(u)
    for need in ("Incisos tachados declarados INEXEQUIBLES por la Corte Constitucional mediante Sentencia C-535-08 de 28 "
                 "de mayo de 2008",
                 "Apartes tachados declarados INEXEQUIBLES por la Corte Constitucional mediante Sentencia C-978-10 de 1o. "
                 "de diciembre de 2010, Magistrado Ponente Dr. Luis Ernesto Vargas Silva. Con efectos retroactivos a partir "
                 "de la fecha de promulgación de esta ley",
                 "Inciso 23 declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-979-10 de 1o. de "
                 "diciembre de 2010, Magistrado Ponente Dr. Juan Carlos Heno Pérez. Con efectos retroactivos a partir de "
                 "la fecha de promulgación de esta ley"):
        _need(need in jv, f"L1151 art. 6 JV {need[:40]!r}")
    items = u["items"]
    # the paragraphs with struck words, each followed by its ruling's box, and inciso 23's label paragraph
    struck = [i for i, it in enumerate(items) if it[0] == "p" and E.tidy(E.to_text(it[1], True)) != E.tidy(E.to_text(it[1], False))]
    _need(struck == [109, 213, 215, 217], f"L1151 art. 6 struck paragraphs {struck}")

    def box_after(i):
        return next(E.plain(it[2]) for it in items[i + 1:] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")
    _need("C-978-10" in box_after(109) and "C-535-08" in box_after(217) and "C-535-08" not in box_after(109)
          and E.markers(items[109][1]) == ["Apartes tachados INEXEQUIBLES"]
          and E.markers(items[201][1]) == ["Incisos tachados INEXEQUIBLES"], "L1151 art. 6 rulings by paragraph")
    _need(E.markers(items[92][1]) == ["Inciso 23 INEXEQUIBLE"] and not re.search(r"\w", E.tidy(E.to_text(items[92][1], True))),
          "L1151 art. 6 inciso 23 label")
    blks = [blk for b in H.B23._boxes(u, "Legislación Anterior") for blk in E.la_blocks(b)]
    _need(len(blks) == 1 and blks[0]["head"].rstrip(" :.").startswith("Texto original de la Ley 1151 de 2007"), "L1151 art. 6 box")
    inc = [E.tidy(re.sub(r"^(?:<[^<>]*>\s*)+", "", x)) for x in E.block_text(blks[0]["paras"], False)]
    inc = [x for x in inc if x]
    _need(len(inc) == 1 and inc[0].startswith("Para garantizar lo establecido en el parágrafo 2o del artículo 26 de la Ley "
                                             "1122 de 2007") and "Telemedicina" in inc[0], f"L1151 art. 6 inciso 23 {inc}")
    # inciso 23 of numeral 3.3: its 23rd paragraph after the heading, list items 'i)', 'ii)' ... not counted (the
    # objection note's inciso 20 'Los entes territoriales ...' counts the same way); its label paragraph counted
    ps = [i for i, it in enumerate(items) if it[0] == "p"]
    s33 = next(i for i in ps if E.tidy(E.to_text(items[i][1], True)).startswith("3.3 "))
    inc33 = [i for i in ps if s33 < i <= 92 and not re.match(r"[ivx]+\) ", E.tidy(E.to_text(items[i][1], True)))
             and (i == 92 or re.search(r"\w", E.tidy(E.to_text(items[i][1], True))))]
    _need(len(inc33) == 23 and E.tidy(E.to_text(items[inc33[19]][1], True)).startswith("Los entes territoriales a partir"),
          f"L1151 art. 6 inciso 23 position {len(inc33)}")
    v0 = _lines(u, keep={109, 213, 215, 217}, subst={92: inc[0]})
    v08 = _lines(u, keep={109}, subst={92: inc[0]})
    v10 = H._printed(u)
    _need(_lines(u) == v10 and len(v0) == len(v10) + 4 and len(v08) == len(v10) + 1, "L1151 art. 6 line counts")
    h = H._hist(act, "art-0006")
    # (the engine kept a lone '.' line, the full stop after the struck inciso 'Mientras se cumple ...': left out)
    _need([(d, c) for d, _, c in h] == [(D1151, None), (D1450, [L1450])] and h[0][1] == [H.PH]
          and [x for x in h[1][1] if re.search(r"\w", x)] == v10 and h[1][1].count(".") == 1, f"L1151 art. 6 {H._shape(h)}")
    _need([v["credits"].get("art-0006") for v in act["versions"] if v["from"] == "2008-07-09"] == [["c-714-08"]],
          "L1151 art. 6 C-714-08")
    c535 = E.add_court("C-535-08", "2008-05-28", "c-535_2008.html")
    c978 = E.add_court("C-978-10", "2010-12-01", "c-978_2010.html")
    c979 = E.add_court("C-979-10", "2010-12-01", "c-979_2010.html")
    for c in (c535, c978, c979):
        E.LAWS[c]["note"] = None
    _need((c535, c978, c979) == ("c-535-08", "c-978-10", "c-979-10"), "L1151 art. 6 court keys")
    _apply(act, L1151, "art-0006", [(None, v0, None), ("2008-05-28", v08, c535), ("2008-07-09", v08, "c-714-08"),
                                    ("2010-12-01", v10, c978), (D1450, None, L1450)])
    v = next(v for v in act["versions"] if v["from"] == "2010-12-01")
    v["credits"]["art-0006"] = [c978, c979]
    H._done(T1151, fix_1151_6)
    H.B29.HAND_DONE.append(
        f"{T1151}: art. 6: Sentencias C-978-10 and C-979-10 struck their words 'con efectos retroactivos a partir de la "
        "fecha de promulgación de esta ley' (ex tunc). Coordinator decision (as for Sentencia C-1316-00): a ruling's "
        "effect back to the act's first day is recorded here and does not rewrite the past; the words stand in the "
        "versions before the ruling's day and leave on that day.")


def fix_1151_38(act):
    """art. 38 (the pension liabilities of the national state universities): the page shows struck the end of its
    first inciso ('en los términos establecidos en el artículo 131 de la Ley 100 de 1993. Las sumas que se hayan
    transferido ...') and the words of its parágrafo, which Sentencia C-507-08 (21 May 2008) struck ('Apartes
    subrayados declarados EXEQUIBLES, tachado INEXEQUIBLE'). The words stand from 25 July 2007 and the struck ones go on
    21 May 2008, credited to the ruling (the engine had left them out of every version); the article leaves on 16 June
    2011 (Ley 1450 de 2011 art. 276 did not keep it). Sentencias C-459-08 and C-665-08 ('estarse a lo resuelto') make
    no version."""
    E = H.E
    u = _u(L1151, "38")
    _need("Apartes subrayados declarados EXEQUIBLES, tachado INEXEQUIBLE, por la Corte Constitucional mediante Sentencia "
          "C-507-08 de 21 de mayo de 2008" in H._jv(u)
          and E.markers(next(it[1] for it in u["items"] if it[0] == "p"))[:2]
          == ["Artículo derogado por el artículo 276 de la Ley 1450 de 2011", "Aparte tachado INEXEQUIBLE"], "L1151 art. 38 page")
    before, after = _lines(u, keep={0, 1}), _lines(u)
    _need(len(before) == len(after) == 2 and before != after and after[1] == "PARÁGRAFO..", f"L1151 art. 38 lines {after}")
    h = H._hist(act, "art-0038")
    _need([(d, c) for d, _, c in h] == [(D1151, None), (D1450, [L1450])] and h[0][1] == after, f"L1151 art. 38 {H._shape(h)}")
    _need(E.LAWS["c-507-08"]["enacted"] == "2008-05-21", "C-507-08 day")
    _apply(act, L1151, "art-0038", [(None, before, None), ("2008-05-21", after, "c-507-08"), (D1450, None, L1450)])
    H._done(T1151, fix_1151_38)


def fix_1151_156(act):
    """art. 156 (the UGPP): kept by Ley 1450 de 2011 art. 276. The page gives the 2007 words of numerals 1 to 5 and of
    the inciso after them in its earlier-text boxes; the inciso's box underlines the word 'año', which Decreto 1193 de
    2012 art. 1 (a correction decree, Diario Oficial No. 48.452 of 5 June 2012) added ('en el máximo de un (1) año
    posterior'). The words without 'año' stand from 25 July 2007; the correction from 5 June 2012, credited to the
    decree; Ley 1607 de 2012 art. 198 repealed numerals 1 to 5 and the inciso from 26 December 2012, as the engine read
    them (it had the placeholder up to 2012)."""
    u = _u(L1151, "156")
    nv = H._nv(u)
    _need("Inciso corregido - adiciona la palabra 'año'- por el artículo 1 del Decreto 1193 de 2012, publicado en el "
          "Diario Oficial No. 48.452 de 5 de junio de 2012" in nv
          and "Este artículo continúa vigente según lo dispuesto por el artículo 276 de la Ley 1450 de 2011" in nv,
          "L1151 art. 156 NV")
    raw = " ".join(str(b) for b in H.B23._boxes(u, "Legislación Anterior"))
    _need(raw.count("<U>") == 1 and "un (1) <U>a&ntilde;o</U> posterior a la interposici" in raw, "L1151 art. 156 box 'año'")
    h = H._hist(act, "art-0156")
    _need([(d, c) for d, _, c in h] == [(D1151, None), ("2012-06-05", ["dec-1193-2012"]), ("2012-12-26", ["ley-1607-2012"])]
          and h[0][1] == [H.PH], f"L1151 art. 156 {H._shape(h)}")
    t12 = h[1][1]
    k = [i for i, x in enumerate(t12) if "en el máximo de un (1) año posterior a la interposición" in x]
    _need(len(k) == 1 and t12[k[0]].startswith("Previamente a la expedición de la liquidación oficial"), "L1151 art. 156 line")
    t07 = list(t12)
    t07[k[0]] = t12[k[0]].replace("un (1) año posterior", "un (1) posterior")
    _apply(act, L1151, "art-0156", [(None, t07, None), ("2012-06-05", t12, "dec-1193-2012"),
                                    ("2012-12-26", h[2][1], "ley-1607-2012")])
    H._done(T1151, fix_1151_156)


# ------------------------------------------------------------------------------------------------- Ley 812 de 2003

def _events(act, key):
    """[(day, body lines or None, law)]: the unit's first text and every version that changes it or credits a law for
    it (a ruling that changed no words keeps its day and credit), one law each."""
    out, last = [], object()
    for v in act["versions"]:
        if "units" not in v:
            if v["credits"].get(key):
                c = v["credits"][key]
                _need(len(c) == 1, f"{key} {v['from']} credits {c}")
                out.append((v["from"], out[-1][1], c[0]))
            continue
        t = (v["units"].get(key) or {}).get("text")
        c = v["credits"].get(key)
        if t != last or c:
            _need(len(c or []) <= 1, f"{key} {v['from']} credits {c}")
            out.append((v["from"], None if t is None else t.split(chr(10))[1:-1], (c or [None])[0]))
            last = t
    return out


def fix_812_8(act):
    """art. 8 (the description of the main investment programmes), before it lapsed in 2007 (below): numeral 3, literal
    D, inciso 8 reads the original words the page gives in its earlier-text box (headed 'Texto original de la Ley 848 de
    2003', a slip for Ley 812 de 2003: the box sits under this act's inciso 8) up to Ley 917 de 2004 art. 16 (3 December
    2004) and Ley 921 de 2004 art. 60 (27 December 2004), as the engine read those two (it had the placeholder for the
    whole article up to 2004). The inciso 'Las loterías asociadas ...' (its words from the 'Texto original de la Ley 812
    de 2003' box) stands until Sentencia C-573-04 (8 June 2004) struck it. The struck words of the inciso 'Conforme con
    la reglamentación que expida el Gobierno Nacional ...' leave on 12 October 2004 (Sentencia C-991-04, the ruling the
    box under them names; the engine had credited them to Sentencia C-533-05), those of the inciso 'Las nuevas
    inversiones en la red terciaria ...' on 24 May 2005 (Sentencia C-533-05). Sentencia C-1114-03 (25 November 2003)
    struck Ley 788 de 2002 art. 103, which an inciso of this article cites: no word change, its credit kept; Sentencia
    C-1128-04 ('estarse a lo resuelto') makes no version. Labels with no words left ('-' of the struck inciso) are not
    lines of the text."""
    E = H.E
    u = _u(L812, "8")
    items = u["items"]
    _need(E.markers(items[199][1]) == ["Inciso INEXEQUIBLE"] and E.markers(items[89][1]) == ["Aparte tachado INEXEQUIBLE"]
          and E.markers(items[332][1]) == ["Aparte tachado INEXEQUIBLE"]
          and E.plain(items[365][1]).startswith("- <Inciso modificado por el por el artículo 60 de la Ley 921 de 2004."),
          "L812 art. 8 items")

    def box_after(i, title):
        return next(it[2] for it in items[i + 1:] if it[0] == "box" and it[1] == title)
    _need("Sentencia C-533-05 de 24 de mayo de 2005" in E.plain(box_after(89, "Jurisprudencia Vigencia"))
          and "Inciso declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-573-04 de 8 de junio de 2004"
          in E.plain(box_after(199, "Jurisprudencia Vigencia"))
          and "Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-991-04 de 12 de octubre "
              "de 2004" in E.plain(box_after(332, "Jurisprudencia Vigencia")), "L812 art. 8 rulings")
    lot = [blk for blk in E.la_blocks(box_after(199, "Legislación Anterior"))]
    _need(len(lot) == 1 and lot[0]["head"].rstrip(" :.") == "Texto original de la Ley 812 de 2003", "L812 art. 8 lotteries box")
    lot = [E.tidy(x) for x in E.block_text(lot[0]["paras"], False) if E.tidy(x)]
    _need(len(lot) == 1 and lot[0].startswith("- Las loterías asociadas, o donde confluyan dos o más departamentos"),
          f"L812 art. 8 lotteries {lot}")
    bl = {b["head"].rstrip(" :."): [E.tidy(re.sub(r"^<(?:INCISO|Inciso) \d+o?\.?>\s*", "", x))
                                   for x in E.block_text(b["paras"], False) if E.tidy(x)]
          for b in E.la_blocks(box_after(365, "Legislación Anterior"))}
    _need(sorted(bl) == ["Texto modificado por la Ley 917 de 2004", "Texto original de la Ley 848 de 2003"], f"L812 art. 8 heads {sorted(bl)}")
    orig, l917 = bl["Texto original de la Ley 848 de 2003"], bl["Texto modificado por la Ley 917 de 2004"]
    _need(len(orig) == 1 and orig[0].startswith("El Departamento Nacional de Planeación suministrará a los alcaldes")
          and "Diario Oficial 45.751 de 3 de diciembre de 2004" in H._nv(u)
          and "Inciso 8. del numeral 3, Literal D. modificado por el artículo 60 de la Ley 921 de 2004" in H._nv(u), "L812 art. 8 inciso 8")
    p365 = E.tidy(E.to_text(items[365][1], False))
    p366 = E.tidy(E.to_text(items[366][1], False))
    _need(p365.startswith("- Los municipios") and l917 == [p365[2:], p366], f"L812 art. 8 Ley 917 = Ley 921 words")
    v533 = _lines(u)
    v921 = _lines(u, keep={89})
    v917 = _lines(u, keep={89}, subst={365: p365[2:]})
    v991 = _lines(u, keep={89}, subst={365: orig[0], 366: ""})
    v573 = _lines(u, keep={89, 332}, subst={365: orig[0], 366: ""})
    v0 = _lines(u, keep={89, 332}, subst={365: orig[0], 366: "", 199: lot[0]})
    h = _events(act, "art-0008")
    _need([(d, c) for d, _, c in h] == [("2003-06-27", None), ("2003-11-25", "c-1114-03"), ("2004-12-03", "ley-917-2004"),
                                        ("2004-12-27", "ley-921-2004"), ("2005-05-24", "c-533-05")]
          and h[0][1] == [H.PH] and [x for x in h[4][1] if re.search(r"\w", x)] == v533
          and [x for x in h[3][1] if re.search(r"\w", x)] == _lines(u, keep={89, 332})
          and [x for x in h[2][1] if re.search(r"\w", x)] == _lines(u, keep={89, 332}, subst={365: p365[2:]}),
          f"L812 art. 8 {H._shape(H._hist(act, 'art-0008'))}")
    c573 = E.add_court("C-573-04", "2004-06-08", "c-573_2004.html")
    c991 = E.add_court("C-991-04", "2004-10-12", "c-991_2004.html")
    for c in (c573, c991):
        E.LAWS[c]["note"] = None
    _need((c573, c991) == ("c-573-04", "c-991-04"), "L812 art. 8 court keys")
    _apply(act, L812, "art-0008", [(None, v0, None), ("2003-11-25", v0, "c-1114-03"), ("2004-06-08", v573, c573),
                                   ("2004-10-12", v991, c991), ("2004-12-03", v917, "ley-917-2004"),
                                   ("2004-12-27", v921, "ley-921-2004"), ("2005-05-24", v533, "c-533-05")])
    H._done(T812, fix_812_8)


def fix_812_11(act):
    """art. 11 (the evaluation of the plan): two struck apartes, two rulings. Sentencia C-022-04 (20 January 2004)
    struck 'concertarán con el Gobierno Nacional la inclusión de las inversiones contenidas en el rubro de "inversiones
    regionales por sectorizar ... vigencia 2003'; Sentencia C-373-04 (27 April 2004) struck the words 'parte del' (the
    struck words in italics). The engine had both go on the second ruling's day."""
    E = H.E
    u = _u(L812, "11")
    jv = H._jv(u)
    _need("Aparte tachado y en letra itálica 'parte del' declarado INEXEQUIBLE" in jv and "Sentencia C-373-04 de 27 de abril "
          "de 2004" in jv and "Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-022-04 "
          "de 20 de enero de 2004" in jv, "L812 art. 11 JV")
    raw = u["items"][0][1]
    spans = re.findall(r"<S>.*?</S>", raw, flags=re.S)
    _need(len(spans) == 2 and E.plain(spans[0]).strip() == "parte del" and E.plain(spans[1]).startswith("concertarán con el"),
          f"L812 art. 11 spans {[E.plain(s)[:20] for s in spans]}")
    t022 = E.tidy(E.to_text(raw.replace(spans[1], ""), True))
    v0, v022, v373 = _lines(u, keep={0}), _lines(u, subst={0: t022}), _lines(u)
    h = _events(act, "art-0011")
    _need([(d, c) for d, _, c in h] == [("2003-06-27", None), ("2004-04-27", "c-373-04")] and h[0][1] == v0
          and h[1][1] == v373 and v0 != v022 != v373, f"L812 art. 11 {H._shape(H._hist(act, 'art-0011'))}")
    _need(E.LAWS["c-022-04"]["enacted"] == "2004-01-20", "C-022-04 day")
    _apply(act, L812, "art-0011", [(None, v0, None), ("2004-01-20", v022, "c-022-04"), ("2004-04-27", v373, "c-373-04")])
    H._done(T812, fix_812_11)


def fix_812_87(act):
    """art. 87 (rewrites numeral 3 of Ley 21 de 1982 art. 11): the page prints '<Artículo INEXEQUIBLE>' and gives the
    words in its 'Texto original de la Ley 812 de 2003' box (heading misprinted 'ARTÍCILO 87.'); Sentencia C-669-04 (13
    July 2004) struck the article. The words stand from 27 June 2003 to the ruling's day, credited to it (the engine had
    the article in no version)."""
    E = H.E
    u = _u(L812, "87")
    _need(E.markers(next(it[1] for it in u["items"] if it[0] == "p")) == ["Artículo INEXEQUIBLE"]
          and "Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-669-04 de 13 de julio de 2004"
          in H._jv(u), "L812 art. 87 page")
    blks = [b for x in H.B23._boxes(u, "Legislación Anterior") for b in E.la_blocks(x)]
    _need(len(blks) == 1 and blks[0]["head"].rstrip(" :.") == "Texto original de la Ley 812 de 2003", "L812 art. 87 box")
    ls = [E.tidy(x) for x in E.block_text(blks[0]["paras"], False) if E.tidy(x)]
    _need(len(ls) == 2 and ls[0] == "ARTÍCILO 87. El numeral 3 del artículo 11 de la Ley 21 de 1982, quedará así:"
          and ls[1].startswith("3. El medio por ciento (1/2%) será destinado"), f"L812 art. 87 lines {ls}")
    epi = E.tidy(E.ART_HEAD.sub("", u["label"], count=1))
    _need(epi == "DESTINACIÓN DE LOS RECURSOS A LOS QUE HACE MENCIÓN EL ARTÍCULO 11 DE LA LEY 21 DE 1982.", f"L812 art. 87 {epi}")
    words = [f"{epi} {ls[0][len('ARTÍCILO 87. '):]}", ls[1]]
    _need(all(b is None for _, b, _ in H._hist(act, "art-0087")), "L812 art. 87 already there")
    c669 = E.add_court("C-669-04", "2004-07-13", "c-669_2004.html")
    E.LAWS[c669]["note"] = None
    _units_on(act, {"2004-07-13"})
    H._set(act, "art-0087", "Art. 87", [(None, words, None), ("2004-07-13", None, c669)])
    H.B23._forget(L812, "art-0087")
    H._done(T812, fix_812_87)


def fix_812_160(act):
    """Ley 1151 de 2007 art. 160 (in force from its publication, 25 July 2007) kept in force the articles of Ley 812 de
    2003 it lists. The page marks every other article '<La vigencia de este artículo no fue prorrogada por el artículo
    160 de la Ley 1151 de 2007>' and still prints its words. Coordinator decision (the rule for tacit loss of force):
    those articles leave on 25 July 2007, credited to Ley 1151 de 2007 (the engine kept them to today). Art. 131: art.
    160 names '131', but the page marks art. 131 as not extended and prints art. 132 (the Superintendencia's fondo
    empresarial) as continuing under art. 160 and the later plans; the history follows the page (art. 131 out on 25 July
    2007, art. 132 to today). Art. 137 (the vigencia article), which the page does not mark, stays in the text."""
    E = H.E
    done = []
    for u in H.P.doc_units(L812)[1:]:
        num = E.label_num(u["label"] or "")
        if not num:
            continue
        ps = [it[1] for it in u["items"] if it[0] == "p"]
        if not ps or not any(m == LAPSE160 for m in E.markers(ps[0])):
            continue
        key = _key(num)
        h = _events(act, key)
        _need(h and h[-1][1] is not None and all(d < D1151 for d, _, _ in h), f"L812 {key} {H._shape(H._hist(act, key))}")
        _apply(act, L812, key, [(None if i == 0 else d, b, c) for i, (d, b, c) in enumerate(h)] + [(D1151, None, K1151)])
        GONE[(L812, key)] = ("p0", LAPSE160)
        done.append(int(num))
    _need(len(done) == 99 and 131 in done and 132 not in done and 137 not in done, f"L812 160 {len(done)}")
    u132 = _u(L812, "132")
    _need("Este artículo continúa vigente según lo dispuesto por el artículo 160 de la Ley 1151 de 2007" in H._nv(u132),
          "L812 art. 132 NV")
    _need("Este artículo continúa vigente según lo dispuesto por el artículo 160 de la Ley 1151 de 2007" in H._nv(_u(L812, "131")),
          "L812 art. 131 NV")
    _need(E.law_day(K1151) == D1151, f"Ley 1151 day {E.law_day(K1151)}")
    H.B29.HAND_DONE.append(f"{T812}: " + " ".join(fix_812_160.__doc__.split()) + " Articles out on 25 July 2007: "
                           + ", ".join(map(str, sorted(done))) + ".")


L1450_MARK = ("Artículo derogado el artículo 276 de la Ley 1450 de 2011", "Artículo derogado por el artículo 276 de la Ley 1450 de 2011")


def fix_812_276(act):
    """Ley 1450 de 2011 art. 276 (16 June 2011) kept only arts. 20, 59, 61, 64, 65, 81 and 121 of Ley 812 de 2003 and
    repealed the rest. Arts. 13, 14, 21, 43, 51, 69, 71, 75, 82, 83, 86, 92, 103 and 110 (kept in 2007 by Ley 1151 de
    2007 art. 160; page marker 'Artículo derogado [por] el artículo 276 de la Ley 1450 de 2011') read the words the page
    prints from 27 June 2003 and leave on 16 June 2011, credited to Ley 1450 de 2011 (the engine had the placeholder up
    to 2011 and the words from then to today; art. 82 it already read so). Art. 83 is not in art. 160's list, but the page gives it the Ley 1450
    marker and no note of a lapse in 2007: the page is followed. Art. 38: art. 160 kept it 'reemplazando la expresión
    "el CNSSS" por "la Comisión de Regulación en Salud"': 'El CNSSS definirá ...' from 2003, 'La Comisión de Regulación
    en Salud definirá ...' from 25 July 2007, credited to Ley 1151 de 2007 (the page prints 'El CNSSS* <la Comisión de
    Regulación en Salud>'), out on 16 June 2011. Art. 63: the page marks the article but its parágrafo as out under art.
    160 and the parágrafo as not extended by Ley 1450: all its words from 2003, the parágrafo alone from 25 July 2007
    (credited to Ley 1151 de 2007), out on 16 June 2011. Art. 65 was kept 'para el servicio de gas natural', which
    changes no words: no version."""
    E = H.E
    done = []
    for num in ("13", "14", "21", "38", "43", "51", "63", "69", "71", "75", "82", "83", "86", "92", "103", "110"):
        u = _u(L812, num)
        ms = E.markers(next(it[1] for it in u["items"] if it[0] == "p"))
        key = _key(num)
        h = H._hist(act, key)
        printed = H._printed(u)
        if num == "82":  # the engine read this one right: the printed words from 2003, out on 16 June 2011
            _need([(d, c) for d, _, c in h] == [("2003-06-27", None), (D1450, [L1450])] and h[0][1] == printed
                  and h[1][1] is None and ms[:1] == ["Artículo derogado por el artículo 276 de la Ley 1450 de 2011"],
                  f"L812 art. 82 {H._shape(h)}")
            GONE[(L812, key)] = ("p0", ms[0])
            done.append(num)
            continue
        _need([(d, c) for d, _, c in h] == [("2003-06-27", None), (D1450, [L1450])] and h[0][1] == [H.PH]
              and h[1][1] == printed, f"L812 art. {num} {H._shape(h)}")
        if num == "63":
            _need(ms[0] == ("Artículo, salvo el parágrafo, derogado al no ser prorrogada su vigencia, según lo dispuesto por "
                            "el artículo 160 de la Ley 1151 de 2007"), f"L812 art. 63 {ms}")
            _need(any("<Parágrafo derogado, al no ser prorrogada su vigencia por el artículo 276 de la Ley 1450 de 2011>"
                      in E.plain(it[1]) for it in u["items"] if it[0] == "p"), "L812 art. 63 parágrafo marker")
            _need(len(printed) == 4 and printed[3].startswith("PARÁGRAFO. La Comisión de Regulación de Energía y Gas"),
                  "L812 art. 63 lines")
            GONE[(L812, key)] = ("p0", ms[0])
            tl = [(None, printed, None), (D1151, [printed[3]], K1151), (D1450, None, L1450)]
        else:
            _need(len(ms) >= 1 and ms[0] in L1450_MARK, f"L812 art. {num} marker {ms}")
            GONE[(L812, key)] = ("p0", ms[0])
            tl = [(None, printed, None), (D1450, None, L1450)]
        if num == "83":
            _need(not H._nv(u), "L812 art. 83 notes")
        elif num == "103":  # (its note gives only the 2007 extension; the marker gives the 2011 repeal)
            _need(H._nv(u).strip(" -") == ("Este artículo continúa vigente según lo dispuesto por el artículo 160 de la Ley "
                                           "1151 de 2007, publicada en el Diario Oficial No. 46.700 de 25 de julio de 2007."),
                  "L812 art. 103 notes")
        else:
            _need("no fue prorrogada por el artículo 276 de la Ley 1450 de 2011" in H._nv(u), f"L812 art. {num} NV")
        if num == "38":
            _need("reemplazando la expresión \"el CNSSS\" por \"la Comisión de Regulación en Salud\""
                  in E.plain(next(it[1] for it in _u(L1151, "160")["items"] if it[0] == "p")), "Ley 1151 art. 160 CNSSS")
            k = [i for i, x in enumerate(printed) if "El CNSSS* definirá" in x]
            _need(len(k) == 1, "L812 art. 38 CNSSS line")
            o, n = list(printed), list(printed)
            o[k[0]] = printed[k[0]].replace("El CNSSS* definirá", "El CNSSS definirá")
            n[k[0]] = printed[k[0]].replace("El CNSSS* definirá", "La Comisión de Regulación en Salud definirá")
            tl = [(None, o, None), (D1151, n, K1151), (D1450, None, L1450)]
        _apply(act, L812, key, tl)
        done.append(num)
    _need(len(done) == 16, f"L812 276 {done}")
    u65 = _u(L812, "65")
    _need(E.markers(next(it[1] for it in u65["items"] if it[0] == "p"))[:1] == ["Continúa vigente para el servicio de gas natural"],
          "L812 art. 65 marker")
    H._done(T812, fix_812_276)


def fix_1151_notes(act):
    """readings that change no words. (1) art. 27 (rewrites Ley 160 de 1994 art. 31): Sentencia C-507-08 notes that Ley
    1152 de 2007 art. 178 repealed it, and Sentencia C-175-09 (press release of 18 March 2009) struck Ley 1152 de 2007 as
    a whole; Ley 1450 de 2011 art. 276 then named art. 27 among the articles of this act it kept in force, and the page
    prints it as in force today: it stands from 2007 to today, as the page gives it. (2) art. 61 (the fuel information
    system): not in Ley 1450 de 2011 art. 276's list, but the page prints it as in force and its notes quote Ley 1753 de
    2015 art. 210 on the system 'creado mediante el artículo 61 de la Ley 1151 del 2007 y modificado por el artículo 100 de
    la Ley 1450 del 2011': it stands to today, as the page gives it. (3) art. 160 (vigencia and repeals) stays in the
    text."""
    u27, u61 = _u(L1151, "27"), _u(L1151, "61")
    _need("derogado por el artículo 178 de la Ley 1152 de 2007" in H._jv(u27) and "Sentencia C-175-09" in H._jv(u27)
          and not any(m for it in u27["items"] if it[0] == "p" for m in H.E.markers(it[1])), "L1151 art. 27 page")
    _need("modificado por el artículo 100 de la Ley 1450 del 2011" in H._nv(u61), "L1151 art. 61 NV")
    for key in ("art-0027", "art-0061", "art-0160"):
        h = H._hist(act, key)
        _need(len(h) == 1 and h[0][1], f"L1151 {key} {H._shape(h)}")
    H._done(T1151, fix_1151_notes)


H.FIXES[S1151] = [fix_1151_276, fix_1151_6, fix_1151_38, fix_1151_156, fix_1151_notes]
H.FIXES[S812] = [fix_812_8, fix_812_11, fix_812_87, fix_812_160, fix_812_276]
