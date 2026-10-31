"""One compact block per manual unit of a given kind signature. Usage: brief.py <kind> <ncands> <nrul> <nlater> [max] [tag]"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit as A, triage as T
p = json.load(open(os.path.join(A.TMP, "proposals.json"), encoding="utf-8"))
rows = {(r["tag"], r["unit"]): r for r in json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))}
kind, nc, nr, nl = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
mx = int(sys.argv[5]) if len(sys.argv) > 5 else 10
tg = sys.argv[6] if len(sys.argv) > 6 else None
n = 0
for o in p:
    if o["verdict"] != "manual" or (tg and o["tag"] != tg):
        continue
    for q in o.get("parts", []):
        if q["verdict"] != "manual" or q["kind"] != kind or len({c[0] for c in q["cands"]}) != nc or len(q["rulings"]) != nr or min(len(q["later"]), 3) != nl:
            continue
        x = rows[(o["tag"], o["unit"])]["records"][q["rec"]]
        n += 1
        if n > mx:
            break
        print(f"## {o['tag']} {o['unit']} ev={x['events']} LA={x['la_heads']}")
        print("   marks:", [m[:110] for m in x["marks"]][:5])
        print("   NV:", [v[:150] for v in x["nv"] if v.startswith("-")][:4])
        print("   later:", q["later"], "rul:", q["rulings"])
        ops = T.word_ops(A.body(x["known_last"]), A.body(x["today"]))
        for a, b in ops[:2]:
            print(f"   -[{a[:130]}] +[{b[:130]}]")
