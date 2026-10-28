"""Build corpus.d/70-cst.json for Colombia: the Código Sustantivo del Trabajo (CST).

Reads only ../.cache/ (written by ../fetch.py, ../phase2/fetch_phase2.py and cst/fetch_cst.py); no network.
Deterministic. The reconstruction engine is cst/engine.py (a copy of phase2/engine.py, itself the codes helper's
codes/parse_codes.py): per provision, versions are rebuilt from the basedoc's earlier texts ("Legislación
Anterior"), its inline amendment markers and its Notas de Vigencia; in-force days of amending acts come from their own
vigencia clauses (their basedoc pages) or the default rule. This driver began as build_cst() in phase2/parse_phase2.py.

Usage:  python -X utf8 cst/parse_cst.py [--report] [--out FILE]
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

OUT = os.path.join(COUNTRY, "corpus.d", "70-cst.json")
PAGE = "codigo_sustantivo_trabajo"
SIGN_OFF = re.compile(r"\s*(El Presidente del (honorable |H\. )?Senado|EL PRESIDENTE DEL (HONORABLE |H\. )?SENADO|"
                      r"REP[ÚU]BLICA DE COLOMBIA\s*-\s*GOBIERNO NACIONAL|PUBL[ÍI]QUESE Y (EJEC[ÚU]TESE|C[ÚU]MPLASE))")

_doc_units = E.doc_units


def doc_units(name: str) -> list[dict]:
    """The engine's split, with the signatures after the last article cut off (they are not part of the text)."""
    units = _doc_units(name)
    for u in units:
        # "<Penas aumentadas por el artículo 14 de la Ley 890 de 2004 ...>" is how the Código Penal marks an article
        # whose penalties Ley 890 raised (with its earlier text in Legislación Anterior): for the engine it is an
        # article-level change by that law. Only the marker is rewritten; markers are never part of the text.
        # "<Ley 1288 de 2009 declarada INEXEQUIBLE>" on an article that law added: the whole article was struck.
        u["items"] = [(it[0], re.sub(r"&lt;Ley \d+ de \d{4} declarada INEXEQUIBLE&gt;", "&lt;Artículo INEXEQUIBLE&gt;",
                                     re.sub(r"&lt;Penas? aumentadas? por el art", "&lt;Artículo modificado por el art", it[1])))
                      + tuple(it[2:]) if it[0] == "p" else it for it in u["items"]]
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


DECISIONS: list[str] = []


BRACED = {"empleador": "patrono", "empleadores": "patronos", "EMPLEADOR": "PATRONO", "EMPLEADORES": "PATRONOS"}


def debrace(text: str, before: bool) -> str:
    """'{empleador}': Ley 50 de 1990 art. 107 replaced 'patrono' with 'empleador' throughout the code; the source shows
    the replaced word in braces. Before that law the word was 'patrono'."""
    def rep(m):
        w = m.group(1)
        return BRACED[w] if before and w in BRACED else w
    return re.sub(r"\{([^{}\n]{1,40})\}", rep, text)


def build_cst() -> dict:
    page = "codigo_sustantivo_trabajo"
    units = doc_units(page)
    E.scan_law_dates(units)
    head = " ".join(E.plain(it[1]) for it in units[0]["items"] if it[0] == "p")
    m = re.search(r"Diario Oficial No\.? ?27\.622, del (\d+ de \w+ de \d{4})", head)
    start = E.date_es(m.group(1)) if m else None
    clause = para_text(units, "490")
    if not start or "primero (1o) de enero del año de mil novecientos cincuenta y uno" not in clause:
        raise SystemExit("CST: edition day or art. 490 not found")
    earlier = []
    for k in ("dec-2663-1950", "dec-3743-1950", "dec-905-1951"):
        E.register(k)
        earlier.append(k)
    res = E.build_act(page, start)
    vs = res["versions"]
    # Ley 50 de 1990, art. 107: 'patrono' -> 'empleador' everywhere (shown in braces).
    l50 = E.register("ley-50-1990")
    d50 = E.law_day(l50)
    if not d50:
        raise SystemExit("CST: Ley 50 de 1990 has no in-force day")
    out, prev = [], None
    inserted = False
    for v in vs:
        if not inserted and v["from"] >= d50:
            base = prev
            if v["from"] > d50 and base is not None:
                out.append({"from": d50, "units": {k: dict(u, text=debrace(u["text"], False)) for k, u in base.items()},
                            "credits": {}})
                prev_units_new = out[-1]["units"]
                old = {k: dict(u, text=debrace(u["text"], True)) for k, u in base.items()}
                out[-1]["credits"] = {k: [l50] for k, u in prev_units_new.items() if old.get(k, {}).get("text") != u["text"]}
            inserted = True
        if "units" in v:
            before = v["from"] < d50
            new_units = {k: dict(u, text=debrace(u["text"], before)) for k, u in v["units"].items()}
            if v["from"] == d50 and prev is not None:
                old = {k: dict(u, text=debrace(u["text"], True)) for k, u in prev.items()}
                for k, u in new_units.items():
                    if old.get(k, {}).get("text") != u["text"] and l50 not in v["credits"].get(k, []):
                        v["credits"].setdefault(k, []).append(l50)
            prev = v["units"]
            v = dict(v, units=new_units)
        out.append(v)
    vs = out
    sha = E.doc_sha(page)
    for v in vs:
        v["source_url"] = E.BASE + page + ".html"
        v["sha256"] = sha
    vs[0]["note"] = (f"The official edition of the code ordered by Decreto 3743 de 1950, art. 46, published in Diario Oficial "
                     f"No. 27.622 of {start}, compiling Decretos 2663 and 3743 de 1950 and 905 de 1951, as the source gives "
                     f"it. Its art. 490: '{clause}' The edition's text is dated from its publication; the source does not "
                     "give the text of 1 January 1951.")
    DECISIONS.append(
        "Código Sustantivo del Trabajo: the oldest text the source gives is the official edition published in Diario Oficial "
        f"No. 27.622 of {start}; it is the first version (credited as oldest version available, naming Decretos 2663 and "
        "3743 de 1950 and 905 de 1951). Ley 50 de 1990, art. 107, replaced the word 'patrono' with 'empleador' "
        "throughout the code; the source shows the replaced word in braces ('{empleador}', its Resumen de Notas de "
        f"Vigencia, note 74). Before {d50} those words read 'patrono(s)', from {d50} 'empleador(es)', credited to Ley 50 "
        "de 1990; the braces are dropped.")
    return {"slug": "codigo-sustantivo-del-trabajo", "short": "CST", "title": "Código Sustantivo del Trabajo",
            "url": E.BASE + page + ".html", "first_law": None, "earlier_laws": earlier, "versions": vs}


def to_deltas(versions: list[dict]) -> list[dict]:
    """After the first version, each version gives `changes` ({unit key: unit, or None to remove}) instead of the full
    `units` (SCHEMA.md, "Large acts"); versions that changed no words keep no units at all."""
    out, prev = [], None
    for v in versions:
        if "units" not in v or prev is None:
            out.append(v)
            if "units" in v:
                prev = v["units"]
            continue
        cur = v["units"]
        ch = {k: cur[k] for k in cur if prev.get(k) != cur[k]}
        ch.update({k: None for k in prev if k not in cur})
        w = {k: x for k, x in v.items() if k != "units"}
        w["changes"] = dict(sorted(ch.items()))
        out.append(w)
        prev = cur
    return out


def full_versions(versions: list[dict]) -> list[dict]:
    """The inverse of to_deltas (for checks): every version with its full units."""
    out, cur = [], None
    for v in versions:
        if "units" in v:
            cur = dict(v["units"])
        elif "changes" in v:
            cur = dict(cur)
            for k, u in v["changes"].items():
                if u is None:
                    cur.pop(k, None)
                else:
                    cur[k] = u
        out.append(dict({k: x for k, x in v.items() if k != "changes"}, units=cur))
    return out



def write_part(act: dict, out: str) -> None:
    acts = [act]
    used = ({l for a in acts for v in a["versions"] for ls in v["credits"].values() for l in ls}
            | {a["first_law"] for a in acts if a["first_law"]} | {l for a in acts for l in a["earlier_laws"]})
    laws = {k: dict(v) for k, v in sorted(E.LAWS.items()) if k in used}
    rules = [f"In force {E.IN_FORCE[k]}: {laws[k]['label']} ({E.IN_FORCE_WHY[k]})."
             for k in sorted(laws, key=lambda k: (E.IN_FORCE.get(k, ""), k)) if k in E.IN_FORCE]
    approx = sorted({r.split(":")[0] for r in E.REPORT if "latest earlier text differs" in r and r.startswith(PAGE)})
    part = {
        "sources": [{
            "name": "Secretaría General del Senado, basedoc: Código Sustantivo del Trabajo and the acts that amended it",
            "url": E.BASE + PAGE + ".html", "retrieved": E.RETRIEVED, "requests": 0,
            "licence": "Official legal text is free to reproduce (Ley 23 de 1982, art. 41). The compilation's editorial notes "
                       "(Avance Jurídico) are not reproduced; only the official text and the facts the notes state are used.",
            "notes": PAGE + " (base, continuation pages and js/ note files), plus the base and last page of each amending "
                     "act. Requests are counted in the country's shared log (corpus.json's source)."}],
        "laws": laws,
        "acts": [dict(a, versions=to_deltas(a["versions"])) for a in acts],
        "decisions": [
            "Código Sustantivo del Trabajo (cst/parse_cst.py, with the engine cst/engine.py): versions are rebuilt per "
            "article from the basedoc's earlier texts, inline amendment markers and Notas de Vigencia, as for the "
            "Constitution and the Código Civil. Where the source names an act but gives no text after it, the article "
            "reads '" + E.MISSING_LINE + "' for that period.",
            "Constitutional Court and Corte Suprema rulings that struck text are laws of kind 'court', dated by the ruling's "
            "day as the source gives it; rulings that upheld text on a condition are court laws with a note and change no words.",
            "In-force days of amending acts: the act's own vigencia clause as its basedoc page gives it; otherwise the "
            "default rule (Ley 4 de 1913, art. 52: two months after promulgation). A day a provision's own note gives "
            "applies to that provision. The list below gives the day and the rule for each act.",
            "The source's earlier texts often leave out the article's epigraph (its title); where the latest earlier text "
            "differs from today's only by that or by a change no note names, today's text is used from the latest "
            "named act's day. Articles where that happened: " + (", ".join(approx) or "none") + ".",
        ] + DECISIONS + rules,
        "ai_use": ["None at data-build time: cst/fetch_cst.py, cst/parse_cst.py and cst/engine.py are deterministic code, "
                   "written with Claude Code (claude-opus-5-5); no model reads, writes or summarises legal text."],
    }
    os.makedirs(os.path.dirname(out), exist_ok=True)
    tmp = out + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline=chr(10)) as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write(chr(10))
    os.replace(tmp, out)
    print(f"wrote {out}: {len(act['versions'])} versions, {len(laws)} laws, {os.path.getsize(out) // 1024} KB")


def main(argv: list[str]) -> None:
    act = build_cst()
    out = argv[argv.index("--out") + 1] if "--out" in argv else OUT
    write_part(act, out)
    if "--report" in argv:
        for r in E.REPORT:
            print("  ", r)
    else:
        print(f"  {len(E.REPORT)} report lines (--report to print)")


if __name__ == "__main__":
    main(sys.argv[1:])
