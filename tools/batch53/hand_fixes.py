"""Hand-set histories for batch 53 (bound by parse_batch53.py through install(); each checks the page first)."""
from __future__ import annotations

import re

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


def fix_1395_47(act):
    """Ley 1395 de 2010, art. 47: struck as a whole by Sentencia C-470-11 (press release of 13 June 2011, the day used,
    the day the same ruling took art. 45 out); the page gives its words in the earlier-text box. In force from the act's
    first day to the ruling (the engine had it in no version)."""
    u = B23._unit(L1395, "47")
    B23._need("Artículo declarado INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-470-11 según Comunicado de "
              "Prensa de la Sala Plena de 13 de junio de 2011" in _jv(u), "Ley 1395 art. 47 ruling")
    B23._need(all("art-0047" not in (v.get("units") or {}) for v in act["versions"]), "Ley 1395 art. 47 absent")
    box = B23._box_lines(B23._boxes(u, "Legislación Anterior")[0], "Texto original de la Ley 1395 de 2010")
    box[0] = re.sub(r"^ARTÍCULO 47\.\s*", "", box[0])
    B23._need(box[0].startswith("El numeral 3 del parágrafo 1o del artículo 77 del Código Procesal del Trabajo"), "Ley 1395 art. 47 box")
    c470 = next(l for v in act["versions"] for ls in v["credits"].values() for l in ls if l == "c-470-11")
    B23._need(E.law_day(c470) == "2011-06-13", "C-470-11 day")
    _set(act, "art-0047", "Art. 47", [(None, box, None), ("2011-06-13", None, c470)])
    B23._forget(L1395, "art-0047")
    _done(T1395, fix_1395_47)


def fix_1395_113(act):
    """Ley 1395 de 2010, art. 113: Sentencia C-863-12 (24 October 2012) struck its first two paragraphs and the words
    'Para estos efectos' of the third (shown struck in the earlier-text box); from the ruling the article reads
    'facúltase a los notarios para que reciban declaraciones extraproceso con fines judiciales.' (the engine had put the
    placeholder there); out from 1 January 2014 with the Código General del Proceso's repeal."""
    u = B23._unit(L1395, "113")
    B23._need("Apartes tachados del texto original declarados INEXEQUIBLES, resto del artículo EXEQUIBLE por la Corte "
              "Constitucional mediante Sentencia C-863-12 de 24 de octubre de 2012" in _jv(u), "Ley 1395 art. 113 ruling")
    b = B23._boxes(u, "Legislación Anterior")[0]
    blk = next(x for x in E.la_blocks(b) if x["head"].startswith("Texto original de la Ley 1395 de 2010"))
    rest = [E.tidy(E.to_text(p, False)) for p in blk["paras"]]
    B23._need(rest == ["ARTÍCULO 113.", "", ", facúltase a los notarios para que reciban declaraciones extraproceso con "
                       "fines judiciales."], f"Ley 1395 art. 113 struck words {rest}")
    h = _hist(act, "art-0113")
    B23._need(_shape(h) == [("2010-07-12", None, 3), ("2012-10-24", ["c-863-12"], "PH"), ("2014-01-01", ["ley-1564-2012"], None)],
              f"Ley 1395 art. 113 {_shape(h)}")
    after = ["Facúltase a los notarios para que reciban declaraciones extraproceso con fines judiciales."]
    _set(act, "art-0113", "Art. 113", [(None, h[0][1], None), ("2012-10-24", after, "c-863-12"),
                                       ("2014-01-01", None, "ley-1564-2012")])
    B23._forget(L1395, "art-0113")
    _done(T1395, fix_1395_113)


def fix_1395_44(act):
    """Ley 1395 de 2010, art. 44: out from 1 January 2014 with the Código General del Proceso's repeal (the day the corpus
    uses for that gradual repeal everywhere). Ley 1716 de 2014 (16 May 2014) amended its parágrafo afterwards (the notes:
    the oral system's deadline moved to 31 December 2015); the source gives no wording for that change (the earlier-text
    box, though headed 'con la modificación introducida por la Ley 1716 de 2014', prints the original 'plazo máximo de
    tres años'), and the article is already out of the record on that day, so the change is not shown (open item)."""
    u = B23._unit(L1395, "44")
    B23._need("Parágrafo modificado por el artículo 1 de la Ley 1716 de 2014" in _nv(u), "Ley 1395 art. 44 note")
    h = _hist(act, "art-0044")
    B23._need(_shape(h) == [("2010-07-12", None, 2), ("2014-01-01", ["ley-1564-2012"], None)]
              and any(v["from"] == "2014-05-16" and v["credits"].get("art-0044") == ["ley-1716-2014"] for v in act["versions"]),
              f"Ley 1395 art. 44 {_shape(h)}")
    _set(act, "art-0044", "Art. 44", [(None, h[0][1], None), ("2014-01-01", None, "ley-1564-2012")])
    v16 = next(v for v in act["versions"] if v["from"] == "2014-05-16")
    B23._need(not v16["credits"], f"Ley 1395 2014-05-16 credits {v16['credits']}")
    act["versions"].remove(v16)
    B23._forget(L1395, "art-0044")
    _done(T1395, fix_1395_44)


FIXES["descongestion-judicial-2010"] = [fix_printed(L1395, T1395), fix_1395_47, fix_1395_113, fix_1395_44]


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
