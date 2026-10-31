"""Print the word-level differences between the engine's latest earlier text and today's for audited units.
Usage: python -X utf8 fallback/show.py <tag>[,<tag>...] [unit substring]"""
import difflib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit as A
rows = json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))
tags = sys.argv[1].split(",")
sub = sys.argv[2] if len(sys.argv) > 2 else ""
for r in rows:
    if r["tag"] not in tags or sub not in r["unit"] or "records" not in r:
        continue
    for x in r["records"]:
        k, t = A.body(x["known_last"]), A.body(x["today"])
        if k == t:
            continue
        kw, tw = " | ".join(k).split(" "), " | ".join(t).split(" ")
        ops = [(op, " ".join(kw[a:b]), " ".join(tw[c:d])) for op, a, b, c, d in
               difflib.SequenceMatcher(None, kw, tw, autojunk=False).get_opcodes() if op != "equal"]
        print(f"## {r['tag']} {r['unit']} ev={[(d, l) for d, l in x['events']]} known={len(k)}l today={len(t)}l")
        for op, a, b in ops[:6]:
            print(f"   {op}: -[{a[:160]}] +[{b[:160]}]")
        if len(ops) > 6:
            print(f"   ... {len(ops)} ops")
