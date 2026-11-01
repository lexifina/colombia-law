"""Hand-set histories for batch 47 (bound by parse_batch47.py through install(); each checks the page first)."""
from __future__ import annotations

D = B23 = B29 = B13 = E = P = struck = None
T1260 = "Estatuto del Registro del Estado Civil de las personas (Decreto 1260 de 1970)"
L1260 = "decreto_1260_1970"


def _timeline(act, key):
    """The unit's history as set_history's timeline [(day or None, text or None, law)] (one law per change)."""
    out = []
    for i, (day, u, cr) in enumerate(struck.history(act, key)):
        B23._need(cr is None or len(cr) == 1, f"{act['slug']} {key} credits {cr}")
        text = None if u is None else "\n".join(u["text"].split("\n")[1:-1])
        out.append((None if i == 0 else day, text, cr[0] if cr else None))
    return out


def _done(fn):
    B29.HAND_DONE.append(f"{T1260}: " + " ".join(fn.__doc__.split()))


def fix_1260_53(act):
    """Decreto 1260 de 1970, art. 53: Sentencia C-519-19 (5 November 2019) struck the words 'seguido del' of the text Ley
    54 de 1989 gave the article, with its effect deferred until the end of the legislature that closed on 20 June 2022;
    Ley 2129 de 2021 rewrote the article before then (4 August 2021), so the ruling never took effect on these words and
    no version credits it (the engine had read it as restoring the 1970 text on the ruling's day). Decreto 2582 de 1989
    corrected a reference in Ley 54's parágrafo ('artículo 94' read as 'artículo 6o' of Decreto 999 de 1988); the source
    gives that decree no date, so Ley 54's words are kept as printed."""
    u = B23._unit(L1260, "53")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("Aparte tachado 'seguido del' declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-519-19"
              in jv and "hasta aquella que culmina en sesiones ordinarias el 20 de junio de 2022" in jv, "D1260 art. 53 ruling")
    t = _timeline(act, "art-0053")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("1989-12-31", "ley-54-1989"), ("2019-11-05", "c-519-19"),
                                            ("2021-08-04", "ley-2129-2021")] and t[2][1] == t[0][1],
              f"D1260 art. 53 {[(d, l) for d, _, l in t]}")
    B23._need(E.law_day("ley-2129-2021") == "2021-08-04", "Ley 2129 de 2021 day")
    del t[2]
    B13.B6.set_history(act, "art-0053", "Art. 53", t)
    B23._forget(L1260, "art-0053")
    _done(fix_1260_53)


def install(driver):
    global D, B23, B29, B13, E, P, struck
    D = driver
    B23, B29, B13, E, P, struck = D.B23, D.B29, D.B13, D.E, D.P, D.struck
    # Decreto 1536 de 1989 (art. 75): the only date the source gives is its note's 'Diario Oficial No. 40.693 del 18 de
    # diciembre de 1992' (that issue number belongs to December 1992; no page of the decree on the basedoc): dated by the
    # default rule from that day.
    E.HAND_RULES["dec-1536-1989"] = ("1993-02-18", "Decreto 1536 de 1989: the source's only date for it is the note on "
                                                   "Decreto 1260 de 1970 art. 75, 'publicada en el Diario Oficial No. "
                                                   "40.693 del 18 de diciembre de 1992'; default rule (Ley 4 de 1913, "
                                                   "art. 52: two months after promulgation) from that day")
    B29.HAND_FIXES.update({"registro-del-estado-civil": fix_1260_53})
