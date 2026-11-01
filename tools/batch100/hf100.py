"""Hand-set histories for batch 100 (Ley 756 de 2002), installed by hand_fixes.install(); each checks the page
first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


L756, T756, S756 = "ley_0756_2002", "Reforma de la Ley 141 de 1994, regalías (Ley 756 de 2002)", "reforma-de-regalias-2002"
TRANSF = "PARÁGRAFO. La transferencia de los dineros por parte de la Comisión Nacional de Regalías a las entidades a que hace referencia el literal a) del parágrafo 1o del artículo 1o de la presente ley"
P1_ORIG = "PARÁGRAFO 1o. El porcentaje restante del treinta por ciento (30%)"


def _box(u, head, num):
    blks = [b for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior" for b in H.E.la_blocks(it[2])]
    H.B23._need([b["head"] for b in blks] == [head], f"L756 art. {num} box heads {[b['head'] for b in blks]}")
    ls = H.E.block_text(blks[0]["paras"], False)
    return [re.sub(rf"^ART[ÍI]CULO {num}\.\s*", "", ls[0])] + ls[1:]


def fix_756_8_9(act):
    """Ley 756 de 2002, arts. 8 and 9 (regalías of a deposit in two or more territorial entities; of offshore
    production): repealed by art. 160 of Decreto 4923 de 2011, in force from 1 January 2012 ('Rige a partir del 1o. de
    enero de 2012', the notes), and again by art. 160 of Ley 1530 de 2012 (17 May 2012), which changed no further words
    and makes no version (as for Ley 141 de 1994 arts. 21 and 22). The text as enacted is the page's box 'Texto original
    de la Ley 765 de 2002' (a slip for 756: the box prints this act's article); it stands from the act's first day,
    where the engine had held a placeholder."""
    for num in ("8", "9"):
        key = f"art-000{num}"
        u = H.B23._unit(L756, num)
        nv = " ".join(H._nv(u).split())
        H.B23._need("Artículo derogado por el artículo 160 del Decreto 4923 de 2011" in nv and "Rige a partir del 1o. de enero de 2012" in nv
                    and "Artículo derogado por el artículo 160 de la Ley 1530 de 2012" in nv, f"L756 art. {num} notes")
        ls = _box(u, "Texto original de la Ley 765 de 2002:", num)
        h = H._hist(act, key)
        H.B23._need([d for d, _, _ in h] == ["2002-07-25", "2012-01-01"] and h[0][1] == [H.PH] and h[1][1] is None
                     and h[1][2] == ["dec-4923-2011"], f"L756 art. {num} shape {H._shape(h)}")
        H._set(act, key, H._label(act, key), [(None, ls, None), ("2012-01-01", None, "dec-4923-2011")])
    H._done(T756, fix_756_8_9)


def fix_756_20_21(act):
    """Ley 756 de 2002, arts. 20 and 21 (new arts. 35 and 43 of Ley 141 de 1994, distribution of emerald royalties and
    compensations): Decreto 1660 de 2008 corrected the name of a municipality ('Guvetá' to 'Guayatá') inside the
    distribution table, and tables are left out of the text (as everywhere in the corpus); the words this part holds,
    the paragraphs before the table, are the same before and after the correction. They stand from the act's first day,
    where the engine had held a placeholder until the decree, which changes no words here."""
    for num, dart in (("20", "1"), ("21", "2")):
        key = f"art-00{num}"
        u = H.B23._unit(L756, num)
        H.B23._need(f"Artículo corregido por el artículo {dart} del Decreto 1660 de 2008" in H._nv(u)
                    and "Corrige la referencia al municipio Guvetá por el municipio de Guayatá" in H._nv(u), f"L756 art. {num} notes")
        h = H._hist(act, key)
        H.B23._need([d for d, _, _ in h] == ["2002-07-25", "2008-07-20"] and h[0][1] == [H.PH] and h[1][2] == ["dec-1660-2008"]
                    and not any("Guay" in l or "Guvet" in l for l in h[1][1]), f"L756 art. {num} shape {H._shape(h)}")
        H._set(act, key, H._label(act, key), [(None, h[1][1], None)])
    H._done(T756, fix_756_20_21)


def fix_756_30_33(act):
    """Ley 756 de 2002, arts. 30 to 33 (aforos, revisión de aforos, carencia de aforos, declaración de origen),
    repealed by Ley 962 de 2005: the page's 'Texto original' boxes leave out each article's epigraph, which the page's
    own heading prints; the text as enacted reads with it (as Ley 488 de 1998 art. 100)."""
    for num in ("30", "31", "32", "33"):
        key = f"art-00{num}"
        u = H.B23._unit(L756, num)
        epi = H.E.tidy(H.E.ART_HEAD.sub("", u["label"], count=1))
        h = H._hist(act, key)
        H.B23._need(epi and epi.endswith(".") and epi.upper() == epi and [d for d, _, _ in h] == ["2002-07-25", "2005-07-08"]
                    and h[1][1] is None and h[1][2] == ["ley-962-2005"] and not h[0][1][0].startswith(epi),
                    f"L756 art. {num} shape {epi} {H._shape(h)}")
        H._set(act, key, H._label(act, key), [(None, [f"{epi} {h[0][1][0]}"] + h[0][1][1:], None), ("2005-07-08", None, "ley-962-2005")])
    H._done(T756, fix_756_30_33)


def fix_756_35(act):
    """Ley 756 de 2002, art. 35 transitorio (the 70%/30% of the Fondo Nacional de Regalías' unappropriated resources):
    (a) the 'PARÁGRAFO. La transferencia de los dineros ...' the page prints inside the parágrafo 1o. Ley 859 de 2003
    wrote names 'el literal a) del parágrafo 1o del artículo 1o de la presente ley': it is Ley 859's (art. 1) text, in
    neither the act's original parágrafo 1o. nor Ley 788 de 2002's (the page's boxes); it arrives with Ley 859 (29
    December 2003). (b) Ley 788 de 2002 art. 107 rewrote parágrafo 1o. (27 December 2002) and Sentencia C-1114-03 (25
    November 2003) struck that art. 107; the page does not say the 2002 text revived, and a struck law's predecessor
    text does not revive by itself (the corpus's rule): from the ruling's day parágrafo 1o. reads '[La fuente no da el
    texto vigente en esta fecha.]', credited to the ruling, until Ley 859 de 2003. The engine had put the original
    parágrafo 1o. back on the ruling's day."""
    key = "art-0035t"
    u = next(x for x in H.P.doc_units(L756) if x["name"] == "35")
    H.B23._need("El Artículo 107 de la Ley 788 de 2002 fue declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia "
                "C-1114-03 de 25 de noviembre de 2003" in " ".join(H._jv(u).split()) and "reviv" not in H._jv(u).lower(),
                "L756 art. 35 ruling")
    h = H._hist(act, key)
    H.B23._need([d for d, _, _ in h] == ["2002-07-25", "2002-12-27", "2003-11-25", "2003-12-29"]
                and [c for _, _, c in h[1:]] == [["ley-788-2002"], ["c-1114-03"], ["ley-859-2003"]] and h[2][1] == h[0][1]
                and all(sum(l.startswith(TRANSF) for l in b) == 1 for _, b, _ in h)
                and sum(l.startswith(P1_ORIG) for l in h[0][1]) == 1, f"L756 art. 35 shape {H._shape(h)}")
    drop = [[l for l in b if not l.startswith(TRANSF)] for _, b, _ in h[:3]]
    ph = [H.PH if l.startswith(P1_ORIG) else l for l in drop[0]]
    H._set(act, key, H._label(act, key), [(None, drop[0], None), ("2002-12-27", drop[1], "ley-788-2002"),
                                          ("2003-11-25", ph, "c-1114-03"), ("2003-12-29", h[3][1], "ley-859-2003")])
    H._done(T756, fix_756_35)


def fix_756_empty(act):
    """Ley 756 de 2002: the versions of Decreto 1660 de 2008 (20 July 2008) and Ley 1530 de 2012 (17 May 2012) change no
    words and credit nothing after the fixes above (arts. 20/21, 8/9), so they are not versions."""
    vs, out, last = act["versions"], [], None
    gone = []
    for i, v in enumerate(vs):
        if i and not v["credits"] and ("units" not in v or v["units"] == last):
            gone.append(v["from"])
            continue
        if "units" in v:
            last = v["units"]
        out.append(v)
    H.B23._need(gone == ["2008-07-20", "2012-05-17"], f"L756 empty versions {gone}")
    act["versions"] = out
    H._done(T756, fix_756_empty)


H.FIXES[S756] = [fix_756_8_9, fix_756_20_21, fix_756_30_33, fix_756_35, fix_756_empty]
