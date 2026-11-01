"""Paragraphs inside a unit that start like an article or a heading (unanchored units). Usage: scan.py <page>..."""
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.environ.get("DRVDIR", "batch50")))
import importlib; B = importlib.import_module(os.environ.get("DRV", "parse_batch50"))
for pg in sys.argv[1:]:
    for u in B._units_qa(pg):
        ps = [B.E.tidy(B.E.plain(it[1])) for it in u["items"] if it[0] == "p"]
        for i, p in enumerate(ps):
            if re.match(r"(ART[ÍI]CULO|ARTICULO)\s+\d+|(T[ÍI]TULO|CAP[ÍI]TULO|SECCI[ÓO]N|LIBRO|PARTE)\s+[IVXL\d]+\.?\s*$", p) and (i or u["name"].startswith("N")):
                print(pg, u["name"], i, p[:100])
