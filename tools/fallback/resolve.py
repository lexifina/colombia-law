"""Propose a dated history for each audited fallback unit from the source page's own notes, markers and earlier texts.

For a unit (or a part of it) where the engine put today's text T on the day D of the last act it could name, while the
source's earlier text for that act is K: K is the text from D (it is what the page quotes for that state), and T from
the day of the later act or ruling the page names for the change. The later act is looked for, in this order:
  1. the markers on the page's current paragraphs that hold T's words ('<Numeral modificado por el artículo 2 de la Ley
     2111 de 2021 ...>');
  2. for words now struck: a Constitutional Court ruling the unit's 'Jurisprudencia Vigencia' box dates after D;
  3. any act the unit's 'Notas de Vigencia' box names with a day after D, if there is exactly one.
Units where none of these gives exactly one act are left for a decision by hand (fallback/manual.json).

Usage:  python -X utf8 fallback/resolve.py [-v]      writes fallback/.tmp/proposals.json
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import audit as A  # noqa: E402
import triage as T  # noqa: E402

sys.path.insert(0, os.path.join(os.path.dirname(HERE), "phase2"))
import engine as E  # noqa: E402

MONTHS = {m: i + 1 for i, m in enumerate(
    "enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre".split())}
MONTHS["setiembre"] = 9
DATE = r"(\d{1,2})(?:o\.|º)?\s+de\s+([a-z]+)\s+(?:de\s+|del\s+)?(\d{4})"
RUL = re.compile(r"Sentencia\s+(C-\d+[A-Z]?-\d{2,4})", re.I)


def day_of(s: str) -> str | None:
    m = re.search(DATE, s.lower())
    if not m or m.group(2) not in MONTHS:
        return None
    return f"{int(m.group(3)):04d}-{MONTHS[m.group(2)]:02d}-{int(m.group(1)):02d}"


def ruling_days(x: dict) -> list[tuple[str, str, str]]:
    """(court key, day, text) for every ruling a 'Jurisprudencia Vigencia' line declares INEXEQUIBLE (in whole or part)."""
    out = []
    for t in x.get("jv", []):
        if not re.search(r"INEXEQUIBLE", t) or re.search(r"estarse a lo resuelto|INHIBID", t, re.I):
            continue
        m = RUL.search(t)
        if not m:
            continue
        after = t[m.end():]
        d = day_of(after[:120])
        cm = re.search(r"Comunicado de Prensa (?:No\.?\s*\d+\s*)?de\s+" + DATE, after, re.I)
        if cm:
            d = day_of(cm.group(0))
        if d:
            out.append((E.court_key(m.group(1)), d, t))
    return out


def deacc(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def key(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", deacc(s.lower()))


def acts_in(text: str) -> list[str]:
    out = []
    for g in E.AL_RE.findall(text):
        try:
            out.append(E.al_key(*g))
        except Exception:  # noqa: BLE001
            pass
    return out


def law_days(x: dict) -> dict[str, str | None]:
    return {k: d for k, d in x.get("named", [])}


def para_marks(x: dict, lines: list[str]) -> list[str]:
    """Markers of the page paragraphs whose current words are one of `lines`."""
    want = {key(l) for l in lines if key(l)}
    out = []
    for post, pre, marks in x.get("paras", []):
        kp = key(post)
        if kp and any(kp == w or (len(kp) > 30 and (kp in w or w in kp)) for w in want):
            out += marks
    return out


def first_para_marks(x: dict) -> list[str]:
    for post, pre, marks in x.get("paras", []):
        if marks or post:
            return marks
    return []


VERB = re.compile(r"modificad|adicionad|subrogad|sustituid|reformad|derogad|corregid|eliminad|reemplazad", re.I)


def propose(x: dict, tag: str) -> dict:
    k, t = x["known_last"], x["today"]
    kb, tb = A.body(k), A.body(t)
    kind = T.kind(x)
    if kind == "heading" or kb == tb:
        return {"verdict": "harmless", "why": "heading"}
    dn = x["events"][-1][0]
    days = law_days(x)
    evl = {l for _, l in x["events"]}
    # 1. markers on the paragraphs holding today's words
    cands = []
    src = para_marks(x, t or []) if t else first_para_marks(x)
    for m in src:
        if not VERB.search(m):
            continue
        for a in acts_in(m):
            d = days.get(a) or (E.law_day(a) if a in E.LAWS else None)
            if a not in evl and d and d > dn:
                cands.append((a, d, "marker"))
    cands = sorted(set(cands), key=lambda c: c[1])
    if len({c[0] for c in cands}) == 1:
        return {"verdict": "fix", "end": cands[0][1], "credit": cands[0][0], "how": "marker"}
    # 2. struck words: a ruling dated after D
    ruls = sorted({(c, d) for c, d, _ in ruling_days(x) if d > dn}, key=lambda r: r[1])
    struck = any(pre != post for post, pre, _ in x.get("paras", [])) or any(
        re.search(r"INEXEQUIBLE", m) for m in x.get("marks", []))
    if struck and len(ruls) == 1 and not cands:
        return {"verdict": "fix", "end": ruls[0][1], "credit": ruls[0][0], "how": "ruling"}
    # 3. one act the notes name after D
    later = sorted({(a, d) for a, d in x.get("named", []) if a not in evl and d and d > dn and not a.startswith("c-")},
                   key=lambda c: c[1])
    if not cands and not ruls and len(later) == 1:
        return {"verdict": "fix", "end": later[0][1], "credit": later[0][0], "how": "notes"}
    return {"verdict": "manual", "cands": cands, "rulings": ruls, "later": later, "kind": kind}


def main(argv):
    rows = json.load(open(os.path.join(A.TMP, "audit.json"), encoding="utf-8"))
    out, cnt = [], Counter()
    for r in rows:
        if "records" not in r:
            out.append({"tag": r["tag"], "unit": r["unit"], "verdict": "manual", "why": "no record"})
            cnt["manual"] += 1
            continue
        ps = [propose(x, r["tag"]) for x in r["records"]]
        for i, p in enumerate(ps):
            p["rec"] = i
        verdict = "manual" if any(p["verdict"] == "manual" for p in ps) else (
            "fix" if any(p["verdict"] == "fix" for p in ps) else "harmless")
        out.append({"tag": r["tag"], "unit": r["unit"], "verdict": verdict, "parts": ps})
        cnt[verdict] += 1
        if verdict == "fix":
            cnt["fix:" + "+".join(sorted({p.get("how", "") for p in ps if p["verdict"] == "fix"}))] += 1
    json.dump(out, open(os.path.join(A.TMP, "proposals.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(dict(cnt))
    if "-v" in argv:
        for o in out:
            if o["verdict"] == "manual":
                print(o["tag"], o["unit"], [(p.get("kind"), p.get("cands"), p.get("rulings"), p.get("later")) for p in o.get("parts", []) if p["verdict"] == "manual"])


if __name__ == "__main__":
    main(sys.argv[1:])
