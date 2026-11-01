"""List placeholder-holding units per version in a part: python -X utf8 batch46/ph.py <part.json>"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phase2"))
import parse_phase2 as P2
c = json.load(open(sys.argv[1], encoding="utf-8"))
for a in c["acts"]:
    seen = {}
    for v in P2.full_versions(a["versions"]):
        for k, u in v["units"].items():
            if "[La fuente no da" in u["text"]:
                seen.setdefault(k, []).append(v["from"])
    print(a["slug"], len(seen), "units with placeholders;", sum(1 for k in seen if seen[k][0] == a["versions"][0]["from"]), "in the first version")
    for k, d in sorted(seen.items()):
        print("  ", k, d[0], "..", d[-1], len(d))
