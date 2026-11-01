"""Conditional-ruling notes that are false: the engine's note on a ruling that also changed words.

The engine (phase2/engine.py, codes/parse_codes.py, cst/engine.py) gives every ruling it reads as 'conditional'
(exequibilidad condicionada) the law note COND, which the builder prints on every commit of that law instead of its
standard line. A ruling the source also shows striking or replacing words changes words in some version credited to it,
so the note is false there. resolve() takes the note off such a law and returns one decision line naming the provisions
where the ruling changed no words (the fact the note stood for now lives only there; none when there is no such
provision). A version whose credits name another law besides the ruling (an act's first day with rulings folded into
it) does not show that the ruling changed words.

Used by phase2/parse_phase2.write_part (every part written through it, so new parts never carry the false note) and by
fix_conditional_notes.py (the installed parts, in place; laws shared by several parts are judged across all of them).
"""
from __future__ import annotations

COND = ("A Constitutional Court ruling that upheld this text on a condition of interpretation (exequibilidad "
        "condicionada). It did not change the words.")
MARK = "Conditional ruling notes (2026-11-01)"


def events(acts: list[dict], key: str) -> list[tuple]:
    """(act short, day, unit key, unit label, words changed, credited to the ruling alone) for every unit credited to
    `key`. Versions may give full `units` or `changes` (deltas) against the version before."""
    out = []
    for a in acts:
        st: dict = {}
        for v in a["versions"]:
            prev = st
            if "units" in v:
                st = dict(v["units"])
            elif "changes" in v:
                st = dict(st)
                for k, u in v["changes"].items():
                    if u is None:
                        st.pop(k, None)
                    else:
                        st[k] = u
            for k, c in v["credits"].items():
                if key in c:
                    old, new = prev.get(k), st.get(k)
                    label = (new or old or {}).get("label", k)
                    out.append((a["short"], v["from"], k, label, (old or {}).get("text") != (new or {}).get("text"),
                                list(c) == [key]))
    return out


def changes_words(evs: list[tuple]) -> bool:
    return any(e[4] and e[5] for e in evs)


def sentence(label: str, evs: list[tuple]) -> str | None:
    """The decision line for one part: the provisions credited to the ruling where it changed no words."""
    byday: dict = {}
    for short, day, _, ulabel, changed, _ in evs:
        if not changed:
            byday.setdefault((day, short), [])
            if ulabel not in byday[(day, short)]:
                byday[(day, short)].append(ulabel)
    if not byday:
        return None
    what = "; ".join(f"{short} {', '.join(ls)} on {day}" for (day, short), ls in sorted(byday.items()))
    return (f"{MARK}: {label} upheld these provisions on a condition of interpretation (exequibilidad condicionada) and "
            f"changed no words of them: {what}. The same ruling also struck or replaced words in this record, so its law "
            f"entry carries no note.")


def resolve(laws: dict, acts: list[dict], others: dict | None = None) -> list[str]:
    """Take COND off each law in `laws` (mutated) whose credited units change words, in `acts` or in `others`
    ({law key: events elsewhere}); return the decision lines for this part, in law-key order."""
    lines = []
    for key in sorted(laws):
        law = laws[key]
        if law.get("note") != COND:
            continue
        evs = events(acts, key)
        if not changes_words(evs + list((others or {}).get(key, []))):
            continue
        law["note"] = None
        line = sentence(law["label"], evs)
        if line:
            lines.append(line)
    return lines
