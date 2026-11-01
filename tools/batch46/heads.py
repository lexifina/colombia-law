"""List, for the units whose notes name Decreto 1122 de 1999 or Decreto 266 de 2000, the earlier-text box headings, the
note lines and the ruling lines. Usage: python -X utf8 batch46/heads.py <page>..."""
import os, re, sys
C = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.argv, pages = sys.argv[:1] + ["x", "x"], sys.argv[1:]
exec(open(os.path.join(C, "batch45", "show.py"), encoding="utf-8").read().split("page, name")[0])
HEAD = re.compile(r"Texto (?:(?!Texto ).){0,160}?:")
for page in pages:
    for u in P.doc_units(page)[1:]:
        nv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas de Vigencia")
        if not re.search(r"Decreto 1122 de 1999|Decreto 266 de 2000", nv):
            continue
        print("==", page, E.label_num(u["label"] or ""))
        p0 = next((E.plain(it[1]) for it in u["items"] if it[0] == "p"), "")
        print("  P0:", p0[:160])
        print("  NV:", nv[:900])
        for it in u["items"]:
            if it[0] == "box" and it[1] == "Legislación Anterior":
                t = E.plain(it[2])
                print("  LA:", [m.group(0) for m in HEAD.finditer(t)])
