"""Words struck by a DATED ruling that the engine left out of every version (audit of 2026-10-31, batch 58 session).

Batch 56 found the engine dropped words the page shows struck (<S>) when it could not tie them to a dated ruling
('struck text but no dated ruling'), although the Jurisprudencia Vigencia box names and dates the ruling. Such words
stand in the text until the ruling's day. This script patches the installed parts in place (their parsers no longer all
reproduce them byte for byte), entry by entry:

- each struck span on the page is tied to its ruling: the box line that quotes its words, else the one dated line that
  strikes 'tachado' words (INEXEQUIBLE) when the box has only one; the day is the ruling's (the press release's where
  the box gives only that);
- the span goes back into every version before the ruling's day whose text holds its context (up to four words either
  side, within the span's line, never across another struck span), walking back from the ruling's day while the
  context holds; each insertion is checked to be unique in the text;
- on the ruling's day the words go, credited to the ruling (a new version if none is on that day); a ruling's
  'did not change the words' note is dropped when it now changes words.
Entries that do not meet these checks are printed as MANUAL and left alone. Idempotent (a span already in the version
before its ruling is skipped).

Usage:  python -X utf8 fix_dated_struck.py [--dry] [part ...]
"""
from __future__ import annotations

import difflib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "batch57"))
for _d in ("batch56", "batch55", "batch54", "batch53", "batch52", "batch51", "batch50", "batch49", "batch31", "batch30",
           "batch29", "batch27", "batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20", "batch19",
           "batch18", "batch17", "batch16", "batch15", "batch14", "batch13", "batch12", "batch11", "batch10", "batch8",
           "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(HERE, _d))
import parse_batch57 as B  # noqa: E402

B.SPEC[:] = B.SPEC_ALL
E, P, B23 = B.E, B.P, B.B23
K = 4
SENT = "§§"
MONTH = r"(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|setiembre|octubre|noviembre|diciembre)"
CC = re.compile(r"Sentencias?\s+(?:No\.\s*)?(C-\d+[A-Z]?-\d{2,4})")
CSJ = re.compile(r"Corte Suprema de Justicia,? mediante Sentencia")
QUOTE = re.compile(r"['\"‘“]([^'\"’”]{2,400})['\"’”]")

# (part, act slug, unit key): units the audit found (.tmp-co/struckscan.py + struckhist.py, classes TARGET and NODATE).
ENTRIES: list[tuple[str, str, str]] = []
_list = os.path.join(HERE, "fix_dated_struck.entries")
if os.path.exists(_list):
    ENTRIES = [tuple(l.split()) for l in open(_list, encoding="utf-8") if l.strip() and not l.startswith("#")]


def n(s):
    return re.sub(r"\s+", " ", re.sub(r"[{}]", "", s)).strip()


def jv_rulings(u):
    """[(segment text, ruling key, label, title, day, url)] for dated INEXEQUIBLE lines of the box."""
    out = []
    for b in B23._boxes(u, "Jurisprudencia Vigencia"):
        raw = b
        for seg in re.split(r"(?<=[.'\"’”])\s*-\s+|^\s*-\s*|Corte Constitucional:?\s*-\s*|Corte Constitucional\s*-\s*", E.plain(b)):
            if "INEXEQUIBLE" not in seg or "ESTESE" in seg.upper()[:20]:
                continue
            m = CC.search(seg)
            day = E.date_es(seg[m.end():] if m else seg)
            if not day:
                continue
            if m:
                cid = m.group(1)
                key = E.court_key(cid)
                href = re.search(r'href="([^"#]*' + re.escape(cid.split("-")[0].lower() + "-" + cid.split("-")[1]) + r'_[^"#]*)', raw, re.I)
                url = E.BASE + href.group(1) if href else None
                lab = E.court_label(cid)
                out.append((seg, key, lab, f"Corte Constitucional, {lab}", day, url))
            elif CSJ.search(seg):
                lab = E.court_label(f"CSJ-{day}")
                out.append((seg, E.court_key(f"CSJ-{day}"), lab, lab, day, None))
    return out


def spans(html):
    return list(re.finditer(r"<s\b[^>]*>(.*?)</s>", html, re.S | re.I))


def ctx(html, i):
    """(context without span i, context with it), other struck spans as a sentinel; None if no context."""
    ss = spans(html)

    def build(keep):
        h, last = "", 0
        for j, m in enumerate(ss):
            h += html[last:m.start()] + ((re.sub(r"\[([^\[\]]+)\]", r"\1", m.group(1))) if (j == i and keep) else
                                         ("" if j == i else f" {SENT} "))
            last = m.end()
        h += html[last:]
        return E.tidy(E.to_text(h, True)).split()
    a, b = build(False), build(True)
    ops = [o for o in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if o[0] != "equal"]
    if len(ops) != 1:
        return None
    t, i1, i2, j1, j2 = ops[0]
    lo = i1
    while lo > 0 and i1 - lo < K and SENT not in a[lo - 1]:
        lo -= 1
    hi = i2
    while hi < len(a) and hi - i2 < K and SENT not in a[hi]:
        hi += 1
    if any(SENT in x for x in a[lo:hi] + b[j1 - (i1 - lo):j2 + (hi - i2)]) or (lo == i1 and hi == i2):
        return None
    return " ".join(a[lo:hi]), " ".join(b[j1 - (i1 - lo):j2 + (hi - i2)])


def states(act, key):
    """[(version index, text)] in order (text None when absent)."""
    st, out = {}, []
    for i, v in enumerate(act["versions"]):
        if "units" in v:
            st = dict(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = u
        out.append((i, (st.get(key) or {}).get("text")))
    return out


def set_text(act, i, key, text):
    """Make the unit's text in version i `text` (the versions after it that inherit it inherit the new text)."""
    v = act["versions"][i]
    cur = dict(next(t for j, t in reversed(_unit_at(act, key, i))))
    cur["text"] = text
    if "units" in v:
        v["units"][key] = cur
    else:
        v.setdefault("changes", {})[key] = cur


def _unit_at(act, key, i):
    st = {}
    out = []
    for j, v in enumerate(act["versions"][:i + 1]):
        if "units" in v:
            st = dict(v["units"])
        for k, u in (v.get("changes") or {}).items():
            if u is None:
                st.pop(k, None)
            else:
                st[k] = u
        if key in st:
            out.append((j, st[key]))
    return out


def fix_unit(part, act, key, log, dry):
    page = os.path.basename(act["url"])[:-5]
    u = next((x for x in P.doc_units(page)[1:]
              if (E.unit_key(E.label_num(x["label"] or "") or "") or (None,))[0] == key), None)
    if u is None:
        return log.append(("MANUAL", key, "unit not on the page"))
    rul = jv_rulings(u)
    hist = states(act, key)
    texts = [n(t) for _, t in hist if t]
    work = []
    ps = [it for it in u["items"] if it[0] == "p"]
    for pi, it in enumerate(ps):
        whole = not re.search(r"\w", E.tidy(E.to_text(it[1], False)))
        for i, m in enumerate(spans(it[1])):
            w = n(E.tidy(E.plain(re.sub(r"\[([^\[\]]+)\]", r"\1", m.group(1)))))
            if not re.search(r"\w", w) or (whole and i > 0):
                continue  # a paragraph struck whole is one entry (its first span)
            sub_m = None if whole else re.match(r"(?:\s|&#160;|&nbsp;)*(?:</[^>]+>\s*)*&lt;((?:(?!&gt;|&lt;).){1,200}?)&gt;", it[1][m.end():])
            if whole:
                # anchored to the paragraph before it, as today's text has it
                prev = [x for x in (E.tidy(E.to_text(y[1], False)) for y in ps[:pi]) if re.search(r"\w", x)]
                line = E.tidy(E.to_text(re.sub(r"\[([^\[\]]+)\]", r"\1", it[1]), True))
                w = n(line)
                c = (prev[-1] + "\n", prev[-1] + "\n" + line + "\n") if prev else None
            else:
                c = ctx(it[1], i)
            if c and any(c[1] in (t or "") for _, t in hist):
                continue  # the words are in a version already (the engine's or an earlier run)
            if not c and any(w in t for t in texts):
                continue
            hit = [r for r in rul if any(n(q) == w or (len(w) > 12 and (w in n(q) or n(q) in w))
                                         for q in QUOTE.findall(r[0]))]
            if not hit:
                tach = [r for r in rul if re.search(r"tachad", r[0], re.I)]
                hit = tach if len({r[1] for r in tach}) == 1 else []
            if len({r[1] for r in hit}) != 1:
                log.append(("MANUAL", key, f"no single dated ruling for '{w[:60]}' ({[r[1] for r in rul]})"))
                continue
            if not c:
                log.append(("MANUAL", key, f"no context for '{w[:60]}'"))
                continue
            sub = None
            if sub_m:
                # words the ruling ordered read in place of the struck ones ('<S>old</S> <new>'): from its day
                h2 = it[1][:m.start()] + "<S>" + sub_m.group(1) + "</S>" + it[1][m.end() + sub_m.end():]
                c2 = ctx(h2, i)
                if not c2 or c2[0] != c[0]:
                    log.append(("MANUAL", key, f"'{w[:60]}': substitution context"))
                    continue
                sub = (c2[1], E.tidy(E.plain(sub_m.group(1))))
            work.append((hit[0], c, w, sub, whole, pi))
    # latest ruling first; on one day, paragraphs struck whole first, the last of them first (each goes in right after
    # its anchor, so they end up in page order before the in-line spans change that anchor)
    for r, (cmin, cplus), w, sub, _, _ in sorted(work, key=lambda x: (x[0][4], x[4], x[5]), reverse=True):
        day = r[4]
        before = [(i, t) for i, t in hist if act["versions"][i]["from"] < day]
        if not before or before[-1][1] is None or before[-1][1].count(cmin) != 1:
            log.append(("MANUAL", key, f"'{w[:50]}' ({r[1]} {day}): context not once in the text before the ruling"))
            continue
        # walk back from the ruling's day while the context holds
        run = []
        for i, t in reversed(before):
            if t is None or t.count(cmin) != 1:
                break
            run.append(i)
        last_text = before[-1][1]
        post = last_text.replace(cmin, sub[0]) if sub else last_text
        first_diff = [i for i in run if hist[i][1] != last_text]
        if dry:
            log.append(("APPLY", key, f"'{w[:50]}' {r[1]} {day}: {len(run)} versions from "
                        f"{act['versions'][run[-1]]['from']}" + (f" (earlier text differs from {act['versions'][first_diff[0]]['from']})" if first_diff else "")))
            continue
        for i in run:
            if "units" in act["versions"][i] or key in (act["versions"][i].get("changes") or {}) or i == run[-1]:
                set_text(act, i, key, hist[i][1].replace(cmin, cplus))
        # the ruling's day
        vs = act["versions"]
        on = [k for k, v in enumerate(vs) if v["from"] == day]
        if on:
            v = vs[on[-1]]
            if "units" not in v and key not in (v.get("changes") or {}):
                v.setdefault("changes", {})[key] = dict(_unit_at(act, key, on[-1] - 1)[-1][1], text=post)
        else:
            k = next((k for k, v in enumerate(vs) if v["from"] > day), len(vs))
            prev = vs[k - 1]
            nv = {"from": day, "credits": {}, "source_url": prev.get("source_url"), "sha256": prev.get("sha256"),
                  "changes": {key: dict(_unit_at(act, key, k - 1)[-1][1], text=post)}}
            vs.insert(k, nv)
            on = [k]
        v = vs[on[-1]]
        v["credits"][key] = sorted(set(v["credits"].get(key) or []) | {r[1]})
        law = part["laws"].get(r[1])
        if law is None:
            part["laws"][r[1]] = {"label": r[2], "title": r[3], "kind": "court", "enacted": day, "published": None,
                                  "url": r[5], "temporary_until": None, "restores": None, "note": None}
        elif law.get("note"):
            law["note"] = None
        hist = states(act, key)
        log.append(("DONE", key, f"'{w[:60]}' in {len(run)} version(s) from {vs[run[-1]]['from']} to {day}, then "
                                 f"out" + (f" (the ruling's words '{sub[1]}' read in their place from then)" if sub else "") + f", credited to {r[2]}" + (" (earlier text differs)" if first_diff else "")))
    return None


# Hand entries (fix_dated_struck.hand.json), for units the generic rule above cannot settle (the text before the ruling
# differs from today's: later amendments, a placeholder, or a ruling that predates today's wording). Each entry was read
# off the unit's page (struck words, Jurisprudencia Vigencia box, Notas de Vigencia) and names:
#   part, slug, key, ruling (law key), day (the ruling's day: the words go then), why (for the decision line),
#   edits: [{from, to (default: day), old, new}] - in every version from `from` up to `to`, the unit's text must hold
#   `old` exactly once and gets `new` in its place (old = the placeholder line where the source's earlier text was not
#   known; new = that period's words with the struck ones). A version that already holds `new` and not `old` is done.
#   end (optional): {from, old, new} for versions on/after `day` (a ruling whose substituted words the engine missed).
# On `day` the unit keeps (or gets, in a new version) the text it had before the entry, credited to the ruling.
HAND = []
for _hand in sorted(f for f in os.listdir(HERE) if re.fullmatch(r"fix_dated_struck\.hand.*\.json", f)):
    HAND += json.load(open(os.path.join(HERE, _hand), encoding="utf-8"))


PLACEHOLDER = "[La fuente no da el texto vigente en esta fecha.]"


class Manual(Exception):
    pass


def add_unit(part, act, h, log, dry):
    """Entry with 'add': {from, label, text}: a whole article the engine left out of every version, which the page
    prints (struck) with the ruling that took it out: present from `from` until `day`, then out, credited to the
    ruling. Idempotent (an article already present exactly so is skipped)."""
    key, day, rk, ad = h["key"], h["day"], h["ruling"], h["add"]
    vs = act["versions"]
    hist = states(act, key)
    want = [ad["text"] if ad["from"] <= vs[i]["from"] < day else None for i, _ in hist]
    if [t for _, t in hist] == want and any(v["from"] == day and rk in (v["credits"].get(key) or []) for v in vs):
        return
    if any(t is not None for _, t in hist):
        raise Manual("the unit is already in some version")
    if not any(v["from"] == ad["from"] for v in vs):
        raise Manual(f"no version on {ad['from']}")
    if dry:
        log.append(("APPLY", key, f"add: {ad['from']} to {day}, {rk}"))
        return
    unit = {"label": ad["label"], "kind": "art", "text": ad["text"]}
    for v in vs:
        if ad["from"] <= v["from"] < day and ("units" in v or v["from"] == ad["from"]):
            if "units" in v:
                us = list(v["units"].items())
                k = next((j for j, (x, _) in enumerate(us) if x > key and x.startswith("art-")), len(us))
                v["units"] = dict(us[:k] + [(key, dict(unit))] + us[k:])
            else:
                v.setdefault("changes", {})[key] = dict(unit)
    if not any(v["from"] == day for v in vs):
        k = next((k for k, v in enumerate(vs) if v["from"] > day), len(vs))
        prev = vs[k - 1]
        vs.insert(k, {"from": day, "credits": {}, "source_url": prev.get("source_url"), "sha256": prev.get("sha256"),
                      "changes": {}})
    v = next(v for v in vs if v["from"] == day)
    if "units" in v:
        v["units"].pop(key, None)
    else:
        v.setdefault("changes", {})[key] = None
    v["credits"][key] = sorted(set(v["credits"].get(key) or []) | {rk})
    if [t for _, t in states(act, key)] != [ad["text"] if ad["from"] <= x["from"] < day else None for x in vs]:
        raise Manual("add: states do not come out as wanted")
    if rk not in part["laws"]:
        raise Manual(f"law {rk} not in the part")
    log.append(("DONE", key, h["why"]))


def hand_unit(part, act, h, log, dry):
    if h.get("add"):
        return add_unit(part, act, h, log, dry)
    key, day, rk = h["key"], h.get("day"), h.get("ruling")
    vs = act["versions"]
    hist = states(act, key)
    plan = []  # (version index, new text)
    edits = list(h["edits"]) + ([dict(h["end"], to="9999-12-31")] if h.get("end") else [])
    if any(x in ("@page", "@placeholder") for e in edits for x in (e["old"], e["new"])):
        page = os.path.basename(act["url"])[:-5]
        u = next((x for x in P.doc_units(page)[1:]
                  if (E.unit_key(E.label_num(x["label"] or "") or "") or (None,))[0] == key), None)
        if u is None:
            raise Manual("unit not on the page")
        tok = {"@placeholder": PLACEHOLDER,
               "@page": "\n".join(re.sub(r"\[([^\[\]]+)\]", r"\1", x) for x in B.hand_fixes._printed(u, True))}
        edits = [dict(e, old=tok.get(e["old"], e["old"]), new=tok.get(e["new"], e["new"])) for e in edits]
    cur = {i: t for i, t in hist}  # edits apply in order, each on the text the earlier ones left
    for e in edits:
        to = e.get("to", day or "9999-12-31")
        rng = [(i, cur[i]) for i, _ in hist if e["from"] <= vs[i]["from"] < to]
        if not rng or vs[rng[0][0]]["from"] != e["from"]:
            raise Manual(f"no version on {e['from']}")
        for i, t in rng:
            if t is None:
                raise Manual(f"unit absent on {vs[i]['from']}")
            if e["new"] in t and (e["old"] not in t or e["old"] in e["new"]) and t.count(e["old"]) <= e["new"].count(e["old"]):
                continue
            if t.count(e["old"]) != 1:
                raise Manual(f"'{e['old'][:50]}' not once in the text of {vs[i]['from']}")
            cur[i] = t.replace(e["old"], e["new"])
    plan = [(i, cur[i], None) for i, t in hist if cur[i] != t]
    if day is None:
        # no ruling takes the words out (e.g. the box upholds them): the edits alone
        if dry:
            log.append(("APPLY", key, f"hand: {len(plan)} version(s), no ruling day"))
        elif plan:
            reconcile(act, key, [cur[i] for i, _ in hist])
            log.append(("DONE", key, h["why"]))
        return
    on = [k for k, v in enumerate(vs) if v["from"] == day]
    credited = bool(on) and rk in (vs[on[-1]]["credits"].get(key) or [])
    if not plan and credited:
        return
    if dry:
        log.append(("APPLY", key, f"hand: {len(plan)} version(s), ruling {rk} {day}" + ("" if credited else " (credit added)")))
        return
    expected = [cur[i] for i, _ in hist]
    if not on or ("units" not in vs[on[-1]] and key not in (vs[on[-1]].get("changes") or {})):
        # the ruling's day must carry the unit's own (unedited) text, so the edited words stop there
        base = dict(_unit_at(act, key, (on[-1] if on else next((k for k, v in enumerate(vs) if v["from"] > day), len(vs))) - 1)[-1][1])
        if not on:
            k = next((k for k, v in enumerate(vs) if v["from"] > day), len(vs))
            prev = vs[k - 1]
            vs.insert(k, {"from": day, "credits": {}, "source_url": prev.get("source_url"), "sha256": prev.get("sha256"),
                          "changes": {key: base}})
            on = [k]
            expected.insert(k, base["text"])
        else:
            vs[on[-1]].setdefault("changes", {})[key] = dict(base, text=expected[on[-1]])
    reconcile(act, key, expected)
    v = vs[on[-1]]
    v["credits"][key] = sorted(set(v["credits"].get(key) or []) | {rk})
    law = part["laws"].get(rk)
    if law is None:
        if not h.get("law"):
            raise Manual(f"law {rk} not in the part and no 'law' given")
        part["laws"][rk] = dict(h["law"])
    elif law.get("note") and "did not change the words" in law["note"]:
        law["note"] = None
    log.append(("DONE", key, h["why"]))


def reconcile(act, key, expected):
    """Give version i the unit text expected[i] wherever its state differs (an explicit text where it inherits)."""
    for i in range(len(act["versions"])):
        t = states(act, key)[i][1]
        if t != expected[i]:
            if expected[i] is None or t is None:
                raise Manual(f"presence would change on {act['versions'][i]['from']}")
            set_text(act, i, key, expected[i])
    if [t for _, t in states(act, key)] != expected:
        raise Manual("reconcile failed")


def main(argv):
    dry = "--dry" in argv
    out_dir = None  # --to DIR: write the patched parts there (reading them from DIR when present there), for trials
    if "--to" in argv:
        k = argv.index("--to")
        out_dir = argv[k + 1]
        argv = argv[:k] + argv[k + 2:]
        os.makedirs(out_dir, exist_ok=True)
    only = [a for a in argv if not a.startswith("--")]
    by_part = {}
    for p, s, k in ENTRIES:
        if not only or any(o in p for o in only):
            by_part.setdefault(p, []).append((s, k))
    hand_by_part = {}
    for h in HAND:
        if not only or any(o in h["part"] for o in only):
            hand_by_part.setdefault(h["part"], []).append(h)
            by_part.setdefault(h["part"], [])
    for p, items in by_part.items():
        path = os.path.join(HERE, p) if p == "corpus.json" else os.path.join(HERE, "corpus.d", p)
        if out_dir:
            src = os.path.join(out_dir, p)
            path = src if os.path.exists(src) else path
        part = json.load(open(path, encoding="utf-8"))
        if out_dir:
            path = os.path.join(out_dir, p)
        done, hdone = [], []
        handkeys = {(h["slug"], h["key"]) for h in hand_by_part.get(p, [])}
        for s, k in items:
            if (s, k) in handkeys:
                continue  # settled by a hand entry below
            act = next(a for a in part["acts"] if a["slug"] == s)
            log = []
            fix_unit(part, act, k, log, dry)
            for kind, key, what in log:
                print(kind, p, s, key, what)
                if kind == "DONE":
                    done.append(f"{act['title']} {key.replace('art-', 'art. ').lstrip('0')}: {what}")
        for h in hand_by_part.get(p, []):
            act = next(a for a in part["acts"] if a["slug"] == h["slug"])
            log = []
            try:
                hand_unit(part, act, h, log, dry)
            except Manual as e:
                log.append(("MANUAL", h["key"], f"hand entry: {e}"))
            for kind, key, what in log:
                print(kind, p, h["slug"], key, what)
                if kind == "DONE":
                    hdone.append(f"{act['title']} {re.sub(r'art-0*', 'art. ', key)}: {what}")
        if hdone and not dry:
            part["decisions"].append(
                "Dated-struck audit, hand entries (2026-10-31): words the page shows struck or replaced, which the "
                "engine had left out of the versions they belong to (the text before the change differs from today's, "
                "the source's earlier text was not known, or the page marks a substitution), were put back by hand "
                "from the page's own struck words, notes and rulings box, each in the versions its entry names; on "
                "the day the page gives they go or change, credited to the ruling or act that made the change: "
                + "; ".join(hdone) + ".")
        # an entry's own 'decision' line (a rule the entry follows), added once
        extra = [h["decision"] for h in hand_by_part.get(p, []) if h.get("decision") and h["decision"] not in part["decisions"]]
        if extra and not dry:
            part["decisions"].extend(dict.fromkeys(extra))
            hdone = hdone or extra
        if (done or hdone) and not dry:
            d = ("Dated-struck audit (2026-10-31): words the page shows struck by a ruling its Jurisprudencia Vigencia "
                 "box names and dates, which the engine had left out of every version, are in the text up to the "
                 "ruling's day (the press release's day where the box gives only that), then go, credited to the "
                 "ruling: " + "; ".join(done) + ".")
            if done:
                part["decisions"].append(d)
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
                f.write("\n")
            os.replace(tmp, path)


if __name__ == "__main__":
    main(sys.argv[1:])
