"""Check corpus.d/95-batch5.json against today's text on the source pages (batch4/verify_batch4.py's check, with this
batch's page repairs, which parse_batch5 applies on import).

Usage: python -X utf8 batch5/verify_batch5.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(COUNTRY, "batch4"))
sys.path.insert(0, os.path.join(COUNTRY, "phase2"))
import parse_batch5  # noqa: E402,F401  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402

V = V4.V
V.ACTS = (("estatuto-tributario", "estatuto_tributario"),
          ("estatuto-general-de-contratacion", "ley_0080_1993"),
          ("estatuto-del-consumidor", "ley_1480_2011"),
          ("codigo-nacional-de-transito", "ley_0769_2002"))
V.P.OUT = os.path.join(COUNTRY, "corpus.d", "95-batch5.json")

# Words under an anchor with no heading of its own (phase2/stray.py) are read as part of the article before them, as the
# part holds them after ../fix_stray_headings.py (Ley 769 de 2002, art. 52's last paragraph).
import stray  # noqa: E402
_units = V.P.doc_units
V.P.doc_units = lambda name: stray.repair(name, _units(name), V.E)

if __name__ == "__main__":
    V.main(sys.argv[1:])
