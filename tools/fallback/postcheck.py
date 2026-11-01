"""After apply.py: for every fix, no version from the last named act's day D up to the day of the change holds today's
words T (unless the earlier text holds them too), and the version on that day does. Usage: postcheck.py [corpus.d]"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import apply as AP  # noqa: E402

folder = sys.argv[1] if len(sys.argv) > 1 else os.path.join(AP.COUNTRY, "corpus.d")
rows = {(r["tag"], r["unit"]): r for r in json.load(open(os.path.join(AP.TMP, "audit.json"), encoding="utf-8"))}
census = {(o["tag"], o["unit"], o["rec"]): o for o in json.load(open(os.path.join(AP.TMP, "census.json"), encoding="utf-8"))}
fixes = {}
for o in json.load(open(os.path.join(AP.TMP, "proposals.json"), encoding="utf-8")):
    for p in o.get("parts", []):
        if p["verdict"] == "fix":
            fixes[(o["tag"], o["unit"], p["rec"])] = {"end": p["end"]}
for f in sorted(glob.glob(os.path.join(HERE, "manual*.json"))):
    for m in json.load(open(f, encoding="utf-8")):
        fixes[(m["tag"], m["unit"], m.get("rec", 0))] = m
parts = {}
bad = ok = 0
for (tag, unit, rec), f in sorted(fixes.items()):
    if f.get("verdict", "fix") != "fix" or census[(tag, unit, rec)]["effect"] != "effective" or \
            census[(tag, unit, rec)]["kind"] in ("punct", "typo") and not f.get("why"):
        continue
    if tag not in parts:
        parts[tag] = json.load(open(glob.glob(os.path.join(folder, tag + "-*.json"))[0], encoding="utf-8"))
    page, key = unit.split(" ", 1)
    a = next(a for a in parts[tag]["acts"] if a["url"].rsplit("/", 1)[-1].rsplit(".", 1)[0] == page)
    x = rows[(tag, unit)]["records"][rec]
    T, K = x["today"] or [], x["known_last"] or []
    dn, end = x["events"][-1][0], f["end"]
    occ = int(f.get("occurrence", 0))
    starts = f.get("start", "known")
    k_has_t = T and AP.find_run(K, T) is not None
    for v, st in zip(a["versions"], AP.states(a["versions"])):
        if dn <= v["from"] < end and T and not k_has_t and not isinstance(starts, (list, dict)) and not f.get("mid"):
            bl = AP.body_lines(st.get(key))
            n = sum(1 for i in range(len(bl)) if AP.find_run(bl[i:], T) == 0)
            base = sum(1 for i in range(len(AP.body_lines(AP.states(a["versions"])[-1].get(key)))) if False)
            if n > occ:
                bad += 1
                print("STILL", tag, unit, rec, v["from"])
                break
    else:
        ok += 1
print(ok, "fixes checked,", bad, "with today's words still before the change")
