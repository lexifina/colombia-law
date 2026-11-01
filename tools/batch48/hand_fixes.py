"""Hand-set histories for batch 48, Decreto 960 de 1970 (bound by parse_batch48.py through install(); each checks the
page first)."""
from __future__ import annotations

import re

D = B23 = B29 = B13 = E = P = struck = None
T960 = "Estatuto del Notariado (Decreto 960 de 1970)"
L960 = "decreto_0960_1970"
C159_DAY = "2023-06-20"
DEFERRED_2106 = ["18", "79", "80", "113"]
OPEN: list[str] = []


def _timeline(act, key):
    """The unit's history as set_history's timeline [(day or None, text or None, law)] (one law per change)."""
    out = []
    for i, (day, u, cr) in enumerate(struck.history(act, key)):
        B23._need(cr is None or len(cr) == 1, f"{act['slug']} {key} credits {cr}")
        text = None if u is None else "\n".join(u["text"].split("\n")[1:-1])
        out.append((None if i == 0 else day, text, cr[0] if cr else None))
    return out


def _done(fn, extra=""):
    B29.HAND_DONE.append(f"{T960}: " + " ".join(fn.__doc__.split()) + extra)


def _page_lines(num, keep_struck=False):
    """The article's lines as the page prints them today: epigraph (from the heading) + paragraphs, markers out."""
    u = B23._unit(L960, num)
    epi = re.sub(r"^ART[ÍI]CULO\s+\d+[A-Z]?o?\.\s*", "", u["label"] or "").strip()
    ps = [E.tidy(E.to_text(E.strip_markers(it[1]), keep_struck=keep_struck)) for it in u["items"] if it[0] == "p"]
    ps = [x for x in ps if x]
    return [(epi + " " + ps[0]).strip()] + ps[1:]


def fix_960_2106(act):
    """Decreto 960 de 1970, arts. 18, 79, 80 and 113: Decreto Ley 2106 de 2019 (arts. 60-63, in force 2019-11-22) rewrote
    them; Sentencia C-159-21 (26 May 2021) struck those articles of Decreto Ley 2106 with effect deferred to 20 June
    2023. The page prints Decreto 2106's words under '<Artículo INEXEQUIBLE, con efectos diferidos a partir del 20 de
    junio de 2023>' and does not say whether the 1970 text revived (revival is not automatic). History: the earlier text;
    Decreto 2106's words from 2019-11-22; from 2023-06-20 the article reads '[La fuente no da el texto vigente en esta
    fecha.]', credited to C-159-21 (open item: the text in force since then)."""
    c159 = "c-159-21"
    B23._need(E.LAWS[c159]["enacted"] == "2021-05-26", "C-159-21 day")
    for num in DEFERRED_2106:
        u = B23._unit(L960, num)
        p0 = next(it[1] for it in u["items"] if it[0] == "p")
        B23._need("&lt;Art&iacute;culo INEXEQUIBLE, con efectos diferidos a partir del 20 de junio de 2023&gt;" in p0,
                  f"D960 art. {num} marker")
        jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
        B23._need("Sentencia C-159-21 de 26 de mayo de 2021" in jv and "con efectos diferidos a partir del 20 de junio de "
                  "2023" in jv, f"D960 art. {num} ruling")
        key = E.unit_key(num)[0]
        t = _timeline(act, key)
        B23._need([(d, l) for d, _, l in t][-2:] == [("2019-11-22", "dec-2106-2019"), ("2021-05-26", c159)]
                  and t[-2][1] == E.MISSING_LINE and t[-1][1] is None, f"D960 art. {num} {[(d, l) for d, _, l in t]}")
        t[-2] = ("2019-11-22", "\n".join(_page_lines(num)), "dec-2106-2019")
        t[-1] = (C159_DAY, E.MISSING_LINE, c159)
        B13.B6.set_history(act, key, f"Art. {num}", t)
        B23._forget(L960, key)
    OPEN.append("arts. 18, 79, 80 and 113 from 2023-06-20 (C-159-21): the text in force is not given by the page")
    _done(fix_960_2106)


def fix_960_134(act):
    """Decreto 960 de 1970, art. 134: the page marks the article '<Artículo INEXEQUIBLE>' but names no ruling that struck
    it (its rulings box gives only Sentencia C-128-00 of 16 February 2000, which declared it EXEQUIBLE). The removal has no
    date in the source, so the article keeps its original text (from its earlier-text box) in every version (open item);
    the engine had left it out of every version."""
    u = B23._unit(L960, "134")
    B23._need("&lt;Art&iacute;culo INEXEQUIBLE&gt;" in next(it[1] for it in u["items"] if it[0] == "p"), "D960 art. 134")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("INEXEQUIBLE" not in jv and "EXEQUIBLE por la Corte Constitucional mediante Sentencia C-128-00" in jv,
              f"D960 art. 134 rulings {jv[:200]}")
    orig = B23._box_lines(B23._boxes(u, "Legislación Anterior")[0], "Texto original del Decreto 960 de 1970", True)
    B23._need(len(orig) == 1 and orig[0].startswith("<INHABILIDAD POR CARGO PÚBLICO>. No podrán ser nombrados")
              or orig[0].startswith("No podrán ser nombrados"), f"D960 art. 134 box {orig}")
    text = re.sub(r"^<[^>]*>\.\s*", "", orig[0])
    B23._need(all(cr is None for _, _, cr in struck.history(act, "art-0134")), "D960 art. 134 history")
    B13.B6.set_history(act, "art-0134", "Art. 134", [(None, text, None)])
    B23._forget(L960, "art-0134")
    OPEN.append("art. 134: marked INEXEQUIBLE on the page with no ruling or date; kept in every version")
    _done(fix_960_134)


def fix_960_176(act):
    """Decreto 960 de 1970, art. 176: Sentencia C-153-99 (10 March 1999) struck its numerals 1 and 2 (the original text's
    box marks them '<Numeral INEXEQUIBLE>'); Ley 588 de 2000 art. 11 repealed the article (2000-07-06). History: the
    original text; without numerals 1 and 2 from the ruling's day (the engine had a placeholder); gone from 2000-07-06."""
    u = B23._unit(L960, "176")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("con excepción de los numerales 1 y 2 que se declaran INEXEQUIBLES por la Corte Constitucional mediante "
              "Sentencia C-153-99 del 10 de marzo de 1999" in jv, "D960 art. 176 ruling")
    t = _timeline(act, "art-0176")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("1999-03-10", "c-153-99"), ("2000-07-06", "ley-588-2000")]
              and t[1][1] == E.MISSING_LINE, f"D960 art. 176 {[(d, l) for d, _, l in t]}")
    lines = t[0][1].split("\n")
    B23._need(len(lines) == 4 and lines[1].startswith("1. Estar ejerciendo") and lines[2].startswith("2. Haber ejercido"),
              f"D960 art. 176 text {lines}")
    t[1] = ("1999-03-10", "\n".join([lines[0], lines[3]]), "c-153-99")
    B13.B6.set_history(act, "art-0176", "Art. 176", t)
    B23._forget(L960, "art-0176")
    _done(fix_960_176)


def fix_960_198(act):
    """Decreto 960 de 1970, art. 198: Ley 29 de 1973 art. 7 rewrote numeral 14 (in force 1974-03-25); Sentencia C-399-99
    (2 June 1999) struck its words 'el Colegio de Notarios'; Sentencia C-373-02 (15 May 2002) struck numerals 1 and 6,
    which the page prints as '1.' and '6.' with the original words in earlier-text boxes. History: the original text;
    numeral 14 as Ley 29 worded it from 1974-03-25; without 'el Colegio de Notarios' from 1999-06-02; numerals 1 and 6
    emptied from 2002-05-15 (the engine had a placeholder from 1974 to 2002)."""
    u = B23._unit(L960, "198")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("'el Colegio de Notarios' fue declarado INEXEQUIBLE, por la Corte Constitucional mediante Sentencia C-399-99 "
              "de 2 de junio de 1999" in jv, "D960 art. 198 C-399-99")
    t = _timeline(act, "art-0198")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("1974-03-25", "ley-29-1973"), ("2002-05-15", "c-373-02")]
              and t[1][1] == E.MISSING_LINE, f"D960 art. 198 {[(d, l) for d, _, l in t]}")
    orig, today = t[0][1].split("\n"), t[2][1].split("\n")
    with_words = _page_lines("198", keep_struck=True)
    n14 = [x for x in with_words if x.startswith("14. ")]
    B23._need(len(n14) == 1 and "Fondo Nacional del Notariado, el Colegio de Notarios, sus empleados" in n14[0], f"{n14}")
    i14 = [i for i, x in enumerate(orig) if x.startswith("14. ")]
    B23._need(len(orig) == len(today) == 16 and len(i14) == 1 and today[i14[0]].startswith("14. ")
              and today[1] == "1." and today[6] == "6.", f"D960 art. 198 lines {len(orig)} {len(today)}")
    v1974 = orig[:i14[0]] + n14 + orig[i14[0] + 1:]
    v1999 = orig[:i14[0]] + [today[i14[0]]] + orig[i14[0] + 1:]
    c399 = E.add_court("C-399-99", "1999-06-02", "c-399_1999.html")
    E.LAWS[c399]["note"] = None
    B13.B6.set_history(act, "art-0198", "Art. 198", [(None, t[0][1], None), ("1974-03-25", "\n".join(v1974), "ley-29-1973"),
                                                     ("1999-06-02", "\n".join(v1999), c399),
                                                     ("2002-05-15", t[2][1], "c-373-02")])
    B23._forget(L960, "art-0198")
    _done(fix_960_198)


def fix_960_179(act):
    """Decreto 960 de 1970, art. 179: Sentencia C-153-99 (10 March 1999) declared the whole article INEXEQUIBLE; Ley 588
    de 2000 later named it among its repeals. History: the original text, gone from the ruling's day (the engine had a
    placeholder until the repeal)."""
    u = B23._unit(L960, "179")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-153-99 del 10 de marzo de "
              "1999" in jv, "D960 art. 179 ruling")
    t = _timeline(act, "art-0179")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("1999-03-10", "c-153-99"), ("2000-07-06", "ley-588-2000")]
              and t[1][1] == E.MISSING_LINE and t[2][1] is None, f"D960 art. 179 {[(d, l) for d, _, l in t]}")
    B13.B6.set_history(act, "art-0179", "Art. 179", [t[0], ("1999-03-10", None, "c-153-99")])
    B23._forget(L960, "art-0179")
    _done(fix_960_179)


def fix_960(act):
    fix_960_2106(act)
    fix_960_179(act)
    fix_960_134(act)
    fix_960_176(act)
    fix_960_198(act)


def install(driver):
    global D, B23, B29, B13, E, P, struck
    D = driver
    B23, B29, B13, E, P, struck = D.B23, D.B29, D.B13, D.E, D.P, D.struck
    B29.HAND_FIXES.update({"estatuto-del-notariado": fix_960})
