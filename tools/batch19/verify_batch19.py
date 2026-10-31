"""Check corpus.d/99k-batch19.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch19 applies on import). Versions dated after the retrieval day are left
out: the text checked is the one in force on that day. Words the source shows replaced in place are read as the new words.

Usage: python -X utf8 batch19/verify_batch19.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch18", "batch17", "batch16", "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch19  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch19.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch19.PART)
_full = V.P.full_versions
V.P.full_versions = lambda vs: [v for v in _full(vs) if v["from"] <= parse_batch19.E.RETRIEVED]

_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}  # replaced words: today's are the new

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

import verify_extra  # noqa: E402  (articles repealed or struck whole, with words still printed: not in force today)

verify_extra.install(V)

if __name__ == "__main__":
    V.main(sys.argv[1:])
