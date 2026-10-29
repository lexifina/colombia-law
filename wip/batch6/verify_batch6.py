"""Check corpus.d/97-batch6.json against today's text on the source pages (batch4/verify_batch4.py's check, with this
batch's page repairs, which parse_batch6 applies on import).

Usage: python -X utf8 batch6/verify_batch6.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch6  # noqa: E402,F401  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402

V = V4.V
V.ACTS = (("estatuto-organico-del-sistema-financiero", "estatuto_organico_sistema_financiero"),
          ("codigo-de-minas", "ley_0685_2001"),
          ("codigo-procesal-del-trabajo", "codigo_procedimental_laboral"),
          ("regimen-de-insolvencia", "ley_1116_2006"),
          ("servicios-publicos-domiciliarios", "ley_0142_1994"))
V.P.OUT = os.path.join(COUNTRY, "corpus.d", "97-batch6.json")

if __name__ == "__main__":
    V.main(sys.argv[1:])
