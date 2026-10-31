"""Words the source shows replaced in place: '<S>old words</S> <*new words>' or '<S>old</S> <new*>'. The struck words are
the earlier text and the words in angle brackets with an asterisk are the text that replaced them; the asterisk points
to the note that says what replaced them (a ruling that ordered the change, such as Sentencia C-458 de 2015, or an act
that substituted an expression). The engine reads the struck words as struck and the bracketed words as an editor's
marker, so both would be lost.

install(E, pages) rewrites each such pair on those pages' HTML into one token '⟦old¦new⟧' before the engine reads them.
resolve(act, rules, E) then gives each version the old words before the rule's day and the new ones from it, adds a
version on that day if the act has none, and credits the change to the rule's law. Every token must have a rule.
today_new(lines) turns tokens in a check's 'today' text into the new words.
"""
from __future__ import annotations

import re

SUB = re.compile(r"((?:<S>(?:(?!</?S>).)*?</S>\s*)+)&lt;(\*(?:(?!&gt;).)+|(?:(?!&gt;).)+\*)&gt;", re.S)
STRUCK = re.compile(r"<S>((?:(?!</?S>).)*?)</S>", re.S)
TOKEN = re.compile(r"⟦(.*?)¦(.*?)⟧", re.S)
SEEN: dict[str, list[tuple[str, str]]] = {}


def _rewrite(page: str, html: str) -> str:
    def rep(m):
        # One or more struck spans in a row ('<S>y</S> <S>minusvalía</S> <e invalidez*>') are the old words together.
        old = " ".join(x.strip() for x in STRUCK.findall(m.group(1)) if x.strip())
        new = m.group(2).strip().strip("*").strip()
        SEEN.setdefault(page, []).append((old, new))
        return f"⟦{old}¦{new}⟧ "
    return SUB.sub(rep, html)


def install(E, pages: set[str]) -> None:
    """Rewrite the pairs on these pages' HTML as E.read returns it (once per process; later calls add pages)."""
    read = E.read
    if getattr(read, "_subst_pages", None) is not None:
        read._subst_pages |= set(pages)
        return
    pages_ref = set(pages)

    def read_any(url: str):
        t = read(url)
        if t is None or not url.endswith(".html"):
            return t
        base = re.sub(r"_pr\d{3}$", "", url.rsplit("/", 1)[-1][:-5])
        return _rewrite(base, t) if base in pages_ref else t

    read_any._subst_pages = pages_ref
    E.read = read_any


def pick(text: str, new: bool) -> str:
    return TOKEN.sub(lambda m: m.group(2) if new else m.group(1), text)


def resolve(act: dict, rules: dict, E, done: list[str]) -> None:
    """rules: {unit key: (law key, day, why)}. Versions hold full units."""
    vs = act["versions"]
    for key, (law, day, _) in sorted(rules.items()):
        on_day = [v for v in vs if v["from"] == day]
        if on_day and "units" not in on_day[-1]:
            # A version on that day that changed no words (the ruling's own note): it now holds the change.
            prev = next(v for v in reversed(vs) if v["from"] < day and "units" in v)
            on_day[-1]["units"] = dict(prev["units"])
        if not on_day:
            prev = next((v for v in reversed(vs) if v["from"] < day and "units" in v), None)
            if prev is not None:
                k = next((i for i, v in enumerate(vs) if v["from"] > day), len(vs))
                vs.insert(k, {"from": day, "units": dict(prev["units"]), "credits": {}, "source_url": prev["source_url"],
                              "sha256": prev["sha256"]})
    tokened = set()
    for v in vs:
        if "units" not in v:
            continue
        for k, u in list(v["units"].items()):
            if "⟦" not in u["text"]:
                continue
            if k not in rules:
                raise SystemExit(f"{act['slug']} {k}: replaced words with no rule: {TOKEN.findall(u['text'])}")
            tokened.add(k)
    for key in sorted(tokened):
        law, day, why = rules[key]
        if E.LAWS.get(law, {}).get("kind") == "court":
            # A ruling that ordered words replaced changes the text: not the note of a ruling that only conditioned it.
            E.LAWS[law]["note"] = None
        before = None
        for v in vs:
            if "units" not in v or key not in v["units"]:
                before = None if "units" in v else before
                continue
            u = v["units"][key]
            t = pick(u["text"], v["from"] >= day)
            if v["from"] == day and before is not None and before != t:
                v["credits"][key] = sorted(set(v["credits"].get(key) or []) | {law})
            if t != u["text"]:
                v["units"] = dict(v["units"])
                v["units"][key] = dict(u, text=t)
            before = t
        done.append(f"{act['title'].split(' (')[0]} {key} ({E.LAWS[law]['label']}, {day}: {why})")
    for key in rules:
        if key not in tokened:
            raise SystemExit(f"{act['slug']} {key}: rule with no replaced words")


def today_new(lines: list[str]) -> list[str]:
    return [pick(l, True) for l in lines]
