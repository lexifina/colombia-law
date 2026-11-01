"""Several rulings struck different words of one article, but the engine put every strike on one day (the last
ruling's) - the batch 94 LESSON, audited corpus-wide in the fifteenth session (2026-11-01, .tmp-co/b96/multiscan.py).

The engine (phase2/engine.py article_history, before E.PER_SLOT_STRIKE) took the ruling for all of a provision's struck
words from ruling_for(jv, None): the LATEST dated INEXEQUIBLE ruling of the Jurisprudencia Vigencia box. Where the box
ties struck words to an earlier ruling (the line quoting them, or the box printed right after their paragraph naming one
ruling), those words stood in the versions only until that ruling's day. This script moves each such strike to its own
ruling's day, entry by entry (fix_multi_struck.json):

  part, slug, key, ruling (law key), day (the ruling's day), words (the struck words, for the record),
  with / without: the unit's text around the words with them and without them (context of up to four words either side,
  as on the page), why (for the decision line), law (optional: the ruling's law record when the part lacks it),
  uncredit (optional, list of law keys): rulings the engine credited on the unit that change none of its words once the
  strikes are on their own days (their credit on the unit is dropped where the unit's text does not change),
  law_set (optional): fields of the ruling's law entry to set (a day the ruling's own text settles),
  drop_decision (optional): a decision line the move makes false (fix_shared_notes' 'changed no words' line for the
  ruling), dropped from the part.

For an entry: every version from `day` on that holds `with` exactly once gets `without` in its place (the words go on the
ruling's day, a new version on that day if none); every version before `day` and after the first one that held the
words, which holds `without` once and not `with`, gets `with` back (words the engine took out before their ruling). The
version on `day` is credited to the ruling. Versions whose text holds neither (an amending act's own text in between)
are left alone. Idempotent: an entry already applied changes nothing.

Usage: python -X utf8 fix_multi_struck.py [--dry] [--to DIR] [part ...]
Re-run order: after fix_dated_struck.py (and fix_et_420_657.py), before fix_box_text.py.
"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRIES = json.load(open(os.path.join(HERE, "fix_multi_struck.json"), encoding="utf-8"))
DECISION = ("Strikes on their own rulings' days (2026-11-01): where several Constitutional Court rulings struck different "
            "words of one provision, each ruling's words now go on that ruling's day, as the page's Jurisprudencia "
            "Vigencia box ties them (the line quoting the words, or the box printed right after their paragraph); the "
            "engine had put all of them on the latest ruling's day: ")


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


def ensure_version(act, day):
    vs = act["versions"]
    if any(v["from"] == day for v in vs):
        return
    k = next((k for k, v in enumerate(vs) if v["from"] > day), len(vs))
    if k == 0:
        raise Manual(f"{day} before the act's first version")
    prev = vs[k - 1]
    vs.insert(k, {"from": day, "credits": {}, "source_url": prev.get("source_url"), "sha256": prev.get("sha256"),
                  "changes": {}})


def cut_index(act, day, create):
    """Index of the version the words leave on: the version on `day` (made when `create`), or, for a ruling before the
    act's first day, the act's 'same_day' version (batch 10's pre-start rule: the act as enacted, then on the same day
    the words the earlier ruling struck go). None when there is none yet (dry run)."""
    vs = act["versions"]
    if day < vs[0]["from"]:
        k = next((i for i, v in enumerate(vs) if v["from"] == vs[0]["from"] and v.get("same_day")), None)
        if k is None:
            raise Manual(f"{day} before the act's first version and no same_day version")
        return k
    if create:
        ensure_version(act, day)
    return next((i for i, v in enumerate(vs) if v["from"] == day), None)


def plan(act, e, cut):
    """[(version index, new text)] for the entry, on the act as it stands (cut: index the words leave on)."""
    key, day, w, wo = e["key"], e["day"], e["with"], e["without"]
    vs = act["versions"]
    if cut is None:
        cut = next((i for i, v in enumerate(vs) if v["from"] > day), len(vs))
    st = states(act, key)
    out = []
    for i in range(cut, len(st)):
        t = (st[i] or {}).get("text")
        if t and w in t:
            if t.count(w) != 1:
                raise Manual(f"'with' {t.count(w)} times on {vs[i]['from']}")
            out.append((i, t.replace(w, wo)))
    # words the engine took out before their ruling: back in each version before the cut, walking back while the
    # version holds the text without them (once) and not with them
    for i in range(cut - 1, -1, -1):
        t = (st[i] or {}).get("text")
        if not t or w in t or wo not in t:
            break
        if t.count(wo) != 1:
            raise Manual(f"'without' {t.count(wo)} times on {vs[i]['from']}")
        out.append((i, t.replace(wo, w)))
    return out


def reconcile(act, key, expected):
    """Give version i the unit text expected[i] where its state differs (explicit text where it inherited)."""
    vs = act["versions"]
    for i in range(len(vs)):
        u = states(act, key)[i]
        if (u or {}).get("text") != expected[i]:
            if u is None or expected[i] is None:
                raise Manual(f"presence would change on {vs[i]['from']}")
            set_text(act, i, key, u, expected[i])
    if [(u or {}).get("text") for u in states(act, key)] != expected:
        raise Manual("reconcile failed")


def apply_unit(part, act, ents, log, dry):
    key = ents[0]["key"]
    vs = act["versions"]
    for e in sorted(ents, key=lambda e: e["day"]):
        on = cut_index(act, e["day"], False)
        credited = on is not None and e["ruling"] in (vs[on]["credits"].get(key) or [])
        p = plan(act, e, on)
        if not p and credited:
            continue
        if dry:
            log.append(("APPLY", key, f"'{e['words'][:50]}' {e['ruling']} {e['day']}: {len(p)} version(s) "
                        + ",".join(vs[i]["from"] for i, _ in p)))
            continue
        on = cut_index(act, e["day"], True)
        p = plan(act, e, on)
        st = states(act, key)
        exp = [(u or {}).get("text") for u in st]
        for i, t in p:
            exp[i] = t
        reconcile(act, key, exp)
        st = states(act, key)
        if st[on] is None:
            raise Manual(f"unit absent on {e['day']}")
        if on and st[on] == st[on - 1]:
            # the words leave while the source gives no text for the article (a placeholder): nothing to credit
            if "units" not in vs[on] and not vs[on].get("changes") and not vs[on]["credits"]:
                del vs[on]
            if p:
                log.append(("DONE", key, e["why"] + " [no text on the ruling's day: not credited]"))
            continue
        vs[on]["credits"][key] = sorted(set(vs[on]["credits"].get(key) or []) | {e["ruling"]})
        if e["ruling"] not in part["laws"]:
            if not e.get("law"):
                raise Manual(f"law {e['ruling']} not in the part and no 'law' given")
            part["laws"][e["ruling"]] = dict(e["law"])
        law = part["laws"][e["ruling"]]
        for f, val in (e.get("law_set") or {}).items():
            law[f] = val
        if law.get("note") and "did not change the words" in law["note"]:
            law["note"] = None
        log.append(("DONE", key, e["why"]))
    if dry:
        return
    # rulings the engine credited that change none of the unit's words now
    st = states(act, key)
    for rk in sorted({r for e in ents for r in e.get("uncredit", [])}):
        for i in range(len(vs) - 1, 0, -1):
            v = vs[i]
            if rk in (v["credits"].get(key) or []) and st[i] == st[i - 1]:
                v["credits"][key] = [c for c in v["credits"][key] if c != rk]
                if not v["credits"][key]:
                    del v["credits"][key]
                ch = v.get("changes") or {}
                if key in ch and ch[key] == st[i - 1]:
                    del ch[key]
                log.append(("DONE", key, f"credit of {rk} on {v['from']} dropped (it changes none of the words)"))
                if "units" not in v and not v.get("changes") and not v["credits"]:
                    del vs[i]
                    st = states(act, key)
        used = any(rk in cs for a in part["acts"] for v in a["versions"] for cs in v["credits"].values()) or any(
            l.get("restores") == rk for l in part["laws"].values()) or any(
            a.get("first_law") == rk or rk in (a.get("earlier_laws") or []) for a in part["acts"])
        if not used and rk in part["laws"]:
            del part["laws"][rk]
            log.append(("DONE", key, f"law {rk} dropped from the part (credited nowhere)"))


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
    for p, ents in by_part.items():
        path = os.path.join(HERE, p) if p == "corpus.json" else os.path.join(HERE, "corpus.d", p)
        if out_dir and os.path.exists(os.path.join(out_dir, p)):
            path = os.path.join(out_dir, p)
        raw = open(path, encoding="utf-8").read()
        part = json.loads(raw)
        done = []
        units = {}
        for e in ents:
            units.setdefault((e["slug"], e["key"]), []).append(e)
        for (slug, key), es in units.items():
            act = next(a for a in part["acts"] if a["slug"] == slug)
            log = []
            try:
                apply_unit(part, act, es, log, dry)
            except Manual as x:
                log.append(("MANUAL", key, str(x)))
                bad += 1
            for kind, k, what in log:
                print(kind, p, slug, k, what)
                if kind == "DONE" and not what.startswith(("credit of", "law ")):
                    done.append(f"{act['title']} {k.replace('art-', 'art. ').replace('art. 0', 'art. ').lstrip()}: {what}")
        if dry:
            continue
        line = DECISION
        stale = {e["drop_decision"] for e in ents if e.get("drop_decision")}
        part["decisions"] = [d for d in part["decisions"] if not d.startswith(DECISION) and d not in stale]
        allwhy = []
        for (slug, key), es in units.items():
            act = next(a for a in part["acts"] if a["slug"] == slug)
            for e in sorted(es, key=lambda e: e["day"]):
                allwhy.append(f"{act['title']} {_art(key)}: {e['why']}")
        part["decisions"].append(line + "; ".join(allwhy) + ".")
        txt = json.dumps(part, ensure_ascii=False, separators=(",", ":")) + "\n"
        if txt == raw:
            continue
        out = os.path.join(out_dir, p) if out_dir else path
        tmp = out + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            f.write(txt)
        os.replace(tmp, out)
        print("WROTE", out)
    sys.exit(1 if bad else 0)


def _art(key):
    num = key.split("-", 1)[1].lstrip("0") or "0"
    return f"art. {num}"


if __name__ == "__main__":
    main(sys.argv[1:])
