"""Check corpus.d/99a-batch9.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch9 applies on import).

Usage: python -X utf8 batch9/verify_batch9.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch9  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch9.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch9.PART)

if __name__ == "__main__":
    V.main(sys.argv[1:])
