"""The anachronism check of batch3/parse_batch3.py, over part files as written (laws merged across all parts): no
version credits an act before that act's own sanction or publication day, and no ruling is older than the act it
rules on. Usage: python -X utf8 fallback/anachro.py [corpus.d folder] [part ...]"""
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
folder = next((a for a in sys.argv[1:] if os.path.isdir(a)), os.path.join(os.path.dirname(HERE), "corpus.d"))
only = [a for a in sys.argv[1:] if not os.path.isdir(a)]
laws = {}
parts = sorted(p for p in glob.glob(os.path.join(folder, "*.json")))
for p in parts:
    for k, l in json.load(open(p, encoding="utf-8")).get("laws", {}).items():
        laws.setdefault(k, l)
total = 0
for p in parts:
    name = os.path.basename(p)
    if only and not any(name.startswith(o) for o in only):
        continue
    out = []
    for a in json.load(open(p, encoding="utf-8"))["acts"]:
        born = (laws.get(a["first_law"] or "") or {})
        born = born.get("enacted") or born.get("published")
        for v in a["versions"]:
            for k, ls in v.get("credits", {}).items():
                for l in ls:
                    law = laws.get(l, {})
                    ds = [d for d in (law.get("enacted"), law.get("published")) if d]
                    if ds and v["from"] < min(ds):
                        out.append(f"{a['slug']} {k}: {l} credited on {v['from']}, before {min(ds)}")
                    if law.get("kind") == "court" and born and law.get("enacted") and law["enacted"] < born:
                        out.append(f"{a['slug']} {k}: ruling {l} ({law['enacted']}) older than the act ({born})")
    total += len(out)
    print(name, len(out), "anachronisms", out[:5])
print("TOTAL", total)
