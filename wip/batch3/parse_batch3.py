"""Build corpus.d/80-batch3.json for Colombia: Código de Comercio (Decreto 410 de 1971), CPACA (Ley 1437 de 2011),
Código de Procedimiento Penal (Ley 906 de 2004) and Código de la Infancia y la Adolescencia (Ley 1098 de 2006).

Reads only ../.cache/ (batch3/fetch_batch3.py, ../fetch.py); no network; deterministic. Uses the Phase 2 driver and
engine (phase2/parse_phase2.py, phase2/engine.py): the same per-provision reconstruction, in-force rules and checks.

Usage:  python -X utf8 batch3/parse_batch3.py [--report] [--out-dir DIR] [--only slug,...]
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(COUNTRY, "phase2"))
import parse_phase2 as P  # noqa: E402

E = P.E
# The Código de Comercio ends "Comuníquese y publíquese. Dado en Bogotá, D.E., a 27 de marzo de 1971." and the signers.
P.SIGN_OFF = re.compile(P.SIGN_OFF.pattern + r"|\s*COMUN[ÍI]QUESE Y PUBL[ÍI]QUESE|\s*Comun[íi]quese y publ[íi]quese")
OUT_DIR = os.path.join(COUNTRY, "corpus.d")
DECISIONS = P.DECISIONS


def article_text(units: list[dict], number: str) -> str:
    """Plain text of the article numbered `number` (by its heading label)."""
    for u in units:
        if E.label_num(u["label"] or "") == number:
            return " ".join(E.plain(E.strip_markers(it[1])) for it in u["items"] if it[0] == "p")
    raise SystemExit(f"article {number} not found")


def register_first(key: str, page: str, title: str) -> tuple[str | None, str | None]:
    kind, n, y = key.split("-")
    enacted, pub = E.page_header(page, y)
    E.register(key)
    E.LAWS[key].update({"title": title, "enacted": enacted, "published": pub, "url": E.BASE + page + ".html"})
    return enacted, pub


def build(page: str, key: str, slug: str, short: str, title: str, law_title: str, start_fn) -> dict:
    units = P.doc_units(page)
    E.scan_law_dates(units)
    enacted, pub = register_first(key, page, law_title)
    start, why, note = start_fn(units, enacted, pub)
    E.IN_FORCE[key], E.IN_FORCE_WHY[key] = start, why
    res = E.build_act(page, start)
    vs = P.finish(res, page)
    vs[0]["note"] = note
    DECISIONS.append(f"{title}: first version from {start}: {why}")
    return {"slug": slug, "short": short, "title": title, "url": E.BASE + page + ".html",
            "first_law": key, "earlier_laws": [], "versions": vs}


def start_comercio(units, enacted, pub):
    a = article_text(units, "2038")
    if "empezará a regir el 1o. de enero de 1972, con excepción del artículo 821" not in a or not enacted:
        raise SystemExit(f"Código de Comercio art. 2038 or heading: {a!r}")
    return (enacted, f"Decreto 410 de 1971, art. 2038: '{a}' (the first version is dated from the day it was issued, "
                     f"{enacted}, when the parts excepted took effect; the rest from 1 January 1972)",
            f"The code as issued (Decreto 410 de 1971, of {enacted}, Diario Oficial of {pub}). Its art. 2038: '{a}' The "
            f"history dates the whole code from {enacted}, the day the excepted parts (art. 821, Libro IV Título XIII "
            f"Capítulo V and Libro VI) took effect; the rest took effect on 1 January 1972.")


def start_cpaca(units, enacted, pub):
    a = article_text(units, "308")
    m = re.search(r"comenzar[áa] a regir el dos \(2\) de julio del año 2012", a)
    if not m:
        raise SystemExit(f"CPACA art. 308: {a[:300]!r}")
    return ("2012-07-02", f"Ley 1437 de 2011, art. 308: '{a[:300]}'",
            f"The code as promulgated (Ley 1437 de 2011, Diario Oficial of {pub}), in force from 2 July 2012 under its art. "
            f"308: '{a[:300]}'")


def start_cpp(units, enacted, pub):
    a = article_text(units, "533")
    b = article_text(units, "530")
    if "1o. de enero de 2005" not in b and "primero (1o.) de enero de 2005" not in b and "1o de enero de 2005" not in b:
        raise SystemExit(f"CPP art. 530: {b[:400]!r}")
    return ("2005-01-01", f"Ley 906 de 2004, art. 530 (gradual entry by judicial district from 1 January 2005): '{b[:400]}'",
            f"The code as promulgated (Ley 906 de 2004, Diario Oficial of {pub}). Its art. 530 brought it into force by "
            f"judicial district, gradually, from 1 January 2005; its art. 533 keeps the earlier procedure for crimes "
            f"before that. The history dates the whole code from 1 January 2005: '{b[:400]}'")


def start_cia(units, enacted, pub):
    a = article_text(units, "216")
    if not re.search(r"seis \(6\) meses después de su promulgación", a) or not pub:
        raise SystemExit(f"CIA art. 216: {a[:300]!r}")
    start = E.add_months(pub, 6)
    return (start, f"Ley 1098 de 2006, art. 216: '{a[:400]}'",
            f"The code as promulgated (Ley 1098 de 2006, Diario Oficial of {pub}), in force six months later under its art. "
            f"216; the system of criminal responsibility for adolescents came in gradually by district: '{a[:400]}'")


BUILDERS = {
    "codigo-de-comercio": lambda: build("codigo_comercio", "dec-410-1971", "codigo-de-comercio", "CCo",
                                        "Código de Comercio (Decreto 410 de 1971)", "Por el cual se expide el Código de Comercio",
                                        start_comercio),
    "cpaca": lambda: build("ley_1437_2011", "ley-1437-2011", "cpaca", "CPACA",
                           "Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 1437 de 2011)",
                           "Por la cual se expide el Código de Procedimiento Administrativo y de lo Contencioso Administrativo",
                           start_cpaca),
    "codigo-de-procedimiento-penal": lambda: build("ley_0906_2004", "ley-906-2004", "codigo-de-procedimiento-penal", "CPP",
                                                   "Código de Procedimiento Penal (Ley 906 de 2004)",
                                                   "Por la cual se expide el Código de Procedimiento Penal", start_cpp),
    "codigo-de-la-infancia-y-la-adolescencia": lambda: build("ley_1098_2006", "ley-1098-2006",
                                                             "codigo-de-la-infancia-y-la-adolescencia", "CIA",
                                                             "Código de la Infancia y la Adolescencia (Ley 1098 de 2006)",
                                                             "Por la cual se expide el Código de la Infancia y la Adolescencia",
                                                             start_cia),
}
P.PREFIX.update({"codigo-de-comercio": ("codigo_comercio", "CCo"), "cpaca": ("ley_1437_2011", "CPACA"),
                 "codigo-de-procedimiento-penal": ("ley_0906_2004", "CPP"),
                 "codigo-de-la-infancia-y-la-adolescencia": ("ley_1098_2006", "CIA")})
NAMES = ("Código de Comercio", "Código de Procedimiento Administrativo", "Código de Procedimiento Penal",
         "Código de la Infancia")


def anachronisms(acts: list[dict]) -> list[str]:
    """No change may take effect before its act exists: a version credited to an act dated before that act's own
    sanction or publication (unless the act's own clause reaches back) is an error; so is a ruling dated before the
    text it rules on. Returns the problems found."""
    out = []
    for a in acts:
        for v in a["versions"]:
            for k, ls in v.get("credits", {}).items():
                for l in ls:
                    law = E.LAWS.get(l, {})
                    first = min(d for d in (law.get("enacted"), law.get("published")) if d) if (
                        law.get("enacted") or law.get("published")) else None
                    if first and v["from"] < first:
                        out.append(f"{a['slug']} {k}: {l} credited on {v['from']}, before the act's own date {first}")
    return out


def main(argv: list[str]) -> None:
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else list(BUILDERS)
    acts = [BUILDERS[s]() for s in BUILDERS if s in only]
    problems = anachronisms(acts)
    for p in problems:
        E.note("anachronism " + p)
    d = argv[argv.index("--out-dir") + 1] if "--out-dir" in argv else OUT_DIR
    P.write_part(acts, os.path.join(d, "80-batch3.json"), tuple(n for n in NAMES))
    print(f"  {len(problems)} anachronisms")
    if "--report" in argv:
        for r in E.REPORT:
            print("  ", r)


if __name__ == "__main__":
    main(sys.argv[1:])
