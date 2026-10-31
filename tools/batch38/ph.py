"""Units holding the placeholder line, per version (with the version's credit). Usage: ph.py part.json [slug]"""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
for a in d["acts"]:
    if len(sys.argv) > 2 and a["slug"] != sys.argv[2]:
        continue
    st = {}
    seen = {}
    for v in a["versions"]:
        if "units" in v:
            st = dict(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None: st.pop(k, None)
            else: st[k] = u
        for k, u in st.items():
            ph = "[La fuente no da el texto vigente en esta fecha.]" in u["text"]
            if ph != seen.get(k, False):
                print(a["slug"], k, v["from"], "placeholder" if ph else "text", v["credits"].get(k))
                seen[k] = ph
