"""Article words under heading-named anchors, by page (quoted-heading scan, 2026-10-31).

The basedoc sometimes gives words of an article an anchor named like a heading ('Nivel001', 'Nivel-309', 'TITULO I',
'CAPÍTULO II-I-I'). The engine reads every such unit as a heading, so its words went into titulos.md (or, for a run of
such units, were dropped: a heading line only shows while an article follows it) and the article lost them. Each page
here gets the repairs listed for it, and only those; a repair that no longer finds its unit stops the parse (the page
changed). Kinds:

  ("head", anchor, num)        a unit named `anchor` with no heading whose first paragraph starts with the article's
                               heading ('<span class="b_aj">ARTÍCULO 642. ...</span>'): it is art. num;
  ("split", anchor, num)       a heading unit named `anchor` whose paragraphs go on with art. num's heading in bold
                               ('<B>ARTÍCULO 5o. ...</B>'): the heading keeps the paragraphs before it, the rest is art. num;
  ("label", anchor, num, bad, good)  a unit named `anchor` whose heading misspells 'ARTÍCULO' (`bad`, e.g. 'ARTICUL0'
                               with a zero): it is art. num, its heading with `good`;
  ("tail", num, anchor, n)     the n units right after art. num, each named `anchor` with no heading of its own, are the
                               rest of art. num (their paragraphs and note boxes are joined to it, after "tail_at").

A joined tail is today's text of the article's last part, and the history (install(E)) reads it so: the engine builds
the article's history from the article without its tail, as it did before the repair, and the tail's lines (as the
check reads today's text) end every state equal to the article's last one. The tail's note boxes are not read for the
history: for the articles listed (Estatuto Orgánico del Sistema Financiero arts. 193, 218, 270) the engine's reading
of them mixed texts of different years in one version (earlier wordings of other numerals beside today's), and the
tails' words came with the article's last text (Ley 2294 de 2023 for arts. 112, 183, 193 and Ley 715 art. 84A, whose
pages print those words in the amending article itself).

repair(name, units, E, rules) returns the repaired units (the input is not changed) and records what it did in
DONE[name]. The published parts were patched in place to match by ../fix_quoted_heads.py.
"""
from __future__ import annotations

import re

DONE: dict[str, list[str]] = {}
_ART = r"ART(?:Í|&Iacute;|I)CULO\s+(\d+[A-Z]?)(?:o|º)?\."
SPAN_HEAD = re.compile(r'\s*<span class="b_aj">\s*(' + _ART + r'(?:(?!</span>).)*?)\s*</span>', re.S)
BOLD_HEAD = re.compile(r"\s*<[Bb]>\s*(" + _ART + r".*?)\s*</[Bb]>", re.S)


def _blank(u) -> bool:
    return not (u.get("label") or "").strip()


def _text(E, it) -> str:
    return E.plain(it[1]).strip() if it[0] == "p" else ""


def repair(name: str, units: list[dict], E, rules: dict) -> list[dict]:
    todo = rules.get(name)
    if not todo:
        return units
    units = [dict(u, items=list(u["items"])) for u in units]
    done = []
    for rule in todo:
        kind = rule[0]
        if kind == "head":
            _, anchor, num = rule
            hits = []
            for i, u in enumerate(units):
                if u["name"] != anchor or not _blank(u):
                    continue
                k = next((k for k, it in enumerate(u["items"]) if it[0] == "p" and _text(E, it)), None)
                m = SPAN_HEAD.match(u["items"][k][1]) or BOLD_HEAD.match(u["items"][k][1]) if k is not None else None
                if m and m.group(2) == num:
                    hits.append((i, k, m))
            if len(hits) != 1:
                raise SystemExit(f"{name}: repair {rule} found {len(hits)} units (the page changed)")
            i, k, m = hits[0]
            u = units[i]
            items = u["items"][:k] + [("p", u["items"][k][1][m.end():]) + tuple(u["items"][k][2:])] + u["items"][k + 1:]
            units[i] = dict(u, name=num, label=E.tidy(E.plain(m.group(1))), items=items)
            done.append(f"art. {num} (its heading in the text, under an anchor named '{anchor}')")
        elif kind == "split":
            _, anchor, num = rule
            hits = []
            for i, u in enumerate(units):
                if u["name"] != anchor:
                    continue
                for k, it in enumerate(u["items"]):
                    m = BOLD_HEAD.match(it[1]) if it[0] == "p" else None
                    if m and m.group(2) == num:
                        hits.append((i, k, m))
            if len(hits) != 1:
                raise SystemExit(f"{name}: repair {rule} found {len(hits)} units (the page changed)")
            i, k, m = hits[0]
            u = units[i]
            art = {"name": num, "label": E.tidy(E.plain(m.group(1))), "page": u.get("page"),
                   "items": [("p", u["items"][k][1][m.end():]) + tuple(u["items"][k][2:])] + u["items"][k + 1:]}
            units[i:i + 1] = [dict(u, items=u["items"][:k]), art]
            done.append(f"art. {num} (in the heading unit '{anchor}' after the heading's words)")
        elif kind == "label":
            _, anchor, num, bad, good = rule
            hits = [i for i, u in enumerate(units) if u["name"] == anchor and (u["label"] or "").startswith(bad + " " + num)]
            if len(hits) != 1:
                raise SystemExit(f"{name}: repair {rule} found {len(hits)} units (the page changed)")
            u = units[hits[0]]
            units[hits[0]] = dict(u, name=num, label=good + u["label"][len(bad):])
            done.append(f"art. {num} (its heading spelt '{bad}', under an anchor named '{anchor}')")
        elif kind == "tail":
            _, num, anchor, n = rule
            hits = [i for i, u in enumerate(units) if u["name"] == num and re.match(r"ART[IÍ]CULO", u["label"] or "")]
            if len(hits) != 1:
                raise SystemExit(f"{name}: repair {rule}: art. {num} found {len(hits)} times (the page changed)")
            i = hits[0]
            run = units[i + 1:i + 1 + n]
            after = units[i + 1 + n] if i + 1 + n < len(units) else None
            if (len(run) != n or any(u["name"] != anchor or not _blank(u) for u in run)
                    or (after is not None and after["name"] == anchor and _blank(after))):
                raise SystemExit(f"{name}: repair {rule}: the units after art. {num} are not {n} '{anchor}' blocks "
                                 f"(the page changed)")
            u = units[i]
            if "tail_at" in u:
                raise SystemExit(f"{name}: repair {rule}: art. {num} already has a tail")
            units[i:i + 1 + n] = [dict(u, items=u["items"] + [it for r in run for it in r["items"]], tail_at=len(u["items"]))]
            done.append(f"art. {num} ({n} blocks under anchors named '{anchor}')" if n > 1
                        else f"art. {num} (1 block under an anchor named '{anchor}')")
        else:
            raise SystemExit(f"headjoin: unknown repair {rule}")
    DONE[name] = done
    return units


def decision(title: str, done: list[str] | None) -> list[str]:
    """The part's decision sentence for one act's repairs ([] when none); ../fix_quoted_heads.py writes the same one."""
    if not done:
        return []
    return [f"{title}: article words the page puts under anchors named like headings ('Nivel001', 'TITULO I', ...) had "
            f"been read as headings, so they were missing from their articles (in titulos.md, or nowhere); they are back in "
            f"them (quoted-heading scan, 2026-10-31; phase2/headjoin.py): " + "; ".join(done) + "."]


def tail_lines(E, u: dict) -> list[str]:
    """Today's lines of a joined tail, read as the checks read today's text (struck words out unless a tacit marker
    keeps them; publisher markers and page links dropped)."""
    out = []
    for it in u["items"][u["tail_at"]:]:
        if it[0] != "p" or "antsig" in it[1]:
            continue
        tacit = any(E.TACIT.search(m) for m in E.markers(it[1]))
        t = E.tidy(E.to_text(it[1], keep_struck=tacit))
        if t and re.search(r"\w", t):
            out.append(t)
    return out


def install(E) -> None:
    """Wrap E.article_history (once) so that an article with a joined tail keeps the history of the article without it,
    the tail's lines ending every state equal to its last."""
    if getattr(E.article_history, "headjoin", False):
        return
    orig = E.article_history

    def article_history(u: dict, *a, **k) -> dict:
        if "tail_at" not in u:
            return orig(u, *a, **k)
        h = orig(dict(u, items=u["items"][:u["tail_at"]]), *a, **k)
        last = h["states"][-1][1]
        if not isinstance(last, list) or not last:
            raise SystemExit(f"headjoin: {u['name']}: the article's last state holds no text, its tail has nowhere to go")
        tl = tail_lines(E, u)
        return dict(h, states=[(d, (s + tl) if isinstance(s, list) and s == last else s, law) for d, s, law in h["states"]])

    article_history.headjoin = True
    E.article_history = article_history
