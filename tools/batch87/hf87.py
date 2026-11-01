"""Hand-set histories for batch 87 (Leyes 549 de 1999, 974 de 2005), installed by hand_fixes.install();
each checks the page first."""
from __future__ import annotations

import re

import hand_fixes as H  # noqa: F401

L974, T974 = "ley_0974_2005", "Régimen de bancadas (Ley 974 de 2005)"
START = "2006-07-19"
ORIG = "Texto original de la Ley 974 de 2005:"


def _u(name):
    return next(u for u in H.P.doc_units(L974)[1:] if u["name"] == name)


def _orig(u):
    for b in H.B23._boxes(u, "Legislación Anterior"):
        for blk in H.E.la_blocks(b):
            if blk["head"] == ORIG:
                return [t for t in (H.E.tidy(H.E.to_text(p, True)) for p in blk["paras"]) if t]
    H.B23._need(False, f"L974 art. {u['name']}: no '{ORIG}' box")


def _pre_start_done(key):
    pre = H.B29.B4.PRE_START
    pre[:] = [x for x in pre if not x.startswith(f"{L974} {key}:")]
    H.B23._forget(L974, key)


def fix_974_5(act):
    """art. 5: Sentencia C-859 de 2006 (19 October 2006) struck the words of inciso 2 after 'asuntos de conciencia,' ('o de
    aquellos en los que, por razones de conveniencia política, ... decidan no adoptar una decisión única'); Sentencia
    C-036 de 2007 (31 January 2007) struck inciso 3 ('Cuando exista empate ...'). The Jurisprudencia Vigencia box of each
    inciso names its ruling, so the article has a version for each; the engine had put both strikes on 31 January 2007.
    The comma before the struck words and the full stop after them stay, as the page prints them (Sentencia C-897 de 2006,
    'estarse a lo resuelto en la Sentencia C-859-06', changes no words)."""
    B23 = H.B23
    u = _u("5")
    jv = H._jv(u)
    B23._need("Aparte tachado declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-859-06 de 19 de octubre "
              "de 2006" in jv and "Inciso 3o. declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-036-07 "
              "de 31 de enero de 2007" in jv, "L974 art. 5 JV")
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    B23._need(len(ps) == 3 and all(re.search(r"<S>", p) for p in ps[1:]), "L974 art. 5 paragraphs")
    key = "art-0005"
    h = H._hist(act, key)
    B23._need([(d, c) for d, _, c in h] == [(START, None), ("2007-01-31", ["c-036-07"])], f"L974 art. 5 {H._shape(h)}")
    full, cut = h[0][1], h[1][1]
    B23._need(full == H._printed(u, True) and [x for x in cut if x != "."] == H._printed(u, False), "L974 art. 5 texts")
    mid = cut[:2] + full[2:]
    B23._need(mid[1] == "La bancada puede adoptar esta decisión cuando se trate de asuntos de conciencia,." and
              mid[2].startswith("Cuando exista empate") and cut[2:] == ["."], f"L974 art. 5 lines {mid[1:]} {cut[2:]}")
    H.E.add_court("C-859-06", "2006-10-19", "c-859_2006.html")
    H._set(act, key, H._label(act, key), [(None, full, None), ("2006-10-19", mid, "c-859-06"), ("2007-01-31", cut, "c-036-07")])
    B23._forget(L974, key)
    H._done(T974, fix_974_5)


def fix_974_4_20(act):
    """art. 4 and art. 20 transitorio. Art. 4's last inciso ('No incurrirá en doble militancia ...', the earlier-text box)
    was struck by Sentencia C-342 de 2006 (3 May 2006), after the act's promulgation and before its start on 19 July
    2006: by the record's rule for such rulings (Leyes 600 de 2000, 472 de 1998), the version of 19 July 2006 is the act
    as enacted, and a second version on the same day takes the inciso out, credited to the ruling. Art. 20 transitorio
    (the one-time leave for the Representantes a la Cámara of 2002-2006 to change party, 'La presente disposición tendrá
    vigencia hasta el 16 de diciembre de 2005') is excepted from that start by art. 21 ('Se exceptúa el artículo
    transitorio'), which gives it no day of its own: it takes the default rule (Ley 4 de 1913, art. 52: two months after
    promulgation in Diario Oficial No. 45.980 of 25 July 2005), so the act's first version, of 25 September 2005, holds
    only that article (with the heading of Capítulo III); its own term ends with 16 December 2005, and from 17 December
    2005 to 18 July 2006 no provision of the act is in force (an empty version, credited to the act's own term). The
    article's words are the earlier-text box's. Sentencia C-453 de 2006 (7 June 2006), which struck the article after
    its term had run out, and Sentencia C-477 de 2006 ('estarse a lo resuelto'), change no words in this record."""
    B23, E = H.B23, H.E
    u4, u20, u21 = _u("4"), _u("20"), _u("21")
    jv4 = H._jv(u4)
    B23._need("Inciso declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-342-06 de 3 de mayo de 2006" in jv4,
              "L974 art. 4 JV")
    old4 = _orig(u4)
    B23._need(len(old4) == 1 and old4[0].startswith("No incurrirá en doble militancia, ni podrá ser sancionado"), f"L974 art. 4 box {old4}")
    jv20 = H._jv(u20)
    B23._need("Artículo declarado INEXEQUIBLE, por los cargos analizados, por la Corte Constitucional mediante Sentencia "
              "C-453-06 de 7 de junio de 2006" in jv20, "L974 art. 20 JV")
    old20 = _orig(u20)
    B23._need(len(old20) == 4 and old20[0].startswith("ARTÍCULO 20 TRANSITORIO. Para todos los efectos legales")
              and old20[-1] == "La presente disposición tendrá vigencia hasta el 16 de diciembre de 2005.", f"L974 art. 20 box {old20}")
    old20 = [re.sub(r"^ARTÍCULO 20 TRANSITORIO\.\s*", "", old20[0])] + old20[1:]
    p21 = " ".join(E.plain(it[1]) for it in u21["items"] if it[0] == "p")
    B23._need("La presente ley rige a partir del 19 de julio del año 2006 y deroga las normas que le sean contrarias. Se "
              "exceptúa el artículo transitorio." in p21, "L974 art. 21")
    head = " ".join(E.plain(it[1]) for it in H.P.doc_units(L974)[0]["items"] if it[0] == "p")
    B23._need("Diario Oficial No. 45.980 de 25 de julio de 2005" in head, "L974 Diario Oficial")
    vs = act["versions"]
    v0 = vs[0]
    B23._need(v0["from"] == START and "art-0020t" not in v0["units"] and v0["units"]["titulos"]["text"].endswith(
        "### CAPITULO III. DISPOSICIONES FINALES.\n"), "L974 first version")
    t4 = v0["units"]["art-0004"]
    B23._need(not any(k == "art-0004" for v in vs[1:] for k in v["credits"]), "L974 art. 4 later changes")
    enacted = dict(v0["units"])
    enacted["art-0004"] = dict(t4, text=t4["text"] + old4[0] + "\n")
    key20, lab20 = E.unit_key(E.label_num(u20["label"]))
    B23._need(key20 == "art-0020t", f"L974 art. 20 key {key20}")
    first = {"from": "2005-09-25", "credits": {}, "source_url": v0["source_url"], "sha256": v0["sha256"],
             "units": {key20: {"label": lab20, "kind": "art", "text": f"# {lab20}\n" + "\n".join(old20) + "\n"},
                       "titulos": dict(v0["units"]["titulos"], text="### CAPITULO III. DISPOSICIONES FINALES.\n")},
             "note": ("Art. 20 transitorio of Ley 974 de 2005 (sanctioned 2005-07-22, Diario Oficial No. 45.980 of "
                      "2005-07-25), in force from 2005-09-25: art. 21 ('La presente ley rige a partir del 19 de julio del "
                      "año 2006 ... Se exceptúa el artículo transitorio') excepts it from the act's start and gives it no "
                      "day, so the default rule applies (Ley 4 de 1913, art. 52: two months after promulgation).")}
    lapse = {"from": "2005-12-17", "units": {}, "credits": {key20: ["ley-974-2005"], "titulos": ["ley-974-2005"]},
             "source_url": v0["source_url"], "sha256": v0["sha256"],
             "note": "Art. 20 transitorio's own term ran out: 'La presente disposición tendrá vigencia hasta el 16 de "
                     "diciembre de 2005.' No other provision of the act is in force until 19 July 2006 (art. 21)."}
    start = dict(v0, units=enacted, credits={k: ["ley-974-2005"] for k in enacted})
    struck = {"from": START, "units": dict(v0["units"]), "credits": {"art-0004": ["c-342-06"]}, "same_day": True,
              "source_url": v0["source_url"], "sha256": v0["sha256"],
              "note": "Words the Constitutional Court struck after the act's promulgation and before it took effect "
                      "(ruling of 2006-05-03) are out of the text from its first day."}
    H.E.add_court("C-342-06", "2006-05-03", "c-342_2006.html")
    act["versions"] = [first, lapse, start, struck] + vs[1:]
    for k in ("art-0004", "art-0020t"):
        _pre_start_done(k)
    import parse_batch3 as B3
    ds = B3.DECISIONS
    i = [i for i, x in enumerate(ds) if x.startswith(f"{T974}: first version from {START}: ")]
    B23._need(len(i) == 1, "L974 first-version decision")
    ds[i[0]] = ds[i[0]].replace(f"first version from {START}: ", "first version from 2005-09-25 (art. 20 transitorio only, "
                                "by the default rule; see the hand-set history below); the rest of the act from "
                                f"{START}: ", 1)
    H._done(T974, fix_974_4_20)


L549, T549 = "ley_0549_1999", "Financiación del pasivo pensional de las entidades territoriales (Ley 549 de 1999)"


def fix_549_2(act):
    """art. 2: Sentencia C-1187 de 2000 declined to rule on numerals 1, 2 and 3, holding them repealed by Decreto 955 de
    2000 (the Plan Nacional de Desarrollo decree); Sentencia C-1403 de 2000 (19 October 2000) struck that decree as a
    whole from its promulgation, and the page names no act that changed the numerals' words before Ley 2468 de 2025: the
    article reads as enacted until then. Neither ruling changes words of this act."""
    B23 = H.B23
    jv = H._jv(next(u for u in H.P.doc_units(L549)[1:] if u["name"] == "2"))
    B23._need("se declaró inhibida de fallar sobre los numeral 1, 2, y 3 por considerar que esta norma fue derogada por el "
              "Decreto 955 de 2000" in jv.replace("de declaró", "se declaró") and "Sentencia C-1403-00 del 19 de octubre de "
              "2000" in jv, "L549 art. 2 JV")
    h = H._hist(act, "art-0002")
    B23._need([(d, c) for d, _, c in h] == [("1999-12-30", None), ("2025-07-02", ["ley-2468-2025"])], f"L549 art. 2 {H._shape(h)}")
    H._done(T549, fix_549_2)


H.FIXES["regimen-de-bancadas-2005"] = [fix_974_5, fix_974_4_20]
H.FIXES["pasivo-pensional-territorial-1999"] = [fix_549_2]
