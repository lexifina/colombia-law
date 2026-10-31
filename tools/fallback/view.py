"""Show one audited unit: events, acts named in its notes and markers, earlier-text headings, and the word diff.
Usage: python -X utf8 fallback/view.py <tag> <unit substring> [--notes]"""
import difflib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit as A
rows = json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))
tag, sub = sys.argv[1], sys.argv[2]
for r in rows:
    if r["tag"] != tag or sub not in r["unit"] or "records" not in r:
        continue
    print("#####", r["tag"], r["unit"], r["class"])
    x0 = r["records"][0]
    print(" label:", x0.get("label"))
    print(" named:", x0.get("named"))
    print(" LA heads:", x0.get("la_heads"))
    print(" marks:", [m[:140] for m in x0.get("marks", [])])
    if "--notes" in sys.argv or "--full" in sys.argv:
        for n in x0.get("nv", []):
            print("  NV:", n[:300])
        for n in x0.get("jv", []):
            print("  JV:", n[:300])
    if "--full" in sys.argv:
        for b in x0.get("la", []):
            print("  LA:", b["head"], b["state"], "|", " / ".join(b["lines"])[:600])
        for post, pre, marks in x0.get("paras", []):
            print("  P:", marks, "|", pre[:300], "" if pre == post else " [STRUCK words; without them: " + post[:200] + "]")
    print(" states:", [(d, l, s if isinstance(s, str) else (len(s) if s else s)) for d, s, l in x0.get("states", [])])
    for x in r["records"]:
        k, t = A.body(x["known_last"]), A.body(x["today"])
        print(" -- chain events", x["events"], "pre:", [s if isinstance(s, str) else (len(s) if s else s) for s in x["pre"]])
        if k == t:
            print("    same body"); continue
        kw, tw = " | ".join(k).split(" "), " | ".join(t).split(" ")
        for op, a, b, c, d in difflib.SequenceMatcher(None, kw, tw, autojunk=False).get_opcodes():
            if op != "equal":
                print(f"    {op}: -[{' '.join(kw[a:b])[:200]}] +[{' '.join(tw[c:d])[:200]}]")
