"""Hand-set histories for batch 51, the Planes Nacionales de Desarrollo Ley 1450 de 2011 and Ley 1753 de 2015 (bound by
parse_batch51.py through install(); each checks the page and the engine's history first)."""
from __future__ import annotations

import re

D = B23 = B29 = B13 = E = P = None
L1450, L1753 = "ley_1450_2011", "ley_1753_2015"
T1450 = "Plan Nacional de Desarrollo 2010-2014 (Ley 1450 de 2011)"
T1753 = "Plan Nacional de Desarrollo 2014-2018 (Ley 1753 de 2015)"
FIXES: dict = {}
PH = "[La fuente no da el texto vigente en esta fecha.]"


def _done(title, fn):
    B29.HAND_DONE.append(f"{title}: " + " ".join(fn.__doc__.split()))


def _hist(act, key):
    """[(day, body lines or None, credits)] for each change of the unit (body: the text without its '# Art.' line)."""
    out, last = [], object()
    for v in act["versions"]:
        if "units" in v:
            t = (v["units"].get(key) or {}).get("text")
            if t != last:
                out.append((v["from"], None if t is None else t.split("\n")[1:-1], v["credits"].get(key)))
                last = t
    return out


def _shape(h):
    return [(d, c, None if b is None else ("PH" if b == [PH] else len(b))) for d, b, c in h]


def _set(act, key, label, timeline):
    """timeline [(day or None, body lines or None, law)]."""
    B13.B6.set_history(act, key, label, [(d, None if b is None else "\n".join(b), l) for d, b, l in timeline])


def _label(act, key):
    for v in act["versions"]:
        u = (v.get("units") or {}).get(key)
        if u:
            return u["label"]
    raise SystemExit(f"{act['slug']} {key}: no label")


def _nv(u):
    return " ".join(E.plain(b) for b in B23._boxes(u, "Notas de Vigencia"))


def _jv(u):
    return " ".join(E.plain(b) for b in B23._boxes(u, "Jurisprudencia Vigencia"))


def _printed(u, keep_struck=False):
    """The article's printed words (markers out), its epigraph in front, as the engine writes a unit's lines."""
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    lines = [t for t in (E.tidy(E.to_text(x, keep_struck)) for x in ps) if re.search(r"\w", t)]
    epi = E.tidy(E.ART_HEAD.sub("", u["label"], count=1))
    return ([f"{epi} {lines[0]}"] if epi else [lines[0]]) + lines[1:]


# ---------------------------------------------------------------- Ley 1450 de 2011

def fix_1450_44(act):
    """Ley 1450 de 2011, art. 44 (rewrote Ley 590 de 2000 art. 17): repealed by Ley 2294 de 2023 art. 372 (19 May 2023);
    the page prints its words under that marker. Its notes also say 'Artículo modificado por el artículo 13 de la Ley
    1753 de 2015 ... en cuanto establece' and quote that article, which merged the fund it governs into another; Ley
    1753 changed no words of this article, so the printed words stand from the act's first day to the repeal (the engine
    had put the placeholder there)."""
    u = B23._unit(L1450, "44")
    B23._need("Artículo modificado por el artículo 13 de la Ley 1753 de 2015" in _nv(u) and "en cuanto establece" in _nv(u)
              and not B23._boxes(u, "Legislación Anterior"), "Ley 1450 art. 44 notes")
    h = _hist(act, "art-0044")
    B23._need(_shape(h) == [("2011-06-16", None, "PH"), ("2023-05-19", ["ley-2294-2023"], 3)]
              and any(v["from"] == "2015-06-09" and v["credits"].get("art-0044") == ["ley-1753-2015"] for v in act["versions"]),
              f"Ley 1450 art. 44 {_shape(h)}")
    printed = _printed(u)
    B23._need(printed == h[-1][1], "Ley 1450 art. 44 printed words")
    _set(act, "art-0044", "Art. 44", [(None, printed, None), ("2023-05-19", None, "ley-2294-2023")])
    B23._forget(L1450, "art-0044")
    _done(T1450, fix_1450_44)


def fix_1450_46(act):
    """Ley 1450 de 2011, art. 46: its original text (earlier-text box) carries '<Ver Notas de Vigencia sobre
    modificación tácita por la Ley 1753 de 2015>'; a tacit change names no words, so the original text stands until Ley
    2294 de 2023 art. 372 repealed the article (19 May 2023) (the engine had put the placeholder from 2015)."""
    u = B23._unit(L1450, "46")
    la = " ".join(E.plain(b) for b in B23._boxes(u, "Legislación Anterior"))
    B23._need("<Ver Notas de Vigencia sobre modificación tácita por la Ley 1753 de 2015>" in la, "Ley 1450 art. 46 box")
    h = _hist(act, "art-0046")
    B23._need(_shape(h)[1:] == [("2015-06-09", ["ley-1753-2015"], "PH"), ("2023-05-19", ["ley-2294-2023"], None)],
              f"Ley 1450 art. 46 {_shape(h)}")
    _set(act, "art-0046", "Art. 46", [(None, h[0][1], None), ("2023-05-19", None, "ley-2294-2023")])
    B23._forget(L1450, "art-0046")
    _done(T1450, fix_1450_46)


def fix_1450_89(act):
    """Ley 1450 de 2011, art. 89: Sentencia C-218-15 (22 April 2015) struck the words 'y/o inversión' of inciso 1 and the
    whole of inciso 2 (the earlier-text box marks them); the parágrafo stays. The rest from the ruling's day; the article
    out from 9 June 2015 (Ley 1753 de 2015 art. 267). The engine had put the placeholder between the two."""
    u = B23._unit(L1450, "89")
    B23._need("salvo el aparte tachado declarado INEXEQUIBLE, y el Inciso 2o. delarado INEXEQUIBLE por la Corte "
              "Constitucional mediante Sentencia C-218-15 de 22 de abril de 2015" in _jv(u), "Ley 1450 art. 89 ruling")
    box = B23._boxes(u, "Legislación Anterior")[0]
    B23._need("su funcionamiento <S><span class='b_aj'>y/o inversi&oacute;n</span></S>.</p><p>&lt;Inciso INEXEQUIBLE&gt;"
              in box, "Ley 1450 art. 89 struck words")
    h = _hist(act, "art-0089")
    B23._need(_shape(h) == [("2011-06-16", None, 3), ("2015-04-22", ["c-218-15"], "PH"), ("2015-06-09", ["ley-1753-2015"], None)],
              f"Ley 1450 art. 89 {_shape(h)}")
    first = h[0][1]
    B23._need(first[0].endswith("su funcionamiento y/o inversión.") and first[1].startswith("Aquellos sujetos")
              and first[2].startswith("PARÁGRAFO."), "Ley 1450 art. 89 lines")
    after = [first[0][: -len(" y/o inversión.")] + "."] + first[2:]
    _set(act, "art-0089", "Art. 89", [(None, first, None), ("2015-04-22", after, "c-218-15"),
                                      ("2015-06-09", None, "ley-1753-2015")])
    B23._forget(L1450, "art-0089")
    _done(T1450, fix_1450_89)


def fix_1450_199(act):
    """Ley 1450 de 2011, art. 199: the page marks it '<Artículo subrogado por el artículo 24 de la Ley 1564 de 2012.
    Sentencia C-156-13>' (the Corte Constitucional held it replaced by that article of the Código General del Proceso,
    which took effect on promulgation, 12 July 2012); it leaves the record that day, credited to Ley 1564 (the engine had
    put the placeholder until Ley 1753 de 2015's repeal)."""
    u = B23._unit(L1450, "199")
    B23._need("Artículo subrogado por el artículo 24 de la Ley 1564 de 2012" in _nv(u) and "C-156-13" in _jv(u),
              "Ley 1450 art. 199 notes")
    h = _hist(act, "art-0199")
    B23._need(_shape(h)[1:] == [("2012-07-12", ["ley-1564-2012"], "PH"), ("2015-06-09", ["ley-1753-2015"], None)],
              f"Ley 1450 art. 199 {_shape(h)}")
    _set(act, "art-0199", "Art. 199", [(None, h[0][1], None), ("2012-07-12", None, "ley-1564-2012")])
    B23._forget(L1450, "art-0199")
    _done(T1450, fix_1450_199)


C206_WORDS = ("Los prestadores del servicio de Internet podrán hacer ofertas según las necesidades de los segmentos de "
              "mercado o de sus usuarios de acuerdo con sus perfiles de uso y consumo, lo cual no se entenderá como "
              "discriminación")


def keep_c206(lines):
    """The numeral 1 line with C-206-25's struck words put back (used by the verifier too)."""
    out, n = [], 0
    for x in lines:
        if x.startswith("1. Sin perjuicio de lo establecido en la Ley 1336 de 2006") and x.endswith("propiedad de estos.."):
            x = x[:-1] + " " + C206_WORDS + "."
            n += 1
        out.append(x)
    B23._need(n == 1, "Ley 1450 art. 56 numeral 1")
    return out


def fix_1450_56(act):
    """Ley 1450 de 2011, art. 56, numeral 1: Sentencia C-206-25 (press release of 14 May 2025) struck its last sentence
    ('Los prestadores del servicio de Internet podrán hacer ofertas ... no se entenderá como discriminación') with
    effect deferred one year from the publication of the ruling's full text on the Court's website, a day the source
    does not give; the words stay in every version until a dated source fixes that day (the engine had dropped them
    from every version)."""
    u = B23._unit(L1450, "56")
    B23._need("declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-206-25 según Comunicado de Prensa de "
              "14 de mayo de 2025" in _jv(u) and "Los efectos de la presente sentencia se difieran por un (1) año a partir de "
              "la fecha de publicación del texto completo" in _jv(u), "Ley 1450 art. 56 ruling")
    raw = next(it[1] for it in u["items"] if it[0] == "p" and "<S>" in it[1])
    B23._need(E.html.unescape(re.sub(r"<[^>]+>", "", raw.split("<S>")[1].split("</S>")[0])) == f"[{C206_WORDS}]",
              "Ley 1450 art. 56 struck words")
    n = 0
    for v in act["versions"]:
        if "units" in v and "art-0056" in v["units"]:
            un = v["units"]["art-0056"]
            ls = un["text"].split("\n")
            v["units"] = dict(v["units"], **{"art-0056": dict(un, text="\n".join([ls[0]] + keep_c206(ls[1:-1]) + [ls[-1]]))})
            n += 1
    B23._need(n > 3, "Ley 1450 art. 56 versions")
    _done(T1450, fix_1450_56)


# ---------------------------------------------------------------- Ley 1753 de 2015

def fix_1753_13(act):
    """Ley 1753 de 2015, art. 13: the earlier-text box gives the article as Ley 2069 de 2020 art. 46 rewrote it with the
    parágrafo Ley 2254 de 2022 art. 16 added ('PARÁGRAFO. INNpulsa Colombia creará una oferta institucional directa para
    el programa de "Escalera de la Formalidad" ...'): from 31 December 2020 the box's text without that parágrafo, from
    15 July 2022 with it (the engine had put the placeholder between the two)."""
    h = _hist(act, "art-0013")
    B23._need(_shape(h)[1:3] == [("2020-12-31", ["ley-2069-2020"], "PH"), ("2022-07-15", ["ley-2254-2022"], len(h[2][1] or []))]
              and h[3][0] == "2023-05-19" and h[3][1] is None, f"Ley 1753 art. 13 {_shape(h)}")
    t22 = h[2][1]
    B23._need(t22[-1].startswith("PARÁGRAFO. INNpulsa Colombia creará una oferta institucional directa para el programa de "
                                 "'Escalera de la Formalidad'"), f"Ley 1753 art. 13 last line {t22[-1][:60]}")
    _set(act, "art-0013", "Art. 13", [(None, h[0][1], None), ("2020-12-31", t22[:-1], "ley-2069-2020"),
                                      ("2022-07-15", t22, "ley-2254-2022"), ("2023-05-19", None, "ley-2294-2023")])
    B23._forget(L1753, "art-0013")
    _done(T1753, fix_1753_13)


C008_DAY = "2019-05-29"


def _fix_c008(act, num):
    u = B23._unit(L1753, num)
    B23._need("Artículo declarado INEXEQUIBLE, difiriendo los efectos de este fallo por el término de un (1) año, contado a "
              "partir de la notificación del mismo, por la Corte Constitucional mediante Sentencia C-008-18 de 7 de marzo de "
              "2018" in _jv(u) and "Notificada por Edicto el 29 de mayo de 2018" in _jv(u), f"Ley 1753 art. {num} ruling")
    key = f"art-{int(num):04d}"
    B23._need(all(key not in (v.get("units") or {}) for v in act["versions"]), f"Ley 1753 art. {num} absent")
    B23._need(E.add_months("2018-05-29", 12) == C008_DAY, "C-008-18 day")
    c008 = E.add_court("C-008-18", "2018-03-07", "c-008_2018.html")
    E.LAWS[c008]["note"] = None
    _set(act, key, f"Art. {num}", [(None, _printed(u), None), (C008_DAY, None, c008)])
    B23._forget(L1753, key)


def fix_1753_25_26(act):
    """Ley 1753 de 2015, arts. 25 and 26 (fuel distribution and hydrocarbon sanctions): Sentencia C-008-18 (7 March 2018)
    struck them with effect deferred one year from its notification (edicto of 29 May 2018); the page prints their words
    under that marker. They are in force from the act's first day and out from 29 May 2019, credited to the ruling (the
    engine had left them out of every version)."""
    _fix_c008(act, "25")
    _fix_c008(act, "26")
    _done(T1753, fix_1753_25_26)


def fix_1753_59(act):
    """Ley 1753 de 2015, art. 59 (Fondo de Financiamiento de la Infraestructura Educativa): parágrafo 5 added by Decreto
    Legislativo 155 de 2025 (7 February 2025; earlier-text box), in force only while the estado de conmoción interior
    lasted, which the page says was lifted from 24 April 2025: the words leave on that day, credited to the decree whose
    term ended (C-218-25 later struck it, June 2025); the bare 'PARÁGRAFO 5o.' the page still prints stays. The second
    parágrafo 5 is Decreto Legislativo 227 de 2026's (Diario Oficial of 6 March 2026, in force on publication); the
    engine had credited it to Decreto 150 de 2026 (the emergency's declaration, 11 February 2026). Its 'pérdida de
    fuerza ejecutoria por cumplimiento del período de aplicación' has no day in the source: the words stay."""
    u = B23._unit(L1753, "59")
    bx = [b for b in B23._boxes(u, "Legislación Anterior") if "Decreto Legislativo 155" in b]
    B23._need(len(bx) == 1 and "Estado de Conmoción Interior levantado a partir del 24 de abril de 2025" in E.plain(bx[0]),
              "Ley 1753 art. 59 D155 box")
    p5 = B23._box_lines(bx[0], "Texto adicionado por el Decreto Legislativo 155 de 2025")
    B23._need(len(p5) == 1 and p5[0].startswith("PARÁGRAFO 5. En el caso de los territorios"), "Ley 1753 art. 59 D155 text")
    B23._need("Parágrafo adicionado por el artículo 1 del Decreto Legislativo 227 de 5 de marzo de 2026" in _nv(u)
              and "publicado en el Diario Oficial No. 53.419 de 6 de marzo de 2026. Rige a partir de su publicación" in _nv(u),
              "Ley 1753 art. 59 D227 note")
    h = _hist(act, "art-0059")
    B23._need([(d, c) for d, _, c in h] == [("2015-06-09", None), ("2019-05-25", ["ley-1955-2019"]),
                                            ("2025-02-07", ["dec-155-2025"]), ("2026-02-11", ["dec-150-2026"]),
                                            ("2026-09-17", ["dec-1421-2026"])], f"Ley 1753 art. 59 {_shape(h)}")
    t25 = h[2][1]
    k = t25.index("PARÁGRAFO 5o.")
    with5 = t25[:k] + ["PARÁGRAFO 5o. " + p5[0][len("PARÁGRAFO 5. "):]] + t25[k + 1:]
    d227 = E.register("dec-227-2026")
    B23._need(E.law_day(d227) == "2026-03-06", "Decreto 227 de 2026 day")
    _set(act, "art-0059", "Art. 59", [(None, h[0][1], None), ("2019-05-25", h[1][1], "ley-1955-2019"),
                                      ("2025-02-07", with5, "dec-155-2025"), ("2025-04-24", t25, "dec-155-2025"),
                                      ("2026-03-06", h[3][1], d227), ("2026-09-17", h[4][1], "dec-1421-2026")])
    B23._forget(L1753, "art-0059")
    _done(T1753, fix_1753_59)


def fix_1753_222(act):
    """Ley 1753 de 2015, art. 222: the earlier-text box gives the article with the parágrafo transitorio Decreto Ley 892
    de 2017 added (28 May 2017); the original text is that box without the parágrafo transitorio and its second inciso
    (the engine had put the placeholder before the decree)."""
    h = _hist(act, "art-0222")
    B23._need(_shape(h)[0] == ("2015-06-09", None, "PH") and h[1][2] == ["dec-892-2017"], f"Ley 1753 art. 222 {_shape(h)}")
    t17 = h[1][1]
    k = next(i for i, x in enumerate(t17) if x.startswith("PARÁGRAFO TRANSITORIO."))
    B23._need(k == 3 and len(t17) == 5 and t17[4].startswith("En todo caso, el Ministerio de Educación Nacional, a partir de "
                                                             "la expedición del decreto"), "Ley 1753 art. 222 lines")
    rest = [(d, b, (c or [None])[0]) for d, b, c in h[1:]]
    # a ruling that changed no words of the article (C-535-17 upheld the decree's words on a condition) keeps its day
    for v in act["versions"]:
        c = v["credits"].get("art-0222")
        if c and v["from"] not in [d for d, _, _ in rest]:
            prev = [b for d, b, _ in [(h[0][0], t17, None)] + rest if d < v["from"]][-1]
            rest.append((v["from"], prev, c[0]))
    rest.sort(key=lambda x: x[0])
    _set(act, "art-0222", "Art. 222", [(None, t17[:3], None)] + rest)
    B23._forget(L1753, "art-0222")
    _done(T1753, fix_1753_222)


FIXES["plan-nacional-de-desarrollo-2010-2014"] = [fix_1450_44, fix_1450_46, fix_1450_89, fix_1450_199, fix_1450_56]
FIXES["plan-nacional-de-desarrollo-2014-2018"] = [fix_1753_13, fix_1753_25_26, fix_1753_59, fix_1753_222]


def run(slug):
    def go(act):
        for f in FIXES.get(slug, []):
            f(act)
        # a version left with no credit and no change by the fixes above (its only change was re-dated) goes
        vs = act["versions"]
        act["versions"] = [vs[0]] + [v for p, v in zip(vs, vs[1:]) if v["credits"] or v.get("units") != p.get("units")]
        for v in vs:
            if v not in act["versions"]:
                B29.HAND_DONE.append(f"{act['title']}: the version of {v['from']} is gone (its only change was re-dated "
                                     "above).")
    return go


def install(driver):
    global D, B23, B29, B13, E, P
    D = driver
    B23, B29, B13, E, P = D.B23, D.B29, D.B13, D.E, D.P
    B29.HAND_FIXES.update({s: run(s) for s in FIXES})
