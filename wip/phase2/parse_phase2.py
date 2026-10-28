"""Build corpus.d/60-phase2.json for Colombia: Código Penal (Ley 599 de 2000), Código General del Proceso
(Ley 1564 de 2012) and Código Sustantivo del Trabajo.

Reads only ../.cache/ (written by ../fetch.py and phase2/fetch_phase2.py); no network. Deterministic.
The reconstruction engine is phase2/engine.py (a frozen copy of the codes helper's codes/parse_codes.py, itself a
generalisation of ../parse.py): per provision, versions are rebuilt from the basedoc's earlier texts ("Legislación
Anterior"), its inline amendment markers and its Notas de Vigencia; in-force days of amending acts come from their own
vigencia clauses (their basedoc pages) or the default rule.

Usage:  python -X utf8 phase2/parse_phase2.py [--report] [--out FILE] [--only codigo-penal,...]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import engine as E  # noqa: E402

OUT = os.path.join(COUNTRY, "corpus.d", "60-phase2.json")
SIGN_OFF = re.compile(r"\s*(El Presidente del (honorable |H\. )?Senado|EL PRESIDENTE DEL (HONORABLE |H\. )?SENADO|"
                      r"REP[ÚU]BLICA DE COLOMBIA\s*-\s*GOBIERNO NACIONAL|PUBL[ÍI]QUESE Y (EJEC[ÚU]TESE|C[ÚU]MPLASE))")

_doc_units = E.doc_units


def doc_units(name: str) -> list[dict]:
    """The engine's split, with the signatures after the last article cut off (they are not part of the text)."""
    units = _doc_units(name)
    for u in units[1:]:
        items = u["items"]
        for k, it in enumerate(items):
            if it[0] == "p" and SIGN_OFF.match(E.plain(it[1])):
                # the signer's name stands on the paragraph before "El Presidente ..."
                cut = k - 1 if k > 0 and items[k - 1][0] == "p" and E.plain(items[k - 1][1]).isupper() else k
                u["items"] = items[:cut]
                break
    return units


E.doc_units = doc_units


def para_text(units: list[dict], anchor: str) -> str:
    u = next(u for u in units if u["name"] == anchor)
    return " ".join(E.plain(E.strip_markers(it[1])) for it in u["items"] if it[0] == "p")


def first_law(key: str, page: str, title: str, units: list[dict], vig_anchor: str | None, rule_note: str) -> str:
    """Register the act itself, dated by its own heading (sanction, Diario Oficial) and its own vigencia article."""
    kind, n, y = key.split("-")
    enacted, pub = E.page_header(page, y)
    E.register(key)
    law = E.LAWS[key]
    law.update({"title": title, "enacted": enacted, "published": pub, "url": E.BASE + page + ".html"})
    return enacted, pub


def finish(res: dict, page: str) -> list[dict]:
    sha = E.doc_sha(page)
    for v in res["versions"]:
        v["source_url"] = E.BASE + page + ".html"
        v["sha256"] = sha
    return res["versions"]


DECISIONS: list[str] = []


def build_penal() -> dict:
    page = "ley_0599_2000"
    units = doc_units(page)
    E.scan_law_dates(units)
    key = "ley-599-2000"
    enacted, pub = first_law(key, page, "Por la cual se expide el Código Penal", units, "476", "")
    clause = para_text(units, "476")
    m = re.search(r"un \(1\) año después de su promulgación", clause)
    if not m or not pub:
        raise SystemExit(f"Código Penal: vigencia clause or publication day not found ({clause!r}, {pub})")
    start = E.add_months(pub, 12)
    E.IN_FORCE[key], E.IN_FORCE_WHY[key] = start, f"Ley 599 de 2000, art. 476: '{clause}'"
    res = E.build_act(page, start)
    vs = finish(res, page)
    vs[0]["note"] = (f"The code as enacted (Ley 599 de 2000, sanctioned {enacted}, Diario Oficial No. 44.097 of {pub}), in "
                     f"force from {start} under its art. 476: '{clause}'")
    DECISIONS.append(
        "Código Penal: the figures of the penalties in the Parte Especial after 1 January 2005 are the publisher's: Ley 890 "
        "de 2004, art. 14, raised every penalty of the Parte Especial by a third in the minimum and a half in the maximum "
        "without rewriting the articles, and the source shows each article 'con las penas aumentadas' under the marker "
        "'<Penas aumentadas por el artículo 14 de la Ley 890 de 2004, a partir del 1o. de enero de 2005>', with the "
        "earlier wording in its Legislación Anterior. Those changes are credited to Ley 890 de 2004 on 1 January 2005; "
        "the source's own warning says the computation is the editor's reading of art. 14.")
    return {"slug": "codigo-penal", "short": "CPen", "title": "Código Penal (Ley 599 de 2000)", "url": E.BASE + page + ".html",
            "first_law": key, "earlier_laws": [], "versions": vs}


BUILDERS = {"codigo-penal": build_penal}


def main(argv: list[str]) -> None:
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else list(BUILDERS)
    acts = [BUILDERS[s]() for s in BUILDERS if s in only]
    used = {l for a in acts for v in a["versions"] for ls in v["credits"].values() for l in ls} | {a["first_law"] for a in acts}
    laws = {k: dict(v) for k, v in sorted(E.LAWS.items()) if k in used}
    rules = [f"In force {E.IN_FORCE[k]}: {laws[k]['label']} ({E.IN_FORCE_WHY[k]})."
             for k in sorted(laws, key=lambda k: (E.IN_FORCE.get(k, ""), k)) if k in E.IN_FORCE]
    part = {
        "sources": [{
            "name": "Secretaría General del Senado, basedoc: Código Penal, Código General del Proceso, Código Sustantivo "
                    "del Trabajo and the acts that amended them",
            "url": E.BASE, "retrieved": E.RETRIEVED, "requests": 0,
            "licence": "Official legal text is free to reproduce (Ley 23 de 1982, art. 41). The compilation's editorial notes "
                       "(Avance Jurídico) are not reproduced; only the official text and the facts the notes state are used.",
            "notes": "ley_0599_2000, ley_1564_2012 and codigo_sustantivo_trabajo (base, continuation pages and js/ note "
                     "files), plus the base and last page of each amending act. Requests are counted in the country's "
                     "shared log (corpus.json's source)."}],
        "laws": laws,
        "acts": acts,
        "decisions": [
            "Código Penal, Código General del Proceso and Código Sustantivo del Trabajo (phase2/parse_phase2.py, with the "
            "engine phase2/engine.py): versions are rebuilt per article from the basedoc's earlier texts, inline "
            "amendment markers and Notas de Vigencia, as for the Constitution and the Código Civil. Where the source names "
            "an act but gives no text after it, the article reads '" + E.MISSING_LINE + "' for that period.",
            "Constitutional Court rulings that struck text are laws of kind 'court', dated by the ruling's day as the "
            "source gives it; rulings that upheld text on a condition are court laws with a note and change no words.",
            "In-force days of amending acts: the act's own vigencia clause as its basedoc page gives it; otherwise the "
            "default rule (Ley 4 de 1913, art. 52: two months after promulgation). A day a provision's own note gives "
            "applies to that provision. The list below gives the day and the rule for each act.",
        ] + DECISIONS + rules,
        "ai_use": ["None at data-build time: phase2/fetch_phase2.py, phase2/parse_phase2.py and phase2/engine.py are "
                   "deterministic code, written with Claude Code (claude-opus-5-5); no model reads, writes or summarises "
                   "legal text."],
    }
    out = argv[argv.index("--out") + 1] if "--out" in argv else OUT
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, out)
    print(f"wrote {out}: {len(acts)} acts, {sum(len(a['versions']) for a in acts)} versions, {len(laws)} laws, "
          f"{os.path.getsize(out) // 1024} KB")
    for a in acts:
        print(f"  {a['slug']}: {len(a['versions'])} versions")
    if "--report" in argv:
        for r in E.REPORT:
            print("  ", r)
    else:
        print(f"  {len(E.REPORT)} report lines (--report to print)")


if __name__ == "__main__":
    main(sys.argv[1:])
