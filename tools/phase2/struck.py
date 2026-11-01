"""Amendments by decrees the Constitutional Court later struck down as a whole (Decreto 1122 de 1999, struck by
Sentencia C-923-99; Decreto 266 de 2000, struck by Sentencia C-1316-00).

The basedoc prints such an article with the text that stands today (the original wording, which revived when the Court
struck the amending decree, or a later valid amendment), names the decree in its 'Notas de Vigencia', names the ruling
in its 'Jurisprudencia Vigencia' and gives the decree's wording in a 'Legislación Anterior' block. The engine already
reads a block headed '... declarado INEXEQUIBLE ...' as wording that held from the decree's day until the ruling's day,
when the text before it returns (credited to the ruling). This module makes the page's other variants read the same:

- a block headed only 'Texto modificado por el Decreto 1122 de 1999:' (no 'INEXEQUIBLE') whose unit's
  'Jurisprudencia Vigencia' states the ruling gets ', declarado INEXEQUIBLE' added to its heading (without it the engine
  credited today's revived text to the struck decree);
- a heading whose last words ('declarado INEXEQUIBLE por la Corte Constitucional:') stand in a paragraph of their own
  is joined into one heading;
- typing slips in the blocks' article headings ('ARTÏCULO 14.', 'ARTÍCULO4.') that stop the engine from reading the
  block's text are corrected.

A unit whose notes name one of the decrees but whose rulings box does not state that decree's ruling stops the parse
(listed in UNCONFIRMED unless allowed in ALLOW_UNCONFIRMED with a reason).

install(E, P, pages) wraps P.doc_units / E.doc_units for the given pages. DONE lists what was changed, for decisions.
"""
from __future__ import annotations

import re

DECREES = {
    # decree as the notes name it -> regex for its ruling in a 'Jurisprudencia Vigencia' box (plain text)
    "Decreto 1122 de 1999": re.compile(r"INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-923-99 del 18 de "
                                       r"noviembre de 1999"),
    "Decreto 266 de 2000": re.compile(r"INEXEQUIBLE por la Corte Constitucional mediante Sentencia C-1316-(?:00|2000) del "
                                      r"26 de septiembre de 2000"),
}
SPAN = re.compile(r"(<span class='b_aj'>)(.*?)(</span>)", re.S)
PARA = re.compile(r"<p\b[^>]*>(.*?)</p>", re.S | re.I)
TYPOS = [
    (re.compile(r"ART(?:&Iuml;|Ï)CULO"), "ART&Iacute;CULO", "'ARTÏCULO' read as 'ARTÍCULO'"),
    (re.compile(r"(ART(?:&Iacute;|Í|I)CULO)(\d)"), r"\1 \2", "'ARTÍCULO4.' read as 'ARTÍCULO 4.'"),
]
DONE: list[str] = []
UNCONFIRMED: list[str] = []
ALLOW_UNCONFIRMED: dict[tuple[str, str], str] = {}


def install(E, P, pages: set[str]) -> None:
    inner = P.doc_units

    def _done(x):
        if x not in DONE:
            DONE.append(x)

    def doc_units(name: str) -> list[dict]:
        units = inner(name)
        if name not in pages:
            return units
        kind, num0, year = re.fullmatch(r"(ley|decreto)_0*(\d+)_(\d{4})", name).groups()
        own = f"{kind.capitalize()} {num0} de {year}"
        for u in units[1:]:
            nv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas de Vigencia")
            named = [d for d in DECREES if d in nv]
            if not named:
                continue
            jv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Jurisprudencia Vigencia")
            num = E.label_num(u["label"] or "") or u["name"]
            confirmed = []
            for d in named:
                if DECREES[d].search(jv):
                    confirmed.append(d)
                elif (name, num) not in ALLOW_UNCONFIRMED:
                    UNCONFIRMED.append(f"{name} art. {num}: {d}")
            items, skip_next = [], set()
            for it in u["items"]:
                if it[0] == "box" and it[1] == "Legislación Anterior":
                    h = it[2]
                    ps = list(PARA.finditer(h))
                    out, k = [], 0
                    for i, m in enumerate(ps):
                        if i and ps[i - 1].group(0) in skip_next:
                            out.append(h[k:m.start()])
                            k = m.end()
                            continue
                        t = E.tidy(E.plain(m.group(1)))
                        rest = re.sub("|".join(map(re.escape, confirmed + [own])), "", t) if confirmed else t
                        if not (t.lower().startswith("texto") and "INEXEQUIBLE" not in t.upper()
                                and any(d in t for d in confirmed) and not E.AL_RE.search(rest)
                                and SPAN.search(m.group(1))):
                            continue
                        nxt = E.tidy(E.plain(ps[i + 1].group(1))) if i + 1 < len(ps) else ""
                        if re.match(r"(?:el cual fue )?declarado INEXEQUIBLE", nxt):
                            # the heading's last words stand in a paragraph of their own: joined to it
                            add = " " + nxt.rstrip(" :")
                            skip_next.add(m.group(0))
                            why = f"heading '{t} / {nxt}' read as one heading"
                        else:
                            add = ", declarado INEXEQUIBLE"
                            why = f"heading '{t}' read as struck ({', '.join(confirmed)})"
                        last = list(SPAN.finditer(m.group(0)))[-1]
                        body = last.group(2).rstrip()
                        colon = body.endswith(":") or bool(re.match(r"(?:el cual fue )?declarado INEXEQUIBLE.*:$", nxt))
                        new_p = (m.group(0)[:last.start()] + last.group(1) + body.rstrip(": ,") + add + (":" if colon else "")
                                 + last.group(3) + m.group(0)[last.end():])
                        out.append(h[k:m.start()] + new_p)
                        k = m.end()
                        _done(f"{name} art. {num}: {why}")
                    h = "".join(out) + h[k:]
                    for rx, new, why in TYPOS:
                        h2 = rx.sub(new, h)
                        if h2 != h:
                            _done(f"{name} art. {num}: {why}")
                            h = h2
                    it = (it[0], it[1], h) + tuple(it[3:])
                items.append(it)
            u["items"] = items
        if UNCONFIRMED:
            raise SystemExit("struck decrees named without their ruling: " + "; ".join(UNCONFIRMED))
        return units

    P.doc_units = doc_units
    E.doc_units = doc_units


def history(act: dict, key: str) -> list[tuple[str, dict | None, list | None]]:
    """The unit's changes in the act as built (every version holds full units): [(day, unit or None, credits)]."""
    out, prev, full = [], object(), {}
    for v in act["versions"]:
        full = v.get("units", full)  # a version that changed no words keeps no units
        u = full.get(key)
        cr = v["credits"].get(key)
        if u != prev or cr:
            out.append((v["from"], u, cr))
            prev = u
    return out


def respan(act: dict, key: str, spans: list[tuple], missing_line: str) -> list[tuple]:
    """Set the periods in which a struck decree's wording held, over the engine's history of the other acts.

    spans: [(decree law, decree day, ruling law, ruling day, lines | None | False)] with lines = the article's text
    lines while the decree held (None: the source does not give them, so the placeholder line; False: the decree
    repealed the article, so absent). The engine's changes credited to the decrees or their rulings, or dated inside a
    span, are dropped; at each ruling's day the text that stood before the decree returns, credited to the ruling.
    A change by another act inside a span stops the parse. Returns the new history."""
    struck = {d for d, *_ in spans} | {r for _, _, r, *_ in spans}
    h = history(act, key)
    label = next(u["label"] for _, u, _ in h if u is not None)
    for day, _, cr in h:
        for d, d0, r, r0, _ in spans:
            if d0 < day < r0 and not set(cr or []) <= struck:
                raise SystemExit(f"{act['slug']} {key}: {cr} on {day} inside the span of {d}")
    base = [(day, u, cr) for day, u, cr in h if not set(cr or []) & struck]
    events = []
    for d, d0, r, r0, lines in spans:
        if lines is False:
            u = None
        else:
            body = missing_line if lines is None else "\n".join(lines)
            u = {"label": label, "kind": "art", "text": f"# {label}\n{body}\n"}
        events.append((d0, u, [d], "decree"))
        events.append((r0, None, [r], "ruling"))
    vs = act["versions"]
    for day, *_ in events:
        if not any(v["from"] == day for v in vs):
            prev = next(v for v in reversed(vs) if v["from"] < day and "units" in v)
            k = next((i for i, v in enumerate(vs) if v["from"] > day), len(vs))
            vs.insert(k, {"from": day, "units": dict(prev["units"]), "credits": {}, "source_url": prev["source_url"],
                          "sha256": prev["sha256"]})
    timeline = sorted([(day, u, cr, "base") for day, u, cr in base] + events, key=lambda x: x[0])
    state, out = None, []
    valid = None
    for day, u, cr, what in timeline:
        if what == "base":
            state = valid = u
        elif what == "decree":
            state = u
        else:
            state = valid
        out.append((day, state, cr))
    days = {}
    for day, u, cr in out:
        days[day] = (u, cr)
    cur, full = None, {}
    for v in vs:
        if v["from"] in days:
            cur, cr = days[v["from"]]
            if cr:
                v["credits"][key] = list(cr)
            else:
                v["credits"].pop(key, None)
            if "units" not in v:
                v["units"] = dict(full)
        elif "units" in v:
            v["credits"].pop(key, None)
        if "units" not in v:
            continue
        v["units"] = dict(v["units"])
        if cur is None:
            v["units"].pop(key, None)
        else:
            v["units"][key] = cur
        full = v["units"]
    return out
