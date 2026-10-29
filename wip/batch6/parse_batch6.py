"""Build corpus.d/97-batch6.json for Colombia: Estatuto Orgánico del Sistema Financiero (Decreto 663 de 1993), Código de
Minas (Ley 685 de 2001), Código Procesal del Trabajo y de la Seguridad Social (Decreto-Ley 2158 de 1948), Régimen de
Insolvencia Empresarial (Ley 1116 de 2006) and Régimen de los Servicios Públicos Domiciliarios (Ley 142 de 1994).

Reads only ../.cache/ (batch6/fetch_batch6.py, ../fetch.py); no network; deterministic. Imports the batch 5 driver
(batch5/parse_batch5.py: its generic page repairs and key fixes), which imports the batch 4, batch 3 and Phase 2 drivers
and the engine (phase2/engine.py): the same per-provision reconstruction from the Senado basedoc, rulings as `court`
laws, and in-force days from each act's own vigencia clause.

Usage:  python -X utf8 batch6/parse_batch6.py [--report] [--out-dir DIR] [--only slug,...] [--show page:art,...]
"""
from __future__ import annotations

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
for _d in ("batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch5 as B5  # noqa: E402

B4 = B5.B4
B3 = B5.B3
P = B5.P
E = B5.E
OUT_DIR = os.path.join(COUNTRY, "corpus.d")
PART = "97-batch6.json"
DECISIONS = P.DECISIONS
E.RETRIEVED = "2026-10-29"  # this batch's fetch day (the part's `retrieved`)
PRE_START = B4.PRE_START
PRE_START.clear()

# Typing slips in these acts' notes and earlier-text headings, each fixed by what the same article shows. wrong -> right.
KEY_FIXES = {
    "dec-673-1999": "dec-673-1994",   # EOSF art. 83: marker '<Numeral derogado por el artículo 17 del Decreto 673 de 1994>'
    "dec-674-1999": "dec-673-1994",   # EOSF art. 83 num. 3: same marker; Decreto 673 de 1994, art. 17, names both numerals
    "dec-2489-1989": "dec-2489-1999",  # EOSF art. 327: 'Texto modificado por el Decreto 2489 de 1989' (notes: art. 4 Decreto 2489 de 1999, DO 43.819)
    "ley-685-2021": "ley-685-2001",   # Código de Minas art. 295: 'Texto original de la Ley 685 de 2021' (the code's own original)
}
E.KEY_FIXES.update(KEY_FIXES)
DECISIONS.append("Estatuto Orgánico del Sistema Financiero and Código de Minas: typing slips in act numbers or years of the "
                 "source's notes and earlier-text headings are read as the act the same article names: "
                 + "; ".join(f"{E.law_label(a)} as {E.law_label(b)}" for a, b in KEY_FIXES.items()) + ".")
# Acts the basedoc and Colpensiones do not hold, dated from what the EOSF's own notes or the act's text say.
E.HAND_RULES["dec-673-1994"] = ("1994-05-01", "Decreto 673 de 1994 (Diario Oficial No. 41.287 of 29 March 1994), art. 17: "
                                              "'El presente Decreto rige a partir del 1o de mayo de 1994, y deja sin efecto "
                                              "... los numerales 1o y 3o del artículo 83 del Estatuto Orgánico del Sistema "
                                              "Financiero ...' (the basedoc does not hold it: read from the Secretaría "
                                              "Jurídica Distrital de Bogotá's Régimen Legal, "
                                              "https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=7036, in the "
                                              "cache)")
E.HAND_RULES["dec-2423-1993"] = ("1994-01-01", "the Estatuto Orgánico del Sistema Financiero's note on art. 12: 'el ordinal "
                                               "a) del artículo 6o. del Decreto 2423 de 1993; el cual entra en vigencia a "
                                               "partir del 1o. de enero de 1994' (the basedoc does not hold the decree)")
# Decreto 1154 de 1999 (struck whole by Sentencia C-969 de 1999): no source holds it; the EOSF's notes give its Diario
# Oficial ('No 43.623, de 29 de Junio de 1999', a capital the engine's date pattern does not read). Default rule.
E.PUB["dec-1154-1999"] = "1999-06-29"
DECISIONS.append("Estatuto Orgánico del Sistema Financiero: " + E.HAND_RULES["dec-673-1994"][1] + ".")
DECISIONS.append("Estatuto Orgánico del Sistema Financiero: Decreto 2423 de 1993 is dated 1 January 1994 from "
                 + E.HAND_RULES["dec-2423-1993"][1] + ".")
DECISIONS.append("Estatuto Orgánico del Sistema Financiero: Decreto 1154 de 1999 (struck whole by Sentencia C-969 de 1999) "
                 "is held by no cached source; its Diario Oficial day (29 June 1999) is the EOSF notes', and it is dated by "
                 "the default rule (two months after promulgation).")

_page_header = E.page_header


DO_MONTH_FIRST = re.compile(r"Diario Oficial No\.? ?[\d.]+,? de ([a-z]+) (\d{1,2}) de (\d{4})$")
MONTH_FIRST_DO: set[str] = set()


def page_header(page: str, year: str):
    """The Estatuto Orgánico del Sistema Financiero's heading writes its day month first: '(Abril 2 de 1993)'. Some
    amending acts' headings write the Diario Oficial day month first ('Diario Oficial No. 44.537, de agosto 31 de
    2001', Ley 689 de 2001), which the engine does not read: that day is read here when the engine finds none."""
    if page != "estatuto_organico_sistema_financiero":
        enacted, pub = _page_header(page, year)
        if pub is None and not page.startswith("http"):
            ps = E.page_paras(page)
            for p in ps[:12]:
                m = DO_MONTH_FIRST.match(p)
                if m and m.group(1) in E.MONTHS and m.group(3) == year:
                    pub = f"{m.group(3)}-{E.MONTHS[m.group(1)]:02d}-{int(m.group(2)):02d}"
                    MONTH_FIRST_DO.add(f"{page}: '{p}'")
                    break
        return enacted, pub
    ps = E.page_paras(page)
    i = ps.index("DECRETO 663 DE 1993")
    m = re.fullmatch(r"\(([A-Za-z]+) (\d{1,2}) de (\d{4})\)", ps[i + 1])
    d = E.DO_RE.search(ps[i + 2])
    if not m or not d or ps[i + 2] != "Diario Oficial No. 40.820, del 5 de abril de 1993":
        raise SystemExit(f"EOSF heading: {ps[i:i + 3]}")
    return f"{m.group(3)}-{E.MONTHS[m.group(1).lower()]:02d}-{int(m.group(2)):02d}", E.date_es(d.group(1))


E.page_header = page_header


def cut_signers(a: str) -> str:
    for s in ("El Presidente del", "La Presidenta del", "El presidente del", "Dado en", "Publíquese"):
        if s in a:
            a = a[:a.index(s)]
    return a.strip()


def start_eosf(units, enacted, pub):
    a = cut_signers(B3.article_text(units, "339"))
    if not a.startswith("El presente Decreto rige a partir del 2o. de mayo de 1993") or enacted != "1993-04-02" or not pub:
        raise SystemExit(f"EOSF art. 339: {a[:300]!r} {enacted} {pub}")
    return ("1993-05-02", f"Decreto 663 de 1993, art. 339: '{a[:700]}' (issued {enacted}, published {pub})",
            f"The Estatuto as issued (Decreto 663 de 1993, of {enacted}, Diario Oficial No. 40.820 of {pub}), in force from "
            f"2 May 1993 under its art. 339: '{a[:400]} ...'")


def start_minas(units, enacted, pub):
    a = cut_signers(B3.article_text(units, "362"))
    if a != "El presente Código rige desde su promulgación." or not pub:
        raise SystemExit(f"Código de Minas art. 362: {a[:300]!r}")
    return (pub, f"Ley 685 de 2001, art. 362: '{a}' (sanctioned {enacted}, Diario Oficial No. 44.545 of {pub})",
            f"The code as promulgated (Ley 685 de 2001, sanctioned {enacted}, Diario Oficial No. 44.545 of {pub}), in force "
            f"from promulgation under its art. 362: '{a}'")


def start_cpt(units, enacted, pub):
    a = cut_signers(B3.article_text(units, "156"))
    if a != "Este decreto regirá cinco días después de su expedición." or enacted != "1948-06-24":
        raise SystemExit(f"CPT art. 156: {a[:300]!r} {enacted}")
    start = E.add_days(enacted, 5)
    return (start, f"Decreto-Ley 2158 de 1948, art. 156: '{a}' (issued {enacted}; the source gives no Diario Oficial)",
            f"The code as issued (Decreto-Ley 2158 de 1948, of {enacted}, 'Sobre los procedimientos en los juicios del "
            f"trabajo'), in force from {start} under its art. 156: '{a}' The source gives no Diario Oficial for it.")


def start_1116(units, enacted, pub):
    a = cut_signers(B3.article_text(units, "126"))
    if not a.startswith("Salvo lo que se indica en los incisos anteriores, la presente ley comenzará a regir seis (6) "
                        "meses después de su promulgación") or not pub:
        raise SystemExit(f"Ley 1116 art. 126: {a[:300]!r}")
    later = E.add_months(pub, 6)
    return (pub, f"Ley 1116 de 2006, art. 126: '{a}' The first version is dated from promulgation ({pub}), when the "
                 f"parts of arts. 125 and 126 that say so took effect; the rest six months later ({later}).",
            f"The act as promulgated (Ley 1116 de 2006, Diario Oficial No. 46.494 of {pub}). Under its art. 126 it took "
            f"effect six months after promulgation ({later}), save the parts of arts. 125 and 126 that apply from "
            f"promulgation (the extension of Ley 550 de 1999 and the restructuring agreements of territorial entities). "
            f"The history dates the whole act from promulgation. Art. 126: '{a}'")


def start_142(units, enacted, pub):
    a = cut_signers(B3.article_text(units, "189"))
    if a != "Salvo cuando ella disponga otra cosa, esta Ley rige a partir de la fecha de su publicación en el Diario " \
            "Oficial." or not pub:
        raise SystemExit(f"Ley 142 art. 189: {a[:300]!r}")
    return (pub, f"Ley 142 de 1994, art. 189: '{a}' (Diario Oficial No. 41.433 of {pub})",
            f"The act as published (Ley 142 de 1994, Diario Oficial No. 41.433 of {pub}), in force from publication under "
            f"its art. 189: '{a}'")


BUILDERS: dict = {
    "estatuto-organico-del-sistema-financiero": lambda: B3.build(
        "estatuto_organico_sistema_financiero", "dec-663-1993", "estatuto-organico-del-sistema-financiero", "EOSF",
        "Estatuto Orgánico del Sistema Financiero (Decreto 663 de 1993)",
        "Por medio del cual se actualiza el Estatuto Orgánico del Sistema Financiero y se modifica su titulación y "
        "numeración", start_eosf),
    "codigo-de-minas": lambda: B3.build(
        "ley_0685_2001", "ley-685-2001", "codigo-de-minas", "CMin", "Código de Minas (Ley 685 de 2001)",
        "Por la cual se expide el Código de Minas y se dictan otras disposiciones", start_minas),
    "codigo-procesal-del-trabajo": lambda: B3.build(
        "codigo_procedimental_laboral", "dec-2158-1948", "codigo-procesal-del-trabajo", "CPTSS",
        "Código Procesal del Trabajo y de la Seguridad Social (Decreto-Ley 2158 de 1948)",
        "Sobre los procedimientos en los juicios del trabajo", start_cpt),
    "regimen-de-insolvencia": lambda: B3.build(
        "ley_1116_2006", "ley-1116-2006", "regimen-de-insolvencia", "RIE",
        "Régimen de Insolvencia Empresarial (Ley 1116 de 2006)",
        "Por la cual se establece el Régimen de Insolvencia Empresarial en la República de Colombia y se dictan otras "
        "disposiciones", start_1116),
    "servicios-publicos-domiciliarios": lambda: B3.build(
        "ley_0142_1994", "ley-142-1994", "servicios-publicos-domiciliarios", "LSPD",
        "Régimen de los Servicios Públicos Domiciliarios (Ley 142 de 1994)",
        "Por la cual se establece el régimen de los servicios públicos domiciliarios y se dictan otras disposiciones",
        start_142),
}
P.PREFIX.update({"estatuto-organico-del-sistema-financiero": ("estatuto_organico_sistema_financiero", "EOSF"),
                 "codigo-de-minas": ("ley_0685_2001", "CMin"),
                 "codigo-procesal-del-trabajo": ("codigo_procedimental_laboral", "CPTSS"),
                 "regimen-de-insolvencia": ("ley_1116_2006", "RIE"),
                 "servicios-publicos-domiciliarios": ("ley_0142_1994", "LSPD")})
NAMES = ("Estatuto Orgánico del Sistema Financiero", "Código de Minas", "Código Procesal del Trabajo",
         "Régimen de Insolvencia Empresarial", "Régimen de los Servicios Públicos Domiciliarios")


def finish_part(path: str) -> None:
    with open(path, encoding="utf-8") as f:
        part = json.load(f)
    part["ai_use"] = ["None at data-build time: batch6/fetch_batch6.py and batch6/parse_batch6.py (with batch5/, batch4/, "
                      "batch3/ and phase2/, which they import) are deterministic code, written with Claude Code "
                      "(claude-opus-5-5); no model reads, writes or summarises legal text."]
    part["sources"][0]["notes"] += (" Terms checked 2026-10-28: robots.txt disallows only the Joomla system folders, not "
                                    "/senado/basedoc/; each page's footer reserves Avance Jurídico's notes, concordances "
                                    "and arrangement, so only the official text and the facts the notes state are used. "
                                    "Pages retrieved on 2026-10-29 (some amending acts' pages earlier, for the other "
                                    "parts, from the same cache).")
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, path)


def main(argv: list[str]) -> None:
    if "--show" in argv:
        for x in argv[argv.index("--show") + 1].split(","):
            page, art = x.split(":")
            print(page, art, B3.article_text(P.doc_units(page), art)[:1500])
        return
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
