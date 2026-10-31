"""Date Ley 716 de 2001 from its publication (29 December 2001, its art. 21: 'La presente ley rige a partir de la fecha
de su publicación'), and rebuild the four Estatuto Tributario articles it changed, in corpus.d/95-batch5.json, without
re-parsing the part.

The part dated Ley 716 de 2001 on 2003-12-29, after Sentencia C-886 de 2002 (22 October 2002) had struck the four
articles of it that changed the Estatuto (arts. 14, 15, 16 and 20), so its additions appeared after their own strike and
stayed in force. The page's notes name Ley 716 de 2001 (not Ley 863 de 2003) for each:
  art. 147   parágrafo 2o added by Ley 716 art. 20; struck by C-886-02;
  art. 505   parágrafo transitorio added by Ley 716 art. 14; struck by C-886-02;
  art. 555-1 incisos 2 to 5 and parágrafo added by Ley 716 art. 16; struck by C-886-02; then rewritten by Ley 788 de 2002
             art. 79 (2002-12-27), inciso 4 repealed by Ley 863 de 2003 art. 69 (2003-12-29);
  art. 618-1 parágrafo added by Ley 716 art. 15; struck by C-886-02.
The articles' histories up to their next change are taken from the engine's reading of the cached page with Ley 716's
day corrected (batch4/parse_batch4.py's HAND_RULES now carries it), and set by hand where that reading cannot see the
ruling's effect: art. 147 loses only its parágrafo 2o on 2002-10-22; art. 555-1 returns to its 1990 text on 2002-10-22,
takes Ley 788's text (as the part has it) on 2002-12-27 and loses inciso 4 on 2003-12-29; art. 505 reads, before Ley 716
and after the ruling, Ley 223 de 1995's text that the page's earlier-text box gives with the parágrafo. Idempotent.

Usage:  python -X utf8 fix_ley716.py [corpus.d folder]
"""
from __future__ import annotations

import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "batch5"))
for _d in ("batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(HERE, _d))

PART, SLUG, LAW = "95-batch5.json", "estatuto-tributario", "ley-716-2001"
NEW, OLD = "2001-12-29", "2003-12-29"
DECISION = ("Ley 716 de 2001 is dated 2001-12-29 from its art. 21 ('La presente ley rige a partir de la fecha de su "
            "publicación', Diario Oficial No. 44.661 of 29 December 2001); the four Estatuto Tributario articles it changed "
            "(arts. 147, 505, 555-1, 618-1; its arts. 20, 14, 16, 15) hold its words from that day until Sentencia C-886 "
            "de 2002 (22 October 2002) struck them; art. 555-1 then reads its 1990 text until Ley 788 de 2002, and Ley 863 "
            "de 2003 repealed its inciso 4 (fix_ley716.py).")


def states(vs):
    cur, out = {}, []
    for v in vs:
        if "units" in v:
            cur = copy.deepcopy(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append(dict(cur))
    return out


def at(vs, sts, day, key):
    i = max(j for j, v in enumerate(vs) if v["from"] <= day)
    return sts[i].get(key)


def drop_line(u, start):
    lines = u["text"].split("\n")
    hit = [l for l in lines if l.startswith(start)]
    if len(hit) != 1:
        raise SystemExit(f"{u['label']}: line {start!r} found {len(hit)} times")
    return dict(u, text="\n".join(l for l in lines if not l.startswith(start)))


def main(argv):
    folder = argv[0] if argv else os.path.join(HERE, "corpus.d")
    path = os.path.join(folder, PART)
    part = json.load(open(path, encoding="utf-8"))
    if DECISION in part["decisions"]:
        print(PART, "already fixed")
        return
    import parse_batch5 as B5  # noqa: E402  (reads the cache only)
    E = B5.E
    if E.law_day(E.register(LAW)) != NEW:
        raise SystemExit(f"{LAW}: engine day {E.law_day(LAW)}")
    eng = B5.build_all(["estatuto-tributario"])[0]
    evs, ests = eng["versions"], states(eng["versions"])
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    vs = act["versions"]
    last_before = states(vs)[-1]
    psts = states(vs)
    pub = lambda d, k: at(vs, psts, d, k)  # noqa: E731
    eng_at = lambda d, k: at(evs, ests, d, k)  # noqa: E731
    C = "c-886-02"
    # timelines: key -> [(day, unit or None, credits)], applied from the first day up to `until` (exclusive)
    b147 = eng_at(NEW, "art-0147")
    b505 = eng_at(NEW, "art-0505")
    plans = {
        "art-0147": ("2006-12-27", [("1989-05-30", pub("1989-05-30", "art-0147"), None),
                                    (NEW, b147, [LAW]),
                                    ("2002-10-22", drop_line(b147, "PARÁGRAFO 2o."), [C]),
                                    ("2002-12-27", pub(OLD, "art-0147"), ["ley-788-2002"])]),
        "art-0505": ("2018-12-28", [("1989-05-30", pub("1989-05-30", "art-0505"), None),
                                    ("1995-12-22", drop_line(b505, "PARÁGRAFO TRANSITORIO."), ["ley-223-1995"]),
                                    (NEW, b505, [LAW]),
                                    ("2002-10-22", drop_line(b505, "PARÁGRAFO TRANSITORIO."), [C])]),
        "art-0555-01": ("2012-12-26", [("1991-02-28", pub("1991-02-28", "art-0555-01"), ["ley-49-1990"]),
                                       (NEW, eng_at(NEW, "art-0555-01"), [LAW]),
                                       ("2002-10-22", pub("1991-02-28", "art-0555-01"), [C]),
                                       ("2002-12-27", pub("2002-12-27", "art-0555-01"), ["ley-788-2002"]),
                                       (OLD, drop_line(pub("2002-12-27", "art-0555-01"), "Las personas no obligadas a "
                                                                                          "inscribirse"),
                                        ["ley-863-2003"])]),
        "art-0618-01": ("9999-12-31", [(v["from"], ests[j].get("art-0618-01"), v["credits"].get("art-0618-01"))
                                       for j, v in enumerate(evs) if "art-0618-01" in v["credits"] or j == 0]),
    }
    for k, (until, tl) in plans.items():
        for d, u, _ in tl:
            if u is not None and ("Texto" in u["text"].split("\n")[1][:6] or "&lt;" in u["text"]):
                raise SystemExit(f"{k} {d}: not article text")
        last_pub = [v for v in vs if v["from"] < until][-1]["from"]
        if until == "9999-12-31" and tl[-1][1] != last_before.get(k):
            raise SystemExit(f"{k}: today's text would change")
        for d in [d for d, _, _ in tl if d not in [v["from"] for v in vs]]:
            j = next((i for i, v in enumerate(vs) if v["from"] > d), len(vs))
            vs.insert(j, {"from": d, "credits": {}})
            psts.insert(j, dict(psts[j - 1]))
        for j, v in enumerate(vs):
            if not (tl[0][0] <= v["from"] < until):
                continue
            seg = [s for s in tl if s[0] <= v["from"]][-1]
            if seg[1] is None:
                psts[j].pop(k, None)
            else:
                psts[j][k] = seg[1]
            v["credits"].pop(k, None)
            if v["from"] == seg[0] and seg[2] and v is not vs[0]:
                v["credits"][k] = list(seg[2])
        _ = last_pub
    # titulos no longer credited to Ley 716 on the old day
    for v in vs:
        if v["from"] == OLD and LAW in v["credits"].get("titulos", []):
            v["credits"]["titulos"] = [l for l in v["credits"]["titulos"] if l != LAW] or v["credits"].pop("titulos")
            if not v["credits"].get("titulos"):
                v["credits"].pop("titulos", None)
    prev = None
    for j, (v, st) in enumerate(zip(vs, psts)):
        if j == 0:
            v["units"] = st
        else:
            ch = {k: u for k, u in st.items() if prev.get(k) != u}
            ch.update({k: None for k in prev if k not in st})
            if ch:
                v["changes"] = ch
            else:
                v.pop("changes", None)
            for k in list(v["credits"]):
                if k in plans and k not in ch:
                    v["credits"].pop(k)
        prev = st
    act["versions"] = [v for j, v in enumerate(vs) if j == 0 or v.get("changes") or v.get("credits")]
    if states(act["versions"])[-1] != last_before:
        raise SystemExit("today's text changed")
    for l in (LAW, C, "ley-788-2002", "ley-863-2003", "ley-223-1995", "ley-49-1990"):
        if l not in part["laws"]:
            raise SystemExit(f"law {l} missing")
    ds = part["decisions"]
    for i, d in enumerate(ds):
        if d.startswith(f"In force {OLD}: Ley 716 de 2001 ("):
            ds[i] = d.replace(f"In force {OLD}:", f"In force {NEW}:", 1)
    ds.append(DECISION)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)
    print(PART, "fixed")


if __name__ == "__main__":
    main(sys.argv[1:])
