"""Anachronism audit beyond credits: for each unit, list versions before the unit's last change that already hold
today's words (today's text T, or any of its lines longer than 40 characters that no earlier-text of the unit held at
the start). A revert (a ruling restoring words) shows up too and is reviewed by hand.
Usage: python -X utf8 batch33/early_today.py <part.json> ..."""
import json, sys


def states(vs):
    st = {}
    for v in vs:
        if "units" in v:
            st = dict(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = u
        yield v, st


bad = 0
for p in sys.argv[1:]:
    for a in json.load(open(p, encoding="utf-8"))["acts"]:
        hist = {}
        for v, st in states(a["versions"]):
            for k in set(st) | set(hist):
                t = st.get(k, {}).get("text") if k in st else None
                h = hist.setdefault(k, [])
                if not h or h[-1][1] != t:
                    h.append((v["from"], t, v["credits"].get(k)))
        for k, h in hist.items():
            if len(h) < 2 or h[-1][1] is None:
                continue
            T = h[-1][1]
            first = set(l for l in (h[0][1] or "").split("\n"))
            tl = [l for l in T.split("\n")[1:] if len(l) > 40 and l not in first]
            for d, t, c in h[1:-1]:
                if t is None:
                    continue
                if t == T or any(l in t.split("\n") for l in tl):
                    # words of today's text that the first text lacked, in a version before the last change
                    late = [l for l in tl if l in t.split("\n")]
                    # fine when the change that brought them is before this version and no later change credits them
                    print(f"{a['slug']} {k} {d} {c}: holds {'today' if t == T else len(late)} new line(s) of today's "
                          f"text before its last change ({h[-1][0]} {h[-1][2]})")
                    bad += 1
print("FLAGS", bad)
