"""Ley 446 de 1998 hand fixes (batch 54), bound into hand_fixes.FIXES. Coordinator decision (2026-10-31): incorporation
into a compilation decree is not a repeal; an article's earlier-text box words stay in force to today unless the page
dates a repeal or a later rewrite, which ends them on that day."""
from __future__ import annotations

import re

H = None  # hand_fixes module
L446 = "ley_0446_1998"
T446 = "Descongestión, eficiencia y acceso a la justicia (Ley 446 de 1998)"
BOXED: set = set()      # keys whose box words stand today while the page prints none (verifier)
PH_TODAY: set = set()   # keys whose text today is the placeholder while the page prints none (verifier)


def _unit(n):
    return H.B23._unit(L446, n)


def _strip_head(line, n):
    line = re.sub(r"^ART[ÍI]CULO " + n + r"\.\s*", "", line)
    return re.sub(r"^(?:<[^<>]*>\s*)+", "", line)


def _orig(u, n):
    box = next(b for b in H.B23._boxes(u, "Legislación Anterior") if "Texto original de la Ley 446 de 1998" in b)
    ls = H.B23._box_lines(box, "Texto original de la Ley 446 de 1998")
    ls[0] = _strip_head(ls[0], n)
    return [x for x in ls if x]


def _absent_everywhere(act, key):
    return all(key not in (v.get("units") or {}) for v in act["versions"])


INCORPORATED = ["53", "86", "133", "134", "135", "136", "147"]


def fix_incorporated(act):
    """Ley 446 de 1998, arts. 53, 86, 133 to 136 and 147: the page prints no words today, only '<Incorporado en el
    Estatuto de los Mecanismos Alternativos de Solución de Conflictos, artículo N>' or '<Artículo incorporado en el
    Artículo 326 Numeral 8o. del Estatuto Orgánico del Sistema Financiero ...>', with the act's words in the earlier-text
    box. Incorporation into a compilation decree is not a repeal (coordinator decision; the page's own editor's note cites
    C-558-92), and the page dates no repeal or later rewrite of these articles: the box words stand from the act's first
    day to today (the engine had them in no version). Art. 133's marker adds that the text in force is EOSF art. 326
    numeral 8 (C-930-06); that is the compilation's text, not a change to this article."""
    for n in INCORPORATED:
        u = _unit(n)
        ms = H._p0_markers(u)
        H.B23._need(any("ncorporad" in m for m in ms) and not any("derogad" in m.lower() for m in ms), f"Ley 446 art. {n} {ms}")
        key = f"art-{int(n):04d}"
        H.B23._need(_absent_everywhere(act, key), f"Ley 446 art. {n} in a version")
        H._set(act, key, f"Art. {n}", [(None, _orig(u, n), None)])
        BOXED.add(key)
    H._done(T446, fix_incorporated)


def fix_446_77(act):
    """Ley 446 de 1998, art. 77 (rewrote inciso 2 of Ley 23 de 1991 art. 75): words from the earlier-text box from the
    act's first day; the underlined words 'contencioso administrativa' out from 29 June 1999 (Decreto 1122 de 1999 art.
    154) and back from 18 November 1999 (C-923-99 struck that decree as a whole); the article ends on the day Ley 640 de
    2001 art. 49 repealed Ley 23 de 1991 art. 75, which the page dates '24 de enero de 2002' and the corpus dates 5
    January 2002 (Ley 640's articles; see the Ley 640 decision). The engine had it in no version."""
    u = _unit("77")
    H.B23._need("Aparte subrayado derogado por el artículo 154 del Decreto 1122 de 1999" in H._nv(u) and "C-923-99" in H._jv(u),
                "Ley 446 art. 77 notes")
    H.B23._need(any(m.startswith("Artículo 75 de la Ley 23 de 1991 derogado por el artículo 49 de la Ley 640 de 2001")
                    for m in H._p0_markers(u)), "Ley 446 art. 77 marker")
    box = H.B23._boxes(u, "Legislación Anterior")[0]
    H.B23._need(re.findall(r"<U>(.*?)</U>", box) == ["contencioso administrativa"], "Ley 446 art. 77 underlined")
    o = _orig(u, "77")
    k = [i for i, x in enumerate(o) if "civil, contencioso administrativa, comercial" in x]
    H.B23._need(len(k) == 1, "Ley 446 art. 77 words")
    cut = list(o)
    cut[k[0]] = cut[k[0]].replace("civil, contencioso administrativa, comercial", "civil, comercial")
    H.B23._need(_absent_everywhere(act, "art-0077"), "Ley 446 art. 77 in a version")
    H._set(act, "art-0077", "Art. 77", [(None, o, None), ("1999-06-29", cut, "dec-1122-1999"), ("1999-11-18", o, "c-923-99"),
                                        ("2002-01-05", None, "ley-640-2001")])
    H._done(T446, fix_446_77)


def fix_446_85_87(act):
    """Ley 446 de 1998, arts. 85 and 87: struck as a whole by Sentencia C-160-99 (17 March 1999); the source gives no
    words for them (no earlier-text box), so they read '[La fuente no da el texto vigente en esta fecha.]' from the act's
    first day to the ruling (the engine had them in no version)."""
    for n in ("85", "87"):
        u = _unit(n)
        H.B23._need("Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-160-99 del 17 de marzo de "
                    "1999" in H._jv(u) and not H.B23._boxes(u, "Legislación Anterior"), f"Ley 446 art. {n} ruling")
        key = f"art-{int(n):04d}"
        H.B23._need(_absent_everywhere(act, key), f"Ley 446 art. {n} in a version")
        H._set(act, key, f"Art. {n}", [(None, [H.PH], None), ("1999-03-17", None, "c-160-99")])
    H._done(T446, fix_446_85_87)


def _struck_after(u, n):
    box = next(b for b in H.B23._boxes(u, "Legislación Anterior") if "Texto original de la Ley 446 de 1998" in b)
    blk = next(x for x in H.E.la_blocks(box) if x["head"].startswith("Texto original de la Ley 446 de 1998"))
    out = []
    for p in blk["paras"]:
        t = _strip_head(H.E.tidy(H.E.to_text(p, False)), n).replace("..", ".")
        t = re.sub(r"^[,;]\s*", "", t)
        if t:
            out.append(t[0].upper() + t[1:])
    return out


def fix_446_121_122(act):
    """Ley 446 de 1998, arts. 121 and 122: Sentencia C-1038-02 (28 November 2002) struck the words shown struck in the
    earlier-text box; from the ruling the articles read the box without them (a paragraph struck whole keeps its bare
    'PARAGRAFO.' label, as the page prints such labels); out from 12 October 2012 (Ley 1563 de 2012 art. 118). The
    engine had put the placeholder there."""
    for n in ("121", "122"):
        u = _unit(n)
        H.B23._need("Sentencia C-1038-02 de 28 de noviembre de 2002" in H._jv(u), f"Ley 446 art. {n} ruling")
        key = f"art-{int(n):04d}"
        h = H._hist(act, key)
        H.B23._need(H._shape(h)[1:] == [("2002-11-28", ["c-1038-02"], "PH"), ("2012-10-12", ["ley-1563-2012"], None)],
                    f"Ley 446 art. {n} {H._shape(h)}")
        after = _struck_after(u, n)
        H.B23._need(after != h[0][1] and len(after) <= len(h[0][1]), f"Ley 446 art. {n} struck words")
        H._set(act, key, f"Art. {n}", [(None, h[0][1], None), ("2002-11-28", after, "c-1038-02"),
                                       ("2012-10-12", None, "ley-1563-2012")])
    H._done(T446, fix_446_121_122)


def fix_446_151(act):
    """Ley 446 de 1998, art. 151: Sentencia C-247-99 (21 April 1999) struck numerals 4 and 5 ('exepto los numerales 4 y
    5 que se declaran INEXEQUIBLES'); from the ruling the article reads without them; out from 1 January 2000 with its
    title (Ley 552 de 1999). The engine had put the placeholder there."""
    u = _unit("151")
    H.B23._need("exepto los numerales 4 y 5 que se declaran INEXEQUIBLES" in H._jv(u), "Ley 446 art. 151 ruling")
    h = H._hist(act, "art-0151")
    H.B23._need(H._shape(h)[1:] == [("1999-04-21", ["c-247-99"], "PH"), ("2000-01-01", ["ley-552-1999"], None)],
                f"Ley 446 art. 151 {H._shape(h)}")
    o = h[0][1]
    gone = [x for x in o if re.match(r"[45]\. ", x)]
    H.B23._need(len(gone) == 2, f"Ley 446 art. 151 numerals {gone}")
    H._set(act, "art-0151", "Art. 151", [(None, o, None), ("1999-04-21", [x for x in o if x not in gone], "c-247-99"),
                                         ("2000-01-01", None, "ley-552-1999")])
    H._done(T446, fix_446_151)


def fix_446_146_148(act):
    """Ley 446 de 1998, arts. 146 and 148 (Superintendencias' judicial functions; incorporated in EOSF art. 326 numeral
    8): Ley 510 de 1999 art. 51 rewrote art. 146 (4 August 1999); the source gives no wording for that rewrite, so the
    article reads the placeholder from then; C-1641-00 (29 November 2000) struck the rewrite and no revival of the 1998
    words is stated, so the placeholder stays (the rule for struck rewrites), to today (the page prints no words).
    Ley 510 de 1999 also rewrote art. 148: the original words (earlier-text box) from the act's first day, Ley 510's words
    (box 'Texto modificado por la Ley 510 de 1999') from 4 August 1999 to today (incorporated, no dated repeal). The
    engine had the placeholder before 1999 for art. 148 and both out of the record after Ley 510 or the ruling."""
    u = _unit("146")
    H.B23._need("Artículo modificado por el artículo 51 de la Ley 510 de 1999" in H._nv(u) and "La modificación fue "
                "declarada INEXEQUIBLE" in H._nv(u) and "C-1641-00 del 29 de noviembre de 2000" in H._jv(u), "Ley 446 art. 146")
    h = H._hist(act, "art-0146")
    H.B23._need(H._shape(h)[1:] == [("1999-08-04", ["ley-510-1999"], "PH"), ("2000-11-29", ["c-1641-00"], None)],
                f"Ley 446 art. 146 {H._shape(h)}")
    H._set(act, "art-0146", "Art. 146", [(None, h[0][1], None), ("1999-08-04", [H.PH], "ley-510-1999"),
                                         ("2000-11-29", [H.PH], "c-1641-00")])
    PH_TODAY.add("art-0146")
    u = _unit("148")
    box = H.B23._boxes(u, "Legislación Anterior")[0]
    new = H.B23._box_lines(box, "Texto modificado por la Ley 510 de 1999")
    new[0] = _strip_head(new[0], "148")
    orig = H.B23._box_lines(box, "Texto original de la Ley 446 de 1998")
    orig[0] = _strip_head(orig[0], "148")
    H.B23._need(new[0].startswith("El procedimiento que utilizarán las Superintendencias") and
                orig[0].startswith("El procedimiento que utilizarán las Superintendencias"), "Ley 446 art. 148 boxes")
    h = H._hist(act, "art-0148")
    H.B23._need(H._shape(h) == [("1998-07-08", None, "PH"), ("1999-08-04", ["ley-510-1999"], None)],
                f"Ley 446 art. 148 {H._shape(h)}")
    H._set(act, "art-0148", "Art. 148", [(None, [x for x in orig if x], None),
                                         ("1999-08-04", [x for x in new if x], "ley-510-1999")])
    BOXED.add("art-0148")
    H._done(T446, fix_446_146_148)


def install(hmod):
    global H
    H = hmod
    H.FIXES["descongestion-y-acceso-a-la-justicia-1998"] += [fix_incorporated, fix_446_77, fix_446_121_122,
                                                              fix_446_151, fix_446_146_148]
