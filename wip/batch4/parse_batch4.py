"""Build corpus.d/90-batch4.json for Colombia: Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016),
Ley 100 de 1993 (Sistema de Seguridad Social Integral), Código General Disciplinario (Ley 1952 de 2019) and Código
Electoral (Decreto 2241 de 1986).

Reads only ../.cache/ (batch4/fetch_batch4.py, ../fetch.py); no network; deterministic. Imports the batch 3 driver
(batch3/parse_batch3.py: its page repairs, sign-off rule and anachronism check), which imports the Phase 2 driver and
engine (phase2/parse_phase2.py, phase2/engine.py): the same per-provision reconstruction from the Senado basedoc, rulings
as `court` laws, and in-force days from each act's own vigencia clause.

Usage:  python -X utf8 batch4/parse_batch4.py [--report] [--out-dir DIR] [--only slug,...]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(COUNTRY, "batch3"))
sys.path.insert(0, os.path.join(COUNTRY, "phase2"))
import parse_batch3 as B3  # noqa: E402

P = B3.P
E = B3.E
OUT_DIR = os.path.join(COUNTRY, "corpus.d")
PART = "90-batch4.json"
DECISIONS = P.DECISIONS

# Events a provision's history dates before the act's own first day: the engine would fold them into the first version
# (credited to the act itself), so they are listed and the build stops unless each is explained here.
PRE_START: list[str] = []
_assemble = E.assemble


def assemble(timelines, labels, notes_all, order, start):
    for key, sts in timelines.items():
        for d, stt, law in sts[1:]:
            if d < start:
                PRE_START.append(f"{E.CUR_UNIT[0].split(' ')[0]} {key}: {law} on {d}, before the first day {start}")
    return _assemble(timelines, labels, notes_all, order, start)


E.assemble = assemble


def start_1801(units, enacted, pub):
    a = B3.article_text(units, "243")
    if "La presente ley regirá seis (6) meses después de su promulgación" not in a or not pub:
        raise SystemExit(f"Ley 1801 art. 243: {a!r}")
    start = E.add_months(pub, 6)
    return (start, f"Ley 1801 de 2016, art. 243: '{a}' (published {pub})",
            f"The code as promulgated (Ley 1801 de 2016, sanctioned {enacted}, Diario Oficial No. 49.949 of {pub}), in "
            f"force from {start} under its art. 243: '{a}'")


BUILDERS = {
    "codigo-nacional-de-seguridad-y-convivencia-ciudadana": lambda: B3.build(
        "ley_1801_2016", "ley-1801-2016", "codigo-nacional-de-seguridad-y-convivencia-ciudadana", "CNSCC",
        "Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016)",
        "Por la cual se expide el Código Nacional de Seguridad y Convivencia Ciudadana", start_1801),
}
P.PREFIX.update({"codigo-nacional-de-seguridad-y-convivencia-ciudadana": ("ley_1801_2016", "CNSCC")})
NAMES = ("Código Nacional de Seguridad y Convivencia Ciudadana", "Ley 100 de 1993", "Código General Disciplinario",
         "Código Electoral")


def finish_part(path: str) -> None:
    """write_part is the Phase 2 one; name this batch's own scripts in ai_use and rewrite atomically."""
    with open(path, encoding="utf-8") as f:
        part = json.load(f)
    part["ai_use"] = ["None at data-build time: batch4/fetch_batch4.py and batch4/parse_batch4.py (with batch3/ and "
                      "phase2/, which they import) are deterministic code, written with Claude Code (claude-opus-5-5); no "
                      "model reads, writes or summarises legal text."]
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)


def main(argv: list[str]) -> None:
    only = argv[argv.index("--only") + 1].split(",") if "--only" in argv else list(BUILDERS)
    acts = [BUILDERS[s]() for s in BUILDERS if s in only]
    problems = B3.anachronisms(acts)
    for p in problems:
        E.note("anachronism " + p)
    for p in PRE_START:
        E.note("pre-start " + p)
    d = argv[argv.index("--out-dir") + 1] if "--out-dir" in argv else OUT_DIR
    out = os.path.join(d, PART)
    P.write_part(acts, out, tuple(n for n in NAMES if any(a["title"].startswith(n) for a in acts)))
    finish_part(out)
    print(f"  {len(problems)} anachronisms, {len(PRE_START)} pre-start events")
    if "--report" in argv:
        for r in E.REPORT:
            print("  ", r)


if __name__ == "__main__":
    main(sys.argv[1:])
