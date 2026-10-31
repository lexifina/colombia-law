"""Compare re-parsed parts in fallback/.tmp/<tag>/ with the published corpus.d parts: per act, version days and the full
state of every version (units by key). Usage: python -X utf8 fallback/cmp_parts.py"""
import glob, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)


def states(vs):
    cur, out = {}, []
    for v in vs:
        if "units" in v:
            cur = dict(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append((v["from"], {k: u["text"] for k, u in cur.items()}, v.get("credits", {})))
    return out


for pub in sorted(glob.glob(os.path.join(COUNTRY, "corpus.d", "*.json"))):
    name = os.path.basename(pub)
    tag = name.split("-")[0]
    new = glob.glob(os.path.join(HERE, ".tmp", tag, name))
    if not new:
        continue
    a = {x["slug"]: x for x in json.load(open(pub, encoding="utf-8"))["acts"]}
    b = {x["slug"]: x for x in json.load(open(new[0], encoding="utf-8"))["acts"]}
    for slug in a:
        if slug not in b:
            print(tag, slug, "MISSING in re-parse"); continue
        sa, sb = states(a[slug]["versions"]), states(b[slug]["versions"])
        da, db = [d for d, _, _ in sa], [d for d, _, _ in sb]
        diff_units = set()
        ma, mb = dict((d, s) for d, s, _ in sa), dict((d, s) for d, s, _ in sb)
        for d in set(da) & set(db):
            for k in set(ma[d]) | set(mb[d]):
                if ma[d].get(k) != mb[d].get(k):
                    diff_units.add(k)
        print(tag, slug, "days", "same" if da == db else f"pub {len(da)} new {len(db)} only-pub {sorted(set(da)-set(db))[:4]} only-new {sorted(set(db)-set(da))[:4]}",
              "| units differing:", len(diff_units), sorted(diff_units)[:6])
