"""A term that runs out on a stated day (a law's own words: 'tendrán una vigencia de cuatro (4) años, a partir de su
promulgación'): one version on the day after the term, taking out the provisions under it and the headings of
titulos.md left with no provision, credited to the law that set the term. Shared by batch65/parse_batch65.py (Ley 2272
de 2022) and fix_ley418_term.py (Ley 418 de 1997 in 99l-batch20).

heading_scope(order, kept_names): order = the page's units in order as (name, label, is_article); kept_names = article
units still in force after the lapse. A heading stays while some kept article lies between it and the next heading of
its level or above (TÍTULO 1, CAPÍTULO 2, other 3)."""
from __future__ import annotations

import re


def level(label: str) -> int:
    t = label.strip().upper()
    if t.startswith(("PARTE", "PRIMERA PARTE", "SEGUNDA PARTE", "LIBRO")):
        return 0
    if t.startswith(("TÍTULO", "TITULO")):
        return 1
    if t.startswith(("CAPÍTULO", "CAPITULO")):
        return 2
    return 3


def heading_keep(order, kept_names, before_names=None) -> list[bool]:
    """For each heading in order (in page order), whether it keeps an article under it. With before_names (the articles
    in force without the lapse), a heading that had none of those either is kept as it was: only headings the lapse
    empties leave."""
    heads = [i for i, (_, _, art) in enumerate(order) if not art]
    out = []
    for i in heads:
        lv = level(order[i][1])
        j = next((k for k in heads if k > i and level(order[k][1]) <= lv), len(order))
        has = any(order[k][2] and order[k][0] in kept_names for k in range(i + 1, j))
        had = before_names is None or any(order[k][2] and order[k][0] in before_names for k in range(i + 1, j))
        out.append(has or not had)
    return out


def titulos_after(text: str, order, kept_names, before_names=None) -> str:
    """titulos.md lines bound in order to the page's headings (a page heading with no line is skipped); lines whose
    heading keeps no article leave. Every line must bind."""
    lines = [l for l in text.split("\n") if l]
    keep = heading_keep(order, kept_names, before_names)
    labels = [order[i][1].strip() for i, (_, _, art) in enumerate(order) if not art]
    out, k = [], 0
    for lab, kp in zip(labels, keep):
        if k < len(lines) and (lines[k] == "### " + lab or lines[k].startswith("### " + lab + " ")):
            if kp:
                out.append(lines[k])
            k += 1
    if k != len(lines):
        raise SystemExit(f"titulos: {len(lines) - k} lines not bound to a page heading (first: {lines[k]!r})")
    return "\n".join(out) + "\n"


def state_of(versions) -> dict:
    st: dict = {}
    for v in versions:
        if "units" in v:
            st = dict(v["units"])
        for k, x in (v.get("changes") or {}).items():
            if x is None:
                st.pop(k, None)
            else:
                st[k] = x
    return st


def apply_lapses(versions, events, order, key_of, dropped=None):
    """Insert one version per event (day, unit keys out, law, note) into a delta chain (SCHEMA 'Large acts': units in
    the first version, changes after), and keep titulos.md without the headings the lapses empty (only those) in every
    version from the first event on. No existing version may fall on an event's day, and no later version may touch a
    unit an event takes out. dropped (a list) receives the days of versions whose titulos change the pruning cancels.
    Returns the new chain."""
    days = {d for d, *_ in events}
    if any(v["from"] in days for v in versions):
        raise SystemExit("a version already on a lapse day")
    out_day = {k: d for d, ks, _, _ in events for k in ks}
    first = min(days)
    for v in versions:
        touched = set(v.get("changes") or {}) | set(v.get("units") or {}) | set(v["credits"])
        late = [k for k in touched if k in out_day and v["from"] > out_day[k]]
        if late:
            raise SystemExit(f"version {v['from']} touches {late}, out earlier")
    chain = list(versions)
    for d, ks, law, note in sorted(events):
        i = next((n for n, v in enumerate(chain) if v["from"] > d), len(chain))
        prev = chain[i - 1]
        chain.insert(i, {"from": d, "changes": {k: None for k in sorted(ks)}, "credits": {k: [law] for k in sorted(ks)},
                         "source_url": prev["source_url"], "sha256": prev["sha256"], "note": note, "_lapse": law})
    names = {key_of(n): n for n, _, art in order if art}
    eng, out_keys, prev_tit = {}, set(), None
    for v in chain:
        lapse = v.get("_lapse")
        if "units" in v:
            eng = dict(v["units"])
        if lapse:
            out_keys |= set(v["changes"])
        else:
            for k, x in (v.get("changes") or {}).items():
                if x is None:
                    eng.pop(k, None)
                else:
                    eng[k] = x
        if "titulos" not in eng:
            continue
        if out_keys:
            before = {names[k] for k in eng if k in names}
            kept = {names[k] for k in eng if k in names and k not in out_keys}
            tit = titulos_after(eng["titulos"]["text"], order, kept, before)
        else:
            tit = eng["titulos"]["text"]
        if prev_tit is not None and v["from"] >= first:
            had = "titulos" in (v.get("changes") or {})
            if tit != prev_tit:
                v.setdefault("changes", {})["titulos"] = dict(eng["titulos"], text=tit)
                if lapse:
                    v["credits"]["titulos"] = [lapse]
                elif "titulos" not in v["credits"]:
                    raise SystemExit(f"{v['from']}: titulos change with no credit")
            elif had:
                v["changes"].pop("titulos")
                if v["credits"].pop("titulos", None) is not None and dropped is not None:
                    dropped.append(v["from"])
                if not v["credits"] and not v["changes"]:
                    raise SystemExit(f"{v['from']}: version left with nothing")
            if tit != prev_tit or had:
                v["changes"] = dict(sorted(v["changes"].items()))
                v["credits"] = dict(sorted(v["credits"].items()))
        prev_tit = tit
    for v in chain:
        v.pop("_lapse", None)
    return chain
