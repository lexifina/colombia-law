"""Apply the fallback audit's dated histories to the published parts in place (no re-parse).

Where the engine had put today's text T (of an article, or of a part of it) on the day D of the last act it could name,
the source's own earlier text K for that act is put back from D, and T from the day of the later act or ruling that
made the change (credited to it), with any intermediate state given by hand (an earlier text, or the placeholder
'[La fuente no da el texto vigente en esta fecha.]' where the source gives none). Today's text is never changed (the
last version of every act is checked to be identical before and after).

Inputs: fallback/.tmp/audit.json (records written by hook.py), fallback/.tmp/proposals.json (resolve.py) and the
decisions by hand in fallback/manual*.json. Each fix: {"tag", "unit": "<page> <key>", "rec": i, "end": day,
"credit": law key, optional "mid": [{"from", "lines": [...] | "placeholder" | "known" | null, "credit"}], optional
"start": [...] | "placeholder" | null (replaces K), optional "laws": {key: law}, "why": text}.

Usage:  python -X utf8 fallback/apply.py [--dry-run] [--only TAG,...] [corpus.d folder]
Idempotent: a unit already fixed (its decision sentence is in the part) is skipped.
"""
from __future__ import annotations

import copy
import glob
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
TMP = os.path.join(HERE, "data")  # the audit's records and decisions (rec-*.json, the raw runs, stay in .tmp)
REC_DIR = os.path.join(HERE, ".tmp")
MISSING = "[La fuente no da el texto vigente en esta fecha.]"
ART_HEAD = re.compile(r"^\s*ART[IÍ]CULO\s+(TRANSITORIO\s*)?([0-9]+[A-Z]?(?:-[0-9]+\b|-[A-Z]\b)?|NUEVO|[IVXL]+)?\s*(?:o\.|º|°)?\s*[.\-:]*\s*", re.I)
SENT = "Fallback audit (2026-10-31)"


class Skip(Exception):
    pass


_E = None


def engine():
    global _E
    if _E is None:
        sys.path.insert(0, os.path.join(COUNTRY, "phase2"))
        import engine as e  # noqa: E402
        _E = e
    return _E


def make_law(k: str, day: str | None) -> dict | None:
    """A law entry for a key no part has yet: a Constitutional Court ruling (dated by the day the page gives), or an
    act the engine can register from its cached page."""
    E = engine()
    m = re.fullmatch(r"c-(\d{3,4})([a-z]?)-(\d{2})", k)
    if m:
        y = int(m.group(3))
        y = 1900 + y if y > 50 else 2000 + y
        cid = f"C-{int(m.group(1))}{m.group(2).upper()}-{m.group(3)}"
        label = E.court_label(cid)
        return {"label": label, "title": f"Corte Constitucional, {label}", "kind": "court", "enacted": day,
                "published": None, "url": E.BASE + f"c-{m.group(1)}{m.group(2)}_{y}.html", "temporary_until": None,
                "restores": None, "note": None}
    if re.fullmatch(r"(ley|dec)-\d+-\d{4}", k):
        E.register(k)
        return dict(E.LAWS[k])
    return None


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", deacc(s.lower()))


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
        out.append(cur)
    return out


def body_lines(u):
    return u["text"].split("\n")[1:-1] if u else []


def find_run(lines, run, nth=0):
    """Index where `run` (lines) stands in `lines` (its nth occurrence), comparing letters and digits only; None if
    absent."""
    if not run:
        return None
    ks, kr = [key(l) for l in lines], [key(l) for l in run]
    for i in range(len(ks) - len(kr) + 1):
        if ks[i:i + len(kr)] == kr:
            if nth == 0:
                return i
            nth -= 1
    return None


def epigraph(first: str) -> str:
    """A leading capitals-only epigraph of a first line ('FUNCIONES. ')."""
    m = re.match(r"^((?:[A-ZÁÉÍÓÚÑÜ0-9][A-ZÁÉÍÓÚÑÜ0-9 ,;:()/\-–\"“”]{2,}?)\.)\s+(?=\S)", first)
    return m.group(0) if m and re.search(r"[a-záéíóúñ]", first[m.end():]) else ""


def law_label(k, laws):
    return (laws.get(k) or {}).get("label") or k


def main(argv):
    dry = "--dry-run" in argv
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else None
    folder = next((a for a in argv if not a.startswith("--") and (only is None or a != ",".join(only))),
                  os.path.join(COUNTRY, "corpus.d"))
    rows = {(r["tag"], r["unit"]): r for r in json.load(open(os.path.join(TMP, "audit.json"), encoding="utf-8"))}
    fixes = []
    for o in json.load(open(os.path.join(TMP, "proposals.json"), encoding="utf-8")):
        for p in o.get("parts", []):
            if p["verdict"] == "fix":
                fixes.append({"tag": o["tag"], "unit": o["unit"], "rec": p["rec"], "end": p["end"], "credit": p["credit"],
                              "how": p["how"]})
    manual = {}
    for f in sorted(glob.glob(os.path.join(HERE, "manual*.json"))):
        for m in json.load(open(f, encoding="utf-8")):
            manual[(m["tag"], m["unit"], m.get("rec", 0))] = m
    fixes = [f for f in fixes if (f["tag"], f["unit"], f["rec"]) not in manual]
    fixes += [m for m in manual.values() if m.get("verdict", "fix") == "fix"]
    census = {(o["tag"], o["unit"], o["rec"]): o for o in json.load(open(os.path.join(TMP, "census.json"), encoding="utf-8"))}
    fixes = [f for f in fixes if census[(f["tag"], f["unit"], f["rec"])]["effect"] == "effective"
             and (census[(f["tag"], f["unit"], f["rec"])]["kind"] not in ("punct", "typo") or f.get("why"))]
    open_items = {}
    for (tg, un, rc), m in sorted(manual.items()):
        if m.get("verdict") == "unresolved" and census.get((tg, un, rc), {}).get("effect") == "effective":
            x0 = rows[(tg, un)]["records"][rc]
            E_ = engine()
            lab = (E_.unit_key(E_.label_num(x0.get("label") or "") or "") or (None, un.split(" ", 1)[1]))[1]
            open_items.setdefault(tg, []).append(f"{lab} ({m['why']})")
    all_laws = {}
    for f in sorted(glob.glob(os.path.join(folder, "*.json"))):
        for k, l in json.load(open(f, encoding="utf-8")).get("laws", {}).items():
            all_laws.setdefault(k, l)
    by_tag = {}
    for f in fixes:
        by_tag.setdefault(f["tag"], []).append(f)
    report = {"fixed": 0, "skipped": 0, "covered": 0, "errors": []}
    whole_done = {}
    for tag, fs in sorted(by_tag.items()):
        if only and tag not in only:
            continue
        path = glob.glob(os.path.join(folder, tag + "-*.json"))
        path = [p for p in path if not p.endswith(".tmp")][0]
        part = json.load(open(path, encoding="utf-8"))
        acts = {}
        for a in part["acts"]:
            page = a["url"].rsplit("/", 1)[-1].rsplit(".", 1)[0]
            acts.setdefault(page, a)
        before_last = {a["slug"]: states(a["versions"])[-1] for a in part["acts"]}
        lines_out = []
        # one unit may have several fixes (several parts of it): apply them one at a time, latest day first
        def tlen(f):
            return -len(rows[(tag, f["unit"])]["records"][f["rec"]]["today"] or [])
        for f in sorted(fs, key=lambda f: (f["unit"], tlen(f), -int(f["rec"]))):
            page, ukey = f["unit"].split(" ", 1)
            a = acts.get(page)
            x0 = rows[(tag, f["unit"])]["records"][f["rec"]]
            lab = next((s_[ukey]["label"] for s_ in states(a["versions"]) if ukey in s_), None) if a else None
            if lab is None and f.get("label"):
                lab = f["label"]
            if lab is None and x0.get("label"):
                E_ = engine()
                lab = (E_.unit_key(E_.label_num(x0["label"]) or "") or (None, None))[1]
            nrec = len(rows[(tag, f["unit"])]["records"])
            tagline = f"{SENT}: {a['title'] if a else page}, {lab or ukey}" + (f" (part {f['rec'] + 1} of its history)" if nrec > 1 else "")
            if a is None:
                report["errors"].append(f"{tag} {f['unit']}: no act for page"); continue
            if any(d.startswith(tagline + ":") for d in part["decisions"]):
                report["skipped"] += 1; continue
            try:
                line = apply_one(part, a, ukey, f, rows[(tag, f["unit"])]["records"][f["rec"]], all_laws)
            except Skip as e:
                cover = whole_done.get((tag, f["unit"]))
                if "not found" in str(e) and cover and cover >= f["end"]:
                    report["covered"] += 1  # a part of an article whose whole earlier text was already put back
                    continue
                report["errors"].append(f"{tag} {f['unit']} [{f['rec']}]: {e}")
                continue
            x = rows[(tag, f["unit"])]["records"][f["rec"]]
            if not x["today"] or AP_whole(part, a, ukey, x):
                whole_done[(tag, f["unit"])] = f["end"]
            lines_out.append(tagline + ": " + line)
            report["fixed"] += 1
        for a in part["acts"]:
            if states(a["versions"])[-1] != before_last[a["slug"]]:
                raise SystemExit(f"{tag} {a['slug']}: today's text changed")
        if lines_out and not dry:
            part["decisions"] += lines_out
            fix_sentence(part, open_items.get(tag, []))
            tmp = path + ".tmp"
            with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(part, fh, ensure_ascii=False, separators=(",", ":"))
                fh.write("\n")
            os.replace(tmp, path)
        print(tag, len(lines_out), "fixed")
    print(report["fixed"], "fixed,", report["skipped"], "already done,", report["covered"], "covered by a whole-article fix,",
          len(report["errors"]), "errors")
    for e in report["errors"]:
        print("  ERR", e)


def AP_whole(part, act, ukey, x) -> bool:
    """Whether a record's today's text is the article's whole body (as the last version holds it)."""
    st = states(act["versions"])[-1].get(ukey)
    return st is not None and len(body_lines(st)) == len(x["today"] or [])


def fix_sentence(part, open_list=()):
    """One summary decision after the engine's 'Articles where that happened' list (replaced on a re-run)."""
    listed = []
    for d in part["decisions"]:
        for m in re.finditer(r"Articles where that happened: (.*?)\.(?:$| [A-Z])", d):
            if m.group(1) != "none":
                listed += m.group(1).split(", ")
    if not listed:
        return
    fixed = {d.split(": ", 2)[1] for d in part["decisions"] if d.startswith(SENT + ": ")}
    fixed = {re.sub(r" \(part \d+ of its history\)$", "", x) for x in fixed}
    n, k = len(listed), len(fixed)
    line = (f"{SENT}, summary: each of the {n} articles listed above as taking today's text from the latest named act's "
            f"day was compared with the source's earlier text for that act; {k} of them had later words in an earlier "
            f"version and now carry the source's earlier texts until the act or ruling that changed them (the decisions "
            f"headed '{SENT}'); in the other {n - k} the difference is only the heading line, the source's punctuation or "
            f"a slip in its transcription, or today's text does apply from that day, or the engine's later steps "
            f"replaced that text, so no earlier version holds later words"
            + (f"; except, left as they are because the source does not settle them: {'; '.join(open_list)}" if open_list else "")
            + ".")
    part["decisions"] = [d for d in part["decisions"] if not d.startswith(SENT + ", summary:")] + [line]


def apply_one(part, act, ukey, f, x, all_laws) -> str:
    vs = act["versions"]
    sts = states(vs)
    dn = x["events"][-1][0]
    end = f["end"]
    if not end or end <= dn:
        raise Skip(f"end {end} not after {dn}")
    T = x["today"] or []
    K = x["known_last"] if f.get("start", "known") == "known" else f["start"]
    i0 = [i for i, v in enumerate(vs) if v["from"] == dn]
    if not i0:
        raise Skip(f"no version on {dn}")
    # several versions on D (a 'same_day' one after the first): start on the first if the unit reads the same in all
    i0 = i0[0] if all(sts[i].get(ukey) == sts[i0[-1]].get(ukey) for i in i0) else i0[-1]
    if ukey not in sts[i0] and T:
        raise Skip(f"{ukey} absent on {dn}")
    # segments: (from, lines|None|'placeholder', credit)
    segs = [(dn, K, None)] + [(m["from"], x["known_last"] if m["lines"] == "known" else m["lines"], m.get("credit"))
                              for m in f.get("mid", [])]
    u0 = sts[i0].get(ukey)
    occ = int(f.get("occurrence", 0))
    run_at = find_run(body_lines(u0), T, occ) if T else None
    if T and run_at is None:
        raise Skip(f"today's words not found in {ukey} on {dn}")
    whole = (not T) or (run_at == 0 and len(T) == len(body_lines(u0)))
    label = (u0 or {}).get("label") or next((s[ukey]["label"] for s in sts if ukey in s), None)
    if label is None and f.get("label"):
        label = f["label"]
    if label is None and x.get("label"):
        E = engine()
        uk = E.unit_key(E.label_num(x["label"]) or "")
        if uk and uk[0] == ukey:
            label = uk[1]
    kind = (u0 or {}).get("kind") or next((s[ukey]["kind"] for s in sts if ukey in s), "art")
    head = f"# {label}\n" if label else None
    if head is None:
        raise Skip("no label")

    def text_for(lines, base_unit):
        """The unit's text with T replaced by `lines` (whole: the whole body; {"whole": [...]}: the whole body)."""
        if isinstance(lines, dict):
            ls = lines["whole"]
            if not ls:
                return None
            return dict(base_unit or {"label": label, "kind": kind}, text=head + "".join(l + "\n" for l in ls))
        if lines == "placeholder":
            return {"label": label, "kind": "art", "text": head + MISSING + "\n"}
        if whole:
            if not lines:
                return None
            ls = list(lines)
            ls[0] = ART_HEAD.sub("", ls[0], count=1) if ART_HEAD.match(ls[0]) and not ART_HEAD.match(T[0] if T else "") else ls[0]
            epi = epigraph(T[0]) if T else ""
            if epi and not key(ls[0]).startswith(key(epi)) and not epigraph(ls[0]):
                ls[0] = epi + ls[0]
            base = base_unit or {"label": label, "kind": kind}
            return dict(base, text=head + "".join(l + "\n" for l in ls))
        bl = body_lines(base_unit)
        j = find_run(bl, T, occ)
        if j is None:
            raise Skip("today's words not found in a later version")
        new = bl[:j] + list(lines or []) + bl[j + len(T):]
        if not [l for l in new if re.search(r"\w", l)]:
            return None
        return dict(base_unit, text=head + "".join(l + "\n" for l in new))

    # the versions from dn to end take the segment texts
    new_states = [dict(s) for s in sts]
    days = [v["from"] for v in vs]
    # insert versions for segment days and the end day where none exists
    inserts = sorted({d for d, _, _ in segs[1:]} | {end})
    for d in inserts:
        if d in days:
            continue
        k = next((j for j, v in enumerate(vs) if v["from"] > d), len(vs))
        vs.insert(k, {"from": d, "credits": {}})
        new_states.insert(k, dict(new_states[k - 1]))
        days.insert(k, d)
    sts_now = new_states
    for j, v in enumerate(vs):
        if not (dn <= v["from"] < end) or (v["from"] == dn and j < i0):
            continue
        seg = [s for s in segs if s[0] <= v["from"]][-1]
        base = sts_now[j].get(ukey)
        if base is None and not whole:
            raise Skip(f"{ukey} absent on {v['from']} inside the range")
        t = text_for(seg[1], base)
        if t is None:
            sts_now[j].pop(ukey, None)
        else:
            sts_now[j][ukey] = t
    # credits: the end day (and each segment day) credits its law
    laws = part.setdefault("laws", {})
    for d, _, cr in segs[1:] + [(end, None, f["credit"])]:
        if not cr:
            raise Skip(f"no credit for {d}")
        j = days.index(d)
        lst = vs[j]["credits"].setdefault(ukey, [])
        if cr not in lst:
            lst.append(cr)
        if cr not in laws:
            src = (f.get("laws") or {}).get(cr) or all_laws.get(cr) or make_law(cr, d)
            if not src:
                raise Skip(f"law {cr} not known")
            laws[cr] = src
    # re-deltify and drop credits for words that no longer change (except no-word notes)
    prev = None
    for j, (v, st) in enumerate(zip(vs, sts_now)):
        if j == 0:
            v["units"] = st
            prev = st
            continue
        ch = {k: u for k, u in st.items() if prev.get(k) != u}
        ch.update({k: None for k in prev if k not in st})
        if ch:
            v["changes"] = ch
        else:
            v.pop("changes", None)
        cr = v.get("credits", {})
        if ukey in cr and ukey not in ch:
            keep = [l for l in cr[ukey] if (laws.get(l) or all_laws.get(l) or {}).get("note")]
            if keep:
                cr[ukey] = keep
            else:
                cr.pop(ukey)
        prev = st
    # the unit's change on D itself is credited to the act named last before the fallback (unless it is the first version)
    jd = next((j for j, v in enumerate(vs) if v["from"] == dn and j >= i0), None)
    if jd and ukey in (vs[jd].get("changes") or {}) and not vs[jd]["credits"].get(ukey):
        vs[jd]["credits"][ukey] = [x["events"][-1][1]]
    # drop versions left with nothing
    keep_vs = [v for j, v in enumerate(vs) if j == 0 or v.get("changes") or v.get("credits")]
    if len(keep_vs) != len(vs):
        # a dropped version holds no change and no credit: removing it changes nothing
        act["versions"] = keep_vs
    for v in act["versions"]:
        if v["from"] in {d for d, _, _ in segs[1:]} | {end} and ukey in v.get("credits", {}):
            v["credits"][ukey] = sorted(set(v["credits"][ukey]), key=lambda l: (((laws.get(l) or {}).get("enacted") or ""), l))
    desc = "the source's earlier text" if segs[0][1] not in (None, "placeholder") else (
        "not in force" if segs[0][1] is None else "the placeholder")
    mids = "; ".join(f"from {d}: " + ("the placeholder" if l == "placeholder" else "not in force" if l is None else
                                      "the source's earlier text") + f" ({law_label(c, laws)})" for d, l, c in segs[1:])
    why = f.get("why") or {"marker": "the page's marker on today's words", "ruling": "the ruling that struck the words",
                           "notes": "the only later act the notes name"}.get(f.get("how"), "")
    return (f"from {dn}: {desc} ({law_label(x['events'][-1][1], laws)})" + (f"; {mids}" if mids else "") +
            f"; {'today' + chr(39) + 's wording' if T else 'out of force'} from {end} ({law_label(f['credit'], laws)}{', ' + why if why else ''}).")


if __name__ == "__main__":
    main(sys.argv[1:])
