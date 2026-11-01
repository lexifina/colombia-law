"""Hand-set histories for batch 52 (bound by parse_batch52.py through install(); each checks the page first)."""
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



L1978, L2068 = "ley_1978_2019", "ley_2068_2020"
T1978 = "Modernización del sector de las Tecnologías de la Información y las Comunicaciones (Ley 1978 de 2019)"
T2068 = "Ley General de Turismo (Ley 2068 de 2020)"


def fix_1978_31(act):
    """Ley 1978 de 2019, art. 31: the earlier-text box ('Texto original de la Ley 1978 de 2019, parcialmente adicionado
    por la Ley 2108 de 2021') gives the original article with the two parágrafos Ley 2108 de 2021 art. 6 added; the
    original text is that box without them, from the act's first day (the engine had put the placeholder before Ley
    2108)."""
    u = B23._unit(L1978, "31")
    B23._need("Parágrafos adicionados por el artículo 6 de la Ley 2108 de 2021" in _nv(u), "Ley 1978 art. 31 note")
    h = _hist(act, "art-0031")
    B23._need(_shape(h) == [("2019-07-25", None, "PH"), ("2021-07-29", ["ley-2108-2021"], 3),
                            ("2023-05-19", ["ley-2294-2023"], 2)], f"Ley 1978 art. 31 {_shape(h)}")
    t21 = h[1][1]
    B23._need(t21[1].startswith("PARÁGRAFO 1o.") and t21[2].startswith("PARÁGRAFO 2o."), "Ley 1978 art. 31 lines")
    _set(act, "art-0031", "Art. 31", [(None, t21[:1], None), ("2021-07-29", t21, "ley-2108-2021"),
                                      ("2023-05-19", h[2][1], "ley-2294-2023")])
    B23._forget(L1978, "art-0031")
    _done(T1978, fix_1978_31)


def fix_2068_53(act):
    """Ley 2068 de 2020, art. 53: the page prints the act's own words under '<Ver Notas de Vigencia>'; the notes say
    Decreto Legislativo 117 de 2025 (30 January 2025) modified it transitorily while the estado de conmoción interior of
    Decreto 62 de 2025 and its extensions lasted, and Sentencia C-248-25 (11 June 2025) struck that decree's art. 1. The
    printed words are the act's from its first day (the engine had put the placeholder before 2025 and credited them to
    Decreto 62 de 2025). The decree's transitory wording is left out: the source gives no day on which it stopped
    applying before the ruling (open item)."""
    u = B23._unit(L2068, "53")
    B23._need("Artículo modificado transitoriamente -durante el término de la declaratoria del estado de conmoción interior "
              "de que trata el Decreto 0062 de 2025" in _nv(u) and "Artículo 1 del Decreto Legislativo 117 de 2025 declarado "
              "INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-248-25 de 11 de junio de 2025" in _nv(u)
              and not B23._boxes(u, "Legislación Anterior"), "Ley 2068 art. 53 notes")
    h = _hist(act, "art-0053")
    B23._need(_shape(h) == [("2020-12-31", None, "PH"), ("2025-01-24", ["dec-62-2025"], 6)], f"Ley 2068 art. 53 {_shape(h)}")
    B23._need(h[1][1] == _printed(u), "Ley 2068 art. 53 printed words")
    _set(act, "art-0053", "Art. 53", [(None, h[1][1], None)])
    B23._forget(L2068, "art-0053")
    _done(T2068, fix_2068_53)


FIXES["modernizacion-sector-tic-2019"] = [fix_1978_31]
def fix_2068_44(act):
    """Ley 2068 de 2020, art. 44 (USD 0.5 per tourism tax for San Andrés and Providencia): art. 55 says 'El artículo 44
    expirará finalizada la vigencia fiscal 2021'; the page still prints it with no marker. It is out from 1 January 2022,
    the day after the fiscal year 2021 ended, credited to the act itself."""
    a55 = B13.B7.B3.article_text(P.doc_units(L2068), "55")
    B23._need("El artículo 44 expirará finalizada la vigencia fiscal 2021" in a55, "Ley 2068 art. 55")
    h = _hist(act, "art-0044")
    B23._need(_shape(h) == [("2020-12-31", None, 1)], f"Ley 2068 art. 44 {_shape(h)}")
    _set(act, "art-0044", "Art. 44", [(None, h[0][1], None), ("2022-01-01", None, "ley-2068-2020")])
    B23._forget(L2068, "art-0044")
    _done(T2068, fix_2068_44)


FIXES["ley-general-de-turismo-2020"] = [fix_2068_53, fix_2068_44]


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
