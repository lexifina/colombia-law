"""Check corpus.d/99l-batch20.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch20 applies on import). Versions dated after the retrieval day are left
out: the text checked is the one in force on that day. Words the source shows replaced in place are read as the new words.

Usage: python -X utf8 batch20/verify_batch20.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch19", "batch18", "batch17", "batch16", "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch20  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch20.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch20.PART)
_full = V.P.full_versions
V.P.full_versions = lambda vs: [v for v in _full(vs) if v["from"] <= parse_batch20.E.RETRIEVED]

_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}  # replaced words: today's are the new

# Words a ruling ordered read in place of struck ones, printed '<S>old</S> <new>' without the asterisk subst.py reads
# (fix_dated_struck.py, 2026-10-31): Ley 1922 de 2018 art. 54, 'verificará' -> 'evaluará' (Sentencia C-112 de 2019).
NEW_WORDS = {("ley_1922_2018", "art-0054"): ("La Sección de Revisión que los hechos", "La Sección de Revisión evaluará que los hechos")}
_today_nw = V.today


def _with_new_words(name):
    t = _today_nw(name)
    for (pg, key), (old, new) in NEW_WORDS.items():
        if pg == name:
            ls = t[key]
            if sum(old in l for l in ls) != 1:
                raise SystemExit(f"{pg} {key}: page changed")
            t[key] = [l.replace(old, new) for l in ls]
    return t


V.today = _with_new_words

# An article the Court struck as a whole whose page still prints its words after the marker '<Artículo INEXEQUIBLE>'
# (Ley 2200 de 2022, art. 151, Sentencia C-054-23): not in force today.
import re  # noqa: E402

WHOLE_STRUCK = re.compile(r'^\s*(?:<span class="b_aj">)?&lt;Art&iacute;culo INEXEQUIBLE&gt;')
_today2 = V.today


def today_struck(name):
    out = _today2(name)
    for u in V.P.doc_units(name)[1:]:
        ps = [it for it in u["items"] if it[0] == "p"]
        jv = " ".join(V.E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")
        num = V.E.label_num(u["label"] or "")
        if ps and num and WHOLE_STRUCK.match(ps[0][1]) and "Artículo declarado INEXEQUIBLE" in jv:
            out[V.E.unit_key(num)[0]] = []
    return out


V.today = today_struck

# Ley 418 de 1997 articles the page marks '<Opera la pérdida de fuerza ejecutoria por no haber sido prorrogado este
# artículo por la Ley N de AAAA>': out of force since their last extension term ended (fix_ley418_term.py, 2026-10-31),
# save art. 96, whose day cannot be fixed and which stays as printed.
LAPSED = re.compile(r"&lt;Opera la p(?:&eacute;|é)rdida de fuerza ejecutoria (?:<U>)?por no haber sido prorrogado")
LAPSED_KEEP = {"96"}
_today3 = V.today


def today_lapsed(name):
    out = _today3(name)
    if name != "ley_0418_1997":
        return out
    n = 0
    for u in V.P.doc_units(name)[1:]:
        ps = [it for it in u["items"] if it[0] == "p"]
        if ps and LAPSED.search(" ".join(it[1] for it in ps)) and u["name"] not in LAPSED_KEEP:
            out[V.E.unit_key(u["name"])[0]] = []
            n += 1
    if n != 17:
        raise SystemExit(f"{name}: {n} lapsed articles")
    return out


V.today = today_lapsed

import verify_extra  # noqa: E402  (articles repealed or struck whole, with words still printed: not in force today)

verify_extra.install(V)

if __name__ == "__main__":
    V.main(sys.argv[1:])
