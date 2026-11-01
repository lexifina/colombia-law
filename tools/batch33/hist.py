"""Print one unit's history in a part: python -X utf8 batch33/hist.py <part.json> <act slug> <unit key> [chars]"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
n = int(sys.argv[4]) if len(sys.argv) > 4 else 300
a = next(a for a in d["acts"] if a["slug"] == sys.argv[2])
state = {}
for v in a["versions"]:
    if "units" in v:
        new = dict(v["units"])
    else:
        new = dict(state)
        for k, u in (v.get("changes") or {}).items():
            if u is None: new.pop(k, None)
            else: new[k] = u
    k = sys.argv[3]
    if new.get(k) != state.get(k):
        t = (new.get(k) or {}).get("text")
        print(v["from"], v["credits"].get(k), "|", None if t is None else t.replace("\n", " / ")[:n])
    state = new
