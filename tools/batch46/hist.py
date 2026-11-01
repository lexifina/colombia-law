"""Print a unit's history in a part: python -X utf8 batch46/hist.py <part.json> <slug> <key> [width]"""
import json, sys
c = json.load(open(sys.argv[1], encoding="utf-8"))
a = next(x for x in c["acts"] if x["slug"] == sys.argv[2])
w = int(sys.argv[4]) if len(sys.argv) > 4 else 160
state, units = None, {}
for v in a["versions"]:
    if "units" in v:
        units = v["units"]
    else:
        units = dict(units)
        for k, u in v.get("changes", {}).items():
            if u is None:
                units.pop(k, None)
            else:
                units[k] = u
    t = units.get(sys.argv[3])
    t = None if t is None else t["text"]
    cr = v["credits"].get(sys.argv[3])
    if t != state or cr:
        print(v["from"], cr, "|", (t or "<absent>").replace("\n", " / ")[:w])
        state = t
