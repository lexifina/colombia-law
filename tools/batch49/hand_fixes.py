"""Hand-set histories for batch 49, Ley 640 de 2001 (bound by parse_batch49.py through install(); each checks the page
first)."""
from __future__ import annotations

D = B23 = B29 = B13 = E = P = struck = None
T640 = "Conciliación (Ley 640 de 2001)"
L640 = "ley_0640_2001"


def _timeline(act, key):
    """The unit's history as set_history's timeline [(day or None, text or None, law)] (one law per change)."""
    out = []
    for i, (day, u, cr) in enumerate(struck.history(act, key)):
        text = None if u is None else "\n".join(u["text"].split("\n")[1:-1])
        out.append((None if i == 0 else day, text, cr))
    return out


def _set(act, key, label, timeline):
    """set_history with a list of laws per change (the first version's credits as built are kept)."""
    B13.B6.set_history(act, key, label, [(d, t, (ls or [None])[0]) for d, t, ls in timeline])
    for d, _, ls in timeline:
        for v in act["versions"]:
            if v["from"] == d and ls:
                v["credits"][key] = list(ls)


def _done(fn):
    B29.HAND_DONE.append(f"{T640}: " + " ".join(fn.__doc__.split()))


def fix_640_35(act):
    """Ley 640 de 2001, art. 35: Sentencia C-598-11 (10 August 2011) struck the last sentence of parágrafo 2o., as Ley
    1395 de 2010 worded it ('De fracasar la conciliación, en el proceso que se promueva no serán admitidas las pruebas
    ...'); the words are out from the ruling's day (the engine had removed them on 2012-07-02 with Ley 1437 de 2011's
    repeal of other words). Sentencia C-893-01 (22 August 2001) struck the requirement as to the labour jurisdiction
    ('... requisito de procedibilidad ... laboral ...', 'en los términos de esta sentencia'); the page marks no words, so
    the original words stand until Ley 1395 de 2010 rewrote the article."""
    u = B23._unit(L640, "35")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("salvo el aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-598-11 de 10 "
              "de agosto de 2011" in jv, "Ley 640 art. 35 C-598-11")
    t = _timeline(act, "art-0035")
    days = [(d, l) for d, _, l in t]
    B23._need(days == [(None, None), ("2002-01-05", ["ley-640-2001"]), ("2010-07-12", ["ley-1395-2010"]),
                       ("2012-07-02", ["ley-1437-2011"])], f"Ley 640 art. 35 {days}")
    l2010, l2012 = t[2][1].split("\n"), t[3][1].split("\n")
    k = [i for i, x in enumerate(l2010) if x.startswith("PARÁGRAFO 2o.")]
    B23._need(len(k) == 1 and "De fracasar la conciliación" in l2010[k[0]] and l2012[k[0]].startswith("PARÁGRAFO 2o.")
              and "De fracasar" not in l2012[k[0]], "Ley 640 art. 35 parágrafo 2")
    c598 = E.add_court("C-598-11", "2011-08-10", "c-598_2011.html")
    E.LAWS[c598]["note"] = None
    l2011 = l2010[:k[0]] + [l2012[k[0]]] + l2010[k[0] + 1:]
    t.insert(3, ("2011-08-10", "\n".join(l2011), [c598]))
    _set(act, "art-0035", "Art. 35", t)
    B23._forget(L640, "art-0035")
    _done(fix_640_35)


def fix_640_43(act):
    """Ley 640 de 2001, art. 43: the page's earlier-text box gives the article 'con la adición introducida por la ley
    1395 de 2010' and marks the added inciso ('<Inciso adicionado por el artículo 70 de la Ley 1395 de 2010 ...>', with
    the parágrafo the notes say Ley 1395's art. 70 also holds). History: the article without that inciso and parágrafo
    from 2002-01-05 (the engine had a placeholder); with them from 2010-07-12; gone from 2014-01-01 (Ley 1564 de 2012)."""
    u = B23._unit(L640, "43")
    box = B23._boxes(u, "Legislación Anterior")[0]
    B23._need("&lt;Inciso adicionado por el art" in box or "<Inciso adicionado por el art" in E.plain(box), "Ley 640 art. 43 box")
    t = _timeline(act, "art-0043")
    B23._need([(d, l) for d, _, l in t] == [(None, None), ("2002-01-05", ["ley-640-2001"]),
                                            ("2010-07-12", ["ley-1395-2010"]), ("2014-01-01", ["ley-1564-2012"])]
              and t[1][1] == E.MISSING_LINE, f"Ley 640 art. 43 {[(d, l) for d, _, l in t]}")
    lines = t[2][1].split("\n")
    B23._need(len(lines) == 5 and lines[3].startswith("En materia de lo contencioso administrativo")
              and lines[4].startswith("PARÁGRAFO. Si el apelante"), f"Ley 640 art. 43 text {len(lines)}")
    t[1] = ("2002-01-05", "\n".join(lines[:3]), ["ley-640-2001"])
    _set(act, "art-0043", "Art. 43", t)
    B23._forget(L640, "art-0043")
    _done(fix_640_43)


def note_640_131(act):
    """Ley 640 de 2001 was first published in Diario Oficial No. 44.282 of 5 January 2001 (its law record gives that
    day). Decreto 131 de 2001 (Diario Oficial No. 44.303 of 24 January 2001) corrected art. 47 (its art. 1) and art. 37
    (art. 2) and ordered the act republished (art. 3); the Consejo de Estado declared its art. 1 NULO on 22 November 2002
    (Sección Primera, Radicación 6871: the decree's own basedoc page). By then art. 47 was already out (Sentencia
    C-500-01 of 15 May 2001 struck it as first published), so the annulment changes no version; art. 37 arrives on
    5 January 2002 with the corrected words. Art. 50's one year is counted from the first publication."""
    u = B23._unit("decreto_0131_2001", "1")
    jv = " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))
    B23._need("Artículo declarado NULO por el Consejo de Estado mediante Sentencia del 22 de noviembre de 2002" in jv,
              "Decreto 131 de 2001 art. 1 annulment")
    B23._need(E.LAWS["ley-640-2001"]["published"] == "2001-01-24", "Ley 640 record")
    E.LAWS["ley-640-2001"]["published"] = D.FIRST_640
    _done(note_640_131)


def fix_640(act):
    note_640_131(act)
    D.late_640(act)
    fix_640_35(act)
    fix_640_43(act)


def install(driver):
    global D, B23, B29, B13, E, P, struck
    D = driver
    B23, B29, B13, E, P, struck = D.B23, D.B29, D.B13, D.E, D.P, D.struck
    B29.HAND_FIXES.update({"conciliacion-2001": fix_640})
