"""Hand-set histories for batch 54 (bound by parse_batch54.py through install(); each checks the page first)."""
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



L446 = "ley_0446_1998"
T446 = "Descongestión, eficiencia y acceso a la justicia (Ley 446 de 1998)"


def fix_446_640(act):
    """Ley 446 de 1998: the articles Ley 640 de 2001 art. 49 repealed are marked '... a partir del 24 de enero de 2002'
    (one year after the act's republication with Decreto 131 de 2001's corrections); the corpus dates Ley 640 de 2001's
    articles, art. 49 among them, from 5 January 2002 (one year after its first publication; Conciliación (Ley 640 de
    2001)), so its repeals here are dated that day too."""
    vs = [v for v in act["versions"] if v["from"] == "2002-01-24"]
    B23._need(len(vs) == 1 and {l for ls in vs[0]["credits"].values() for l in ls} == {"ley-640-2001"}
              and not any(v["from"] == "2002-01-05" for v in act["versions"]), "Ley 446 Ley 640 version")
    n = 0
    for u in P.doc_units(L446)[1:]:
        if any("derogado por el artículo 49 de la Ley 640 de 2001, a partir de" in m and "24 de enero de 2002" in m
               for m in _p0_markers(u)):
            n += 1
    B23._need(n >= 15, f"Ley 446 Ley 640 markers {n}")
    vs[0]["from"] = "2002-01-05"
    _done(T446, fix_446_640)


FIXES["descongestion-y-acceso-a-la-justicia-1998"] = [fix_446_640]


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
    import hf446
    hf446.install(sys.modules[__name__])
    B29.HAND_FIXES.update({s: run(s) for s in FIXES})
