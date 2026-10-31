"""Check corpus.d/98-batch7.json against today's text on the Secretaría del Senado's basedoc pages (batch4/verify_batch4.py's
check, with this batch's page repairs, which parse_batch7 applies on import).

Usage: python -X utf8 batch7/verify_batch7.py [part.json] [-v]
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
for _d in ("batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch7  # noqa: E402  (its page repairs apply to the check too)
import verify_batch4 as V4  # noqa: E402

V = V4.V
V.ACTS = tuple((slug, page) for slug, page, *_ in parse_batch7.ACTS)
V.P.OUT = os.path.join(COUNTRY, "corpus.d", parse_batch7.PART)
E = V.E
_units = V.P.doc_units
GONE = "&lt;Art&iacute;culo INEXEQUIBLE&gt;"


def doc_units(name):
    """Today's text where the page's marker says more than the check reads:
    - Ley 99 de 1993, art. 11: '<Artículo derogado, EXCEPTO el parágrafo 1o., por el artículo 20 del Decreto 1687 de
      1997 ...>' over the parágrafo 1, which is in force: the marker paragraph is left out, so the parágrafo is read.
    - Ley 99 de 1993, art. 61A: struck by Sentencia C-539 de 2023, its first words with an effect deferred to 2 October
      2024, before the retrieval day: not in force today.
    - Ley 789 de 2002, art. 30 (parse_batch7 takes its marker out): repealed by Ley 2466 de 2025, art. 21: not in force.
    - Ley 99 de 1993, art. 71: its parágrafo transitorio, struck by Sentencia C-539 de 2023 with an effect deferred to 2
      October 2024, is not in force.
    - Estatuto Anticorrupción: the 20 articles printed under "<Artículo derogado a partir del 29 de marzo de 2022 ...>"
      (parse_batch7 takes the marker out) are not in force."""
    units = _units(name)
    for u in units:
        ps = [it for it in u["items"] if it[0] == "p"]
        if name == parse_batch7.L99 and u["name"] == "11":
            if not (ps and "EXCEPTO el par&aacute;grafo 1o." in ps[0][1] and not E.plain(E.strip_markers(ps[0][1])).strip()):
                raise SystemExit("Ley 99 art. 11: marker changed")
            u["items"] = [it for it in u["items"] if it is not ps[0]]
        elif name == parse_batch7.L99 and u["name"] == "71":
            par = [it for it in ps if "PAR&Aacute;GRAFO TRANSITORIO." in it[1] and "efectos diferidos" in it[1]]
            if len(par) != 1:
                raise SystemExit("Ley 99 art. 71: parágrafo transitorio changed")
            u["items"] = [it for it in u["items"] if it is not par[0]]
        elif ((name == parse_batch7.L99 and u["name"] == "61A") or (name == parse_batch7.L789 and u["name"] == "30")
              or (name == parse_batch7.EAC and u["name"] in parse_batch7.DEROG_2022_UNITS)):
            u["items"] = [("p", GONE)]
    return units


V.P.doc_units = doc_units

if __name__ == "__main__":
    V.main(sys.argv[1:])
