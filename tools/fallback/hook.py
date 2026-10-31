"""Run one Colombia parser with the engine's chain() observed, for the fallback audit.

Where the earlier text the source gives for the last named act differs from today's text, the engine uses today's text
from that act's day ('latest earlier text differs ... today's text used from ...'). This records, for every such case,
the unit, the dated events, every resolved state and both texts, so fallback/audit.py can compare them.

Usage:  python -X utf8 fallback/hook.py <engine dir> <record.json> <parser.py> [parser args ...]
Writes only <record.json> (and whatever the parser writes to the --out-dir/--out it is given).
"""
from __future__ import annotations

import json
import os
import runpy
import sys

engine_dir, record, parser = sys.argv[1:4]
sys.argv = [parser] + sys.argv[4:]
sys.path.insert(0, os.path.abspath(engine_dir))
import engine as E  # noqa: E402

_chain = E.chain
REC: list[dict] = []


def _state(v):
    return "UNKNOWN" if v is E.UNKNOWN else v


def chain(events, known, base_known, last, struck, added):
    evs = sorted({e for e in events if e[0] and e[0] != "9999"}, key=lambda e: (e[0], e[1]))
    n = len(evs)
    st = [E.UNKNOWN] * (n + 1)
    st[0] = base_known
    for i, (d, law) in enumerate(evs):
        if law in known:
            st[i + 1] = known[law]
        if f"before:{law}" in known and st[i] is E.UNKNOWN:
            st[i] = known[f"before:{law}"]
    out = _chain(events, known, base_known, last, struck, added)
    if st[n] is not E.UNKNOWN and n and last is not E.UNKNOWN and (st[n] or None) != (last or None):
        REC.append({"unit": E.CUR_UNIT[0], "events": evs, "known_last": _state(st[n]), "today": _state(last),
                    "pre": [_state(s) for s in st], "out": [(d, _state(s), law) for d, s, law in out],
                    "laws": {law: E.LAWS.get(law, {}).get("label") for _, law in evs}})
    return out


_history = E.article_history


def article_history(u, *a, **k):
    n0 = len(REC)
    h = _history(u, *a, **k)
    if len(REC) > n0:
        items = u["items"]
        nv_all, jv_all = [], []
        for it in items:
            if it[0] == "box" and it[1] == "Notas de Vigencia":
                nv_all += [E.norm_refs(E.plain(ph)) for ph in E.box_paras(it[2])]
            if it[0] == "box" and it[1] == "Jurisprudencia Vigencia":
                jv_all += [E.plain(ph) for ph in E.box_paras(it[2])]
        la = [b["head"] for it in items if it[0] == "box" and it[1] in ("Legislación Anterior", "Redacción Anterior")
              for b in E.la_blocks(it[2])]
        marks = [m for it in items if it[0] == "p" for m in E.markers(it[1])]
        named = []
        for t in nv_all + marks:
            for g in E.AL_RE.findall(t):
                try:
                    key = E.al_key(*g)
                except Exception:  # noqa: BLE001
                    continue
                named.append((key, E.law_day(key) if key in E.LAWS else None))
        states = [(d, _state(s), law) for d, s, law in h["states"]]
        _, jv = E.parse_notes(items)
        rulings = [{"id": r["id"], "date": r["date"], "dec": r["dec"], "al": r["al"], "text": r["text"][:300]} for r in jv]
        paras = [(E.tidy(E.to_text(it[1], False)), E.tidy(E.to_text(it[1])), E.markers(it[1]))
                 for it in items if it[0] == "p"]
        la_full = [{"head": b["head"], "state": list(b["state"]) if b["state"] else None,
                    "lines": E.block_text(b["paras"], False)}
                   for it in items if it[0] == "box" and it[1] in ("Legislación Anterior", "Redacción Anterior")
                   for b in E.la_blocks(it[2])]
        for r in REC[n0:]:
            r.update({"nv": nv_all, "la_heads": la, "marks": marks, "named": sorted(set(named), key=str),
                      "states": states, "label": u["label"], "rulings": rulings, "paras": paras, "la": la_full,
                      "jv": jv_all})
    return h


E.article_history = article_history
E.chain = chain
try:
    runpy.run_path(parser, run_name="__main__")
finally:
    with open(record + ".tmp", "w", encoding="utf-8", newline="\n") as f:
        json.dump(REC, f, ensure_ascii=False, indent=1)
    os.replace(record + ".tmp", record)
