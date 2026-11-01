"""Check corpus.d/99d-batch12.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch12 applies on import). Versions dated after the retrieval day are left
out: the text checked is the one in force on that day. Words the source shows replaced in place are read as the new words.

Usage: python -X utf8 batch12/verify_batch12.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch12  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402
import subst  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch12.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch12.PART)
_full = V.P.full_versions
V.P.full_versions = lambda vs: [v for v in _full(vs) if v["from"] <= parse_batch12.E.RETRIEVED]

_today = V.today
V.today = lambda name: {k: subst.today_new(ls) for k, ls in _today(name).items()}  # replaced words: today's are the new

import verify_extra  # noqa: E402  (articles repealed or struck whole, with words still printed: not in force today)

verify_extra.install(V)

if __name__ == "__main__":
    V.main(sys.argv[1:])
