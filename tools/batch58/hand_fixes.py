"""Hand-set histories for batch 58 (bound by parse_batch58.py through install(); each checks the page first)."""
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


FIXES["codigo-disciplinario-unico-1995"] = [fix_200_41]


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
