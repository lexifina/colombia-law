"""Hand-set histories for batch 87 (bound by parse_batch59.py through install(); each checks the page first)."""
from __future__ import annotations

import re
import sys

D = B23 = B29 = B13 = E = P = None
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




L1395 = "ley_1395_2010"
T1395 = "Descongestión judicial (Ley 1395 de 2010)"

# Articles repealed on a later day whose words the page still prints under a marker that names the repeal and its day:
# page -> [(marker start, repealing law, day)]. The printed words stand from the act's first day; the article leaves on
# the day the marker gives, credited to the repealing law. (The engine had read these as words that arrive on the repeal
# day, with the placeholder before, and for the Código General del Proceso's staged repeal took its promulgation day.)
PRINTED = {
    L1395: [
        ("Artículo derogado por el literal c) del artículo 626 de la Ley 1564 de 2012. Rige a partir del 1o. de enero de "
         "2014, en forma gradual, en los términos del numeral 6) del artículo 627", "ley-1564-2012", "2014-01-01"),
        ("Artículo derogado a partir del 30 de diciembre de 2022 por el artículo 146 de la Ley 2220 de 2022",
         "ley-2220-2022", "2022-12-30"),
        ("Artículo derogado a partir del 2 de abril de 2026 por el artículo de la artículo 331 de la Ley 2452 de 2025",
         "ley-2452-2025", "2026-04-02"),
        ("Artículo derogado por el artículo 309 de la Ley 1437 de 2011. Rige a partir del dos (2) de julio del año 2012",
         "ley-1437-2011", "2012-07-02"),
    ],
}
PRINTED_DONE: dict = {}   # (page, key) -> marker (used by the verifier)


def _p0_markers(u):
    p0 = next((it[1] for it in u["items"] if it[0] == "p"), "")
    return E.markers(p0)


def fix_printed(page, title):
    def fix(act):
        done = []
        for u in P.doc_units(page)[1:]:
            num = E.label_num(u["label"] or "")
            if not num:
                continue
            ms = _p0_markers(u)
            hit = [(m, law, day) for m in ms for start, law, day in PRINTED[page] if m.startswith(start)]
            if not hit:
                continue
            B23._need(len(hit) == 1, f"{page} art. {num}: markers {ms}")
            m, law, day = hit[0]
            key = E.unit_key(u["name"])[0]
            ps = [it[1] for it in u["items"] if it[0] == "p"]
            if not any(re.search(r"\w", E.tidy(E.to_text(x, False))) for x in ps):
                continue  # no words printed (the earlier-text box has them; the engine reads it)
            printed = _printed(u)
            h = _hist(act, key)
            B23._need(h, f"{page} {key}: not in the act")
            tl = [(None, printed, None)]
            for d, b, c in h[1:]:
                if c == [law] or (d >= day):
                    continue
                B23._need(b in (None, printed, [PH]), f"{page} {key}: change on {d} {c} {_shape(h)}")
            # events that changed no words of the article (a ruling's note) keep their day and credit
            for v in act["versions"][1:]:
                c = v["credits"].get(key)
                if c and c != [law] and v["from"] < day:
                    tl.append((v["from"], printed, c[0]))
            tl.append((day, None, law))
            ends = [x for x in h if x[0] >= day and x[2] != [law]]
            B23._need(not ends, f"{page} {key}: events after the repeal {ends}")
            label = f"Art. {num}"
            _set(act, key, label, tl)
            B23._forget(page, key)
            PRINTED_DONE[(page, key)] = m
            done.append(f"{num} ({law}, {day})")
        B29.HAND_DONE.append(f"{title}: articles repealed on a later day whose words the page still prints under the marker "
                             "naming the repeal and its day read those words from the act's first day and leave on that "
                             "day, credited to the repealing act (the engine had the placeholder before and the words "
                             "arriving on the repeal day): art(s). " + ", ".join(done) + ".")
    return fix







L1561, T1561 = "ley_1561_2012", "Titulación de la posesión y saneamiento de la falsa tradición (Ley 1561 de 2012)"
D902, T902 = "decreto_0902_2017", "Reforma Rural Integral en materia de tierras (Decreto Ley 902 de 2017)"

# Words the page shows struck by a ruling the Jurisprudencia Vigencia box dates, which the engine dropped from every
# version ('struck text but no dated ruling'): the words stand from the act's first day to the ruling's day, then go,
# credited to the ruling; events before that day that changed no words keep their day and credit.
# STRUCK: page -> [(article, ruling, day, href, words the box must hold)].
STRUCK = {
    L1561: [("23", "C-399-24", "2024-09-19", "c-399_2024.html",
             "INEXEQUIBLE la expresión 'de pleno derecho' por la Corte Constitucional mediante Sentencia C-399-24 de 19 de "
             "septiembre de 2024")],
    D902: [(a, "C-099-26", "2026-04-22", "c-099_2026.html",
            "salvo el aparte tachado 'en los términos del presente decreto ley' declarado INEXEQUIBLE"
            + (", " if a == "38" else " ") + "por la Corte Constitucional mediante Sentencia C-099-26 según Comunicado "
            "de Prensa de 22 de abril de 2026") for a in ("38", "39")],
}


def fix_struck(page, title):
    def fix(act):
        done = []
        for num, rid, day, href, need in STRUCK[page]:
            u = B23._unit(page, num)
            B23._need(need in _jv(u), f"{page} art. {num}: ruling text")
            before, after = _printed(u, True), _printed(u)
            B23._need(before != after and len(before) == len(after), f"{page} art. {num}: struck words")
            # the page wraps some struck words in the editor's square brackets inside the struck markup: not law text
            before = [re.sub(r"\[([^\[\]]+)\]", r"\1", b) if b != a else b for b, a in zip(before, after)]
            key = E.unit_key(num)[0]
            h = _hist(act, key)
            B23._need(h and h[0][1] == after and all(b == after for _, b, _ in h), f"{page} {key}: {_shape(h)}")
            c = E.add_court(rid, day, href)
            E.LAWS[c]["note"] = None
            tl = [(None, before, None)]
            for v in act["versions"][1:]:
                cr = v["credits"].get(key)
                if cr and cr != [c] and v["from"] < day:
                    tl.append((v["from"], before, cr[0]))
            B23._need(not [v for v in act["versions"] if v["from"] > day and v["credits"].get(key)],
                      f"{page} {key}: events after the ruling")
            tl.append((day, after, c))
            # a version already on the ruling's day that changed no words carries no units: give it the full state
            vs = act["versions"]
            for i, v in enumerate(vs):
                if v["from"] == day and "units" not in v:
                    v["units"] = dict(next(w for w in reversed(vs[:i]) if "units" in w)["units"])
            _set(act, key, f"Art. {num}", tl)
            B23._forget(page, key)
            done.append(f"{num} ({rid}, {day})")
        B29.HAND_DONE.append(f"{title}: words the page shows struck by a ruling its Jurisprudencia Vigencia box names and "
                             "dates (the engine had left them out of every version) are in the text from the act's first "
                             "day to the ruling's day (the press release's day where the box gives only that), then go, "
                             "credited to the ruling (square brackets the page puts round struck words are the editor's "
                             "and are left out): art(s). " + ", ".join(done) + ".")
    return fix


STRUCK = {}
FIXES: dict = {}
L200, T200 = "ley_0200_1995", "Código Disciplinario Único (Ley 200 de 1995)"


def fix_200_41(act):
    """Ley 200 de 1995, art. 41, numeral 29: the page prints '29. <Numeral INEXEQUIBLE>' and gives the original words in
    the earlier-text box ('Texto Original de la Ley 200 de 1995: ARTÍCULO 41. 29) Solicitar u obtener préstamos ...');
    Sentencia C-280-96 (25 June 1996) struck it. The engine had the bare '29.' from the act's first day. The numeral
    reads its original words (numbered '29.' as the article's other numerals are) up to the ruling, then the bare
    number, as today's text has it."""
    u = B23._unit(L200, "41")
    B23._need("Numeral 29 declarado INEXEQUIBLE por la Corte Constitucional mediante sentencia C-280-96 del 25 de junio de "
              "1996" in _jv(u), "L200 art. 41 ruling")
    box = " ".join(E.plain(b) for b in B23._boxes(u, "Legislación Anterior"))
    words = ("Solicitar u obtener préstamos o garantías de los organismos crediticios, sin autorización escrita y previa "
             "del jefe del respectivo organismo, o de quien esté delegado.")
    B23._need("Texto Original de la Ley 200 de 1995:ARTÍCULO 41. 29) " + words in box, "L200 art. 41 box")
    h = _hist(act, "art-0041")
    B23._need([(d, c) for d, _, c in h] == [("1995-09-11", None)] and h[0][1].count("29.") == 1, f"L200 art. 41 {_shape(h)}")
    today = h[0][1]
    orig = [("29. " + words) if l == "29." else l for l in today]
    B23._need(orig != today, "L200 art. 41 numeral 29")
    c280 = "c-280-96"
    E.LAWS[c280]["note"] = None
    _set(act, "art-0041", _label(act, "art-0041"), [(None, orig, None), ("1996-06-25", today, c280)])
    B23._forget(L200, "art-0041")
    _done(T200, fix_200_41)


# (batch 58's fix_200_41 for Ley 200 de 1995 is published in 99zx-batch58; not run here)

L4, T4 = "ley_0004_1913", "Código de Régimen Político y Municipal (Ley 4 de 1913)"
L454, T454 = "ley_0454_1998", "Economía solidaria (Ley 454 de 1998)"


def _n(s):
    return re.sub(r"\s+", " ", s or "").strip()


def _one(h, what):
    """credits of a history entry as one law key (None for the first)."""
    return [(d, b, (c or [None])[0]) for d, b, c in h] if all(len(c or []) <= 1 for _, _, c in h) else \
        B23._need(False, f"{what}: several credits {_shape(h)}")


def _added_after_marker(page, num, marker, law, day, title):
    """Lines a paragraph-level marker '<... adicionada(s) por ... Ley X ...>' puts at the end of the article: absent
    before the law's day, then there, credited to it (the engine had them from the act's first day)."""
    u = B23._unit(page, num)
    ps = [it[1] for it in u["items"] if it[0] == "p"]
    k = next(i for i, ph in enumerate(ps) if marker in E.plain(ph))
    added = [t for t in (E.tidy(E.to_text(ph, False)) for ph in ps[k:]) if re.search(r"\w", t)]
    act_label = marker.split(" de la ")[-1].split(".")[0]  # e.g. 'Ley 84 de 1915'
    B23._need(bool(added) and E.law_day(law) == day and act_label in _nv(u),
              f"{page} art. {num}: {law} day {E.law_day(law)} / note")

    def fix(act):
        key = E.unit_key(num)[0]
        h = _one(_hist(act, key), f"{page} {num}")
        B23._need(all(d != day for d, _, _ in h) and h[0][0] < day, f"{page} {num}: {_shape(h)}")
        out, prev, inserted = [], None, False
        for idx, (d, b, c) in enumerate(h):
            if d > day and not inserted:
                out.append((day, prev, law))
                inserted = True
            if d < day:
                B23._need(b is not None and [_n(x) for x in b[-len(added):]] == [_n(x) for x in added],
                          f"{page} {num}: added lines not at the end on {d}")
                out.append((None if idx == 0 else d, b[:-len(added)], c))
                prev = b
            else:
                out.append((d, b, c))
        if not inserted:
            out.append((day, prev, law))
        _set(act, key, _label(act, key), out)
        B23._forget(page, key)
        B29.HAND_DONE.append(f"{title}: art. {num}: the lines the page puts after its marker '<{marker}>' "
                             f"({len(added)} line(s)) are absent before {day}, the day of the act that added them, and "
                             f"arrive then, credited to it (the engine had them from the act's first day).")
    return fix


def _orig_from_box(page, num, old_first, n_old, law, title, why):
    """The first version's text: the text of the version after it (`law`'s), with the `n_old` lines starting with
    `old_first` replaced by the paragraph(s) of the article's earlier-text box (its heading out)."""
    u = B23._unit(page, num)
    box = [E.tidy(E.to_text(p, False)) for b in B23._boxes(u, "Legislación Anterior") for p in E.box_paras(b)]
    box = [re.sub(r"^Texto original de la Ley [\d ]+ de \d{4}:\s*", "", t) for t in box if re.search(r"\w", t)]
    box = [t for t in box if t]

    def fix(act):
        key = E.unit_key(num)[0]
        h = _one(_hist(act, key), f"{page} {num}")
        B23._need(len(h) == 2 and h[0][1] == [PH] and h[1][2] == law, f"{page} {num}: {_shape(h)}")
        later = h[1][1]
        i = next(i for i, l in enumerate(later) if l.startswith(old_first))
        orig = later[:i] + box + later[i + n_old:]
        B23._need(orig != later, f"{page} {num}: no change")
        _set(act, key, _label(act, key), [(None, orig, None), (h[1][0], later, law)])
        B23._forget(page, key)
        B29.HAND_DONE.append(f"{title}: art. {num}: {why}")
    return fix


def fix_454_48_50(act):
    """Ley 454 de 1998, arts. 48 and 50: the engine gave the first version only the opening line its earlier-text box
    quotes. Art. 48: the box quotes the original opening line and a single unnumbered 'PARÁGRAFO', but today's text
    holds 'PARAGRAFO 1o' (Ley 795 de 2003) and 'PARAGRAFO 2o' with no marker, so neither the 1998 nor the 2003 wording is
    settled: both read as the placeholder. Art. 50: the box quotes the original opening line and 'PARÁGRAFO 1o'; the
    notes name only the opening line (Ley 1328 de 2009), parágrafo 1o (Ley 795 de 2003) and parágrafo 3o (added by Ley
    1328 de 2009), so the numerals and parágrafo 2o read as today's: original opening line + numerals + original
    parágrafo 1o + parágrafo 2o from 1998; Ley 795's parágrafo 1o from 2003-01-15; today's text from 2009-07-15."""
    u48, u50 = B23._unit(L454, "48"), B23._unit(L454, "50")
    for u, n in ((u48, "106"), (u50, "107")):
        B23._need(f"Parágrafo modificado por el artículo {n} de la Ley 795 de 2003" in _nv(u), f"L454 {n}")
    box50 = [E.tidy(E.to_text(p, False)) for b in B23._boxes(u50, "Legislación Anterior") for p in E.box_paras(b)]
    par50 = [re.sub(r"^Texto original de la Ley 454 de 1998:\s*", "", t) for t in box50 if "PARÁGRAFO 1o." in t]
    B23._need(len(par50) == 1 and par50[0].startswith("PARÁGRAFO 1o."), "L454 art. 50 box")
    for key in ("art-0048", "art-0050"):
        h = _one(_hist(act, key), key)
        B23._need([(d, c) for d, _, c in h] == [("1998-08-06", None), ("2003-01-15", "ley-795-2003"),
                                                  ("2009-07-15", "ley-1328-2009")] and h[1][1] == [PH] and len(h[0][1]) == 1,
                  f"L454 {key} {_shape(h)}")
        today = h[2][1]
        if key == "art-0048":
            tl = [(None, [PH], None), ("2003-01-15", [PH], "ley-795-2003"), ("2009-07-15", today, "ley-1328-2009")]
        else:
            B23._need([l[:3] for l in today] == [today[0][:3], "1. ", "2. ", "3. ", "4. ", "PAR", "PAR", "PAR"]
                      and today[5].startswith("PARAGRAFO 1o.") and today[6].startswith("PARAGRAFO 2o."),
                      f"L454 art. 50 today {[l[:12] for l in today]}")
            orig = [h[0][1][0]] + today[1:5] + par50 + [today[6]]
            mid = [h[0][1][0]] + today[1:7]
            tl = [(None, orig, None), ("2003-01-15", mid, "ley-795-2003"), ("2009-07-15", today, "ley-1328-2009")]
        _set(act, key, _label(act, key), tl)
        B23._forget(L454, key)
    _done(T454, fix_454_48_50)


def fix_4_294(act):
    """Ley 4 de 1913: the page prints two articles numbered 294 (and none numbered 293). The second is kept under the
    key art-0294-02 and shows the number the page prints, 'Art. 294'."""
    key = "art-0294-02"
    h = _one(_hist(act, key), "L4 294-2")
    B23._need(len(h) == 1 and h[0][1], f"L4 art. 294-2 {_shape(h)}")
    _set(act, key, "Art. 294", [(None, h[0][1], None)])
    _done(T4, fix_4_294)


# (batch 59's Ley 4 de 1913 / Ley 454 de 1998 fixes are published in 99zy-batch59; not run here)
L1719, T1719 = "ley_1719_2014", ("Acceso a la justicia de las víctimas de violencia sexual, en especial con ocasión del "
                                  "conflicto armado (Ley 1719 de 2014)")


def fix_1719_23(act):
    """art. 23: Sentencia C-754-15 (10 December 2015) struck 'facultad' and put 'obligación' in its place; the page
    prints both words (the struck one and the Court's). The act as enacted reads 'están en la facultad de implementar'
    until the ruling, 'están en la obligación de implementar' from it."""
    u = B23._unit(L1719, "23")
    B23._need("Expresión 'facultad' declarada INEXEQUIBLE y sustituida por la expresión 'obligación' por la Corte "
              "Constitucional mediante Sentencia C-754-15 de 10 de diciembre de 2015" in _jv(u), "L1719 art. 23 JV")
    key = "art-0023"
    h = _one(_hist(act, key), key)
    old, orig, new = "en la facultad obligación de implementar", "en la facultad de implementar", "en la obligación de implementar"
    B23._need(len(h) == 2 and h[1][2] == "c-754-15" and h[1][0] == "2015-12-10"
              and sum(old in l for l in h[0][1]) == 1 and sum(new in l for l in h[1][1]) == 1
              and [l.replace(old, new) for l in h[0][1]] == h[1][1], f"L1719 art. 23 {_shape(h)}")
    first = [l.replace(old, orig) for l in h[0][1]]
    _set(act, key, _label(act, key), [(None, first, None), (h[1][0], h[1][1], "c-754-15")])
    _done(T1719, fix_1719_23)


# (fix_1719_23 is published in 99zza-batch61; not run here)
L1826, T1826 = "ley_1826_2017", "Procedimiento penal especial abreviado y acusador privado (Ley 1826 de 2017)"
INC2_1826 = ("En el supuesto contemplado por el inciso anterior, se entenderá que la libertad del capturado representa "
             "peligro futuro para la sociedad en los términos de los artículos 308 y 310 de este código.")


def fix_1826_7(act):
    """art. 7 (numeral 4 of Ley 906 de 2004 art. 313, quoted): its second inciso, which the page gives only in the
    article's earlier-text box ('<INCISO 2> En el supuesto contemplado ...'), stands from the act's first day until
    Sentencia C-567-19 struck it (press release of 27 November 2019, the day the Código de Procedimiento Penal's history
    gives the ruling); the engine had left it out of every version."""
    u = B23._unit(L1826, "7")
    B23._need("La Corte Constitucional mediante Sentencia C-567-19 según Comunicado de Prensa de 27 de noviembre de 2019"
              in _jv(u) and "Declara INEXEQUIBLE el inciso 2o." in _jv(u), "L1826 art. 7 JV")
    box = " ".join(E.plain(b) for b in B23._boxes(u, "Legislación Anterior"))
    B23._need("Texto original de la Ley 1826 de 2017:<INCISO 2> " + INC2_1826 in box, "L1826 art. 7 box")
    key = "art-0007"
    h = _one(_hist(act, key), key)
    B23._need(len(h) == 1 and len(h[0][1]) == 2 and h[0][1][1].startswith("4. Cuando la persona haya sido capturada"),
              f"L1826 art. 7 {_shape(h)}")
    c = E.add_court("C-567-19", "2019-11-27", "c-567_2019.html")
    E.LAWS[c]["note"] = None
    _set(act, key, _label(act, key), [(None, h[0][1] + [INC2_1826], None), ("2019-11-27", h[0][1], c)])
    B23._forget(L1826, key)
    _done(T1826, fix_1826_7)


# (fix_1826_7 is published in 99zzb-batch62; not run here)



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
    import hf87  # noqa: F401  (batch 87 fixes register in FIXES)
    B29.HAND_FIXES.update({s: run(s) for s in FIXES})
