"""Check corpus.d/90-batch4.json against today's text on the source pages (the check of phase2/verify_phase2.py, with
batch 3's page repairs, which parse_batch4 imports).

Usage: python -X utf8 batch4/verify_batch4.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "phase2"))
sys.path.insert(0, HERE)
import parse_batch4  # noqa: E402,F401  (its page repairs apply to the check too)
import verify_phase2 as V  # noqa: E402

V.ACTS = (("codigo-nacional-de-seguridad-y-convivencia-ciudadana", "ley_1801_2016"),
          ("sistema-de-seguridad-social-integral", "ley_0100_1993"),
          ("codigo-general-disciplinario", "ley_1952_2019"),
          ("codigo-electoral", "decreto_2241_1986"))
V.P.OUT = os.path.join(os.path.dirname(HERE), "corpus.d", "90-batch4.json")

if __name__ == "__main__":
    V.main(sys.argv[1:])
