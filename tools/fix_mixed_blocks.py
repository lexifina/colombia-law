"""Mixed blocks: where an earlier text of a labelled part ('PARÁGRAFO 1o. ...', '7. ...') ran over several lines, the
engine (phase2/engine.py article_history, before E.PARA_BLOCK) put the box's earlier block in place of the part's first
paragraph only; the part's later paragraphs ('a) ...', '1. ...') kept today's words in every version. So the versions
before the part was rewritten held BOTH texts: the earlier block and today's lines of the same part (found in Ley 141 de
1994, nineteenth session corpus-wide: .tmp-co/b100/mixscan_all.py and numscan_all.py).

With E.PARA_BLOCK on, the engine reads the part from its label to the box that prints it, so each version holds one text.
fix_mixed_blocks.json holds, per version day of each affected unit, the lines the engine with PARA_BLOCK takes out of the
text the engine without it gave (re-parses of the part's driver, both ways): {part, slug, key, page, day, dels: [[line,
prev, next, copies], ...]} where prev/next are the lines around it in the old text and copies how often it stood
there (to tell a duplicated line's copies apart, and to see that one already went).

For an entry: the part's version on `day` (the day that unit's text starts) loses each listed line where the line sits
between the same neighbours (each must match exactly once), and so does every later version that inherits that text.
Checks: every listed line is on the page (today's paragraphs or a box: the lines are the page's, only misplaced); no
line is added. A change that becomes equal to the version before it is taken out (its credit stays: 'wording unchanged').
Idempotent: a unit the part's 'Mixed blocks' decision line lists already is not cut again (a re-parse writes no
such line, so the fixer applies after one). An entry whose day is not a change day
of the unit in the part (the version was dropped or moved by a later fixer) is reported SKIP.

Later parágrafo lines (2026-11-01, twentieth session; entries with "kind": "orphan"): where a later act added a
parágrafo of several lines, the page marks only its first line as added; the engine kept the lines after it in every
earlier version (the parágrafo's continuation standing alone before the parágrafo existed: .tmp-co/b100/orphanscan.py,
.tmp-co/b101/orphan2.py). These hand entries take those lines out of the versions before the act, with the same
mechanics; they have their own decision line (ORPHAN_DECISION) and idempotency, so a unit already cut as a mixed block
can take an orphan entry for the same day. Part "corpus.json" means the Constitution (country folder's corpus.json).

Parágrafo labels (2026-11-01, twenty-first session; entries with "kind": "label"): where a box gives an earlier text of a
parágrafo's first inciso only ('<INCISO>') or the incisos under a parágrafo heading that stands as its own paragraph, the
version held the inciso without the parágrafo's label. These hand entries ("sets": [[old line, [new lines]]]) put the
label back as the page prints it, in the version on the entry's day and every later version inheriting that text. Each new
line must be on the page (label + its first words), and an inserted label must stand on the page shortly before the
inciso's words. Own decision line (LABEL_DECISION) and idempotency.

Usage: python -X utf8 fix_mixed_blocks.py [--dry] [--to DIR] [part ...]
Re-run order: after fix_multi_struck.py and fix_deferrals.py, before fix_box_text.py.
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = json.load(open(os.path.join(HERE, "fix_mixed_blocks.json"), encoding="utf-8"))
DECISION = ("Mixed blocks (2026-11-01): where an earlier text of a parágrafo, numeral or literal ran over several lines, the "
            "versions before that part was rewritten had held both the earlier block and today's lines of the same part "
            "(today's lines kept under the earlier heading); each version now holds the earlier block only, as the page's "
            "'Legislación Anterior' box prints it: ")

ORPHAN_DECISION = ("Later parágrafo lines (2026-11-01): where a later act added a parágrafo of several lines, the page marks "
                   "only its first line as added, and its other lines had stood in the versions before that act; they now "
                   "start with the parágrafo, on the act's day: ")
LABEL_DECISION = ("Parágrafo labels (2026-11-01): where the page's box gives an earlier text of a parágrafo's incisos without "
                  "the parágrafo's heading, the version had lost the heading ('PARÁGRAFO 2o.'); it now stands as the page "
                  "prints it: ")
DECISIONS = {"mixed": DECISION, "orphan": ORPHAN_DECISION, "label": LABEL_DECISION}

NL = chr(10)
LABEL = re.compile(r"^(?:PAR[ÁA]GRAFO[^.]*\.|\d+[.)]|[a-z]\))\s*")


class Manual(Exception):
    pass


def states(act, key):
    st, out = {}, []
    for v in act["versions"]:
        if "units" in v:
            st = dict(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = u
        out.append(st.get(key))
    return out


def set_text(act, i, key, unit, text):
    v = act["versions"][i]
    new = dict(unit, text=text)
    if "units" in v:
        v["units"] = dict(v["units"])
        v["units"][key] = new
    else:
        v.setdefault("changes", {})[key] = new


_PAGES = {}


def page_norm(page):
    """Every paragraph and box of the page, letters and digits only (raw engine reader)."""
    if page not in _PAGES:
        sys.path.insert(0, os.path.join(HERE, "phase2"))
        cwd = os.getcwd()
        os.chdir(HERE)
        try:
            import engine as E  # noqa: E402
            us = E.doc_units(page)
            _PAGES[page] = norm(" ".join(E.plain(it[1] if it[0] == "p" else it[2]) for u in us for it in u["items"]))
        finally:
            os.chdir(cwd)
    return _PAGES[page]


def norm(s):
    return re.sub(r"[^\w%]+", "", s).lower()


def cut(text, dels):
    """text without the listed lines. dels are [line, prev, next, copies] in old-text order; consecutive lines form
    runs. A run found once is taken where it is; a run found several times is taken where it stands between the same
    neighbours as in the old text. None if no run is there. (Idempotency is by the part's decision line: a unit it
    already lists is not cut again.)"""
    lines = text.split(NL)
    runs = []
    for d in dels:
        if runs and runs[-1][-1][2] == d[0] and d[1] == runs[-1][-1][0]:
            runs[-1].append(d)
        else:
            runs.append([d])
    drop, missing = set(), 0
    for r in runs:
        body, prev, nxt = [d[0] for d in r], r[0][1], r[-1][2]
        n = len(body)
        pos = [p for p in range(len(lines) - n + 1) if lines[p:p + n] == body and not drop & set(range(p, p + n))]
        if len(pos) > 1:
            both = [p for p in pos if (lines[p - 1] if p else "") == prev and (lines[p + n] if p + n < len(lines) else "") == nxt]
            one = [p for p in pos if (lines[p - 1] if p else "") == prev or (lines[p + n] if p + n < len(lines) else "") == nxt]
            pos = both if len(both) == 1 else one
        if len(pos) > 1:
            raise Manual(f"run {body[0][:50]!r} (+{n - 1}) matches {len(pos)} times")
        if not pos:
            missing += 1
            continue
        drop.update(range(pos[0], pos[0] + n))
    if not drop:
        return None
    if missing:
        raise Manual(f"{len(runs) - missing} of {len(runs)} runs found")
    return NL.join(l for i, l in enumerate(lines) if i not in drop)


def relabel(text, sets):
    """text with each [old line, [new lines]] of sets replaced (old must stand exactly once); None if none is there."""
    lines = text.split(NL)
    done = 0
    for old, new in sets:
        pos = [i for i, l in enumerate(lines) if l == old]
        if len(pos) > 1:
            raise Manual(f"line {old[:50]!r} matches {len(pos)} times")
        if pos:
            lines[pos[0]:pos[0] + 1] = new
            done += 1
    if not done:
        return None
    if done != len(sets):
        raise Manual(f"{done} of {len(sets)} lines found")
    return NL.join(lines)


def check_label(e):
    """Each new line's label stands on the page just before the line's words (a marker such as '<Inciso modificado ...>'
    may come between: 400 letters), or a bare heading line shortly before the old line's words (3000 letters: boxes
    between)."""
    pn = page_norm(e["page"])
    for old, new in e["sets"]:
        oa = norm(LABEL.sub("", old))[:60]
        if oa not in pn:
            raise Manual(f"line not on the page {e['page']}: {old[:60]!r}")
        for l in new:
            if l == old:
                continue
            m = LABEL.match(l)
            if not m:
                raise Manual(f"new line is not a label + the old words: {l[:60]!r}")
            lab, rest = norm(m.group(0)), norm(l[m.end():])[:60]
            anchor, win = (rest, 400) if rest else (oa, 3000)
            occ = [i for i in range(len(pn)) if pn.startswith(anchor, i)] if anchor else []
            if not any(pn.rfind(lab, max(0, i - win), i) >= 0 for i in occ):
                raise Manual(f"label {m.group(0)!r} not before {anchor[:40]!r} on the page")


def apply_unit(act, ents, log, dry):
    key = ents[0]["key"]
    vs = act["versions"]
    st = states(act, key)
    expected = [(u or {}).get("text") for u in st]
    starts = set()
    for e in sorted(ents, key=lambda e: e["day"]):
        pn = page_norm(e["page"])
        if e.get("kind") == "label":
            check_label(e)
        for line, *_ in e.get("dels", []):
            if norm(LABEL.sub("", line))[:60] not in pn:  # (60 letters after the label: a box may write the label otherwise or put markers later on)
                raise Manual(f"line not on the page {e['page']}: {line[:60]!r}")
        idx = [i for i, v in enumerate(vs) if v["from"] == e["day"]]
        idx = [i for i in idx if i == 0 or expected[i] != expected[i - 1]]
        if not idx:
            log.append(("SKIP", key, f"{e['day']}: no change of the unit that day"))
            continue
        i0 = idx[-1]
        old = expected[i0]
        new = (relabel(old, e["sets"]) if e.get("kind") == "label" else cut(old, e["dels"])) if old else None
        if new is None:
            continue
        starts.add(i0)
        j = i0
        while j < len(vs) and expected[j] == old:
            expected[j] = new
            j += 1
        log.append(("DONE", key, f"{e['day']}: " + (f"{len(e['sets'])} labels back" if e.get("kind") == "label" else f"{len(e['dels'])} lines out")))
    if dry:
        return
    for i in range(len(vs)):
        u = states(act, key)[i]  # fresh: a version that inherits takes the new text from the one before
        if (u or {}).get("text") != expected[i]:
            set_text(act, i, key, u, expected[i])
    # a change the cut made equal to the version before it changes nothing now
    for i in sorted(starts):
        ch = vs[i].get("changes") or {}
        if i and key in ch and ch[key] is not None and expected[i] == expected[i - 1] and states(act, key)[i - 1] == ch[key]:
            del ch[key]
            log.append(("NOOP", key, f"{vs[i]['from']}: change equal to the version before, taken out (credit kept)"))
    if [(u or {}).get("text") for u in states(act, key)] != expected:
        raise Manual("reconcile failed")


def _art(key):
    return "art. " + re.sub(r"^0+", "", key[4:]).replace("-0", "-")


def main(argv):
    dry = "--dry" in argv
    out_dir = None
    if "--to" in argv:
        k = argv.index("--to")
        out_dir = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
        os.makedirs(out_dir, exist_ok=True)
    only = [a for a in argv if not a.startswith("--")]
    by_part = {}
    for e in ENTRIES:
        if not only or any(o in e["part"] for o in only):
            by_part.setdefault(e["part"], []).append(e)
    bad = 0
    for p, ents in sorted(by_part.items()):
        path = os.path.join(HERE, p) if p == "corpus.json" else os.path.join(HERE, "corpus.d", p)
        if out_dir and os.path.exists(os.path.join(out_dir, p)):
            path = os.path.join(out_dir, p)
        raw = open(path, encoding="utf-8").read()
        part = json.loads(raw)
        for kind in ("mixed", "orphan", "label"):
            dec = DECISIONS[kind]
            kents = [e for e in ents if e.get("kind", "mixed") == kind]
            if not kents:
                continue
            units = {}
            for e in kents:
                units.setdefault((e["slug"], e["key"]), []).append(e)
            why = []
            prior = next((d for d in part["decisions"] if d.startswith(dec)), "")
            for (slug, key), es in sorted(units.items()):
                act = next(a for a in part["acts"] if a["slug"] == slug)
                log = []
                try:
                    if f"{act['title']} {_art(key)} (" in prior:
                        log.append(("APPLIED", key, "listed in the part's decision line already"))
                    else:
                        apply_unit(act, es, log, dry)
                except Manual as x:
                    log.append(("MANUAL", key, str(x)))
                    bad += 1
                for k_, k, what in log:
                    print(k_ if kind == "mixed" else k_ + "/" + kind, p, slug, k, what)
                days = sorted({e["day"] for e in es})
                why.append(f"{act['title']} {_art(key)} ({', '.join(days)})")
            if dry:
                continue
            part["decisions"] = [d for d in part["decisions"] if not d.startswith(dec)]
            part["decisions"].append(dec + "; ".join(why) + ".")
        if dry:
            continue
        txt = json.dumps(part, ensure_ascii=False, separators=(",", ":")) + NL
        if txt == raw:
            continue
        out = os.path.join(out_dir, p) if out_dir else path
        tmp = out + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline=NL) as f:
            f.write(txt)
        os.replace(tmp, out)
        print("WROTE", out)
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1:])
