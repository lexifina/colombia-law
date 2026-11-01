"""List units whose notes name Decreto 1122 de 1999 or Decreto 266 de 2000 (both struck whole), with their notes' acts and
their earlier-text box headings. Usage: python -X utf8 batch36/survey_struck.py <page> ..."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.dirname(HERE)
for d in ("batch36", "batch35", "batch34", "batch33", "batch32", "batch31", "batch30", "batch29", "batch27", "batch26", "batch25",
          "batch24", "batch23", "batch22", "batch21", "batch20", "batch19", "batch18", "batch17", "batch16", "batch15",
          "batch14", "batch13", "batch12", "batch11", "batch10", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3",
          "phase2"):
    sys.path.insert(0, os.path.join(C, d))
import parse_batch36 as B
E, P = B.E, B.P
ACT = re.compile(r"(?:Ley|Decreto(?: Ley| Legislativo)?|Decreto-[Ll]ey) (\d+) de (\d{4})")
for page in sys.argv[1:]:
    for u in P.doc_units(page)[1:]:
        nv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas de Vigencia")
        if not re.search(r"Decreto 1122 de 1999|Decreto 266 de 2000", nv):
            continue
        acts = sorted(set(ACT.findall(nv)))
        heads = [E.plain(it[2])[:70] for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior"]
        print(page, E.label_num(u["label"] or ""), acts, "|", heads)
