"""Hand-set histories for batch 94 (Leyes 344 de 1996 y 443 de 1998), installed by hand_fixes.install(); each checks
the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L344, T344, S344 = "ley_0344_1996", "Racionalización del gasto público (Ley 344 de 1996)", "racionalizacion-del-gasto-publico-1996"
L443, T443, S443 = "ley_0443_1998", "Carrera administrativa (Ley 443 de 1998)", "carrera-administrativa-1998"
PH = "[La fuente no da el texto vigente en esta fecha.]"


def gone_evidence(page, key):
    """For the verifier (which does not run the fixes): page evidence, as (where, words), that an article of this part
    is out today though the page prints its words ('p0' first paragraph, 'nv' Notas de Vigencia). None: no such rule."""
    return None


def _need(c, what):
    H.B23._need(c, what)


def _units_on(act, days):
    """hf89 rule: a version on one of `days` that carries no units gets a copy of the units before it."""
    full = None
    for v in act["versions"]:
        if "units" in v:
            full = v["units"]
        elif v["from"] in days:
            v["units"] = dict(full)
            full = v["units"]


def _apply(act, page, key, tl, extra_credits=None):
    _units_on(act, {d for d, _, _ in tl[1:]})
    H._set(act, key, H._label(act, key), tl)
    for day, laws in (extra_credits or {}).items():
        v = next(v for v in act["versions"] if v["from"] == day)
        v["credits"][key] = sorted(laws)
    H.B23._forget(page, key)


def _court(cid, day, href):
    k = H.E.add_court(cid, day, href)
    _need(H.E.LAWS[k]["enacted"] == day, f"{cid} day {H.E.LAWS[k]['enacted']}")
    return k


# ------------------------------------------------------------------------------------------------ Ley 344 de 1996

def fix_344_3(act):
    """art. 3 (Fondo Nacional de Regalías, rewriting Ley 141 de 1994 art. 1 parágrafo 2): Decreto 799 de 1997 (Diario
    Oficial No. 43.008 of 21 March 1997) corrected the article 'en el sentido de que el texto del artículo se encuentra
    precedido con la siguiente previsión legal: Artículo 3º. El parágrafo 2º del artículo 1º de la Ley 141 de 1994
    quedará así: Parágrafo 2º.' (Notas de Vigencia), and the page's box gives the text 'con la corrección introducida
    por el Decreto 799 de 1997'. As for Decreto 207 de 2022's corrections (99zh-batch42): the words as first published
    (the box's words without the words the correction put in front, which the note quotes) from the act's first day, the
    corrected words from 21 March 1997, credited to the decree. Sentencia C-497-98 (15 September 1998) struck the article
    ('sólo tendrá efectos hacia el futuro, a partir de la notificación del presente fallo'): out on the ruling's day.
    Decreto 955 de 2000 art. 59 (26 May 2000), which the notes name as modifying the article and which Sentencia
    C-1403-00 struck as a whole, gives no text and came after the article had left: no version. The engine had the
    placeholder until 1997, the corrected words until 2000, and the placeholder to October 2000."""
    u = H.B23._unit(L344, "3")
    nv, jv = H._nv(u), H._jv(u)
    _need("Artículo corregido por el artículo 1o. del Decreto 799 de 1997 publicado en el Diario Oficial No. 43.008 de 21 de "
          "marzo de 1997, en el sentido de que el texto del artículo se encuentra precedido con la siguiente previsión "
          "legal:'Artículo 3º. El parágrafo 2º del artículo 1º de la Ley 141 de 1994 quedará así:Parágrafo 2º.'" in nv,
          "L344 art. 3 NV")
    _need("Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-497-98 de 15 de septiembre de "
          "1998" in jv, "L344 art. 3 JV")
    h = H._hist(act, "art-0003")
    _need([(d, c) for d, _, c in h] == [("1996-12-31", None), ("1997-03-21", ["dec-799-1997"]),
                                        ("2000-05-26", ["dec-955-2000"]), ("2000-10-19", ["c-1403-00"])]
          and h[0][1] == [PH] and h[2][1] == [PH] and h[3][1] is None, f"L344 art. 3 {H._shape(h)}")
    cor = h[1][1]
    pre, par = "El parágrafo 2º del artículo 1º de la Ley 141 de 1994 quedará así:", "Parágrafo 2º. "
    _need(cor[0] == pre and cor[1].startswith(par + "El total de los recursos propios del Fondo Nacional de Regalías"),
          f"L344 art. 3 corrected text {cor[:2]}")
    orig = [cor[1][len(par):]] + cor[2:]
    k497 = _court("C-497-98", "1998-09-15", "c-497_1998.html")
    _apply(act, L344, "art-0003", [(None, orig, None), ("1997-03-21", cor, "dec-799-1997"), ("1998-09-15", None, k497)])
    H._done(T344, fix_344_3)


def fix_344_34(act):
    """art. 34 (rewriting Ley 100 de 1993 art. 221 literal c numeral 2): repealed by Ley 508 de 1999 art. 160 (30 July
    1999), which Sentencia C-557-00 (16 May 2000) struck as a whole, so the article stands again from that day (as Ley 99
    de 1993 art. 43 in 98-batch7); repealed again by Decreto 955 de 2000 art. 105 (26 May 2000). Sentencia C-1165-00 (6
    September 2000) then struck the article itself, so Sentencia C-1403-00 (19 October 2000), which struck Decreto 955 de
    2000, does not bring it back. The engine had it out from 1999 with no return."""
    u = H.B23._unit(L344, "34")
    nv, jv = H._nv(u), H._jv(u)
    _need("Artículo derogado por el artículo 105 del Decreto 955 de 2000" in nv and "Artículo derogado por el artículo 160 de "
          "la Ley 508 de 1999, publicada en el Diario Oficial No. 43.651, del 30 de julio de 1999" in nv, "L344 art. 34 NV")
    _need("Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1165-00 del 6 de septiembre de "
          "2000" in jv and "La Ley 508 de 1999 fue declarada INEXEQUIBLE por la Corte Constitucional, mediante Sentencia "
          "C-557-2000 del 16 de mayo de 2000" in jv, "L344 art. 34 JV")
    h = H._hist(act, "art-0034")
    _need([(d, c) for d, _, c in h] == [("1996-12-31", None), ("1999-07-30", ["ley-508-1999"])] and h[1][1] is None
          and len(h[0][1]) == 3, f"L344 art. 34 {H._shape(h)}")
    k557 = _court("C-557-00", "2000-05-16", "c-557_2000.html")
    _need(H.E.law_day("dec-955-2000") == "2000-05-26", "Decreto 955 de 2000 day")
    _apply(act, L344, "art-0034", [(None, h[0][1], None), ("1999-07-30", None, "ley-508-1999"),
                                   ("2000-05-16", h[0][1], k557), ("2000-05-26", None, "dec-955-2000")])
    H._done(T344, fix_344_34)


# ------------------------------------------------------------------------------------------------ Ley 443 de 1998

def fix_443_5(act):
    """art. 5 (empleos de libre nombramiento y remoción): four rulings struck words on four days, as the Jurisprudencia
    Vigencia boxes say: Sentencia C-368-99 (26 May 1999) 'Juez de Instrucción Penal Militar, Auditor de Guerra,
    Secretario de Tribunal Superior Militar', 'Inspector de Tránsito y Transporte o el que haga sus veces' (Sentencia
    C-372-99's decision: 'ESTESE A LO RESUELTO en la Sentencia C-368 ... en cuanto a la expresión Inspector de Tránsito
    o el que haga sus veces') and the second paragraph of literal b) (the box gives its words); Sentencia C-506-99 (14
    July 1999) 'Rector, Vicerrector y Decano de Institución de Educación Superior distinta a los entes universitarios
    autónomos' (twice); Sentencias C-1177-01 and C-1178-01 (both 8 November 2001) 'Contralor y Personero'; Sentencia
    C-161-03 (25 February 2003) parágrafo 1o. (the box gives its words). Each change on its ruling's day; the engine had
    put all of them on 25 February 2003."""
    u = H.B23._unit(L443, "5")
    jv = H._jv(u)
    for w in ("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-368-99 de 26 de mayo de 1999",
              "Párrafo 2o. declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-368-99 de 26 de mayo de 1999",
              "Expresiones tachadas declaradas INEXEQUIBLES por la Corte Constitucional mediante Sentencia C-368-99 de 26 de mayo "
              "de 1999",
              "Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencias C-506-99 de 14 de julio de 1999",
              "Sentencia C-1178-01 de 8 de noviembre de 2001", "Sentencia C-1177-01 de 8 de noviembre de 2001",
              "Parágrafo 1o. declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-161-03 de 25 de febrero de 2003"):
        _need(w in jv, f"L443 art. 5 JV: {w[:60]}")
    h = H._hist(act, "art-0005")
    _need([(d, c) for d, _, c in h] == [("1998-06-12", None), ("2003-02-25", ["c-161-03"])]
          and len(h[0][1]) == 30 and len(h[1][1]) == 29, f"L443 art. 5 {H._shape(h)}")
    full, last = h[0][1], h[1][1]
    gone = [i for i, x in enumerate(full) if x.startswith("En el Departamento Administrativo de la Presidencia de la República")]
    _need(len(gone) == 1, "L443 art. 5 inciso 2")
    rest = [x for i, x in enumerate(full) if i != gone[0]]
    stage = {}
    keys = [("Juez de Instrucción Penal Militar, Auditor de Guerra, Secretario de Tribunal Superior Militar", "1999-05-26"),
            ("Inspector de Tránsito y Transporte o el que haga sus veces", "1999-05-26"),
            ("Rector, Vicerrector y Decano de Institución de Educación Superior distinta a los entes universitarios autónomos",
             "1999-07-14"),
            ("Contralor y Personero.", "2001-11-08"), ("PARÁGRAFO 1o. También se consideran", "2003-02-25")]
    for i, (a, b) in enumerate(zip(rest, last)):
        if a != b:
            hit = [d for w, d in keys if w in a]
            _need(len(hit) == 1, f"L443 art. 5 line {i}: {a[:80]}")
            stage[i] = hit[0]
    _need(sorted(stage.values()) == ["1999-05-26", "1999-05-26", "1999-07-14", "1999-07-14", "2001-11-08", "2003-02-25"],
          f"L443 art. 5 stages {stage}")

    def at(day):
        return [b if i in stage and stage[i] <= day else a for i, (a, b) in enumerate(zip(rest, last))]
    k368 = _court("C-368-99", "1999-05-26", "c-368_1999.html")
    k1177 = _court("C-1177-01", "2001-11-08", "c-1177_2001.html")
    k1178 = _court("C-1178-01", "2001-11-08", "c-1178_2001.html")
    tl = [(None, full, None), ("1999-05-26", at("1999-05-26"), k368), ("1999-07-14", at("1999-07-14"), "c-506-99"),
          ("2001-11-08", at("2001-11-08"), k1178), ("2003-02-25", at("2003-02-25"), "c-161-03")]
    _need(tl[-1][1] == last, "L443 art. 5 last")
    _apply(act, L443, "art-0005", tl, {"2001-11-08": [k1177, k1178]})
    H._done(T443, fix_443_5)


def _decrees_struck(u, n):
    nv, jv = H._nv(u), H._jv(u)
    _need("Decreto 266 de 2000, publicado en el Diario Oficial No. 43.906 del 22 de febrero de 2000. Declarado INEXEQUIBLE"
          in nv and "Decreto 1122 de 1999, publicado en el Diario Oficial No. 43.622 del 29 de junio de 1999. Declarado "
          "INEXEQUIBLE" in nv, f"L443 art. {n} NV")
    _need("El Decreto 266 fue 1999 fue declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1316-00 del 26 "
          "de septiembre de 2000" in jv and re.search(r"El Decreto 1122 de 1999 fue declarado INEXEQUIBLE por la Corte "
                                                      r"Constitucional mediante Sentencia C-923-99 del? 18 de noviembre de 1999", jv),
          f"L443 art. {n} JV")
    k266 = H.E.register("dec-266-2000")
    _need(H.E.law_day(k266) == "2000-02-22", "Decreto 266 de 2000 day")
    return k266, _court("C-923-99", "1999-11-18", "c-923_1999.html"), _court("C-1316-00", "2000-09-26", "c-1316_2000.html")


def fix_443_22(act):
    """art. 22 (lista de elegibles): its parágrafo was replaced by Decreto 1122 de 1999 art. 128 (29 June 1999; the box
    gives the decree's words) and changed again by Decreto 266 de 2000 art. 69 (22 February 2000; no text on the page);
    Sentencias C-923-99 (18 November 1999) and C-1316-00 (26 September 2000) struck each decree as a whole (the box writes
    'El Decreto 266 fue 1999': read as Decreto 266 de 2000, 99zl-batch46). As for Ley 60 de 1993 art. 18 (99zzzzzzzz-093)
    and the Código de Régimen Municipal's art. 25 (99h-batch16): the act's words, the decree's parágrafo from 29 June 1999,
    the act's words again from 18 November 1999, the placeholder from 22 February 2000 (no text given), the act's words
    again from 26 September 2000. The engine had no change in 2000."""
    u = H.B23._unit(L443, "22")
    k266, k923, k1316 = _decrees_struck(u, "22")
    h = H._hist(act, "art-0022")
    _need([(d, c) for d, _, c in h] == [("1998-06-12", None), ("1999-06-29", ["dec-1122-1999"]), ("1999-11-18", ["c-923-99"])]
          and h[2][1] == h[0][1] and h[1][1][:2] == h[0][1][:2] and h[1][1][2] != h[0][1][2], f"L443 art. 22 {H._shape(h)}")
    _apply(act, L443, "art-0022", [(None, h[0][1], None), ("1999-06-29", h[1][1], "dec-1122-1999"),
                                   ("1999-11-18", h[0][1], k923), ("2000-02-22", [PH], k266), ("2000-09-26", h[0][1], k1316)])
    H._done(T443, fix_443_22)


def fix_443_24(act):
    """art. 24 (concursos generales abiertos; kept by Ley 909 de 2004 art. 58): Sentencia C-372-99 (26 May 1999) struck
    'El Gobierno Nacional reglamentará la materia, teniendo en cuenta la posibilidad de organizar cuadros profesionales y
    grupos ocupacionales' (inciso 1) and 'que realicen las entidades' (the last inciso), as the ruling's decision and the
    boxes say (the engine had put these strikes on 26 September 2000, credited to Sentencia C-1316-00); inciso 3 was
    replaced by Decreto 1122 de 1999 art. 129 (29 June 1999; the box gives its words) and changed again by Decreto 266 de
    2000 art. 70 (22 February 2000; no text on the page), each decree struck as a whole (Sentencias C-923-99 of 18
    November 1999 and C-1316-00 of 26 September 2000): the Ley 60 de 1993 art. 18 rule, as for art. 22."""
    u = H.B23._unit(L443, "24")
    _need(H._jv(u).count("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-372-99 de 26 de "
                         "mayo de 1999") == 2, "L443 art. 24 JV C-372-99")
    k266, k923, k1316 = _decrees_struck(u, "24")
    h = H._hist(act, "art-0024")
    _need([(d, c) for d, _, c in h] == [("1998-06-12", None), ("1999-06-29", ["dec-1122-1999"]), ("1999-11-18", ["c-923-99"]),
                                        ("2000-09-26", ["c-1316-00"])] and h[2][1] == h[0][1], f"L443 art. 24 {H._shape(h)}")
    full, dec, cut = h[0][1], h[1][1], h[3][1]
    _need(len(full) == len(dec) == len(cut) == 4 and [i for i in range(4) if full[i] != dec[i]] == [2]
          and [i for i in range(4) if full[i] != cut[i]] == [0, 3], "L443 art. 24 lines")
    cutdec = cut[:2] + [dec[2]] + cut[3:]
    k372 = _court("C-372-99", "1999-05-26", "c-372_1999.html")
    _apply(act, L443, "art-0024", [(None, full, None), ("1999-05-26", cut, k372), ("1999-06-29", cutdec, "dec-1122-1999"),
                                   ("1999-11-18", cut, k923), ("2000-02-22", [PH], k266), ("2000-09-26", cut, k1316)])
    H._done(T443, fix_443_24)


def fix_443_39(act):
    """art. 39 parágrafo 2o.: two struck passages, two rulings, as the Jurisprudencia Vigencia box says: 'y tendrá los
    mismos efectos jurídicos de una conciliación' (struck and in italics: Sentencia C-642-99, 1 September 1999) and 'Los
    términos de caducidad establecidos en el Código Contencioso Administrativo ... que originó la supresión del empleo'
    (Sentencia C-1341-00, 4 October 2000). The engine had both on the later day."""
    E = H.E
    u = H.B23._unit(L443, "39")
    jv = H._jv(u)
    _need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1341-00 de 4 de octubre de 2000"
          in jv and "Aparte tachado y en cursiva declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-642-99 de "
          "1 de septiembre de 1999" in jv, "L443 art. 39 JV")
    ps = [it[1] for it in u["items"] if it[0] == "p" and "<S>" in it[1]]
    _need(len(ps) == 1, "L443 art. 39 struck paragraph")
    spans = re.findall(r"<S>.*?</S>", ps[0], re.S)
    _need(len(spans) == 2 and 'class="i_aj"' in spans[0] and "i_aj" not in spans[1], "L443 art. 39 spans")
    h = H._hist(act, "art-0039")
    _need([(d, c) for d, _, c in h] == [("1998-06-12", None), ("2000-10-04", ["c-1341-00"])], f"L443 art. 39 {H._shape(h)}")
    full, last = h[0][1], h[1][1]
    d = [i for i in range(len(full)) if full[i] != last[i]]
    _need(len(full) == len(last) and len(d) == 1, "L443 art. 39 lines")
    # the line as the engine reads it, with neither span (check), then with the C-1341-00 span kept (mid)
    both = E.tidy(E.to_text(ps[0], False))
    mid = E.tidy(E.to_text(ps[0].replace(spans[1], spans[1][3:-4]), False))
    _need(both == last[d[0]] and mid != both and "mismos efectos jurídicos" not in mid
          and "Los términos de caducidad" in mid and full[d[0]] != mid, f"L443 art. 39 mid {mid[:160]} | {both[:160]}")
    mids = list(full)
    mids[d[0]] = mid
    k642 = _court("C-642-99", "1999-09-01", "c-642_1999.html")
    _apply(act, L443, "art-0039", [(None, full, None), ("1999-09-01", mids, k642), ("2000-10-04", last, "c-1341-00")])
    H._done(T443, fix_443_39)


def fix_443_41(act):
    """art. 41 (reformas de plantas de personal): Sentencia C-372-99 (26 May 1999) struck the parágrafo (the ruling: 'Es
    INEXEQUIBLE el parágrafo del artículo 41'; the box gives its words; the label stays as the page prints it), Sentencia
    C-994-00 (2 August 2000) the words 'corporaciones autónomas regionales' of inciso 2. The engine had both on the later
    day."""
    u = H.B23._unit(L443, "41")
    jv = H._jv(u)
    _need("Parágrafo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-372-99 de 26 de mayo de 1999" in jv
          and "Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-994-00 de 2 de agosto de 2000"
          in jv, "L443 art. 41 JV")
    h = H._hist(act, "art-0041")
    _need([(d, c) for d, _, c in h] == [("1998-06-12", None), ("2000-08-02", ["c-994-00"])], f"L443 art. 41 {H._shape(h)}")
    full, last = h[0][1], h[1][1]
    _need(len(full) == len(last) == 3 and full[0] == last[0] and full[2].startswith("PARAGRAFO: En el orden territorial")
          and last[2] == "PARAGRAFO..", "L443 art. 41 lines")
    k372 = _court("C-372-99", "1999-05-26", "c-372_1999.html")
    _apply(act, L443, "art-0041", [(None, full, None), ("1999-05-26", full[:2] + [last[2]], k372),
                                   ("2000-08-02", last, "c-994-00")])
    H._done(T443, fix_443_41)


H.FIXES[S344] = [fix_344_3, fix_344_34]
H.FIXES[S443] = [fix_443_5, fix_443_22, fix_443_24, fix_443_39, fix_443_41]
