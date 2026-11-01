"""Articles that take effect after the rest of their act (a vigencia clause with a later day for some articles).

late_start(act, nums, day, law, page, P, E, B23): the units of articles `nums` are absent from every version before `day`
and added on `day` (a version is inserted if the act has none that day), credited to `law`. A ruling (a law of kind 'court')
that changed such a unit before that day is folded into the day: the unit arrives with the ruling's words, credited to
`law` and the ruling (listed in FOLDED); so are changes by the laws in `fold` (corrections of
the act's text published before that day). Stops on any other change before that day, or if the unit is missing from the
page or from a version before it.
"""
from __future__ import annotations

FOLDED: list[str] = []


def late_start(act: dict, nums: list[str], day: str, law: str, page: str, P, E, B23, fold: tuple = ()) -> None:
    have = {E.label_num(u["label"] or "") for u in P.doc_units(page)[1:]}
    B23._need(set(nums) <= have, f"{page}: late articles not on the page {sorted(set(nums) - have)}")
    vs = act["versions"]
    if not any(v["from"] == day for v in vs):
        k = next((i for i, v in enumerate(vs) if v["from"] > day), len(vs))
        prev = next(v for v in reversed(vs[:k]) if "units" in v)
        vs.insert(k, {"from": day, "units": dict(prev["units"]), "credits": {}, "source_url": prev["source_url"],
                      "sha256": prev["sha256"]})
    dv = next(v for v in vs if v["from"] == day)
    if "units" not in dv:  # a version that changed no words: give it the full units it stands for
        dv["units"] = dict(next(w for w in reversed(vs[:vs.index(dv)]) if "units" in w)["units"])
    for num in nums:
        key = E.unit_key(num)[0]
        early = []
        for v in vs:
            if v["from"] <= day:
                for c in v["credits"].get(key) or []:
                    B23._need(E.LAWS[c]["kind"] == "court" or c in fold, f"{page} {key}: change by {c} before {day}")
                    early.append(c)
        for v in vs:
            if v["from"] < day:
                v["credits"].pop(key, None)
                if "units" in v:
                    B23._need(key in v["units"] or early, f"{page} {key}: missing on {v['from']}")
                    v["units"] = {k: x for k, x in v["units"].items() if k != key}
            elif v["from"] == day:
                if key in v["units"]:
                    v["credits"][key] = [law] + sorted(set(early) - {law})
                else:  # a ruling took the whole article out before it took effect: it never appears
                    v["credits"].pop(key, None)
        if early:
            FOLDED.append(f"{page} {key}: {', '.join(E.LAWS[c]['label'] for c in sorted(set(early)))}")
    # versions before that day left with no change at all (only folded rulings were in them) are dropped
    first = vs[0]["from"]
    keep, state = [], None
    for v in vs:
        if first < v["from"] < day and not v["credits"] and ("units" not in v or v["units"] == state):
            continue
        keep.append(v)
        state = v.get("units", state)
    vs[:] = keep
