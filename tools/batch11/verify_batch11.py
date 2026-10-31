"""Check corpus.d/99c-batch11.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch11 applies on import). Versions dated after the retrieval day (the
future branch: Decreto 111 de 1996 arts. 36 and 110 from 1 January 2027) are left out: the text checked is the one in
force on that day.

Usage: python -X utf8 batch11/verify_batch11.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch11  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch11.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch11.PART)
_full = V.P.full_versions
V.P.full_versions = lambda vs: [v for v in _full(vs) if v["from"] <= parse_batch11.E.RETRIEVED]

import verify_extra  # noqa: E402  (articles repealed or struck whole, with words still printed: not in force today)

verify_extra.install(V)

# Ley 617 de 2000, art. 33: repealed by Ley 2200 de 2022 art. 154, the page still prints its words under the marker
# '<Derogado por el artículo 154 (ver sobre el tema el Art. 49) de la Ley 2200 de 2022>' (../fix_ley617_art33.py).
GONE = {"ley_0617_2000": {"art-0033"}}
_today_extra = V.today
V.today = lambda name: {k: ([] if k in GONE.get(name, set()) else ls) for k, ls in _today_extra(name).items()}

if __name__ == "__main__":
    V.main(sys.argv[1:])
