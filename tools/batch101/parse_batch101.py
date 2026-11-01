"""Build corpus.d/99zzzzzzzz-101-batch101.json for Colombia: Ley 2388 de 2024 (familia de crianza) and Ley 548 de
1999 (prórroga y reforma de la Ley 418 de 1997).
SPEC_ALL keeps the specs of batches 50 to 62 (published there; their page
repairs stay keyed by page).

Reads only the source pages the batch fetchers saved; no network; deterministic. Uses batch 46's driver pattern.

Usage:  python -X utf8 batch101/parse_batch101.py [--report] [--out-dir DIR] [--only slug,...]
"""
from __future__ import annotations

import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
COUNTRY = os.path.dirname(HERE)
for _d in ("batch31", "batch30", "batch29", "batch27", "batch26", "batch25", "batch24", "batch23", "batch22", "batch21", "batch20",
           "batch19", "batch18", "batch17", "batch16", "batch15", "batch14", "batch13", "batch12", "batch11", "batch10",
           "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(COUNTRY, _d))
import parse_batch30 as B30  # noqa: E402
import parse_batch10 as B10  # noqa: E402

B29, B27 = B30.B29, B30.B27
B24 = B27.B24
B23, B15, B13, B7, B4, P, E = B29.B23, B29.B15, B29.B13, B29.B7, B29.B4, B29.P, B29.E
PART = "99zzzzzzzz-101-batch101.json"
BATCH = "batch 101"
E.RETRIEVED = "2026-10-31"
E.PER_SLOT_STRIKE = True  # (fifteenth session) each strike dated by its own ruling: phase2/engine.py slot_ruling()
E.PARA_BLOCK = True  # (nineteenth session) a several-line earlier text replaces its whole part: phase2/engine.py
E.DECL_WHOLE = True  # (twenty-second session) '<Artículo declarado INEXEQUIBLE>' is a whole-article strike too: phase2/engine.py

# (sixteenth session) Ley 141 de 1994's heading prints 'Diario Oficial No. 41.414, de 30 de julio de 1994' under
# '(junio 28)'. The Diario Oficial's numbering rules July out (Ley 136 de 1994 of 2 June 1994 is in No. 41.377, Ley 142
# de 1994 of 11 July 1994 in No. 41.433): issue 41.414 falls at the end of June, so the month is a slip and the act is
# dated from 30 June 1994 (the fix_law_entries.py numbering rule, as for Leyes 11 de 1984 and 22 de 1977).
_page_header95 = E.page_header
L141_DO = "Diario Oficial No. 41.414, de 30 de julio de 1994"
L141_PUB_WHY = ("Ley 141 de 1994: its page heads it '(junio 28)' and 'Diario Oficial No. 41.414, de 30 de julio de 1994'; "
                "the Diario Oficial's numbering rules July out (Ley 136 de 1994, of 2 June 1994, is in No. 41.377 and Ley "
                "142 de 1994, of 11 July 1994, in No. 41.433, so issue 41.414 falls at the end of June): the month is read "
                "as a slip and the act is dated from its promulgation in that issue, 30 June 1994 (its art. 70: 'Esta Ley "
                "rige a partir de la fecha de su promulgación').")


def page_header(page: str, year: str):
    enacted, pub = _page_header95(page, year)
    if page == "ley_0141_1994":
        if L141_DO not in [E.plain(x) for x in E.page_paras(page)[:8]] or (enacted, pub) != ("1994-06-28", "1994-07-30"):
            raise SystemExit(f"Ley 141 de 1994: heading changed ({enacted}, {pub})")
        pub = "1994-06-30"
    return enacted, pub


E.page_header = page_header

# (seventeenth session) Decreto 4923 de 2011 (Diario Oficial No. 48.294 of 26 December 2011), issued transitorily under
# Acto Legislativo 5 de 2011, repealed or changed Ley 141's arts. 19-22, 24, 25 and 29 'a partir del 1o. de enero de 2012':
# every note on the page that names it says 'Rige a partir del 1o. de enero de 2012' (the source has no page of the decree
# itself), where the default rule gave 26 February 2012.
E.HAND_RULES["dec-4923-2011"] = ("2012-01-01", "the notes on Ley 141 de 1994 that name Decreto 4923 de 2011 (Diario Oficial "
                                               "No. 48.294 of 26 December 2011): 'Rige a partir del 1o. de enero de 2012'")


def on_publication(page, key, label, art, must, what="promulgation"):
    """batch 7's start function, with a vigencia clause longer than 600 characters cut at its last full sentence
    within them (batch 7 cut it mid-word: Ley 2466 de 2025 art. 70 ends in a long parágrafo)."""
    def start(units, enacted, pub):
        a = B7._clause(units, art, must, key, enacted, pub)
        if len(a) > 600:
            cut = a.rfind(". ", 0, 600)
            cut = cut + 1 if cut > 0 else max(a.rfind(", ", 0, 600), a.rfind("; ", 0, 600))
            a = re.sub(r"\s*PAR[ÁA]GRAFO(?: \w+)?\.$", "", a[:cut]) + " [...]"
        day = enacted if what == "issue" else pub
        return (day, f"{label}, art. {art}: '{a}' (sanctioned {enacted}, Diario Oficial of {pub})",
                f"The act as promulgated ({label}, sanctioned {enacted}, Diario Oficial of {pub}), in force from {day} "
                f"under its art. {art}: '{a}'")
    return start
# (batch 59: also a title that starts 'Sobre', as Ley 4 de 1913's 'Sobre régimen político y municipal')
# (batch 81: also 'A través de la cual', as Ley 1276 de 2009's title)
# (batch 82: also a title that starts 'Por el derecho', as Ley 1388 de 2010's)
TITLE = re.compile(r"^Sobre\b|^Por el derecho\b|\b(por (medio de )?(la|el) cual|mediante la cual|por medio de las cuales|por medio del cual|"
                   r"a trav[ée]s de la cual)\b", re.I)


def page_title(page: str) -> str:
    """The act's own title (batch 22's reading, also 'Por el cual' / 'Por medio del cual', within the first 30
    paragraphs, after a 'FE DE ERRATAS'). A title the page breaks over two paragraphs (Ley 31 de 1992: '... el Banco de
    la' / 'República para ...') is joined."""
    ps = E.page_paras(page)[:30]
    k = next(i for i, x in enumerate(ps) if TITLE.search(x))
    t = ps[k]
    if not t.rstrip().endswith(".") and k + 1 < len(ps) and ps[k + 1][:1].isupper() and ps[k + 1].rstrip().endswith(".") \
            and not ps[k + 1].isupper():
        t = t.rstrip() + " " + ps[k + 1]
    return t.rstrip(". ")


L550, L222 = "ley_0550_1999", "ley_0222_1995"
L1450, L1753 = "ley_1450_2011", "ley_1753_2015"
L1978, L1607, L2068 = "ley_1978_2019", "ley_1607_2012", "ley_2068_2020"
L2157, L1395, L446 = "ley_2157_2021", "ley_1395_2010", "ley_0446_1998"
L1930, L1561, D902 = "ley_1930_2018", "ley_1561_2012", "decreto_0902_2017"
L2099, L2044 = "ley_2099_2021", "ley_2044_2020"
L200, L4, L454 = "ley_0200_1995", "ley_0004_1913", "ley_0454_1998"
FIRST_550 = "1999-12-30"


def start_550(units, enacted, pub):
    """Ley 550 de 1999: art. 79, in force for five years from its publication in the Diario Oficial. First published in
    Diario Oficial No. 43.836 of 30 December 1999; the page prints the text republished in Diario Oficial No. 43.940 of
    19 March 2000 to correct transcription errors (editor's note on the page). Dated from the first publication."""
    a = B7._clause(units, "79", "Esta ley regirá durante cinco (5) años, contados a partir la fecha de su publicación en el "
                   "Diario Oficial", "Ley 550", enacted, pub)
    head = " ".join(E.plain(it[1]) for u in units[:1] for it in u["items"] if it[0] == "p")
    B23._need("originalmente publicada en el Diario Oficial No. 43.836 de fecha 30 de diciembre de 1999" in head
              and "publicada nuevamente para corregir errores de transcripción" in head, "Ley 550 first publication")
    day = FIRST_550
    return (day, f"Ley 550 de 1999, art. 79: '{a}' First published in Diario Oficial No. 43.836 of {day}; republished to "
                 f"correct transcription errors in Diario Oficial No. 43.940 of {pub}, whose text is the one given here.",
            f"The act as promulgated (Ley 550 de 1999, sanctioned {enacted}, first published in Diario Oficial No. 43.836 of "
            f"{day}; text as republished in Diario Oficial No. 43.940 of {pub}), in force from publication under its art. "
            f"79: '{a}'")


SPEC_ALL = [
    ("reestructuracion-empresarial-1999", L550, "ley-550-1999", "LRE99",
     "Reestructuración empresarial (Ley 550 de 1999)", start_550),
    ("regimen-de-sociedades-1995", L222, "ley-222-1995", "LSoc95", "Régimen de sociedades (Ley 222 de 1995)",
     B10.after_months(L222, "Ley 222", "Ley 222 de 1995", "237", "Esta ley empezará a regir al vencimiento de los seis "
                      "meses contados a partir de su promulgación", 6, "six months")),
    ("plan-nacional-de-desarrollo-2010-2014", L1450, "ley-1450-2011", "PND10",
     "Plan Nacional de Desarrollo 2010-2014 (Ley 1450 de 2011)",
     on_publication(L1450, "Ley 1450", "Ley 1450 de 2011", "276", "La presente ley rige a partir de la fecha de su publicación")),
    ("plan-nacional-de-desarrollo-2014-2018", L1753, "ley-1753-2015", "PND14",
     "Plan Nacional de Desarrollo 2014-2018 (Ley 1753 de 2015)",
     on_publication(L1753, "Ley 1753", "Ley 1753 de 2015", "267", "La presente ley rige a partir de su publicación")),
    ("modernizacion-sector-tic-2019", L1978, "ley-1978-2019", "LTIC19",
     "Modernización del sector de las Tecnologías de la Información y las Comunicaciones (Ley 1978 de 2019)",
     on_publication(L1978, "Ley 1978", "Ley 1978 de 2019", "51", "La presente ley rige a partir de su promulgación")),
    ("reforma-tributaria-2012", L1607, "ley-1607-2012", "RT12", "Reforma tributaria (Ley 1607 de 2012)",
     on_publication(L1607, "Ley 1607", "Ley 1607 de 2012", "198", "La presente ley rige a partir de su promulgación")),
    ("ley-general-de-turismo-2020", L2068, "ley-2068-2020", "LTur20", "Ley General de Turismo (Ley 2068 de 2020)",
     on_publication(L2068, "Ley 2068", "Ley 2068 de 2020", "55", "La presente ley rige a partir de su sanción y publicación "
                    "en el Diario Oficial")),
    ("habeas-data-financiero-2021", L2157, "ley-2157-2021", "LHDF21",
     "Habeas data financiero (Ley 2157 de 2021)",
     on_publication(L2157, "Ley 2157", "Ley 2157 de 2021", "15", "Esta ley rige a partir de la fecha de publicación")),
    ("descongestion-judicial-2010", L1395, "ley-1395-2010", "LDJ10", "Descongestión judicial (Ley 1395 de 2010)",
     on_publication(L1395, "Ley 1395", "Ley 1395 de 2010", "122", "Esta ley rige a partir de su promulgación")),
    ("descongestion-y-acceso-a-la-justicia-1998", L446, "ley-446-1998", "LDAJ98",
     "Descongestión, eficiencia y acceso a la justicia (Ley 446 de 1998)",
     on_publication(L446, "Ley 446", "Ley 446 de 1998", "163", "Esta ley rige desde su publicación")),
    ("gestion-integral-de-los-paramos", L1930, "ley-1930-2018", "LPar18",
     "Gestión integral de los páramos (Ley 1930 de 2018)",
     on_publication(L1930, "Ley 1930", "Ley 1930 de 2018", "33", "La presente ley rige a partir de la fecha de su promulgación")),
    ("titulacion-de-la-posesion", L1561, "ley-1561-2012", "LTit12",
     "Titulación de la posesión y saneamiento de la falsa tradición (Ley 1561 de 2012)",
     B10.after_months(L1561, "Ley 1561", "Ley 1561 de 2012", "27", "Esta ley empezará a regir seis (6) meses después de su "
                      "promulgación", 6, "six months")),
    ("reforma-rural-integral-tierras", D902, "dec-902-2017", "DRRI17",
     "Reforma Rural Integral en materia de tierras (Decreto Ley 902 de 2017)",
     on_publication(D902, "Decreto 902", "Decreto Ley 902 de 2017", "82", "El presente decreto ley rige a partir de su "
                    "expedición", what="issue")),
    ("transicion-energetica", L2099, "ley-2099-2021", "LTE21", "Transición energética (Ley 2099 de 2021)",
     on_publication(L2099, "Ley 2099", "Ley 2099 de 2021", "58", "La presente ley rige a partir de la fecha de su promulgación")),
    ("saneamiento-de-asentamientos-humanos", L2044, "ley-2044-2020", "LSAH20",
     "Saneamiento de predios ocupados por asentamientos humanos ilegales (Ley 2044 de 2020)",
     on_publication(L2044, "Ley 2044", "Ley 2044 de 2020", "33", "La presente ley rige a partir de su promulgación")),
]


def after_days(page, key, label, art, must, days, words, base="sanction"):
    """A start function for an act in force a number of calendar days after its sanction (or promulgation)."""
    import datetime

    def start(units, enacted, pub):
        a = B7._clause(units, art, must, key, enacted, pub)
        frm = enacted if base == "sanction" else pub
        day = (datetime.date.fromisoformat(frm) + datetime.timedelta(days=days)).isoformat()
        return (day, f"{label}, art. {art}: '{a[:600]}' ({words} after its {base} on {frm}, counted in calendar days)",
                f"The act as sanctioned ({label}, sanctioned {enacted}, Diario Oficial of {pub}), in force {words} after "
                f"its {base} ({day}, counted in calendar days) under its art. {art}: '{a[:600]}'")
    return start


def default_rule(page, label):
    """No vigencia clause: in force two months after promulgation (Ley 4 de 1913, arts. 52-53, the corpus's default
    rule; for Ley 4 de 1913 itself, the rule it states)."""
    def start(units, enacted, pub):
        day = E.add_months(pub, 2)
        return (day, f"{label}: no article fixes its start; Ley 4 de 1913, art. 52 ('La ley no obliga sino en virtud de "
                     f"su promulgación, y su observancia principia dos meses después de promulgada'): promulgated in the "
                     f"Diario Oficial of {pub}, in force {day}",
                f"The act as promulgated ({label}, sanctioned {enacted}, Diario Oficial of {pub}), in force two months "
                f"after its promulgation ({day}) under the general rule of Ley 4 de 1913, art. 52")
    return start


SPEC_ALL += [
    ("codigo-disciplinario-unico-1995", L200, "ley-200-1995", "CDU95", "Código Disciplinario Único (Ley 200 de 1995)",
     after_days(L200, "Ley 200", "Ley 200 de 1995", "177", "Esta Ley regirá cuarenta y cinco (45) días después de su sanción",
                45, "forty-five days")),
    ("regimen-politico-y-municipal", L4, "ley-4-1913", "CRPM", "Código de Régimen Político y Municipal (Ley 4 de 1913)",
     default_rule(L4, "Ley 4 de 1913")),
    ("economia-solidaria", L454, "ley-454-1998", "LES98", "Economía solidaria (Ley 454 de 1998)",
     on_publication(L454, "Ley 454", "Ley 454 de 1998", "67", "La presente ley empezará a regir a partir de su promulgación")),
]
D4633, D4634, D4635 = "decreto_4633_2011", "decreto_4634_2011", "decreto_4635_2011"
ORIG_VIG = ("El presente decreto rige a partir de su promulgación, tendrá una vigencia de 10 años y deroga todas las "
            "disposiciones que le sean contrarias.")


def from_box_original(page, label, art):
    """The ethnic victims' decree-laws of 2011: their vigencia article as issued ('El presente decreto rige a partir de su
    promulgación, tendrá una vigencia de 10 años ...', the article's 'Texto original' box; Ley 2078 de 2021 later
    replaced the article to extend the term to 9 December 2031). In force from promulgation."""
    def start(units, enacted, pub):
        u = next(x for x in units if (x["name"] or "") == art)
        box = [E.plain(E.html.unescape(it[2])) for it in u["items"] if it[0] == "box" and it[1] == "Legislación Anterior"]
        B23._need(len(box) == 1 and "Texto original del " + label.replace("Decreto Ley", "Decreto") in box[0]
                  and ORIG_VIG in box[0] and pub, f"{page} art. {art}: original vigencia")
        a = ORIG_VIG
        return (pub, f"{label}, art. {art} as issued: '{a}' (issued {enacted}, Diario Oficial of {pub})",
                f"The act as promulgated ({label}, issued {enacted}, Diario Oficial of {pub}), in force from {pub} under "
                f"its art. {art} as issued: '{a}'")
    return start


SPEC_ALL += [
    ("victimas-pueblos-indigenas", D4633, "dec-4633-2011", "DLVInd",
     "Víctimas pertenecientes a pueblos y comunidades indígenas (Decreto Ley 4633 de 2011)",
     from_box_original(D4633, "Decreto Ley 4633 de 2011", "194")),
    ("victimas-pueblo-rrom", D4634, "dec-4634-2011", "DLVRrom",
     "Víctimas pertenecientes al pueblo Rrom o Gitano (Decreto Ley 4634 de 2011)",
     from_box_original(D4634, "Decreto Ley 4634 de 2011", "123")),
    ("victimas-comunidades-negras", D4635, "dec-4635-2011", "DLVAfro",
     "Víctimas pertenecientes a comunidades negras, afrocolombianas, raizales y palenqueras (Decreto Ley 4635 de 2011)",
     from_box_original(D4635, "Decreto Ley 4635 de 2011", "156")),
]
L1610, L1816, L1719 = "ley_1610_2013", "ley_1816_2016", "ley_1719_2014"


def start_1816(units, enacted, pub):
    """Ley 1816 de 2016: in force from 1 January 2017 under its art. 42."""
    a = B7._clause(units, "42", "La presente ley entra a regir el 1o de enero del año 2017", "Ley 1816", enacted, pub)
    day = "2017-01-01"
    return (day, f"Ley 1816 de 2016, art. 42: '{a[:600]}' (sanctioned {enacted}, Diario Oficial of {pub})",
            f"The act as promulgated (Ley 1816 de 2016, sanctioned {enacted}, Diario Oficial of {pub}), in force from {day} "
            f"under its art. 42: '{a[:600]}'")


SPEC_ALL += [
    ("inspeccion-del-trabajo", L1610, "ley-1610-2013", "LIT13",
     "Inspección del trabajo y acuerdos de formalización laboral (Ley 1610 de 2013)",
     on_publication(L1610, "Ley 1610", "Ley 1610 de 2013", "18", "La presente ley rige a partir de su promulgación")),
    ("monopolio-de-licores", L1816, "ley-1816-2016", "LMLic16",
     "Monopolio rentístico de licores destilados (Ley 1816 de 2016)", start_1816),
    ("violencia-sexual-conflicto-armado", L1719, "ley-1719-2014", "LVSex14",
     "Acceso a la justicia de las víctimas de violencia sexual, en especial con ocasión del conflicto armado (Ley 1719 de 2014)",
     on_publication(L1719, "Ley 1719", "Ley 1719 de 2014", "35", "La presente ley rige a partir de su promulgación")),
]
L1826, L1111, L1430 = "ley_1826_2017", "ley_1111_2006", "ley_1430_2010"
SPEC_ALL += [
    ("procedimiento-penal-abreviado", L1826, "ley-1826-2017", "LPPA17",
     "Procedimiento penal especial abreviado y acusador privado (Ley 1826 de 2017)",
     B10.after_months(L1826, "Ley 1826", "Ley 1826 de 2017", "44", "La presente ley entrará a regir seis (6) meses después "
                      "de la fecha de su promulgación", 6, "six months")),
    ("reforma-tributaria-2006", L1111, "ley-1111-2006", "RT06", "Reforma tributaria (Ley 1111 de 2006)",
     on_publication(L1111, "Ley 1111", "Ley 1111 de 2006", "78", "La presente Ley rige a partir de su promulgación")),
    ("reforma-tributaria-2010", L1430, "ley-1430-2010", "RT10",
     "Control tributario y competitividad, reforma tributaria (Ley 1430 de 2010)",
     on_publication(L1430, "Ley 1430", "Ley 1430 de 2010", "67", "La presente ley rige a partir de su promulgación")),
]
L1739, L788, L863 = "ley_1739_2014", "ley_0788_2002", "ley_0863_2003"
SPEC_ALL += [
    ("reforma-tributaria-2014", L1739, "ley-1739-2014", "RT14", "Reforma tributaria (Ley 1739 de 2014)",
     on_publication(L1739, "Ley 1739", "Ley 1739 de 2014", "77", "La presente ley rige a partir de su promulgación")),
    ("reforma-tributaria-2002", L788, "ley-788-2002", "RT02", "Reforma tributaria (Ley 788 de 2002)",
     on_publication(L788, "Ley 788", "Ley 788 de 2002", "118", "La presente ley rige a partir de su promulgación")),
    ("reforma-tributaria-2003", L863, "ley-863-2003", "RT03", "Reforma tributaria (Ley 863 de 2003)",
     on_publication(L863, "Ley 863", "Ley 863 de 2003", "69", "La presente ley rige a partir de la fecha de su publicación")),
]
L2300, L1876, L2232 = "ley_2300_2023", "ley_1876_2017", "ley_2232_2022"
SPEC_ALL += [
    ("intimidad-de-los-consumidores-cobranza", L2300, "ley-2300-2023", "LIntC23",
     "Medidas que protegen el derecho a la intimidad de los consumidores (Ley 2300 de 2023)",
     B10.after_months(L2300, "Ley 2300", "Ley 2300 de 2023", "10", "La presente ley entrará en vigor en un plazo de tres (3) "
                      "meses contados a partir de su promulgación", 3, "three months")),
    ("sistema-nacional-de-innovacion-agropecuaria", L1876, "ley-1876-2017", "SNIA17",
     "Sistema Nacional de Innovación Agropecuaria (Ley 1876 de 2017)",
     on_publication(L1876, "Ley 1876", "Ley 1876 de 2017", "47", "La presente ley rige a partir de la fecha de su publicación")),
    ("plasticos-de-un-solo-uso", L2232, "ley-2232-2022", "LPlas22",
     "Reducción gradual de la producción y consumo de ciertos productos plásticos de un solo uso (Ley 2232 de 2022)",
     on_publication(L2232, "Ley 2232", "Ley 2232 de 2022", "35", "La presente ley rige a partir de la fecha de su promulgación")),
]
L2272, L1530 = "ley_2272_2022", "ley_1530_2012"
VIG_2272 = ("Los artículos 3o, 4o, 5o, 6o, 7o, 8o, 9o y 15 de la presente ley tendrán una vigencia de cuatro (4) años, a partir "
            "de su promulgación")


def start_1530(units, enacted, pub):
    """Ley 1530 de 2012: art. 160, second paragraph: in force from its publication."""
    t = B3.article_text(units, "160")
    w = "La presente ley rige a partir de la fecha de su publicación"
    B23._need(w in t and pub, "Ley 1530 art. 160")
    a = t[t.index(w):]
    a = a[:a.index(".") + 1]
    return (pub, f"Ley 1530 de 2012, art. 160: '{a}' (sanctioned {enacted}, Diario Oficial of {pub})",
            f"The act as promulgated (Ley 1530 de 2012, sanctioned {enacted}, Diario Oficial of {pub}), in force from {pub} "
            f"under its art. 160: '{a}'")


def start_2272(units, enacted, pub):
    """Ley 2272 de 2022: art. 20, every provision from promulgation; arts. 3 to 9 and 15 (art. 19, second paragraph) also
    from promulgation, for a term of four years."""
    a = B7._clause(units, "20", "Con excepción de los artículos 3o, 4o, 5o, 6o, 7o, 8o, 9o y 15 cuya vigencia se establece "
                   "en el artículo anterior, las demás disposiciones de esta ley rigen a partir de su promulgación", "Ley 2272",
                   enacted, pub)
    b = B3.article_text(units, "19")
    B23._need(VIG_2272 in b, "Ley 2272 art. 19 term")
    b = b[b.index(VIG_2272):]
    b = b[:b.index(".") + 1]
    return (pub, f"Ley 2272 de 2022, art. 20: '{a}'; art. 19: '{b}' (sanctioned {enacted}, Diario Oficial of {pub})",
            f"The act as promulgated (Ley 2272 de 2022, sanctioned {enacted}, Diario Oficial of {pub}), in force from {pub} "
            f"under its art. 20: '{a}' and its art. 19: '{b}'")


SPEC_ALL += [
    ("paz-total", L2272, "ley-2272-2022", "LPazT22",
     "Política de paz de Estado y prórroga de la Ley 418 de 1997 (Ley 2272 de 2022)",
     lambda u, e, p: start_2272(u, e, p)),
    ("sistema-general-de-regalias-2012", L1530, "ley-1530-2012", "SGR12",
     "Sistema General de Regalías (Ley 1530 de 2012)",
     lambda u, e, p: start_1530(u, e, p)),
]
L2108, L1680 = "ley_2108_2021", "ley_1680_2013"
SPEC_ALL += [
    ("internet-servicio-publico-esencial", L2108, "ley-2108-2021", "LInt21",
     "Internet como servicio público esencial y universal (Ley 2108 de 2021)",
     on_publication(L2108, "Ley 2108", "Ley 2108 de 2021", "12", "La presente ley rige a partir de su promulgación")),
    ("acceso-tic-personas-ciegas", L1680, "ley-1680-2013", "LCieg13",
     "Acceso de las personas ciegas y con baja visión a la información, las comunicaciones y las TIC (Ley 1680 de 2013)",
     on_publication(L1680, "Ley 1680", "Ley 1680 de 2013", "15", "La presente ley rige a partir de su publicación")),
]
D262, D267 = "decreto_0262_2000", "decreto_0267_2000"
SPEC_ALL += [
    ("procuraduria-general-de-la-nacion", D262, "dec-262-2000", "DLPGN00",
     "Estructura y organización de la Procuraduría General de la Nación (Decreto Ley 262 de 2000)",
     after_days(D262, "Decreto 262", "Decreto Ley 262 de 2000", "262",
                "Este decreto regirá a los diez (10) días calendario contados a partir de la fecha de su publicación",
                10, "ten days", base="publication")),
    ("contraloria-general-de-la-republica", D267, "dec-267-2000", "DLCGR00",
     "Organización y funcionamiento de la Contraloría General de la República (Decreto Ley 267 de 2000)",
     on_publication(D267, "Decreto 267", "Decreto Ley 267 de 2000", "87",
                    "El presente decreto rige a partir de la fecha de su publicación")),
]
L35, L1004, L795 = "ley_0035_1993", "ley_1004_2005", "ley_0795_2003"
VIG_795 = "La presente ley rige a partir de la fecha de su promulgación."


def start_795(units, enacted, pub):
    """Ley 795 de 2003: in force from its promulgation under the last sentence of its art. 114 (the article's first
    sentences list repeals)."""
    a = B7._clause(units, "114", "Derogatorias y vigencia. La presente ley deroga", "Ley 795", enacted, pub)
    B23._need(a.endswith(VIG_795), "Ley 795 art. 114")
    return (pub, f"Ley 795 de 2003, art. 114: '{VIG_795}' (sanctioned {enacted}, Diario Oficial of {pub})",
            f"The act as promulgated (Ley 795 de 2003, sanctioned {enacted}, Diario Oficial of {pub}), in force from {pub} "
            f"under its art. 114: '{VIG_795}'")


SPEC_ALL += [
    ("marco-del-sector-financiero", L35, "ley-35-1993", "LMSF93",
     "Ley marco de las actividades financiera, bursátil y aseguradora (Ley 35 de 1993)",
     on_publication(L35, "Ley 35", "Ley 35 de 1993", "40", "La presente Ley rige desde la fecha de su publicación")),
    ("zonas-francas", L1004, "ley-1004-2005", "LZF05", "Régimen de zonas francas (Ley 1004 de 2005)",
     on_publication(L1004, "Ley 1004", "Ley 1004 de 2005", "13", "La presente ley rige a partir de la fecha de su publicación")),
    ("ajustes-estatuto-organico-sistema-financiero", L795, "ley-795-2003", "LEOSF03",
     "Ajustes al Estatuto Orgánico del Sistema Financiero (Ley 795 de 2003)", lambda u, e, p: start_795(u, e, p)),
]
D760, D785, D1567 = "decreto_0760_2005", "decreto_0785_2005", "decreto_1567_1998"
SPEC_ALL += [
    ("procedimiento-comision-nacional-del-servicio-civil", D760, "dec-760-2005", "DLCNSC05",
     "Procedimiento ante y por la Comisión Nacional del Servicio Civil (Decreto Ley 760 de 2005)",
     on_publication(D760, "Decreto 760", "Decreto Ley 760 de 2005", "49",
                    "El presente decreto rige a partir de la fecha de su publicación")),
    ("nomenclatura-de-empleos-territoriales", D785, "dec-785-2005", "DLNET05",
     "Nomenclatura, clasificación, funciones y requisitos de los empleos de las entidades territoriales (Decreto Ley 785 de "
     "2005)",
     on_publication(D785, "Decreto 785", "Decreto Ley 785 de 2005", "34",
                    "El presente decreto rige a partir de la fecha de su publicación")),
    ("capacitacion-y-estimulos-de-empleados-del-estado", D1567, "dec-1567-1998", "DLCap98",
     "Sistema Nacional de Capacitación y sistema de estímulos para los empleados del Estado (Decreto Ley 1567 de 1998)",
     on_publication(D1567, "Decreto 1567", "Decreto Ley 1567 de 1998", "40", "El presente decreto rige a partir de su publicación")),
]
L223 = "ley_0223_1995"
SPEC_ALL += [
    ("reforma-tributaria-1995", L223, "ley-223-1995", "RT95", "Racionalización tributaria (Ley 223 de 1995)",
     on_publication(L223, "Ley 223", "Ley 223 de 1995", "285", "La presente Ley rige a partir de la fecha de su publicación")),
]
L335, L680, L1273 = "ley_0335_1996", "ley_0680_2001", "ley_1273_2009"
SPEC_ALL += [
    ("television-privada-1996", L335, "ley-335-1996", "LTVP96",
     "Modificación de las Leyes 14 de 1991 y 182 de 1995 y televisión privada (Ley 335 de 1996)",
     on_publication(L335, "Ley 335", "Ley 335 de 1996", "29", "La presente Ley regirá a partir de la fecha de su sanción y promulgación")),
    ("reforma-de-la-television-2001", L680, "ley-680-2001", "LTV01",
     "Reforma de las Leyes 14 de 1991, 182 de 1995 y 335 de 1996 en materia de televisión (Ley 680 de 2001)",
     on_publication(L680, "Ley 680", "Ley 680 de 2001", "15", "Esta ley rige a partir de la fecha de su promulgación")),
    ("delitos-informaticos", L1273, "ley-1273-2009", "LDI09",
     "Protección de la información y de los datos, delitos informáticos (Ley 1273 de 2009)",
     on_publication(L1273, "Ley 1273", "Ley 1273 de 2009", "4", "La presente ley rige a partir de su promulgación")),
]
L310, L1383, L1696 = "ley_0310_1996", "ley_1383_2010", "ley_1696_2013"
SPEC_ALL += [
    ("transporte-masivo-1996", L310, "ley-310-1996", "LTM96",
     "Sistemas de servicio público urbano de transporte masivo de pasajeros, modificación de la Ley 86 de 1989 (Ley 310 de 1996)",
     on_publication(L310, "Ley 310", "Ley 310 de 1996", "8", "La presente Ley rige a partir de la fecha de su promulgación")),
    ("reforma-codigo-de-transito-2010", L1383, "ley-1383-2010", "LRCT10",
     "Reforma del Código Nacional de Tránsito (Ley 1383 de 2010)",
     on_publication(L1383, "Ley 1383", "Ley 1383 de 2010", "28", "VIGENCIA. La presente ley rige a partir de su promulgación")),
    ("conduccion-bajo-el-influjo-del-alcohol", L1696, "ley-1696-2013", "LAlc13",
     "Sanciones por conducción bajo el influjo del alcohol u otras sustancias psicoactivas (Ley 1696 de 2013)",
     on_publication(L1696, "Ley 1696", "Ley 1696 de 2013", "10", "La presente ley rige a partir de su promulgación")),
]
L1811, L1964, L2251 = "ley_1811_2016", "ley_1964_2019", "ley_2251_2022"
SPEC_ALL += [
    ("uso-de-la-bicicleta", L1811, "ley-1811-2016", "LBici16",
     "Incentivos al uso de la bicicleta y reforma del Código Nacional de Tránsito (Ley 1811 de 2016)",
     on_publication(L1811, "Ley 1811", "Ley 1811 de 2016", "19", "La presente ley rige a partir de su promulgación")),
    ("vehiculos-electricos", L1964, "ley-1964-2019", "LVE19",
     "Promoción del uso de vehículos eléctricos (Ley 1964 de 2019)",
     on_publication(L1964, "Ley 1964", "Ley 1964 de 2019", "12", "La presente Ley rige a partir de su promulgación")),
    ("ley-julian-esteban", L2251, "ley-2251-2022", "LJE22",
     "Diseño e implementación de la política de seguridad vial con enfoque de sistema seguro, Ley Julián Esteban (Ley 2251 de 2022)",
     on_publication(L2251, "Ley 2251", "Ley 2251 de 2022", "24", "La presente ley rige a partir de su promulgación")),
]
L1608, L1949, L1966 = "ley_1608_2013", "ley_1949_2019", "ley_1966_2019"
SPEC_ALL += [
    ("liquidez-sector-salud", L1608, "ley-1608-2013", "LLiqS13",
     "Medidas para mejorar la liquidez y el uso de algunos recursos del sector salud (Ley 1608 de 2013)",
     on_publication(L1608, "Ley 1608", "Ley 1608 de 2013", "13", "La presente ley rige a partir de su publicación", "publication")),
    ("reforma-leyes-1122-y-1438", L1949, "ley-1949-2019", "LSal19",
     "Adición y modificación de las Leyes 1122 de 2007 y 1438 de 2011 (Ley 1949 de 2019)",
     on_publication(L1949, "Ley 1949", "Ley 1949 de 2019", "12", "La presente ley rige a partir de la fecha de su promulgación")),
    ("transparencia-sistema-de-salud", L1966, "ley-1966-2019", "LTSal19",
     "Gestión y transparencia en el Sistema de Seguridad Social en Salud (Ley 1966 de 2019)",
     on_publication(L1966, "Ley 1966", "Ley 1966 de 2019", "19", "La presente ley rige desde el momento de su promulgación")),
]
L697, L1274, L2128 = "ley_0697_2001", "ley_1274_2009", "ley_2128_2021"
SPEC_ALL += [
    ("uso-racional-de-la-energia", L697, "ley-697-2001", "LURE01",
     "Uso racional y eficiente de la energía y energías alternativas (Ley 697 de 2001)",
     on_publication(L697, "Ley 697", "Ley 697 de 2001", "11", "La presente ley rige a partir de la fecha de su promulgación")),
    ("servidumbres-petroleras", L1274, "ley-1274-2009", "LServP09",
     "Procedimiento de avalúo para las servidumbres petroleras (Ley 1274 de 2009)",
     on_publication(L1274, "Ley 1274", "Ley 1274 de 2009", "10", "La presente ley rige a partir de su publicación", "publication")),
    ("gas-combustible", L2128, "ley-2128-2021", "LGas21",
     "Abastecimiento, continuidad, confiabilidad y cobertura del gas combustible (Ley 2128 de 2021)",
     on_publication(L2128, "Ley 2128", "Ley 2128 de 2021", "23", "La presente ley rige a partir de su promulgación")),
]
L2250, D588, D589 = "ley_2250_2022", "decreto_0588_2017", "decreto_0589_2017"
SPEC_ALL += [
    ("formalizacion-minera", L2250, "ley-2250-2022", "LFMin22",
     "Legalización y formalización minera, su financiamiento y comercialización (Ley 2250 de 2022)",
     on_publication(L2250, "Ley 2250", "Ley 2250 de 2022", "30", "La presente Ley rige a partir de su promulgación")),
    ("comision-de-la-verdad", D588, "dec-588-2017", "DLCEV17",
     "Comisión para el Esclarecimiento de la Verdad, la Convivencia y la No Repetición (Decreto Ley 588 de 2017)",
     on_publication(D588, "Decreto 588", "Decreto Ley 588 de 2017", "33",
                    "El presente decreto-ley rige a partir de la fecha de su publicación", "publication")),
    ("unidad-de-busqueda-de-personas-desaparecidas", D589, "dec-589-2017", "DLUBPD17",
     "Unidad de Búsqueda de Personas dadas por desaparecidas en el contexto y en razón del conflicto armado (Decreto Ley 589 de 2017)",
     on_publication(D589, "Decreto 589", "Decreto Ley 589 de 2017", "31",
                    "El presente decreto-ley rige a partir de la fecha de su publicación", "publication")),
]
D893, D896, D870 = "decreto_0893_2017", "decreto_0896_2017", "decreto_0870_2017"
SPEC_ALL += [
    ("programas-de-desarrollo-con-enfoque-territorial", D893, "dec-893-2017", "DLPDET17",
     "Programas de Desarrollo con Enfoque Territorial, PDET (Decreto Ley 893 de 2017)",
     on_publication(D893, "Decreto 893", "Decreto Ley 893 de 2017", "15",
                    "El presente decreto rige a partir de la fecha de su publicación", "publication")),
    ("programa-de-sustitucion-de-cultivos-ilicitos", D896, "dec-896-2017", "DLPNIS17",
     "Programa Nacional Integral de Sustitución de Cultivos de Uso Ilícito, PNIS (Decreto Ley 896 de 2017)",
     on_publication(D896, "Decreto 896", "Decreto Ley 896 de 2017", "9",
                    "La vigencia del PNIS será de 10 años", "publication")),
    ("pago-por-servicios-ambientales", D870, "dec-870-2017", "DLPSA17",
     "Pago por servicios ambientales y otros incentivos a la conservación (Decreto Ley 870 de 2017)",
     on_publication(D870, "Decreto 870", "Decreto Ley 870 de 2017", "23",
                    "El presente decreto rige a partir de su publicación", "publication")),
]
L1575, L678, L258 = "ley_1575_2012", "ley_0678_2001", "ley_0258_1996"
SPEC_ALL += [
    ("ley-general-de-bomberos", L1575, "ley-1575-2012", "LBomb12",
     "Ley General de Bomberos de Colombia (Ley 1575 de 2012)",
     on_publication(L1575, "Ley 1575", "Ley 1575 de 2012", "53", "Esta ley rige a partir de la fecha de su promulgación")),
    ("accion-de-repeticion", L678, "ley-678-2001", "LRep01",
     "Acción de repetición y llamamiento en garantía con fines de repetición (Ley 678 de 2001)",
     on_publication(L678, "Ley 678", "Ley 678 de 2001", "31", "La presente ley rige a partir de la fecha de su publicación",
                    "publication")),
    ("afectacion-a-vivienda-familiar", L258, "ley-258-1996", "LAVF96",
     "Afectación a vivienda familiar (Ley 258 de 1996)",
     on_publication(L258, "Ley 258", "Ley 258 de 1996", "13", "La presente ley rige a partir de la fecha de su promulgación")),
]
L2120, L1787, L1209 = "ley_2120_2021", "ley_1787_2016", "ley_1209_2008"
SPEC_ALL += [
    ("entornos-alimentarios-saludables", L2120, "ley-2120-2021", "LEAS21",
     "Entornos alimentarios saludables (Ley 2120 de 2021)",
     on_publication(L2120, "Ley 2120", "Ley 2120 de 2021", "14", "La presente ley entrará en vigencia a partir de su promulgación")),
    ("cannabis-medicinal", L1787, "ley-1787-2016", "LCann16",
     "Acceso seguro e informado al uso médico y científico del cannabis (Ley 1787 de 2016)",
     on_publication(L1787, "Ley 1787", "Ley 1787 de 2016", "19", "La presente ley rige a partir de su promulgación")),
    ("seguridad-en-piscinas", L1209, "ley-1209-2008", "LPisc08",
     "Normas de seguridad en piscinas (Ley 1209 de 2008)",
     B10.after_months(L1209, "Ley 1209", "Ley 1209 de 2008", "19", "La presente ley rige a los seis (6) meses siguientes a "
                      "partir de su promulgación", 6, "six months")),
]
L322, L1881, L2013 = "ley_0322_1996", "ley_1881_2018", "ley_2013_2019"
SPEC_ALL += [
    ("sistema-nacional-de-bomberos-1996", L322, "ley-322-1996", "LBomb96",
     "Sistema Nacional de Bomberos de Colombia (Ley 322 de 1996)",
     on_publication(L322, "Ley 322", "Ley 322 de 1996", "38", "Esta Ley rige a partir de la fecha de su promulgación")),
    ("perdida-de-investidura", L1881, "ley-1881-2018", "LPInv18",
     "Pérdida de la investidura de los congresistas (Ley 1881 de 2018)",
     on_publication(L1881, "Ley 1881", "Ley 1881 de 2018", "24", "Esta ley deroga la Ley 144 de 1994 y las disposiciones legales anteriores y las que le sean contrarias y rige desde la fecha de su promulgación")),
    ("publicacion-de-declaraciones-de-bienes", L2013, "ley-2013-2019", "LDBR19",
     "Publicación de las declaraciones de bienes, renta y conflictos de interés (Ley 2013 de 2019)",
     on_publication(L2013, "Ley 2013", "Ley 2013 de 2019", "6", "La presente ley rige después de su promulgación")),
]
L1336, L1276, L982 = "ley_1336_2009", "ley_1276_2009", "ley_0982_2005"
SPEC_ALL += [
    ("explotacion-sexual-de-menores", L1336, "ley-1336-2009", "LESCNNA09",
     "Lucha contra la explotación, la pornografía y el turismo sexual con niños, niñas y adolescentes (Ley 1336 de 2009)",
     on_publication(L1336, "Ley 1336", "Ley 1336 de 2009", "28", "La presente ley rige a partir de la fecha de su publicación",
                    "publication")),
    ("centros-vida-adulto-mayor", L1276, "ley-1276-2009", "LCVida09",
     "Atención integral del adulto mayor en los centros vida (Ley 1276 de 2009)",
     on_publication(L1276, "Ley 1276", "Ley 1276 de 2009", "15", "La presente ley rige a partir de la fecha de su promulgación")),
    ("personas-sordas-y-sordociegas", L982, "ley-982-2005", "LSordas05",
     "Equiparación de oportunidades para las personas sordas y sordociegas (Ley 982 de 2005)",
     after_days(L982, "Ley 982", "Ley 982 de 2005", "47", "La presente ley regirá sesenta (60) días posteriores a su "
                "promulgación", 60, "sixty (60) days", base="promulgation")),
]
L1388, L919, L1482 = "ley_1388_2010", "ley_0919_2004", "ley_1482_2011"
SPEC_ALL += [
    ("cancer-infantil", L1388, "ley-1388-2010", "LCInf10",
     "Derecho a la vida de los niños con cáncer en Colombia (Ley 1388 de 2010)",
     on_publication(L1388, "Ley 1388", "Ley 1388 de 2010", "16", "Esta ley rige a partir de su sanción y publicación",
                    "publication")),
    ("componentes-anatomicos-trasplante", L919, "ley-919-2004", "LCAnat04",
     "Prohibición de la comercialización de componentes anatómicos humanos para trasplante (Ley 919 de 2004)",
     on_publication(L919, "Ley 919", "Ley 919 de 2004", "4", "La presente ley rige a partir de su promulgación")),
    ("antidiscriminacion", L1482, "ley-1482-2011", "LAntiD11",
     "Actos de discriminación (Ley 1482 de 2011)",
     on_publication(L1482, "Ley 1482", "Ley 1482 de 2011", "8", "La presente ley rige a partir de su promulgación")),
]
L1774, L1232, L1857 = "ley_1774_2016", "ley_1232_2008", "ley_1857_2017"
SPEC_ALL += [
    ("animales-seres-sintientes", L1774, "ley-1774-2016", "LAnim16",
     "Animales como seres sintientes (Ley 1774 de 2016)",
     on_publication(L1774, "Ley 1774", "Ley 1774 de 2016", "11", "La presente ley rige a partir de la fecha de su "
                    "promulgación")),
    ("mujer-cabeza-de-familia-2008", L1232, "ley-1232-2008", "LMCF08",
     "Reforma de la Ley Mujer Cabeza de Familia (Ley 1232 de 2008)",
     on_publication(L1232, "Ley 1232", "Ley 1232 de 2008", "17", "La presente ley rige a partir de la fecha de su "
                    "promulgación")),
    ("proteccion-de-la-familia-2017", L1857, "ley-1857-2017", "LFam17",
     "Medidas de protección de la familia (Ley 1857 de 2017)",
     on_publication(L1857, "Ley 1857", "Ley 1857 de 2017", "5", "La presente ley rige a partir de la fecha de su sanción",
                    "issue")),
]
L905, L1453 = "ley_0905_2004", "ley_1453_2011"
SPEC_ALL += [
    ("reforma-mipymes-2004", L905, "ley-905-2004", "LMIP04",
     "Reforma de la ley de micro, pequeñas y medianas empresas (Ley 905 de 2004)",
     on_publication(L905, "Ley 905", "Ley 905 de 2004", "25", "La presente ley rige a partir de la fecha de su "
                    "promulgación")),
    ("seguridad-ciudadana-2011", L1453, "ley-1453-2011", "LSC11",
     "Seguridad ciudadana (Ley 1453 de 2011)",
     on_publication(L1453, "Ley 1453", "Ley 1453 de 2011", "111", "La presente ley rige a partir de su promulgación")),
]
L938 = "ley_0938_2004"
SPEC_ALL += [
    ("estatuto-organico-fiscalia-2004", L938, "ley-938-2004", "EOFGN04",
     "Estatuto Orgánico de la Fiscalía General de la Nación (Ley 938 de 2004)",
     on_publication(L938, "Ley 938", "Ley 938 de 2004", "79", "La presente ley tiene vigencia a partir de la fecha de su "
                    "publicación", "publication")),
]
L98, L1473, L232 = "ley_0098_1993", "ley_1473_2011", "ley_0232_1995"


def on_fixed_day(page, key, label, art, must, day):
    """A start function for an act whose own article fixes the day it takes effect."""
    def start(units, enacted, pub):
        a = B7._clause(units, art, must, key, enacted, pub)
        return (day, f"{label}, art. {art}: '{a[:600]}' (sanctioned {enacted}, Diario Oficial of {pub})",
                f"The act as promulgated ({label}, sanctioned {enacted}, Diario Oficial of {pub}), in force from {day} "
                f"under its art. {art}: '{a[:600]}'")
    return start
SPEC_ALL += [
    ("fomento-del-libro-1993", L98, "ley-98-1993", "LLIB93",
     "Democratización y fomento del libro colombiano (Ley 98 de 1993)",
     on_publication(L98, "Ley 98", "Ley 98 de 1993", "36", "Esta Ley rige a partir de la fecha de su promulgación")),
    ("regla-fiscal-2011", L1473, "ley-1473-2011", "LRF11",
     "Regla fiscal (Ley 1473 de 2011)",
     on_fixed_day(L1473, "Ley 1473", "Ley 1473 de 2011", "17", "La presente ley rige a partir del 1o de enero de 2012",
                  "2012-01-01")),
    ("establecimientos-de-comercio-1995", L232, "ley-232-1995", "LEC95",
     "Funcionamiento de los establecimientos comerciales (Ley 232 de 1995)",
     on_publication(L232, "Ley 232", "Ley 232 de 1995", "6", "La presente Ley rige a partir de la fecha de su promulgación")),
]
L549, L974 = "ley_0549_1999", "ley_0974_2005"
SPEC_ALL += [
    ("pasivo-pensional-territorial-1999", L549, "ley-549-1999", "LPPT99",
     "Financiación del pasivo pensional de las entidades territoriales (Ley 549 de 1999)",
     on_publication(L549, "Ley 549", "Ley 549 de 1999", "21", "La presente rige a partir de su promulgación")),
]
SPEC_ALL += [
    ("regimen-de-bancadas-2005", L974, "ley-974-2005", "LRB05",
     "Régimen de bancadas (Ley 974 de 2005)",
     on_fixed_day(L974, "Ley 974", "Ley 974 de 2005", "21", "La presente ley rige a partir del 19 de julio del año 2006",
                  "2006-07-19")),
]
L643, L191 = "ley_0643_2001", "ley_0191_1995"
SPEC_ALL += [
    ("juegos-de-suerte-y-azar-2001", L643, "ley-643-2001", "LJSA01",
     "Régimen propio del monopolio rentístico de juegos de suerte y azar (Ley 643 de 2001)",
     on_publication(L643, "Ley 643", "Ley 643 de 2001", "61", "La presente ley rige a partir de la fecha de su publicación",
                    "publication")),
    ("zonas-de-frontera-1995", L191, "ley-191-1995", "LZF95",
     "Zonas de frontera (Ley 191 de 1995)",
     on_publication(L191, "Ley 191", "Ley 191 de 1995", "57", "La presente Ley rige a partir de la fecha de su promulgación")),
]
L1151, L812 = "ley_1151_2007", "ley_0812_2003"
SPEC_ALL += [
    ("plan-nacional-de-desarrollo-2006-2010", L1151, "ley-1151-2007", "PND06",
     "Plan Nacional de Desarrollo 2006-2010 (Ley 1151 de 2007)",
     on_publication(L1151, "Ley 1151", "Ley 1151 de 2007", "160", "La presente ley rige a partir de su publicación")),
    ("plan-nacional-de-desarrollo-2003-2006", L812, "ley-812-2003", "PND03",
     "Plan Nacional de Desarrollo 2003-2006 (Ley 812 de 2003)",
     on_publication(L812, "Ley 812", "Ley 812 de 2003", "137", "La presente ley rige a partir de la fecha de su promulgación")),
]
L790, L1444 = "ley_0790_2002", "ley_1444_2011"
SPEC_ALL += [
    ("renovacion-de-la-administracion-publica-2002", L790, "ley-790-2002", "LRAP02",
     "Renovación de la administración pública (Ley 790 de 2002)",
     on_publication(L790, "Ley 790", "Ley 790 de 2002", "22", "La presente ley rige a partir de la fecha de su promulgación")),
    ("escision-de-ministerios-2011", L1444, "ley-1444-2011", "LEM11",
     "Escisión de ministerios y facultades extraordinarias (Ley 1444 de 2011)",
     on_publication(L1444, "Ley 1444", "Ley 1444 de 2011", "21", "La presente ley rige a partir de la fecha de su promulgación")),
]
L679, L681 = "ley_0679_2001", "ley_0681_2001"
SPEC_ALL += [
    ("explotacion-sexual-de-menores-2001", L679, "ley-679-2001", "LESM01",
     "Prevención de la explotación, la pornografía y el turismo sexual con menores (Ley 679 de 2001)",
     on_publication(L679, "Ley 679", "Ley 679 de 2001", "39", "La presente ley rige a partir de su publicación")),
    ("combustibles-zonas-de-frontera-2001", L681, "ley-681-2001", "LCZF01",
     "Concesiones de combustibles en las zonas de frontera (Ley 681 de 2001)",
     on_publication(L681, "Ley 681", "Ley 681 de 2001", "15", "La presente ley rige a partir de la fecha de su publicación")),
]
L793, L60 = "ley_0793_2002", "ley_0060_1993"
SPEC_ALL += [
    ("extincion-de-dominio-2002", L793, "ley-793-2002", "LED02",
     "Extinción de dominio (Ley 793 de 2002)",
     on_publication(L793, "Ley 793", "Ley 793 de 2002", "24", "Esta Ley rige a partir de la fecha de, su promulgación")),
    ("competencias-y-recursos-1993", L60, "ley-60-1993", "LCR93",
     "Distribución de competencias y recursos (Ley 60 de 1993)",
     on_publication(L60, "Ley 60", "Ley 60 de 1993", "43", "La presente ley deroga todas las disposiciones que le sean contrarias y rige a partir de su publicación")),
]
L344, L443 = "ley_0344_1996", "ley_0443_1998"
SPEC_ALL += [
    ("racionalizacion-del-gasto-publico-1996", L344, "ley-344-1996", "LRGP96",
     "Racionalización del gasto público (Ley 344 de 1996)",
     on_publication(L344, "Ley 344", "Ley 344 de 1996", "44", "La presente Ley rige a partir de la fecha de su publicación")),
    ("carrera-administrativa-1998", L443, "ley-443-1998", "LCA98",
     "Carrera administrativa (Ley 443 de 1998)",
     on_publication(L443, "Ley 443", "Ley 443 de 1998", "87", "Esta ley rige a partir de su publicación")),
]
L141 = "ley_0141_1994"
SPEC_ALL += [
    ("regalias-1994", L141, "ley-141-1994", "LRG94",
     "Fondo Nacional de Regalías y regalías (Ley 141 de 1994)",
     on_publication(L141, "Ley 141", "Ley 141 de 1994", "70", "Esta Ley rige a partir de la fecha de su promulgación")),
]
L1142, L1185 = "ley_1142_2007", "ley_1185_2008"
SPEC_ALL += [
    ("convivencia-y-seguridad-ciudadana-2007", L1142, "ley-1142-2007", "LCSC07",
     "Reforma de las Leyes 906 de 2004, 599 de 2000 y 600 de 2000 y medidas para la convivencia y seguridad ciudadana (Ley 1142 de 2007)",
     on_publication(L1142, "Ley 1142", "Ley 1142 de 2007", "56",
                    "La presente ley rige a partir de la fecha de su publicación", "publication")),
    ("patrimonio-cultural-2008", L1185, "ley-1185-2008", "LPCult08",
     "Patrimonio cultural de la Nación, reforma de la Ley General de Cultura (Ley 1185 de 2008)",
     on_publication(L1185, "Ley 1185", "Ley 1185 de 2008", "26",
                    "La presente ley rige a partir de la fecha de su promulgación")),
]
L890, L1285 = "ley_0890_2004", "ley_1285_2009"


def start_890(units, enacted, pub):
    """Ley 890 de 2004, art. 15: in force from 1 January 2005, save arts. 7 to 13, in force at once. Dated from
    promulgation, when arts. 7-13 took effect (batch 7's Ley 1150 rule: the history dates the whole act from its first
    in-force day and names the later one)."""
    a = B7._clause(units, "15", "La presente ley rige a partir del 1o. de enero de 2005, con excepción de los artículos 7o. a "
                   "13, los que entrarán en vigencia en forma inmediata", "Ley 890", enacted, pub)
    return (pub, f"Ley 890 de 2004, art. 15: '{a}' The first version is dated from promulgation ({pub}), when arts. 7 to 13 "
                 f"took effect; the rest took effect on 2005-01-01.",
            f"The act as promulgated (Ley 890 de 2004, Diario Oficial No. 45.602 of {pub}). Its arts. 7 to 13 took effect on "
            f"promulgation, the rest on 1 January 2005 (art. 15). The history dates the whole act from promulgation. "
            f"Art. 15: '{a}'")
SPEC_ALL += [
    ("reforma-del-codigo-penal-2004", L890, "ley-890-2004", "LRCP04",
     "Reforma del Código Penal (Ley 890 de 2004)", start_890),
    ("reforma-de-la-administracion-de-justicia-2009", L1285, "ley-1285-2009", "LRAJ09",
     "Reforma de la Ley Estatutaria de la Administración de Justicia (Ley 1285 de 2009)",
     on_publication(L1285, "Ley 1285", "Ley 1285 de 2009", "28", "VIGENCIA. La presente ley rige a partir de su promulgación")),
]
L633, L488 = "ley_0633_2000", "ley_0488_1998"
SPEC_ALL += [
    ("reforma-tributaria-2000", L633, "ley-633-2000", "RT00", "Reforma tributaria (Ley 633 de 2000)",
     on_publication(L633, "Ley 633", "Ley 633 de 2000", "134", "La presente ley rige a partir de su promulgación")),
    ("reforma-tributaria-1998", L488, "ley-488-1998", "RT98", "Reforma tributaria (Ley 488 de 1998)",
     on_publication(L488, "Ley 488", "Ley 488 de 1998", "154", "La presente ley rige a partir de la fecha de su publicación")),
]
L1101, L1558 = "ley_1101_2006", "ley_1558_2012"
SPEC_ALL += [
    ("reforma-de-la-ley-general-de-turismo-2006", L1101, "ley-1101-2006", "LTur06",
     "Reforma de la Ley General de Turismo (Ley 1101 de 2006)",
     on_publication(L1101, "Ley 1101", "Ley 1101 de 2006", "20",
                    "La presente ley empezará a regir a partir de la fecha de su publicación", "publication")),
    ("reforma-de-la-ley-general-de-turismo-2012", L1558, "ley-1558-2012", "LTur12",
     "Reforma de la Ley General de Turismo (Ley 1558 de 2012)",
     on_publication(L1558, "Ley 1558", "Ley 1558 de 2012", "39",
                    "La presente ley rige a partir fecha de su publicación", "publication")),
]
L756 = "ley_0756_2002"
SPEC_ALL += [
    ("reforma-de-regalias-2002", L756, "ley-756-2002", "LReg02",
     "Reforma de la Ley 141 de 1994, regalías (Ley 756 de 2002)",
     on_publication(L756, "Ley 756", "Ley 756 de 2002", "42",
                    "La presente ley deroga todas las disposiciones que le sean contrarias y rige a partir de la fecha de su publicación",
                    "publication")),
]
L2388, L548 = "ley_2388_2024", "ley_0548_1999"
SPEC_ALL += [
    ("familia-de-crianza", L2388, "ley-2388-2024", "LFC24",
     "Familia de crianza (Ley 2388 de 2024)",
     on_publication(L2388, "Ley 2388", "Ley 2388 de 2024", "15",
                    "La presente ley entrará en vigencia a partir de su promulgación", "publication")),
    ("prorroga-de-la-ley-418-1999", L548, "ley-548-1999", "LOP99",
     "Prórroga y reforma de la Ley 418 de 1997 (Ley 548 de 1999)",
     on_publication(L548, "Ley 548", "Ley 548 de 1999", "4",
                    "La presente ley rige a partir de la fecha de su promulgación", "publication")),
]
SPEC = [x for x in SPEC_ALL if x[1] in (L2388, L548)]
# (batch 88, published in 99zzzzz-batch88; kept for reference) The Jurisprudencia Vigencia boxes of Ley 191 de 1995 date Sentencia C-615-96 '13 de noviembre de 1995', a year before the
# ruling's own number and the link the page gives it (c-615_1996.html), and before nothing it could rule on: read as 1996.
_PUBLISHED_88_JV = (("ley_0191_1995", ">C-615-96</A> de 13 de noviembre de 1995", ">C-615-96</A> de 13 de noviembre de 1996",
                    "the Jurisprudencia Vigencia boxes date Sentencia C-615 de 1996 '13 de noviembre de 1995'; the ruling's "
                    "number (C-615-96) and the page's own link to it (c-615_1996.html) give 1996: read as 13 November 1996"))

# ---- page repair: a heading with struck words whose '<Apartes tachados INEXEQUIBLES>' marker the page prints in the
# paragraph after a blank one (Ley 1450 de 2011 art. 38): batch 5's struck-heading reader wants the marker in the
# article's first paragraph, so the blank paragraph is dropped. HEAD_BLANK: page -> article names; a page that differs
# stops the parse.
import parse_batch5 as B5  # noqa: E402

HEAD_BLANK = {L1450: ["38"]}
_units_b5 = B5._units_et


def units_head_blank(name: str) -> list[dict]:
    units = _units_b5(name)
    if name not in HEAD_BLANK:
        return units
    done = []
    for u in units:
        ps = [k for k, it in enumerate(u["items"]) if it[0] == "p"]
        if (len(ps) > 1 and not E.plain(u["items"][ps[0]][1]).strip() and "<S>" in (u.get("raw_label") or u["label"] or "")
                or u["name"] in HEAD_BLANK[name]) and len(ps) > 1 and not E.plain(u["items"][ps[0]][1]).strip() \
                and any(re.search(r"tachad\w*\s+(derogad|INEXEQUIBLE)", x, re.I) for x in E.markers(u["items"][ps[1]][1])):
            u["items"] = [it for k, it in enumerate(u["items"]) if k != ps[0]]
            done.append(u["name"])
    B23._need(done == HEAD_BLANK[name], f"{name}: blank paragraph before a struck-heading marker {done}")
    return units


B5._units_et = units_head_blank

# ---- page repair (batch 90): Ley 1151 de 2007 was sanctioned by the President of Congress (Constitución arts. 166, 168):
# after the signatures, the last article's unit holds that sanction statement (quoting arts. 166 and 168 of the
# Constitution) and the Congress President's signature, which the signature cut does not recognise. Nothing from the
# first signature line on is the act's text: cut there. SIGN_CUT: page -> (article name, first signature line); a page
# that differs stops the parse.
SIGN_CUT = {L1151: ("160", "La Presidenta del honorable Senado de la República,")}
SIGN_CUT_DONE: list = []
_units_hb = B5._units_et


def units_sign_cut(name: str) -> list[dict]:
    units = _units_hb(name)
    if name not in SIGN_CUT:
        return units
    art, first = SIGN_CUT[name]
    u = next(u for u in units if u["name"] == art)
    ks = [k for k, it in enumerate(u["items"]) if it[0] == "p" and E.plain(it[1]).strip() == first]
    B23._need(len(ks) == 1, f"{name} art. {art}: signature line {first!r} {len(ks)}")
    rest = [E.plain(it[1]) for it in u["items"][ks[0]:] if it[0] == "p"]
    B23._need(any(x.startswith("En cumplimiento de lo ordenado en los artículos 166 y 168 de la Constitución") for x in rest),
              f"{name} art. {art}: sanction statement")
    B23._need(all(it[0] == "p" for it in u["items"][ks[0]:]), f"{name} art. {art}: boxes after the signatures")
    u["items"] = u["items"][:ks[0]]
    if name not in SIGN_CUT_DONE:
        SIGN_CUT_DONE.append(name)
    return units


B5._units_et = units_sign_cut


ACTS = [(s, pg, k, sh, t, page_title(pg), st) for s, pg, k, sh, t, st in SPEC]
PAGES = {pg for _, pg, *_ in SPEC}
HEADING_FIXES_58: list = [  # (batches 61, 62, 64 and 70's heading fixes, JV fixes and hand rules are published in
]                            # 99zza/99zzb/99zzd/99zzj)
_PUBLISHED_86 = [  # (batch 86's heading fix, published in 99zzz)
    ("ley_1473_2011", "Texto original de la Ley 1437 de 2011", "Texto original de la Ley 1473 de 2011",
     "art. 14: its earlier-text box is headed 'Texto original de la Ley 1437 de 2011' (Ley 1437 de 2011 is the CPACA, which "
     "has no such article; the box gives this act's own original art. 14, 'Comité consultivo para la regla fiscal'); read as "
     "'Texto original de la Ley 1473 de 2011'"),
]
_PUBLISHED_85 = [  # (batch 85's heading fix, published in 99zzy)
    ("ley_0938_2004", "Texto original de la Ley 938 de 2008", "Texto original de la Ley 938 de 2004",
     "art. 78: its earlier-text box is headed 'Texto original de la Ley 938 de 2008' (the act is of 2004; no Ley 938 de 2008 "
     "exists in its notes); read as 'Texto original de la Ley 938 de 2004'"),
]
_PUBLISHED_64 = [
    ("ley_1876_2017", "Texto original de la Ley 160 de 1994", "Texto original de la Ley 1876 de 2017",
     "arts. 30 and 31: their earlier-text boxes are headed 'Texto original de la Ley 160 de 1994' but give this act's own "
     "original articles (Ley 160 de 1994 has no such articles on extension services); read as the act's own original text"),
]
_PUBLISHED_82 = ([  # (batch 82's heading fix, published in 99zzv)
    ("ley_0919_2004", "Texto original de la Ley 919 de 2014", "Texto original de la Ley 919 de 2004",
     "art. 2: its earlier-text box is headed 'Texto original de la Ley 919 de 2014' (the act is of 2004; no Ley 919 de 2014 "
     "exists in its notes); read as 'Texto original de la Ley 919 de 2004'"),
])
B4.HEADING_FIXES.extend(HEADING_FIXES_58)
# Page slips fixed in the HTML before the engine reads it (batch 15's RAW_FIXES; (page, exact HTML, replacement, why)).
RAW_82 = [
    ("ley_1482_2011",
     'OBJETO DE LA LEY.<span class="i_aj"> &lt;</span></A>Art&iacute;culo modificado por el art&iacute;culo '
     '<A href="ley_1752_2015.html#1" >1</A> de la Ley 1752 de 2015. El nuevo texto es el siguiente:<A name="1"><span '
     'class="i_aj">&gt;</span></A>',
     'OBJETO DE LA LEY.</A> &lt;Art&iacute;culo modificado por el art&iacute;culo '
     '<A href="ley_1752_2015.html#1" >1</A> de la Ley 1752 de 2015. El nuevo texto es el siguiente:&gt;',
     "art. 1: the page opens the '<Artículo modificado por el artículo 1 de la Ley 1752 de 2015 ...>' marker inside the "
     "heading anchor and closes it inside a second anchor of the same name; read as heading, then marker"),
    ("ley_0098_1993", "Diario Oficial No. 41.151 de diciembre 23 de 1993.", "Diario Oficial No. 41.151 de 23 de diciembre de 1993.",
     "heading: 'Diario Oficial No. 41.151 de diciembre 23 de 1993' (month before day) read as 23 December 1993"),
]
# batch 90: Ley 812 de 2003 prints four article numbers after the heading anchor ('ARTÍCULO </A><span ...>79.</span>')
for _pg, _n in (("ley_0812_2003_pr001", "79"), ("ley_0812_2003_pr002", "101"), ("ley_0812_2003_pr002", "126"),
                ("ley_0812_2003_pr002", "131")):
    RAW_82.append((_pg, f'<a class="bookmarkaj" name="{_n}">ART&Iacute;CULO </A><span class="b_aj">{_n}.</span>',
                   f'<a class="bookmarkaj" name="{_n}">ART&Iacute;CULO {_n}.</A>',
                   f"art. {_n}: the page prints the article's number after its heading anchor ('ARTÍCULO' alone in the "
                   "anchor); read as one heading"))
RAW_82 += [
    ("ley_1151_2007_pr001",
     'ART&Iacute;CULO 79. MACRO</A> <A name="79"><span class="i_aj"><B>PROYECTOS DE INTER&Eacute;S SOCIAL NACIONAL.</B></span></A>',
     'ART&Iacute;CULO 79. MACRO PROYECTOS DE INTER&Eacute;S SOCIAL NACIONAL.</A>',
     "art. 79: the page splits the heading 'MACRO / PROYECTOS DE INTERÉS SOCIAL NACIONAL.' over two anchors; read as one heading"),
    ("ley_0812_2003_pr001",
     'MENCI&Oacute;N EL ART&Iacute;CULO 11 DE LA LEY 21 DE </A>1982.</span>',
     'MENCI&Oacute;N EL ART&Iacute;CULO 11 DE LA LEY 21 DE 1982.</A></span>',
     "art. 87: the page closes the heading anchor before the year of 'Ley 21 de 1982'; read as one heading"),
]
RAW_HITS_82: dict = {}
_read_82 = E.read


def read_82(url: str):
    """batch 15's page-slip reader for this batch's RAW_82 (its own hits, its own decision lines)."""
    t = _read_82(url)
    if t is None:
        return t
    name = url.rsplit("/", 1)[-1].removesuffix(".html")
    for page, old, new, _ in RAW_82:
        if name == page and url.endswith(".html"):
            n = t.count(old)
            if n != 1:
                raise SystemExit(f"{page}: page slip not found once ({n})")
            RAW_HITS_82[page] = 1
            t = t.replace(old, new)
    return t


E.read = read_82
B23.subst.install(E, PAGES)
B30.C458_PAGES.clear()
B30.C458_PAGES.update(PAGES)
B27.NOTE_PAGES.clear()
B27.NOTE_PAGES.update(PAGES)
B24.PAGES.clear()
B24.PAGES.update(PAGES)
B24.BATCH_LABEL = BATCH
B24.KEY_FIXES_USED = {}
B24.HAND_FIXES.clear()
B24.TAIL.clear()
B24.REPEALS.clear()
# Ley 232 de 1995 repealed as a whole by Ley 1801 de 2016 (Código Nacional de Seguridad y Convivencia Ciudadana) art. 242,
# from the code's start on 29 January 2017 (six months after its promulgation, art. 243): the page prints each of the six
# articles under '<Ley derogada por el artículo 242 de la Ley 1801 de 2016. Rige a partir del 29 de enero de 2017>'. The
# marker is taken out of the text and a last version on that day holds no provisions, credited to Ley 1801 de 2016.
B24.REPEALS[L232] = {
    "marker": re.compile(r"&lt;Ley derogada por el art&iacute;culo (?:<A [^>]*>)?242(?:</A>)? de la Ley (?:<A [^>]*>)?1801"
                         r"(?:</A>)? de 2016\. Rige a partir del 29 de enero de 2017&gt;\s*"),
    "law": "ley-1801-2016", "day": "2017-01-29", "min": 6,
    "note": "Ley 1801 de 2016 (Código Nacional de Seguridad y Convivencia Ciudadana), art. 242, repealed Ley 232 de 1995 from "
            "the code's entry into force on 29 January 2017, six months after its promulgation (art. 243: 'La presente ley "
            "regirá seis (6) meses después de su promulgación'); art. 242 names 'la Ley 232 de 1995' among the acts it "
            "repeals.",
    "check": ("ley_1801_2016", "242", "El presente Código deroga todas las disposiciones que le sean contrarias, en especial "
              "el Decreto-ley 1355 de 1970, la Ley 1356 de 2009 excepto los artículos 4o y del 218A al 218L; el Decreto "
              "número 522 de 1971; la Ley 232 de 1995;"),
}
# (batch 93) Ley 60 de 1993 repealed as a whole by Ley 715 de 2001 art. 113 from its sanction, 21 December 2001 ('La
# presente Ley rige a partir de la fecha de su sanción y deroga la Ley 60 de 1993, ...'): the page prints each article under
# '<Ley derogada por el artículo 113 de la Ley 715 de 2001>' (arts. 40 and 42, struck earlier, under their own
# '<Artículo INEXEQUIBLE>'). The marker is taken out of the text and a last version on that day holds no provisions,
# credited to Ley 715 de 2001.
L715 = "ley_0715_2001"
B24.REPEALS[L60] = {
    "marker": re.compile(r"&lt;Ley derogada por el art&iacute;culo (?:<A [^>]*>)?113(?:</A>)? de la Ley 715 de 2001&gt;\s*"),
    "law": "ley-715-2001", "day": "2001-12-21", "min": 41,
    "note": "Ley 715 de 2001 (Sistema General de Participaciones), art. 113, repealed Ley 60 de 1993 from its own day, the "
            "day of its sanction, 21 December 2001 ('La presente Ley rige a partir de la fecha de su sanción y deroga la Ley "
            "60 de 1993, ...').",
    "check": (L715, "113", "La presente Ley rige a partir de la fecha de su sanción y deroga la Ley 60 de 1993"),
}
B29.HAND_FIXES.clear()
B29.HAND_DONE.clear()
B29.SIGNED.clear()
B29.BATCH = BATCH
B30.BATCH = BATCH
# Printed repeals (batch 10's REPEAL_MARK) also when the marker names a decree with 'del' and no link to the article
# (Decreto 2153 de 1992: '<Artículo derogado por el artículo 19 del Decreto 3523 de 2009>' + the words until then), and
# when the link is on the act's number instead (Ley 550 de 1999 art. 60: 'de la Ley <A ...>1673</A> de 2013').
B13.B10.REPEAL_MARK = re.compile(r'^\s*(?:<span class="b_aj">)?&lt;Art&iacute;culo derogado por el art&iacute;culo '
                                 r'(?:<A [^>]*>)?\d+(?:</A>)? (?:de la|del) (Ley|Decreto) (?:<A [^>]*>)?(\d+)(?:</A>)? de (\d{4})&gt;\s*'
                                 r'(?:</span>)?\s*')


def write_part(acts, out, names):
    """The part's own decision lines; each starts with the act's title (phase2's write_part keeps only those)."""
    title = {pg: t for _, pg, _, _, t, _, _ in ACTS}
    both = names[0] + " and the other acts of " + BATCH
    import stray as _stray  # the page is read more than once: each stray block is listed once
    for _k in _stray.DONE:
        _stray.DONE[_k] = list(dict.fromkeys(_stray.DONE[_k]))
    P.DECISIONS.extend(f"{title[page.split('_pr')[0]]}: {why}." for page, _, _, why in RAW_82
                       if page.split('_pr')[0] in title and RAW_HITS_82.get(page))
    P.DECISIONS.extend(B24.REPEAL_DONE)
    P.DECISIONS.extend(f"{title[page]}: {why}." for page, _, _, why in B4.JV_FIXES if page in PAGES)
    P.DECISIONS.extend(WHOLE_DONE)
    P.DECISIONS.extend(PARTIAL_DONE)
    P.DECISIONS.extend(PARTIAL93_DONE)
    P.DECISIONS.extend(globals().get("PARTIAL94_DONE", []))
    if any(pg == L2272 for _, pg, *_ in ACTS):
        B23._need(VIG_2272 in B3.article_text(P.doc_units(L2272), "19"), "Ley 2272 art. 19 term")
        P.DECISIONS.append(
            "Política de paz de Estado y prórroga de la Ley 418 de 1997 (Ley 2272 de 2022): art. 19 gives arts. 3 to 9 and 15 "
            "'una vigencia de cuatro (4) años, a partir de su promulgación' (to 4 November 2026, after the retrieval day). No "
            "version takes them out: the term has not run on the retrieval day, the source gives no later act on it, and the "
            "four-year terms of Ley 418 de 1997 and its extending acts are likewise no version in this record.")
    if any(pg == "ley_0141_1994" for _, pg, *_ in ACTS):
        P.DECISIONS.append(L141_PUB_WHY)
    P.DECISIONS.extend(QUOTED_ART_DONE)
    P.DECISIONS.extend(QUOTED_ET_DONE)
    P.DECISIONS.extend(QUOTED_633_DONE)  # (batch 98)
    P.DECISIONS.extend(list(dict.fromkeys(QUOTED_HEADS_DONE)))
    P.DECISIONS.extend(sorted(set(PARA_JOIN_DONE)))
    P.DECISIONS.extend(sorted(set(DROP_EMPTY_DONE)))
    P.DECISIONS.extend(list(dict.fromkeys(PAGE59_DONE)))
    if any(pg == L4 for _, pg, *_ in ACTS):
        head = " ".join(E.plain(it[1]) for it in P.doc_units(L4)[0]["items"] if it[0] == "p")
        B23._need("Esta Ley no incluye análisis de vigencia completo" in head, "Ley 4 de 1913: head note")
        P.DECISIONS.append(L4_VIGENCIA)
    P.DECISIONS.extend(BOX_SPILL_DONE)
    P.DECISIONS.extend(list(dict.fromkeys(BOX_TAIL_DONE)))
    P.DECISIONS.extend(list(dict.fromkeys(EMPTY_ANCHOR_DONE)))
    P.DECISIONS.extend(list(dict.fromkeys(END_NOTES_DONE)))
    P.DECISIONS.extend(f"{title[pg]}: art(s). {', '.join(d)}: the quoted heading and words the page prints after the article "
                       "under a heading anchor of their own are read as the article's quoted text, not as the act's headings."
                       for pg, d in sorted(QUOTED_DONE.items()) if d and pg in title and pg not in QUOTED_HEADS)
    P.DECISIONS.extend(UNANCHORED_DONE)
    P.DECISIONS.extend(B26.STAGE_DONE)
    P.DECISIONS.extend(TITLE_GONE_DONE)
    if any(pg == L550 for _, pg, *_ in ACTS):
        P.DECISIONS.append(
            "Reestructuración empresarial (Ley 550 de 1999): art. 79 made the act a five-year law from its publication; "
            "Ley 922 de 2004 art. 1 extended it two years from 31 December 2004 and Ley 1116 de 2006 art. 126 a further "
            "six months from its promulgation, after which it applies permanently only to the territorial entities, "
            "their decentralised bodies and the state universities of Ley 922 de 2004 (Ley 1116 arts. 125-126; the page "
            "prints that scope before every article and in the vigencia notes). These extensions and the narrower scope "
            "change no words of the act, so they are no version here; the text stays in the record. Ley 1116 art. 125's "
            "transfer of the promotion of the universities' agreements to the Ministerio de Educación likewise changes "
            "no printed words (art. 1 still names the Ministerio de Hacienda y Crédito Público, as the page prints it).")
    for _, pg, _, _, t, _, _ in ACTS:
        if pg in (D4633, D4634, D4635):
            P.DECISIONS.append(
                f"{t}: Sentencia C-588-19 (press release of 5 December 2019) struck the words 'tendrá una vigencia de diez "
                "(10) años' of the vigencia article with effect deferred to 10 June 2021; Ley 2078 de 2021 (Diario Oficial "
                "No. 51.551 of 8 January 2021) replaced the article before that day, extending the decree's term to 9 "
                "December 2031, so the ruling never took effect on the printed words: the words as issued stand until 8 "
                "January 2021 and the ruling is no version here.")
    if any(pg == L1111 for _, pg, *_ in ACTS):
        u38 = " ".join(E.plain(b) for b in B23._boxes(B23._unit(L1111, "38"), "Notas de Vigencia"))
        B23._need("Numeral corregido por el artículo 1 del Decreto 4651 de 2006, publicado en el Diario Oficial No. 46.494 de "
                  "27 de diciembre de 2006" in u38, "Ley 1111 art. 38 note")
        P.DECISIONS.append(
            "Reforma tributaria (Ley 1111 de 2006): art. 38, numeral 13 reads 'Las comisiones pagadas ...' from the act's "
            "first day: Decreto 4651 de 2006 art. 1 corrected the printed 'Las emisiones pagadas ...' in Diario Oficial No. "
            "46.494 of 27 December 2006, the same issue that promulgated the act, so the corrected words are the ones in "
            "force from that day.")
    if struck.DONE:
        P.DECISIONS.append(f"{both}: earlier-text blocks of amendments by Decretos 1122 de 1999 and 266 de 2000 (both struck "
                           "as a whole: Sentencias C-923-99 of 18 November 1999 and C-1316-00 of 26 September 2000) are "
                           "read as wording in force from the decree's day to the ruling's, when the text before it returns, "
                           "credited to the ruling on its day (C-1316-00 gave its ruling effect from the decree's "
                           "promulgation; the decree's wording is still shown for the months it was applied); page "
                           "variants read the same way: " + "; ".join(struck.DONE) + ".")
    if SPLIT_DONE:
        P.DECISIONS.append("Heading anchors that hold only the letter 'A' of 'ARTÍCULO' (the rest of the heading starts the "
                           "article's first paragraph) were rebuilt from that paragraph: "
                           + ", ".join(sorted(set(SPLIT_DONE))) + ".")
    return B30.write_part(acts, out, names)



# ---- page repair: heading anchors that hold only the 'A' of 'ARTÍCULO' (Ley 82 de 1993 arts. 5, 7, 8: label 'A', the
# paragraph 'RTÍCULO 5o. <epigraph in bold>. <marker> ...'): the heading is rebuilt from the paragraph.
SPLIT_HEAD = re.compile(r'\s*RT&Iacute;CULO (\d+)o?\.\s*(?:<span class="i_aj"><B>((?:(?!</B>).)+)</B></span><B>\.</B>)?\s*')
SPLIT_DONE: list[str] = []
_units_b48 = P.doc_units


_markers_b48 = E.markers
EXPR_DEROG = re.compile(r"^Expresi[oó]n .{1,80}? derogada por el art[ií]culo \d+ de la Ley \d+ de \d{4}$")


def _markers_heading(h: str) -> list[str]:
    """Batch 5's struck-heading check wants a 'tachad... derogad' marker; Ley 1955 de 2019 art. 118 marks its struck
    heading words '<Expresión "Colombia rural" derogada por el artículo 372 de la Ley 2294 de 2023>' (a marker naming the
    struck expression). Used only while the units are read."""
    ms = _markers_b48(h)
    return ms + ["texto tachado derogado"] if any(EXPR_DEROG.match(m) for m in ms) else ms


def doc_units_split(name: str) -> list[dict]:
    if name in PAGES:
        E.markers = _markers_heading
    try:
        units = _units_b48(name)
    finally:
        E.markers = _markers_b48
    if name not in PAGES:
        return units
    for u in units[1:]:
        ps = [k for k, it in enumerate(u["items"]) if it[0] == "p"]
        if (u["label"] or "").strip() != "A" or not ps:
            continue
        it = u["items"][ps[0]]
        m = SPLIT_HEAD.match(it[1])
        B23._need(m, f"{name} split heading {it[1][:60]}")
        epi = E.tidy(E.plain(m.group(2) or ""))
        u["label"] = f"ARTÍCULO {m.group(1)}o." + (f" {epi}." if epi else "")
        u["items"][ps[0]] = ("p", it[1][m.end():]) + tuple(it[2:])
        if f"{name} {m.group(1)}" not in SPLIT_DONE:
            SPLIT_DONE.append(f"{name} {m.group(1)}")
    return units


P.doc_units = doc_units_split
E.doc_units = doc_units_split


# ---- page repair: amending articles that quote whole books, titles or chapters of another code (as Ley 1819 de 2016,
# batch 44). The page gives the quoted text after a book/title/chapter heading its own heading anchor ('Nivel-N-tail'),
# or keeps a quoted 'LIBRO ...' line inside the article, where the engine's split_libro cuts it off; either way those
# words went into titulos.md. Here each tail goes back to its article (the heading as a line of the text) and the
# articles quoting a book keep it (an article with a rejoined tail is never cut at a 'LIBRO' line). QUOTED_TAILS: page -> article names whose tail follows them; QUOTED_BOOKS: page ->
# articles with a quoted 'LIBRO' line. A page whose tails differ from the list stops the parse.
QUOTED_TAILS: dict[str, list[str]] = {L1395: ["23"], L1607: ["10", "11", "98"], L1826: ["8", "9", "12", "26"]}
QUOTED_TAILS["ley_0795_2003"] = ["48"]  # Ley 795 de 2003 art. 48 quotes the EOSF chapter on the Fondo Nacional de Garantías  # Ley 1395 art. 23 quotes CPC headings (Título XXII, Capítulo II)
QUOTED_BOOKS: dict[str, list[str]] = {}
QUOTED_DONE: dict[str, list[str]] = {}
_units_quoted = P.doc_units
_split_libro_q = E.split_libro


def doc_units_quoted(name: str) -> list[dict]:
    units = _units_quoted(name)
    if name not in QUOTED_TAILS and name not in QUOTED_BOOKS:
        return units
    out, done = [], []
    for u in units:
        m = re.fullmatch(r"Nivel-(\d+)-tail", u["name"] or "")
        if m and out and out[-1]["name"] == m.group(1):
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + [("p", u["label"])] + list(u["items"]), nosplit=True)
            done.append(m.group(1))
            continue
        if u["name"] in QUOTED_BOOKS.get(name, []):
            u = dict(u, nosplit=True)
        out.append(u)
    B23._need(done == QUOTED_TAILS.get(name, []), f"{name}: quoted tails {done}")
    QUOTED_DONE[name] = done
    return out


def split_libro_quoted(u: dict):
    return (u, []) if u.get("nosplit") else _split_libro_q(u)


P.doc_units = doc_units_quoted
E.doc_units = doc_units_quoted
E.split_libro = split_libro_quoted






# ---- page repair: Ley 222 de 1995 prints art. 128 and the heading 'SECCION IX. AUDIENCIAS' with no anchors of their own,
# as the last paragraphs of art. 127; they become an article unit and a heading unit. UNANCHORED: page -> [(unit,
# article label start)]; a page that differs stops the parse.
UNANCHORED = {L222: [("127", "ARTICULO 128. ")]}
UNANCHORED_DONE: list[str] = []
_units_un = P.doc_units


def doc_units_unanchored(name: str) -> list[dict]:
    units = _units_un(name)
    if name not in UNANCHORED:
        return units
    out = []
    for u in units:
        want = [lab for n, lab in UNANCHORED[name] if n == u["name"]]
        if not want:
            out.append(u)
            continue
        items = list(u["items"])
        k = next((i for i, it in enumerate(items) if it[0] == "p" and E.tidy(E.plain(it[1])).startswith(want[0])), None)
        B23._need(k is not None, f"{name} {u['name']}: no '{want[0]}'")
        t = E.tidy(E.plain(items[k][1]))
        m = re.match(r"(ARTICULO (\d+)\. (?:[A-ZÁÉÍÓÚÑ ,]+\.)?)\s*(.*)", t)
        B23._need(m, f"{name} {u['name']}: label {t[:60]}")
        rest = items[k + 1:]
        sec = [i for i, it in enumerate(rest) if it[0] == "p" and re.fullmatch(r"SECCI[ÓO]N [IVX]+\.", E.tidy(E.plain(it[1])))]
        B23._need(len(sec) == 1 and len(rest) == sec[0] + 2, f"{name} {u['name']}: section heading {sec}")
        j = sec[0]
        out.append(dict(u, items=items[:k]))
        for marked in B26.STAGE_UNITS.get(name, {}).values():  # the staged-repeal reader ran on the page's units
            if u["name"] in marked and re.search(r"Ley 1116 de 2006", E.plain(items[k][1])) is None:
                marked.add(m.group(2))
        body = E.html.escape(m.group(3), quote=False)
        out.append({"name": m.group(2), "label": m.group(1), "items": [("p", body)] + rest[:j], "page": u.get("page", name)})
        out.append({"name": f"Nivel-{m.group(2)}-tail", "label": E.tidy(E.plain(rest[j][1])),
                    "items": [("p", ""), ("p", f'<span class="b_aj">{E.html.escape(E.tidy(E.plain(rest[j + 1][1])), quote=False)}</span>')],
                    "page": u.get("page", name)})
        if not UNANCHORED_DONE:
            UNANCHORED_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]}: the page prints art. "
                                   f"{m.group(2)} and the heading '{E.tidy(E.plain(rest[j][1]))} "
                                   f"{E.tidy(E.plain(rest[j + 1][1]))}' as the last paragraphs of art. {u['name']}, with no "
                                   "anchors of their own; they are read as an article and a heading")
    return out


P.doc_units = doc_units_unanchored
E.doc_units = doc_units_unanchored


# ---- page repair: an earlier-text box that stops at its heading ('Texto original de la Ley 1753 de 2015: ARTÍCULO .')
# while the earlier text itself is printed as paragraphs after the article's last box (Ley 1753 de 2015 art. 59): those
# paragraphs go back into the box, after its heading line. BOX_SPILL: page -> article names; a page that differs stops.
BOX_SPILL = {L1753: ["59"]}
BOX_SPILL_DONE: list[str] = []
_units_spill = P.doc_units
SPILL_END = "<p>ART&Iacute;CULO .</p> </td></tr></tbody>"


def doc_units_spill(name: str) -> list[dict]:
    units = _units_spill(name)
    if name not in BOX_SPILL:
        return units
    done = []
    for u in units:
        its = u["items"]
        boxes = [i for i, it in enumerate(its) if it[0] == "box"]
        if not boxes or not its[boxes[-1]][2].endswith(SPILL_END):
            continue
        k = boxes[-1]
        tail = its[k + 1:]
        B23._need(tail and all(it[0] == "p" for it in tail), f"{name} {u['name']}: spilled earlier text")
        paras = [E.tidy(E.plain(it[1])) for it in tail]
        paras = [x for x in paras if x]
        B23._need(re.match(r"A?RT[ÍI]CULO " + re.escape(u["name"]) + r"\.", paras[0].replace("A RT", "ART")) is not None
                  or paras[0].startswith("ARTÍCULO " + u["name"] + "."), f"{name} {u['name']}: spill starts {paras[0][:40]}")
        html_ = "".join(f"<p>{E.html.escape(x, quote=False)}</p>" for x in paras)
        box = its[k][2][: -len(SPILL_END)] + html_ + " </td></tr></tbody>"
        u["items"] = its[:k] + [its[k][:2] + (box,) + tuple(its[k][3:])]
        done.append(u["name"])
    B23._need(done == BOX_SPILL[name], f"{name}: spilled boxes {done}")
    if not BOX_SPILL_DONE:
        BOX_SPILL_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]}: art(s). {', '.join(done)}: the page "
                              "ends the earlier-text box 'Texto original' at its heading ('ARTÍCULO .') and prints the "
                              "original text as paragraphs after the article's notes; they are read as that box's text, "
                              "not as words of today's article")
    return units


P.doc_units = doc_units_spill
E.doc_units = doc_units_spill


# ---- page repair: an earlier-text box that stops after its first lines ('... así: Puntos'), the page printing the rest of
# the original text (a points table, an inciso, the parágrafo's first inciso) as paragraphs after the box (Ley 335 de 1996
# art. 25). BOX_TAIL: page -> {article: number of trailing paragraphs that belong to its last earlier-text box}; each
# must follow that box directly. A page that differs stops the parse.
BOX_TAIL: dict = {}  # (Ley 335 de 1996 art. 25: published in 99zzk-batch71)
BOX_TAIL_DONE: list[str] = []
_units_box_tail = P.doc_units
_TBODY = " </td></tr></tbody>"


def doc_units_box_tail(name: str) -> list[dict]:
    units = _units_box_tail(name)
    if name not in BOX_TAIL:
        return units
    done = []
    for u in units:
        n = BOX_TAIL[name].get(u["name"])
        if not n:
            continue
        its = u["items"]
        k = len(its) - n - 1
        B23._need(k >= 0 and its[k][0] == "box" and its[k][1] == "Legislación Anterior" and its[k][2].endswith(_TBODY)
                  and all(it[0] == "p" for it in its[k + 1:]), f"{name} {u['name']}: box tail")
        box = its[k][2][: -len(_TBODY)] + "".join(f"<p>{it[1]}</p>" for it in its[k + 1:]) + _TBODY
        u["items"] = its[:k] + [its[k][:2] + (box,) + tuple(its[k][3:])]
        done.append(u["name"])
    B23._need(done == list(BOX_TAIL[name]), f"{name}: box tails {done}")
    t = dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]
    BOX_TAIL_DONE.append(f"{t}: art(s). {', '.join(done)}: the page ends the earlier-text box of the original text after "
                         "its first lines and prints the rest of that text (the points table, the next inciso and the "
                         "parágrafo's first inciso) as paragraphs after the box; they are read as that box's text, not as "
                         "words of today's article")
    return units


P.doc_units = doc_units_box_tail
E.doc_units = doc_units_box_tail


# ---- page repair: empty anchors inside an article ('<p><A name="1"></A></p>' before each paragraph of Ley 310 de 1996
# art. 2 as Ley 2294 de 2023 rewrote it), which the engine read as units of their own named '1' (with no heading). Such
# units go back, in order, into the article they follow. EMPTY_ANCHOR_UNITS: page -> {article: number of units}; a page
# that differs stops the parse.
EMPTY_ANCHOR_UNITS: dict = {}  # (Ley 310 de 1996 art. 2: published in 99zzl-batch72)
EMPTY_ANCHOR_DONE: list[str] = []
_units_empty_anchor = P.doc_units


def doc_units_empty_anchor(name: str) -> list[dict]:
    units = _units_empty_anchor(name)
    if name not in EMPTY_ANCHOR_UNITS:
        return units
    out, joined = [], {}
    for u in units:
        if out and out[-1]["name"] in EMPTY_ANCHOR_UNITS[name] and not (u.get("label") or "").strip()                 and re.fullmatch(r"\d+", u["name"] or "") and u["name"] != out[-1]["name"]:
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + list(u["items"]))
            joined[out[-1]["name"]] = joined.get(out[-1]["name"], 0) + 1
            continue
        out.append(u)
    B23._need(set(joined) == set(EMPTY_ANCHOR_UNITS[name]), f"{name}: empty anchors {joined}")
    t = dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]
    EMPTY_ANCHOR_DONE.append(f"{t}: art(s). {', '.join(joined)}: the page puts an empty anchor before each paragraph of "
                             "the article's current text; those paragraphs are read as the article's, not as units of "
                             "their own")
    return out


P.doc_units = doc_units_empty_anchor
E.doc_units = doc_units_empty_anchor


# ---- page repair: the footnotes of a decree's considerations, which the page prints after the signatures of its last
# article, behind a '* * *' line (Decretos Ley 588 and 589 de 2017). They are not words of the act; the paragraphs from
# that line on are dropped from the article (the signature cut then applies as usual). END_NOTES: page -> article; a page
# whose article lacks the line, or whose dropped paragraphs do not all start with a note number (or are a URL or empty),
# stops the parse.
END_NOTES: dict = {}  # (Decretos Ley 588 and 589 de 2017: published in 99zzp-batch76)
END_NOTES_DONE: list[str] = []
_units_end_notes = P.doc_units


def doc_units_end_notes(name: str) -> list[dict]:
    units = _units_end_notes(name)
    if name not in END_NOTES:
        return units
    out = []
    for u in units:
        if u["name"] == END_NOTES[name]:
            items = list(u["items"])
            k = [i for i, it in enumerate(items) if it[0] == "p" and E.plain(it[1]).strip() == "* * *"]
            B23._need(len(k) == 1, f"{name}: end-notes line {k}")
            rest = [E.plain(it[1]).strip() for it in items[k[0]:] if it[0] == "p"][1:]
            B23._need(all(re.match(r"\d{1,2} \S", x) or x.startswith("http") or not x for x in rest)
                      and any(re.match(r"1 \S", x) for x in rest), f"{name}: end notes {rest[:2]}")
            B23._need(all(it[0] == "p" for it in items[k[0]:]), f"{name}: box among end notes")
            u = dict(u, items=items[:k[0]])
            t = dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]
            END_NOTES_DONE.append(f"{t}: art. {END_NOTES[name]}: the footnotes of the decree's considerations, which the "
                                  "page prints after the signatures behind a '* * *' line, are not words of the act and "
                                  "are left out.")
        out.append(u)
    return out


P.doc_units = doc_units_end_notes
E.doc_units = doc_units_end_notes


# ---- page repair: amending articles that quote a whole article of another code ('El artículo 100 del Código de
# Comercio quedará así:') where the page gives the quoted article its own heading anchor ('ARTICULO 100.'), so the
# engine read it as an article of this act (Ley 222 de 1995 arts. 1, 2, 18, 24, 26, 27, 31, 32, 69). Each quoted unit
# goes back into the quoting article: its heading becomes a line of that article's text, its paragraphs and note boxes
# follow. QUOTED_ARTS: page -> [(quoting article, quoted unit)]; a page whose quoted units differ stops the parse.
QUOTED_ARTS: dict[str, list[tuple[str, str]]] = {
    L222: [("1", "100"), ("2", "103"), ("18", "184"), ("24", "200"), ("26", "260"), ("27", "261"), ("31", "265"),
           ("32", "262"), ("69", "429")],
}
QUOTED_ART_DONE: list[str] = []
QUOTES = re.compile(r"quedar[áa]n? as[íi]:\s*$")
_units_qa = P.doc_units


def doc_units_qa(name: str) -> list[dict]:
    units = _units_qa(name)
    if name not in QUOTED_ARTS:
        return units
    out, done, own = [], [], None
    for u in units:
        n = u["name"] or ""
        if own and re.fullmatch(r"\d+", n) and int(n) != int(own) + 1:
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + [("p", E.html.escape(u["label"].strip(), quote=False))]
                           + list(u["items"]))
            done.append((own, n))
            continue
        out.append(u)
        own = None
        if re.fullmatch(r"\d+", n):
            ps = [E.tidy(E.plain(it[1])) for it in u["items"] if it[0] == "p" and E.tidy(E.plain(it[1]))]
            own = n if ps and QUOTES.search(ps[-1]) else None
    B23._need(done == QUOTED_ARTS[name], f"{name}: quoted articles {done}")
    if done and not any(x.startswith(name) for x in QUOTED_ART_DONE):
        QUOTED_ART_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]}: articles that rewrite a whole article of the Código de Comercio print the "
                               "quoted article under its own heading; it is read as part of the quoting article (art. "
                               + ", ".join(f"{a} quotes art. {q}" for a, q in done) + ")")
    return out


P.doc_units = doc_units_qa
E.doc_units = doc_units_qa


# ---- Ley 1607 de 2012 arts. 10 and 11 add Chapters I and II to Título V of Libro I of the Estatuto Tributario; the page
# gives each quoted ET article (329 to 341) and each quoted chapter/section heading its own anchor ('ET_329',
# 'Nivel-ET_330-tail', ...; the chapter headings right after arts. 10 and 11 are QUOTED_TAILS), each with the ET's later notes. Coordinator decision (2026-10-31): the quoted articles are the
# text of arts. 10 and 11 as enacted; they stay inside arts. 10 and 11 as quoted text, with no separate units and none of
# the ET's later notes. So: each quoted unit is joined to its article, its heading a line of the text; its markers and note
# boxes are dropped; ET art. 334 reads its 'Texto original de la Ley 1607 de 2012' box (the page prints Ley 1739 de
# 2014's rewrite) and ET art. 336 drops the parágrafo 3o. Ley 1739 de 2014 added. QUOTED_ET: page -> {article: units}.
QUOTED_ET = {L1607: {"10": ["ET_329", "ET_330", "Nivel-ET_330-tail", "ET_331", "ET_332", "ET_333",
                            "Nivel-ET_333-tail", "ET_334", "ET_335"],
                     "11": ["ET_336", "ET_337", "ET_338", "ET_339", "ET_340", "ET_341"]}}
QUOTED_ET_DONE: list[str] = []
MARK = re.compile(r"(?:<span class=\"b_aj\">\s*)?&lt;(?:(?!&gt;).)*&gt;(?:\s*</span>)?\s*", re.S)
_units_et_q = P.doc_units


def doc_units_quoted_et(name: str) -> list[dict]:
    units = _units_et_q(name)
    if name not in QUOTED_ET:
        return units
    out, cur, seen = [], None, {}
    for u in units:
        n = u["name"] or ""
        if n in QUOTED_ET[name]:
            cur = n
            seen[n] = []
            out.append(u)
            continue
        if cur and (n.startswith("ET_") or (n.startswith("Nivel-") and n.endswith("-tail"))):
            ps = [it for it in u["items"] if it[0] == "p"]
            if n == "ET_334":
                box = B23._boxes(u, "Legislación Anterior")[0]
                ls = B23._box_lines(box, "Texto original de la Ley 1607 de 2012")
                ls[0] = re.sub(r"^ARTÍCULO 334\.\s*", "", ls[0])
                ps = [("p", E.html.escape(x, quote=False)) for x in ls if x]
            if n == "ET_336":
                k = [i for i, it in enumerate(ps) if "Parágrafo adicionado por el artículo 34 de la Ley 1739 de 2014" in E.plain(it[1])]
                B23._need(len(k) == 1 and len(ps) - k[0] == 6, f"{name} ET_336 parágrafo 3")
                ps = ps[:k[0]]  # the parágrafo 3o. and its five following paragraphs (numerals 1-4, closing inciso)
            lines = [("p", E.html.escape(u["label"].strip(), quote=False))]
            lines += [("p", MARK.sub("", it[1])) for it in ps]
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + lines, nosplit=True)
            seen[cur].append(n)
            continue
        cur = None
        out.append(u)
    B23._need(seen == QUOTED_ET[name], f"{name}: quoted ET units {seen}")
    if not QUOTED_ET_DONE:
        QUOTED_ET_DONE.append("Reforma tributaria (Ley 1607 de 2012): arts. 10 and 11 add Chapters I and II to Título V of "
                              "Libro I of the Estatuto Tributario (ET arts. 329 to 341). The page gives each quoted ET "
                              "article and heading its own anchor with the ET's later notes (Ley 1739 de 2014, Ley 1819 de "
                              "2016 art. 1, rulings). Coordinator decision: the quoted articles are the text of arts. 10 and "
                              "11 as enacted; they are read inside those articles as quoted text (headings as lines), with "
                              "no separate units and none of the ET's later notes; ET art. 334 reads its 'Texto original de "
                              "la Ley 1607 de 2012' box (its table, like every table, is left out) and ET art. 336 leaves "
                              "out the parágrafo 3o. that Ley 1739 de 2014 added. Their later fate is the Estatuto "
                              "Tributario's history.")
    return out


P.doc_units = doc_units_quoted_et
E.doc_units = doc_units_quoted_et


# ---- (batch 98) Ley 633 de 2000 art. 1 adds Libro Sexto (Gravamen a los Movimientos Financieros, ET arts. 870 to 881) to
# the Estatuto Tributario; the page gives each quoted ET article its own article-like anchor ('870' ... '881'), so the
# engine read them as articles 870-881 of Ley 633 and art. 1 kept only its first lines. Ley 1607's coordinator decision
# (QUOTED_ET above): the quoted articles are the text of art. 1 as enacted, read inside it as quoted text, with none of
# the ET's later notes. Each quoted unit joins art. 1 (its label a line, markers and boxes dropped). ET art. 879: the
# page first prints Ley 1739 de 2014's numeral 1 (with the ET's notes), then the whole article as enacted from
# 'ARTICULO 879. EXENCIONES DEL GMF.'; only that second copy is read.
# Ley 488 de 1998 does the same with ET art. 249 (its art. 30) and ET art. 362 (its art. 84).
QUOTED_633 = {L633: {"1": [str(n) for n in range(870, 882)]}, L488: {"30": ["249"], "84": ["362"]}}
QUOTED_633_DONE: list[str] = []
_units_633_q = P.doc_units


def doc_units_quoted_633(name: str) -> list[dict]:
    units = _units_633_q(name)
    if name not in QUOTED_633:
        return units
    arts = QUOTED_633[name]
    out, cur, seen = [], None, {}
    for u in units:
        n = u["name"] or ""
        if n in arts:
            cur = n
            seen[n] = []
            out.append(u)
            continue
        if cur and n in arts[cur]:
            ps = [it for it in u["items"] if it[0] == "p"]
            lines = [("p", E.html.escape(u["label"].strip(), quote=False))]
            if n == "879":
                k = [i for i, it in enumerate(ps) if E.plain(it[1]).startswith("ARTICULO 879. EXENCIONES DEL GMF.")]
                B23._need(len(k) == 1 and k[0] == 3, f"{name} 879 enacted copy")
                ps, lines = ps[k[0]:], []
            lines += [("p", MARK.sub("", it[1])) for it in ps]
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + lines, nosplit=True)
            seen[cur].append(n)
            continue
        cur = None
        out.append(u)
    B23._need(seen == arts, f"{name}: quoted ET units {seen}")
    if name == L633 and not any("(Ley 633 de 2000)" in d for d in QUOTED_633_DONE):
        QUOTED_633_DONE.append("Reforma tributaria (Ley 633 de 2000): art. 1 adds Libro Sexto (Gravamen a los Movimientos "
                               "Financieros, ET arts. 870 to 881) to the Estatuto Tributario. The page gives each quoted ET "
                               "article its own anchor with the ET's later notes. As for Ley 1607 de 2012 (coordinator "
                               "decision): the quoted articles are the text of art. 1 as enacted, read inside it as quoted "
                               "text with no separate units and none of the ET's later notes or rulings on them; ET art. "
                               "879 reads the page's copy of the article as enacted (the page first prints Ley 1739 de "
                               "2014's numeral 1). Their later fate is the Estatuto Tributario's history.")
    if name == L488 and not any("(Ley 488 de 1998)" in d for d in QUOTED_633_DONE):
        QUOTED_633_DONE.append("Reforma tributaria (Ley 488 de 1998): arts. 30 and 84 rewrite ET arts. 249 and 362, which "
                               "the page gives their own anchors; read the same way, as quoted text inside arts. 30 and 84.")
    return out


P.doc_units = doc_units_quoted_633
E.doc_units = doc_units_quoted_633


# ---- page repair: parágrafos the page gives their own heading anchors ('PARÁGRAFO 1o') after their article (Decreto Ley
# 902 de 2017 art. 4: parágrafos 1o to 4o, the last one holding the article's note boxes and earlier texts); the engine
# skipped those anchors, so the article lost them and its history. Each goes back into its article: the anchor's label
# starts its first paragraph, its paragraphs and boxes follow. PARA_JOIN: page -> {article: anchor names}; a page that
# differs stops the parse.
PARA_JOIN = {D902: {"4": ["PARÁGRAFO 1o", "PARÁGRAFO 2o", "PARÁGRAFO 3o", "PARÁGRAFO 4o"]}}
PARA_JOIN_DONE: list[str] = []
_units_pj = P.doc_units


def doc_units_para_join(name: str) -> list[dict]:
    units = _units_pj(name)
    if name not in PARA_JOIN:
        return units
    out, seen, cur = [], {}, None
    for u in units:
        n = u["name"] or ""
        if n in PARA_JOIN[name]:
            cur = n
            seen[n] = []
            out.append(u)
            continue
        if cur and re.fullmatch(r"PAR(?:Á|&Aacute;)GRAFO \d+o", n):
            items = list(u["items"])
            k = next(i for i, it in enumerate(items) if it[0] == "p")
            items[k] = ("p", E.html.escape(u["label"].strip(), quote=False) + " " + items[k][1]) + tuple(items[k][2:])
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + items)
            seen[cur].append(n)
            continue
        cur = None
        out.append(u)
    B23._need(seen == PARA_JOIN[name], f"{name}: parágrafo anchors {seen}")
    PARA_JOIN_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]}: the page gives parágrafos their own "
                          "heading anchors after their article; they are read as part of it (art(s). "
                          + ", ".join(f"{a}: {', '.join(v)}" for a, v in seen.items()) + ")")
    return out


P.doc_units = doc_units_para_join
E.doc_units = doc_units_para_join


# ---- page repair: an anchored heading 'ARTÍCULO 49. (ELIMINADO).' with no words (Ley 2099 de 2021), followed by the act's
# own art. 49: the engine kept the empty one as art. 49 and dropped the real article as a duplicate. The empty unit is a
# numbering remnant with no text; it is left out. DROP_EMPTY: page -> unit names; a page that differs stops the parse.
DROP_EMPTY = {L2099: ["49-ELIMINADO"]}
DROP_EMPTY_DONE: list[str] = []
_units_de = P.doc_units


def doc_units_drop_empty(name: str) -> list[dict]:
    units = _units_de(name)
    if name not in DROP_EMPTY:
        return units
    out, done = [], []
    for u in units:
        if u["name"] in DROP_EMPTY[name]:
            B23._need(not any(E.plain(it[1]).strip() for it in u["items"] if it[0] == "p")
                      and not any(it[0] == "box" for it in u["items"]) and "ELIMINADO" in (u["label"] or ""),
                      f"{name} {u['name']}: not empty")
            done.append(u["name"])
            continue
        out.append(u)
    B23._need(done == DROP_EMPTY[name], f"{name}: empty units {done}")
    DROP_EMPTY_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]}: the page prints the heading "
                           "'ARTÍCULO 49. (ELIMINADO).' with no words before the act's own art. 49; that empty heading is "
                           "left out (the engine had kept it as art. 49 and dropped the real article as a duplicate)")
    return out


P.doc_units = doc_units_drop_empty
E.doc_units = doc_units_drop_empty


# ---- page repairs (batch 59). BOX_HEAD: an earlier-text box whose heading names an act that is not the one whose text
# it gives (Ley 454 de 1998 art. 40: 'Texto original del Decreto 663 de 1994:' heads the article's own original text,
# 'ARTÍCULO 40. Son cooperativas financieras ...', which art. 102 of Ley 795 de 2003 replaced; there is no Decreto 663
# de 1994, and the engine dropped the box, leaving the article out of every version before 2003): page -> {article:
# (heading as printed, heading read)}. DUP_NUM: a page that prints two articles under one number (Ley 4 de 1913: two
# 'ARTICULO 294.' and no 293): the second is kept as its own unit (key art-0294-02), with the number the page prints;
# the engine had dropped it as a duplicate. A page that differs stops the parse.
BOX_HEAD = {L454: {"40": ("Texto original del Decreto 663 de 1994:", "Texto original de la Ley 454 de 1998:")}}
DUP_NUM = {L4: {"294": "294-2"}}
# NESTED: a marker that holds a bracketed box name (Ley 454 de 1998 art. 66: '<Artículo derogado ... Ver en <Legislación
# Anterior> la legislación vigente hasta esta fecha.>'): the inner brackets ended the marker early, so the engine read
# its tail as the article's text from the repeal day; they are dropped.
NESTED = {L454: {"66": ("Ver en &lt;Legislaci&oacute;n Anterior&gt; la", "Ver en Legislaci&oacute;n Anterior la")}}
PAGE59_DONE: list[str] = []
L4_VIGENCIA = (
    "Código de Régimen Político y Municipal (Ley 4 de 1913): the page states 'Esta Ley no incluye análisis de vigencia "
    "completo' (its validity analysis is incomplete). Today's text is the text the page prints. Later laws replaced or "
    "emptied many of its articles without a marker on this page (tacit repeal); those articles are given as printed, "
    "with no end day. Every version comes from the page's own markers, earlier-text boxes and notes, dated by the day "
    "they give or by the acts' in-force days. Notes that say an ordinal, numeral or inciso was 'reformado', "
    "'adicionado' or 'modificado en los términos de' a later law and quote or cite that law's own articles (art. 97: "
    "Ley 71 de 1916, quoting its arts. 1, 4, 7 and 8, and Ley 65 de 1939; art. 305: Ley 84 de 1915, quoting its art. 3) "
    "give no new words for this act: the printed words stay in every version. Arts. 162 (Ley 84 de 1915) and "
    "202 (Ley 71 de 1916) were changed by acts whose earlier wording the page does not give: they read as the "
    "placeholder until those acts' days.")
_units_59 = P.doc_units


def doc_units_59(name: str) -> list[dict]:
    units = _units_59(name)
    if name not in BOX_HEAD and name not in DUP_NUM and name not in NESTED:
        return units
    out, seen = [], {}
    for u in units:
        n = u["name"] or ""
        if n in BOX_HEAD.get(name, {}):
            old, new = BOX_HEAD[name][n]
            items = []
            for it in u["items"]:
                if it[0] == "box" and it[1] == "Legislación Anterior" and old in E.html.unescape(it[2]):
                    raw = E.html.unescape(it[2])
                    B23._need(raw.count(old) == 1 and re.search(re.escape(old) + r"</span></p><p>ART[IÍ]CULO " + n + r"\.",
                                                                raw) is not None, f"{name} {n}: box heading")
                    it = (it[0], it[1], raw.replace(old, new)) + tuple(it[3:])
                    seen.setdefault(("box", n), 0)
                    seen[("box", n)] += 1
                items.append(it)
            u = dict(u, items=items)
        if n in NESTED.get(name, {}):
            old, new = NESTED[name][n]
            items = []
            for it in u["items"]:
                if it[0] == "p" and old in it[1]:
                    it = (it[0], it[1].replace(old, new)) + tuple(it[2:])
                    seen[("nested", n)] = seen.get(("nested", n), 0) + 1
                items.append(it)
            u = dict(u, items=items)
        if n in DUP_NUM.get(name, {}):
            seen[("dup", n)] = seen.get(("dup", n), 0) + 1
            if seen[("dup", n)] == 2:
                new = DUP_NUM[name][n]
                B23._need(re.fullmatch(r"ARTICULO " + n + r"\.\s*", u["label"] or "") is not None, f"{name} {n}: label")
                u = dict(u, name=new, label=f"ARTICULO {new}.")
        out.append(u)
    want = ({("box", a): 1 for a in BOX_HEAD.get(name, {})} | {("dup", a): 2 for a in DUP_NUM.get(name, {})}
            | {("nested", a): 1 for a in NESTED.get(name, {})})
    B23._need(seen == want, f"{name}: page repairs {seen}")
    t = dict((pg, t) for _, pg, _, _, t, _ in SPEC)[name]
    for a, (old, new) in BOX_HEAD.get(name, {}).items():
        PAGE59_DONE.append(f"{t}: art. {a}'s earlier-text box is headed '{old}' but gives the article's own original "
                           f"text; it is read as '{new}' (there is no Decreto 663 de 1994; the article was otherwise "
                           "missing from every version before the act that replaced it)")
    for a in NESTED.get(name, {}):
        PAGE59_DONE.append(f"{t}: art. {a}'s repeal marker holds a bracketed box name ('<Legislación Anterior>') "
                           "whose brackets ended the marker early; they are dropped, so the article leaves on the "
                           "repeal day the marker gives (the engine had read the marker's tail as its text)")
    for a in DUP_NUM.get(name, {}):
        PAGE59_DONE.append(f"{t}: the page prints two articles numbered {a} (and none numbered {int(a) - 1}); both are "
                           f"kept in the page's order, each under the number the page prints, the second under the key "
                           f"art-{int(a):04d}-02 (the engine had dropped it as a duplicate)")
    return out


P.doc_units = doc_units_59
E.doc_units = doc_units_59


# ---- amendments by Decretos 1122 de 1999 and 266 de 2000, both struck as a whole (phase2/struck.py)
import struck  # noqa: E402

# (batch 94) Ley 443 de 1998 arts. 45 and 46: the rulings boxes write 'declaro INEXEQUIBLE' for 'declarado INEXEQUIBLE'
# (art. 46 as a whole: the engine left the article out of every version).
B4.JV_FIXES.append(("ley_0443_1998", "- Art&iacute;culo declaro INEXEQUIBLE por ", "- Art&iacute;culo declarado INEXEQUIBLE por ",
                    "art. 46: the rulings box's 'Artículo declaro INEXEQUIBLE por la Corte Constitucional mediante Sentencia "
                    "C-372-99' is read as 'declarado' (typing slip): the article stands as the page's original-text box gives "
                    "it until that ruling (26 May 1999)"))
B4.JV_FIXES.append(("ley_0443_1998", "- Aparte tachado declaro INEXEQUIBLE por ", "- Aparte tachado declarado INEXEQUIBLE por ",
                    "art. 45: two rulings boxes' 'Aparte tachado declaro INEXEQUIBLE' read as 'declarado' (typing slip)"))
B4.JV_FIXES.append(("ley_0443_1998", "- Apartes &#160;tachados declarados EXEQUIBLES por la Corte Constitucional mediante "
                    "Sentencia <A href='c-372_1999.html#1' >C-372-99</A>",
                    "- Apartes &#160;tachados declarados INEXEQUIBLES por la Corte Constitucional mediante "
                    "Sentencia <A href='c-372_1999.html#1' >C-372-99</A>",
                    "art. 27: the rulings box reads 'Apartes tachados declarados EXEQUIBLES ... Sentencia C-372-99', while the "
                    "page strikes the words under '<Apartes tachados INEXEQUIBLES>'; the ruling's own decision (Sentencia "
                    "C-372 de 1999, 26 May 1999) reads 'Es INEXEQUIBLE, en el inciso primero del "
                    "artículo 27, su parte final, que dice: \"Cada Comisión del Servicio Civil dispondrá lo necesario ...\"' "
                    "and 'Son INEXEQUIBLES, en el segundo inciso del artículo 27, las frases \"...a través del Departamento "
                    "Administrativo de la Función Pública...\" y \"...del personal de las entidades del orden nacional\"', so "
                    "the box is read as 'INEXEQUIBLES' and the words leave on that day"))
# (batch 94) Ley 443 de 1998 art. 22: its rulings box states the ruling as 'Sentencia C-923-99 de 18 de noviembre de 1999'
# ('de', not 'del'); the earlier-text block heading already reads 'declarado INEXEQUIBLE', so nothing is rewritten.
struck.ALLOW_UNCONFIRMED[("ley_0443_1998", "22")] = "ruling stated as 'C-923-99 de 18 de noviembre de 1999'"
struck.install(E, P, PAGES)


# ---- Ley 222 de 1995, Título II (arts. 89 to 225, the concordato and liquidación obligatoria) repealed by Ley 1116 de
# 2006 art. 126 from the day that act took effect (batch 26's staged-repeal machinery). The page prints each article of
# the title under '<Título II. derogado por el artículo 126 de la Ley 1116 de 2006, a partir del 28 de junio de 2007>'.
# Ley 1116 'comenzará a regir seis (6) meses después de su promulgación' (Diario Oficial No. 46.494 of 27 December 2006):
# the corpus dates that day 2007-06-27 everywhere else (Código Civil, Estatuto Tributario, Régimen de Insolvencia
# Empresarial), by the same month count it uses for every 'six months after promulgation' act; kept here so the
# repealing law has one day.
B26 = B27.B26
B26.STAGES.clear()
B26.STAGE_CHECK.clear()
B26.STAGES[L222] = [
    (re.compile(r"(?:<span class=\"b_aj\">)?&lt;T(?:&iacute;|í)tulo II\. derogado por el art(?:&iacute;|í)culo (?:<A [^>]*>)?"
                r"126(?:</A>)? de la (?:&#160;)?\s*Ley 1116 de 2006, a partir del 28 de junio de 2007&gt;(?:</span>)?\s*"),
     "ley-1116-2006", "2007-06-27", 137,
     "Ley 1116 de 2006 (Régimen de Insolvencia Empresarial), art. 126: 'la presente ley comenzará a regir seis (6) meses "
     "después de su promulgación y deroga el Título II de la Ley 222 de 1995, la cual estará vigente hasta la fecha en que "
     "entre a regir la presente ley'. The page marks arts. 89 to 225 '<Título II. derogado por el artículo 126 de la Ley "
     "1116 de 2006, a partir del 28 de junio de 2007>'; they leave the record on the day the corpus gives Ley 1116 de 2006 "
     "everywhere (27 June 2007, six months after its promulgation in Diario Oficial No. 46.494 of 27 December 2006, by the "
     "month count used for every such act); the page's '28 de junio' is the day after"),
]
B26.STAGE_CHECK[L222] = ("ley_1116_2006", "126", "Salvo lo que se indica en los incisos anteriores, la presente ley comenzará "
                         "a regir seis (6) meses después de su promulgación y deroga el Título II de la Ley 222 de 1995")


# Título II's headings leave titulos.md with its articles (same day, same credit).
TITLE_GONE = {L222: ("### TITULO II.", "### TITULO III.", "2007-06-27", "ley-1116-2006")}
TITLE_GONE_DONE: list[str] = []


def with_title_gone(page, build):
    def run():
        act = build()
        first, nxt, day, law = TITLE_GONE[page]
        n = 0
        for v in act["versions"]:
            if v["from"] < day or "units" not in v:
                continue
            ls = v["units"]["titulos"]["text"].split("\n")
            i = next(k for k, x in enumerate(ls) if x.startswith(first))
            j = next(k for k, x in enumerate(ls) if x.startswith(nxt))
            n = j - i
            v["units"] = dict(v["units"], titulos=dict(v["units"]["titulos"], text="\n".join(ls[:i] + ls[j:])))
            if v["from"] == day:
                v["credits"]["titulos"] = [law]
        B23._need(n > 10, f"{page}: title headings {n}")
        TITLE_GONE_DONE.append(f"{dict((pg, t) for _, pg, _, _, t, _ in SPEC)[page]}: the {n} headings of Título II "
                               f"(from '{first[4:]}' up to '{nxt[4:]}') leave titulos.md on {day} with the title's "
                               "articles, credited to the same act")
        return act
    return run


# ---- Ley 200 de 1995 replaced as a whole by Ley 734 de 2002 (the repeal-version pattern of batches 24 and 31: a last
# version with no provisions on the repeal day, credited to the repealing act). The page prints no repeal marker on the
# articles; its head note names Ley 734 de 2002 as the new Código Disciplinario Único and quotes its art. 224, which
# Ley 734's own page prints.
WHOLE_REPEAL = {L200: {
    "law": "ley-734-2002", "day": "2002-05-05",
    "head": "Mediante la Ley 734 de 2002, publicada en el Diario Oficial No 44.708, de 13 de febrero de 2002, se expidió el "
            "nuevo Código Disciplinario Único",
    "check": ("ley_0734_2002", "224", "La presente ley regirá tres meses después de su sanción y deroga las disposiciones "
              "que le sean contrarias"),
    "note": "Ley 734 de 2002 (Código Disciplinario Único), sanctioned 5 February 2002 and in force three months later, on "
            "5 May 2002 (its art. 224: 'La presente ley regirá tres meses después de su sanción y deroga las disposiciones "
            "que le sean contrarias, salvo las normas referidas a los aspectos disciplinarios previstos en la Ley 190 de "
            "1995 y el régimen especial disciplinario establecido para los miembros de la fuerza pública'), issued a new "
            "Código Disciplinario Único that regulates the whole matter of Ley 200 de 1995, which leaves the record on "
            "that day (the page's head note names Ley 734 de 2002 as the new code)."}}
WHOLE_DONE: list[str] = []
# Ley 130 de 1913 (jurisdicción contencioso-administrativa), which repealed Ley 4's arts. 112-119 and 181-182: the page's
# notes on each of those articles say 'Rige a partir del 1 de marzo de 1914' (the general rule would give 9 April 1914,
# two months after its publication of 9 February 1914).
E.HAND_RULES["ley-130-1913"] = ("1914-03-01", "Ley 130 de 1913, published in Diario Oficial No. 15.123 of 9 February 1914: "
                                "'Rige a partir del 1 de marzo de 1914' (the notes on Ley 4 de 1913's page)")
# Ley 734 de 2002's day as the corpus gives it in 99-batch8 (its own art. 224: three months after its sanction of 5 February
# 2002); the engine's general reading counts from its publication (13 February).
# Ley 1816 de 2016, art. 42: 'La presente ley entra a regir el 1o de enero del año 2017' (the general reading misses '1o de'
# without a full stop and fell back to the default rule; fix_dates.py patched the published part the same way).
E.HAND_RULES["ley-1816-2016"] = ("2017-01-01", "Ley 1816 de 2016, art. 42: 'La presente ley entra a regir el 1o de enero del "
                                 "año 2017'")
# Decreto Ley 1851 de 2021 (Procuraduría), art. 27: 'El presente decreto entrará en vigencia el 29 de marzo de 2022 excepto
# el artículo 26 que entra a regir de manera inmediata' (art. 26 adds posts to a planta, no words of Decreto Ley 262 de
# 2000); the general reading missed the date and fell back to the default rule.
E.HAND_RULES["dec-1851-2021"] = ("2022-03-29", "Decreto Ley 1851 de 2021, art. 27: 'El presente decreto entrará en vigencia "
                                 "el 29 de marzo de 2022 excepto el artículo 26 que entra a regir de manera inmediata'")
# Ley 2026 de 2020 (Ley Jacobo), art. 7: 'Esta norma comienza a regir a partir de su promulgación ...' (Diario Oficial No.
# 51.384 of 23 July 2020); the engine's vigencia reading does not take 'comienza a regir' and fell back to the default rule.
E.HAND_RULES["ley-2026-2020"] = ("pub", "Ley 2026 de 2020, art. 7: 'Esta norma comienza a regir a partir de su promulgación y "
                                 "modifica las disposiciones expresamente referidas y aquellas que le sean contrarias de forma "
                                 "expresa o tácita'")
# Ley 1024 de 2006, art. 9: 'La presente ley tendrá vigencia a partir de su promulgación.' (published complete in Diario
# Oficial No. 46.274 of 20 May 2006, after an incomplete printing in No. 46.273 of 19 May); the engine did not read the
# clause on this page (it opens with the Diario Oficial's 'ACLARACION') and fell back to the default rule.
E.HAND_RULES["ley-1024-2006"] = ("pub", "Ley 1024 de 2006, art. 9: 'La presente ley tendrá vigencia a partir de su "
                                 "promulgación.' (published complete in Diario Oficial No. 46.274 of 20 May 2006)")
E.HAND_RULES["ley-734-2002"] = ("2002-05-05", "Ley 734 de 2002, art. 224: 'La presente ley regirá tres meses después de su "
                                "sanción' (sanctioned 5 February 2002)")


def with_whole_repeal(page, build):
    def run():
        act = build()
        r = WHOLE_REPEAL[page]
        head = " ".join(E.plain(it[1]) for it in P.doc_units(page)[0]["items"] if it[0] == "p")
        B23._need(r["head"] in head, f"{page}: head note")
        pg, art, words = r["check"]
        B23._need(words in B3.article_text(P.doc_units(pg), art), f"{pg} art. {art}")
        law, day = E.register(r["law"]), r["day"]
        B23._need(E.law_day(law) == day, f"{law}: in force {E.law_day(law)}, expected {day}")
        vs = act["versions"]
        B23._need(vs[-1]["from"] < day, f"{page}: a version on or after the repeal day ({vs[-1]['from']})")
        state = {}
        for v in vs:
            if "units" in v:
                state = dict(v["units"])
        vs.append({"from": day, "units": {}, "credits": {k: [law] for k in sorted(state)},
                   "source_url": vs[-1]["source_url"], "sha256": vs[-1]["sha256"], "note": r["note"]})
        WHOLE_DONE.append(f"{act['title']}: {r['note']} The last version, on {day}, holds no provisions, credited to Ley "
                          "734 de 2002; the version before it is checked against the text the page prints.")
        return act
    return run


B3 = B23.B3 if hasattr(B23, "B3") else __import__("parse_batch3")


# ---- Ley 1530 de 2012 repealed by Ley 2056 de 2020 art. 211 from 1 January 2021, save its arts. 106 to 126 and 128 (kept
# for the transitional procedures of Ley 2056's arts. 199 and 200). The page prints every article under a marker naming the
# repeal: '<Ley derogada a partir del 12 de enero de 2021 por el artículo 211 de la Ley 2056 de 2020>', the 22 kept articles
# '<... de la Ley 2056 de 2020, sobre este artículo tener en cuenta los efectos de la transitoriedad ...>'. A last version on
# the repeal day takes out every other article and the headings of the titles and chapters left with no article, credited to
# Ley 2056 de 2020; the kept articles stay to today as printed. PARTIAL_REPEAL: page -> spec; a page that differs stops.
PARTIAL_REPEAL = {L1530: {
    "law": "ley-2056-2020", "day": "2021-01-01",
    "marker": "Ley derogada a partir del 12 de enero de 2021 por el artículo 211 de la Ley 2056 de 2020",
    "kept_tail": ", sobre este artículo tener en cuenta los efectos de la transitoriedad de los procedimientos administrativos a "
                 "que se refieren los artículos 199 y 200 de la Ley 2056 de 2020",
    "kept": [str(n) for n in range(106, 127)] + ["128"],
    "heads": ["### TÍTULO VI. SISTEMA DE MONITOREO", "### CAPÍTULO II. DEL PROCEDIMIENTO PREVENTIVO",
              "### CAPÍTULO III. DISPOSICIONES COMUNES A LOS PROCEDIMIENTOS"],
    "head_note": "Ley derogada a partir del 1 de enero de 2021 por el artículo 211 de la Ley 2056 de 2020 con excepción de los "
                 "artículos del 106 al 126 y 128 para efectos de la transitoriedad de los procedimientos administrativos a que "
                 "se refieren los artículos 199 y 200 de la Ley 2056 de 2020",
    "check": ("ley_2056_2020", "211", "La presente ley rige a partir del 1 de enero de 2021 y deroga todas las disposiciones "
              "que le sean contrarias, en especial la Ley 1530 de 2012, con excepción de los artículos del 106 al 126 y 128 "
              "para efectos de la transitoriedad de los procedimientos administrativos a que se refieren los artículos 199 y "
              "200 de la presente ley"),
    "note": "Ley 2056 de 2020 (Sistema General de Regalías), art. 211: 'La presente ley rige a partir del 1 de enero de 2021 y "
            "deroga todas las disposiciones que le sean contrarias, en especial la Ley 1530 de 2012, con excepción de los "
            "artículos del 106 al 126 y 128 para efectos de la transitoriedad de los procedimientos administrativos a que se "
            "refieren los artículos 199 y 200 de la presente ley'. Every other article leaves the record on 1 January 2021; "
            "arts. 106 to 126 and 128 stay, for the preventive, corrective and sanctioning procedures that Ley 2056's arts. "
            "199 and 200 leave under them."}}
PARTIAL_DONE: list[str] = []


def with_partial_repeal(page, build):
    def run():
        act = build()
        r = PARTIAL_REPEAL[page]
        units = P.doc_units(page)
        head = " ".join(E.plain(it[1]) for it in units[0]["items"] if it[0] == "p")
        B23._need(r["head_note"] in head, f"{page}: head note")
        pg, art, words = r["check"]
        B23._need(B3.article_text(P.doc_units(pg), art).startswith(words), f"{pg} art. {art}")
        law, day = E.register(r["law"]), r["day"]
        B23._need(E.law_day(law) == day, f"{law}: in force {E.law_day(law)}, expected {day}")
        kept, gone = [], []
        for u in units:
            n = u["name"] or ""
            if not re.fullmatch(r"\d+", n):
                continue
            p0 = next(it[1] for it in u["items"] if it[0] == "p" and E.plain(it[1]).strip())  # first non-empty paragraph
            ms = [m for m in E.markers(p0) if m.startswith(r["marker"])]
            B23._need(len(ms) == 1 and ms[0] in (r["marker"], r["marker"] + r["kept_tail"]), f"{page} art. {n}: marker {ms}")
            (kept if ms[0] != r["marker"] else gone).append(n)
        B23._need(kept == r["kept"], f"{page}: kept articles {kept}")
        vs = act["versions"]
        B23._need(vs[-1]["from"] < day, f"{page}: a version on or after the repeal day ({vs[-1]['from']})")
        state = {}
        for v in vs:
            if "units" in v:
                state = dict(v["units"])
            for k, x in (v.get("changes") or {}).items():
                if x is None:
                    state.pop(k, None)
                else:
                    state[k] = x
        keep = {E.unit_key(n)[0] for n in kept}
        B23._need(keep <= set(state) and {E.unit_key(n)[0] for n in gone} == set(state) - keep - {"titulos"},
                  f"{page}: units in force before the repeal")
        lines = state["titulos"]["text"].split(chr(10))
        heads = [next(l for l in lines if l.startswith(h)) for h in r["heads"]]
        B23._need(all(sum(l.startswith(h) for l in lines) == 1 for h in r["heads"]), f"{page}: kept headings")
        new = {k: x for k, x in state.items() if k in keep}
        new["titulos"] = dict(state["titulos"], text=chr(10).join(heads) + chr(10))
        cr = {k: [law] for k in sorted(state) if k not in keep}
        vs.append({"from": day, "units": new, "credits": cr, "source_url": vs[-1]["source_url"], "sha256": vs[-1]["sha256"],
                   "note": r["note"]})
        PARTIAL_DONE.append(
            f"{act['title']}: {r['note']} The page prints every article under the marker '<{r['marker']}>' (the 22 kept ones "
            "with the words 'sobre este artículo tener en cuenta los efectos de la transitoriedad ...'); its own head note and "
            "Ley 2056's art. 211 give 1 January 2021, so the markers' '12 de enero' is read as that day. The markers are not "
            f"part of the text. The version of {day} keeps the {len(kept)} articles and the headings above them "
            f"({'; '.join(h[4:] for h in heads)}); the version before it is checked against the text the page prints.")
        return act
    return run

# ---- (batch 93) Ley 793 de 2002 repealed by Ley 1708 de 2014 (Código de Extinción de Dominio) art. 218 from 20 July 2014
# (six months after its promulgation of 20 January 2014; art. 218 'deroga expresamente las Leyes 793 y 785 de 2002'). The
# page prints every article but art. 18 under '<Ley, salvo el artículo 18, derogada a partir del 20 de julio de 2014, por el
# artículo 218 de la Ley 1708 de 2014>' (the same words head the page), and art. 18 with no marker. Art. 218's own second
# inciso keeps art. 18 (2014 text, in the page's 'Texto original de la Ley 1708 de 2014' box: 'Sin perjuicio de lo anterior,
# el artículo 18 de la Ley 793 de 2002, y los artículos 9o y 10 la Ley 785 de 2002, seguirán vigentes.'; rewritten by Ley 2197
# de 2022 art. 54, still keeping art. 18): art. 18 stays to today (fourteenth session; both texts checked in the parse).
# A last version on 20 July 2014 takes out every other article in force and the chapter headings left with no article,
# credited to Ley 1708 de 2014. PARTIAL_93: page -> spec; a page that differs stops the parse.
PARTIAL_93 = {L793: {
    "law": "ley-1708-2014", "day": "2014-07-20",
    "marker": "Ley, salvo el artículo 18, derogada a partir del 20 de julio de 2014, por el artículo 218 de la Ley 1708 de 2014",
    "kept": ["18"], "already_out": ["10"], "heads": ["### CAPITULO IV. DE LA COMPETENCIA Y DEL PROCEDIMIENTO."],
    "check": ("ley_1708_2014", "218", "Esta ley entrará a regir seis (6) meses después de la fecha de su promulgación, deroga "
              "expresamente las Leyes 793 y 785 de 2002"),
    "basis": ("js/ley_1708_2014_pr005.js", "Texto original de la Ley 1708 de 2014:",
              "Sin perjuicio de lo anterior, el artículo 18 de la Ley 793 de 2002, y los artículos 9o y 10 la Ley 785 de 2002, "
              "seguirán vigentes.",
              "Sin perjuicio de lo anterior, el artículo 18 de la Ley 793 de 2002, y los artículos 9o y 10 la Ley 785 de 2002, "
              "seguirán vigentes, así como los mecanismos de justicia premial regulados en la Ley 1330 de 2009"),
    "note": "Ley 1708 de 2014 (Código de Extinción de Dominio), art. 218: 'Esta ley entrará a regir seis (6) meses después de "
            "la fecha de su promulgación, deroga expresamente las Leyes 793 y 785 de 2002, Ley 1330 de 2009, así como todas "
            "las demás leyes que las modifican o adicionan ...'; promulgated 20 January 2014, in force 20 July 2014. As the "
            "page reads it ('Ley, salvo el artículo 18, derogada a partir del 20 de julio de 2014'), every article but art. "
            "18 leaves the record on that day; art. 18 stays, kept by the same article's second inciso."}}
PARTIAL93_DONE: list[str] = []


def with_partial_93(page, build):
    def run():
        act = build()
        r = PARTIAL_93[page]
        units = P.doc_units(page)
        head = " ".join(E.plain(it[1]) for it in units[0]["items"] if it[0] == "p")
        B23._need("<" + r["marker"] + ">" in head, f"{page}: head note")
        pg, art, words = r["check"]
        B23._need(B3.article_text(P.doc_units(pg), art).startswith(words), f"{pg} art. {art}")
        js, bhead, borig, bnow = r["basis"]
        B23._need(bnow in B3.article_text(P.doc_units(pg), art), f"{pg} art. {art}: second inciso")
        bx = [E.plain(b) for b in E.js_boxes(E.read(E.BASE + js)).values()]
        B23._need(any(x.startswith(bhead) and borig in x.replace("9 o y", "9o y") for x in bx), f"{js}: original inciso")
        law, day = E.register(r["law"]), r["day"]
        B23._need(E.law_day(law) == day, f"{law}: in force {E.law_day(law)}, expected {day}")
        kept, gone, out = [], [], []
        for u in units:
            n = u["name"] or ""
            if not re.fullmatch(r"\d+(?:-[A-Z])?", n):
                continue
            p0 = next(it[1] for it in u["items"] if it[0] == "p" and E.plain(it[1]).strip())
            ms = [m for m in E.markers(p0) if m.startswith("Ley, salvo")]
            if ms == [r["marker"]]:
                gone.append(n)
            elif not ms and n in r["kept"]:
                kept.append(n)
            elif not ms and n in r["already_out"]:
                out.append(n)
            else:
                B23._need(False, f"{page} art. {n}: marker {ms}")
        B23._need(kept == r["kept"] and out == r["already_out"], f"{page}: kept {kept}, out {out}")
        vs = act["versions"]
        B23._need(vs[-1]["from"] < day, f"{page}: a version on or after the repeal day ({vs[-1]['from']})")
        state = {}
        for v in vs:
            if "units" in v:
                state = dict(v["units"])
        keyof = lambda n: E.unit_key(n.replace("-", ""))[0]  # noqa: E731  ('9-A' -> art-0009a)
        keep = {keyof(n) for n in kept}
        B23._need(keep <= set(state) and {keyof(n) for n in gone} == set(state) - keep - {"titulos"}
                  and not {keyof(n) for n in out} & set(state), f"{page}: units in force before the repeal "
                  f"{sorted(set(state) - keep - {'titulos'} ^ {keyof(n) for n in gone})}")
        lines = state["titulos"]["text"].split(chr(10))
        B23._need(all(sum(l == h for l in lines) == 1 for h in r["heads"]), f"{page}: kept headings")
        new = {k: x for k, x in state.items() if k in keep}
        new["titulos"] = dict(state["titulos"], text=chr(10).join(r["heads"]) + chr(10))
        cr = {k: [law] for k in sorted(state) if k not in keep}
        vs.append({"from": day, "units": new, "credits": cr, "source_url": vs[-1]["source_url"], "sha256": vs[-1]["sha256"],
                   "note": r["note"]})
        basis_orig, basis_now = borig, bnow
        PARTIAL93_DONE.append(
            f"{act['title']}: {r['note']} The page prints those articles under the marker '<{r['marker']}>', which is not "
            f"part of the text, and art. 18 with none. Art. 18 is kept on the law's own words: art. 218's second inciso, "
            f"as enacted in 2014 (the page's 'Texto original de la Ley 1708 de 2014' box), reads '{basis_orig}', and its "
            f"text as rewritten by Ley 2197 de 2022 art. 54 still reads '{basis_now} ...'. The version of {day} keeps art. 18 "
            f"and the heading above it ({r['heads'][0][4:]}); the version before it is checked against the text the page "
            f"prints.")
        return act
    return run


# ---- page repair (batch 68): chapter-named units right after an article that quotes a whole part of another act (Ley
# 795 de 2003 art. 45: 'Sustitúyase la Parte Séptima del Estatuto Orgánico del Sistema Financiero, la cual quedará así:'
# then units 'CAPITULO II', 'CAPITULO III', 'CAPITULO IV' holding EOSF arts. 209-212 as rewritten). The engine read them
# as the act's own headings, so their words went into titulos.md. They are joined to the article as quoted text (coordinator
# rule: quoted text stays inside the amending article). QUOTED_HEADS: page -> {article: unit names}; a page that differs
# stops the parse.
QUOTED_HEADS = {"ley_0795_2003": {"45": ["CAPITULO II", "CAPITULO III", "CAPITULO IV"]}}
QUOTED_HEADS_DONE: list[str] = []
_units_qheads = P.doc_units


def doc_units_qheads(name: str) -> list[dict]:
    units = _units_qheads(name)
    if name not in QUOTED_HEADS:
        return units
    want = {n: a for a, ns in QUOTED_HEADS[name].items() for n in ns}
    out, done = [], []
    for u in units:
        a = want.get(u["name"])
        if a and out and out[-1]["name"] == a:
            out[-1] = dict(out[-1], items=list(out[-1]["items"]) + [("p", u["label"])] + list(u["items"]), nosplit=True)
            done.append(u["name"])
            continue
        out.append(u)
    B23._need(done == [n for ns in QUOTED_HEADS[name].values() for n in ns], f"{name}: quoted chapters {done}")
    t = dict((pg, t) for _, pg, _, _, t, _ in SPEC_ALL)[name]
    QUOTED_HEADS_DONE.append(f"{t}: " + "; ".join(f"art. {a} quotes the chapters {', '.join(ns)} of the part it substitutes, "
                                                      "which the page gives anchors of their own; they are read as the "
                                                      "article's quoted text, not as the act's headings"
                                                      for a, ns in QUOTED_HEADS[name].items())
                             + (f"; art(s). {', '.join(QUOTED_TAILS[name])}: likewise the chapter block printed after it"
                                if name in QUOTED_TAILS else "") + ".")
    return out


P.doc_units = doc_units_qheads
E.doc_units = doc_units_qheads


# ---- (batch 94) Ley 443 de 1998 repealed by Ley 909 de 2004 art. 58 ('La presente ley rige a partir de su publicación,
# deroga la Ley 443 de 1998, a excepción de los artículos 24, 58, 81 y 82 y las demás disposiciones que le sean
# contrarias'), published 23 September 2004. The page prints each repealed article under '<Artículo derogado por el
# artículo 58 de la Ley 909 de 2004>' with a matching 'Notas de Vigencia' line (art. 38: the note only), and the four kept
# articles with neither. Marker and note line are taken out while the units are read (the engine read articles with
# earlier-text boxes under the marker backwards: words from 2004 credited to Ley 909), so every article gets its own
# history; a last version on 23 September 2004 then takes out every article but the four and the headings left with no
# article, credited to Ley 909 de 2004. PARTIAL_94: page -> spec; a page that differs stops the parse.
L909 = "ley_0909_2004"
PARTIAL_94 = {L443: {
    "law": "ley-909-2004", "day": "2004-09-23",
    "p0": re.compile(r"&lt;Art&iacute;culo derogado por el art&iacute;culo <A href=\"ley_0909_2004_pr001\.html#58\" >58</A> "
                     r"de la Ley 909 de 2004&gt;\s*"),
    "nv": re.compile(r"- Art&iacute;culo derogado por el art&iacute;culo <A href='ley_0909_2004_pr001\.html#58' >58</A> de "
                     r"la Ley 909 de 2004, publicada en el Diario Oficial No\. 45\.680, de 23 de septiembre de 2004\.\s*"),
    "head": "Derogada, salvo los artículos 24, 58, 81 y 82 , por la Ley 909 de 2004",
    "kept": ["24", "58", "81", "82"],
    "nv_only": ["38"],
    "heads": ["### TITULO II. VINCULACION A LOS EMPLEOS DE CARRERA", "### CAPITULO II. PROCESOS DE SELECCION O CONCURSOS",
              "### TITULO VI. DEL SISTEMA NACIONAL DE CARRERA Y DE LA FUNCION PUBLICA",
              "### CAPITULO III. DE LA ESCUELA SUPERIOR DE ADMINISTRACION PUBLICA",
              "### TITULO IX. DEL SISTEMA UNICO DE INFORMACION DE PERSONAL"],
    "check": (L909, "58", "La presente ley rige a partir de su publicación, deroga la Ley 443 de 1998, a excepción de los "
              "artículos 24, 58, 81 y 82 y las demás disposiciones que le sean contrarias."),
    "note": "Ley 909 de 2004 (empleo público, carrera administrativa y gerencia pública), art. 58: 'La presente ley rige a "
            "partir de su publicación, deroga la Ley 443 de 1998, a excepción de los artículos 24, 58, 81 y 82 y las demás "
            "disposiciones que le sean contrarias.'; published in Diario Oficial No. 45.680 of 23 September 2004. Every "
            "article but arts. 24, 58, 81 and 82 leaves the record on that day."}}
P94_MARKED: dict[str, dict] = {}
PARTIAL94_DONE: list[str] = []
_units_94 = P.doc_units


def doc_units_94(name: str) -> list[dict]:
    units = _units_94(name)
    if name in PARTIAL_94:
        r = PARTIAL_94[name]
        p0s, nvs = [], []
        for u in units[1:]:
            new, first = [], True
            for it in u["items"]:
                if it[0] == "p" and first and E.plain(it[1]).strip():
                    first = False
                    t, k = r["p0"].subn("", it[1])
                    if k:
                        p0s.append(u["name"])
                        it = ("p", t) + tuple(it[2:])
                elif it[0] == "box" and it[1] == "Notas de Vigencia":
                    t, k = r["nv"].subn("", it[2])
                    if k:
                        nvs.append(u["name"])
                        it = it[:2] + (t,) + tuple(it[3:])
                new.append(it)
            u["items"] = new
        P94_MARKED[name] = {"p0": p0s, "nv": nvs}
    return units


P.doc_units = doc_units_94
E.doc_units = doc_units_94


# ---- page repair (twenty-second session): Ley 488 de 1998 art. 145 prints today's vehicle-tax brackets (the values
# Decreto 1457 de 2025 set for 2026) as an HTML table after '<Valores absolutos que regirán a partir del 1o. de enero de
# 2026 ...> Vehículos particulares:'; the engine reads paragraphs only, so today's text had lost the brackets that every
# earlier-text box prints as lines ('a) Hasta $55.679.000 1,5%'). The table's rows are read as those lines, in place of
# the repeated 'Vehículos particulares:' line the page prints before the table (the boxes, like the act, give the
# brackets under '1. Vehículos particulares:'). A page that differs stops the parse.
TABLE_98 = {L488: ("145", "Valores absolutos que regirán a partir del 1o. de enero de 2026, reajustados por el el artículo 1 "
                          "del Decreto 1457 de 2025", ("a) Hasta ", "b) Más de ", "c) Más de "))}
_units_t98 = P.doc_units


def doc_units_table_98(name: str) -> list[dict]:
    units = _units_t98(name)
    if name not in TABLE_98:
        return units
    num, mark, starts = TABLE_98[name]
    out = []
    for u in units:
        if u["name"] != num:
            out.append(u)
            continue
        its = list(u["items"])
        k = [i for i, it in enumerate(its) if it[0] == "p" and E.plain(it[1]).strip().startswith("<" + mark)]
        B23._need(len(k) == 1 and its[k[0] + 1][0] == "p" and E.plain(its[k[0] + 1][1]).strip() == "Vehículos particulares:",
                  f"{name} {num}: table marker")
        raw = E.read(E.BASE + u["page"] + ".html") or ""
        i = raw.find(E.html.escape("Decreto 1457 de 2025", quote=False))
        t0 = raw.find("<table", i)
        t1 = raw.find("</table>", t0)
        B23._need(i > 0 and 0 < t0 < raw.find("caja_vja_encabezado", i) and t1 > t0, f"{name} {num}: table")
        rows = []
        for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", raw[t0:t1], re.S | re.I):
            cells = [E.tidy(E.plain(c).replace("\t", " ")) for c in re.findall(r"<td\b[^>]*>(.*?)</td>", tr, re.S | re.I)]
            rows.append(" ".join(c for c in cells if c))
        B23._need(len(rows) == 3 and all(r.startswith(s) for r, s in zip(rows, starts)), f"{name} {num}: rows {rows}")
        its[k[0] + 1:k[0] + 2] = [("p", E.html.escape(r, quote=False)) for r in rows]
        out.append(dict(u, items=its))
        if not any("(Ley 488 de 1998): art. 145" in d for d in QUOTED_633_DONE):
            QUOTED_633_DONE.append(
                "Reforma tributaria (Ley 488 de 1998): art. 145 (impuesto sobre vehículos automotores, tarifas): the page "
                "prints today's brackets, the values Decreto 1457 de 2025 set for 2026, as a table; they are read as the "
                "lines the page's earlier-text boxes print ('a) Hasta $... 1,5%'), under '1. Vehículos particulares:' (the "
                "page's repeated 'Vehículos particulares:' line before the table is left out).")
    B23._need(any(u["name"] == num for u in out), f"{name} {num}: unit")
    return out


P.doc_units = doc_units_table_98
E.doc_units = doc_units_table_98


# ---- dates (twenty-second session): the decrees that update absolute values each year take effect, under the corpus
# rule (95-batch5 decision for the Estatuto Tributario), on 1 January of the year the page's own words say their values
# govern: the ET notes ('Mediante el artículo 1 del Decreto 3804 de 2003, publicado en el Diario Oficial ... se
# actualizaron los valores absolutos que regirán para el año 2004'), Ley 488 art. 145's notes ('Mediante el artículo 1
# del Decreto 1493 de 13 de diciembre de 2024, '(...) se reajustan los valores absolutos del Impuesto sobre Vehículos
# Automotores ... para el año gravable 2025', publicado en el Diario Oficial No. 52.969 de 13 de diciembre de 2024') and
# its earlier-text heads ('Texto original de la Ley 488 de 1998 con los valores absolutos establecidos para el año 2016
# por el Decreto 2381 de 2015'). Each must name the year after the decree's own; read from the pages, not a list.
VALUE_ET = re.compile(r"Mediante (?:el )?art[íi]culo [^,]{0,30}? del? Decreto (\d+) de (\d{4}),? publicad[oa] en el "
                      r"Diario Oficial[^,]{0,20},? (?:del? )?(\d{1,2}(?:o\.)? de [a-z]+ de \d{4}),? se "
                      r"(?:actualizaron|establecen)[^.]{0,80}? que regir[áa]n para el año (\d{4})")
VALUE_145 = re.compile(r"Mediante el art[íi]culo \d+ del Decreto (\d+) de (?:\d{1,2} de [a-z]+ de )?(\d{4}),? '[^']*?para "
                       r"el año gravable (\d{4})',? publicad[oa] en el Diario Oficial No\. [\d.]+ de (\d{1,2} de [a-z]+ "
                       r"(?:de )?\d{4})")
VALUE_HEAD = re.compile(r"valores absolutos (?:que regirán |establecidos )?para el año (\d{4}),? (?:establecidos )?por el "
                        r"Decreto (\d+) de (\d{4})")
VALUE_98: dict[str, tuple[str, str]] = {}  # decree key -> (year, the page's words)


def value_decrees_98() -> None:
    """Reads the pages' note boxes straight from their JS (E.plain only: the unit readers and la_blocks register laws,
    which must not happen before these rules are set)."""
    for page in (L633, L488):
        for pg in E.pages(page):
            for box in E.js_boxes(E.read(E.BASE + "js/" + pg + ".js")).values():
                t = E.plain(box)
                for m in VALUE_ET.finditer(t):
                    n, y, pub, year = m.groups()
                    VALUE_98.setdefault(f"dec-{int(n)}-{y}", (year, f"'... del Decreto {n} de {y}, publicado en el Diario "
                                                                    f"Oficial ... de {pub}, se actualizaron los valores absolutos que regirán para el año {year}'"))
                for m in VALUE_145.finditer(t.replace("de 13 de diciembre 2019", "de 13 de diciembre de 2019")):
                    n, y, year, pub = m.groups()
                    VALUE_98.setdefault(f"dec-{int(n)}-{y}", (year, f"'Mediante el artículo 1 del Decreto {n} de {y} ... para el "
                                                                    f"año gravable {year}', publicado en el Diario Oficial ... de {pub}"))
                for m in VALUE_HEAD.finditer(t):
                    year, n, y = m.groups()
                    VALUE_98.setdefault(f"dec-{int(n)}-{y}", (year, f"the earlier-text heading 'con los valores absolutos "
                                                                    f"establecidos para el año {year} por el Decreto {n} de {y}'"))
    for k, (year, why) in sorted(VALUE_98.items()):
        B23._need(int(year) == int(k.split("-")[2]) + 1, f"{k}: values for {year}")
        E.HAND_RULES[k] = (f"{year}-01-01", f"{E.law_label(k)}: {why} (the values apply from 1 January {year})")
    QUOTED_633_DONE.append("Reformas tributarias (Leyes 633 de 2000 and 488 de 1998): the decrees that updated absolute "
                           "values each year (" + ", ".join(E.law_label(k) for k in sorted(VALUE_98, key=lambda k: (k.split("-")[2], int(k.split("-")[1]))))
                           + ") are dated from 1 January of the year the page's notes or earlier-text headings say the "
                           "values govern (the corpus rule, as for the Estatuto Tributario).")



def with_partial_94(page, build):
    def run():
        act = build()
        r = PARTIAL_94[page]
        units = P.doc_units(page)
        head = " ".join(E.plain(it[1]) for it in units[0]["items"] if it[0] == "p")
        B23._need("<NOTA DE VIGENCIA: " + r["head"] + ">" in head, f"{page}: head note")
        pg, art, words = r["check"]
        B23._need(B3.article_text(P.doc_units(pg), art) == words, f"{pg} art. {art}")
        law, day = E.register(r["law"]), r["day"]
        B23._need(E.law_day(law) == day, f"{law}: in force {E.law_day(law)}, expected {day}")
        arts = [u["name"] for u in units if re.fullmatch(r"\d+", u["name"] or "")]
        m = P94_MARKED[page]
        B23._need(sorted(set(arts) - set(m["nv"]), key=int) == sorted(set(r["kept"]) | set(OUT_94.get(page, [])), key=int),
                  f"{page}: articles with no repeal note {sorted(set(arts) - set(m['nv']), key=int)}")
        B23._need(sorted(set(m["nv"]) - set(m["p0"]), key=int) == r["nv_only"] and set(m["p0"]) <= set(m["nv"]),
                  f"{page}: repeal markers {m}")
        vs = act["versions"]
        B23._need(vs[-1]["from"] < day, f"{page}: a version on or after the repeal day ({vs[-1]['from']})")
        state = {}
        for v in vs:
            if "units" in v:
                state = dict(v["units"])
            for k, x in (v.get("changes") or {}).items():
                if x is None:
                    state.pop(k, None)
                else:
                    state[k] = x
        keep = {E.unit_key(n)[0] for n in r["kept"]}
        gone = {E.unit_key(n)[0] for n in m["nv"]}
        B23._need(keep <= set(state) and set(state) - keep - {"titulos"} <= gone,
                  f"{page}: units in force before the repeal {sorted(set(state) - keep - gone - {'titulos'})}")
        lines = state["titulos"]["text"].split(chr(10))
        B23._need(all(sum(l == h for l in lines) == 1 for h in r["heads"]), f"{page}: kept headings")
        new = {k: x for k, x in state.items() if k in keep}
        new["titulos"] = dict(state["titulos"], text=chr(10).join(l for l in lines if l in r["heads"]) + chr(10))
        cr = {k: [law] for k in sorted(state) if k not in keep}
        vs.append({"from": day, "units": new, "credits": cr, "source_url": vs[-1]["source_url"], "sha256": vs[-1]["sha256"],
                   "note": r["note"]})
        PARTIAL94_DONE.append(
            f"{act['title']}: {r['note']} The page prints {len(m['p0'])} of the repealed articles under the marker '<Artículo "
            f"derogado por el artículo 58 de la Ley 909 de 2004>' with a 'Notas de Vigencia' line naming the repeal (art. "
            f"{', '.join(r['nv_only'])}: the line only), and the four kept articles with neither; marker and line are not "
            f"part of the text and are read out so that each article keeps its own earlier history. The version of {day} "
            f"keeps arts. 24, 58, 81 and 82 and the headings above them; the version before it is checked against the text "
            f"the page prints.")
        return act
    return run


# Ley 443 articles out before Ley 909 (struck as a whole by the Court; the page prints no repeal note on them).
OUT_94: dict[str, list[str]] = {L443: ["14", "44", "46", "47", "48", "49", "50", "51", "52", "73", "74", "75", "76", "77", "79"]}


sys.path.insert(0, HERE)
import hand_fixes  # noqa: E402  (batch101/hand_fixes.py)

hand_fixes.install(sys.modules[__name__])


def main(argv):
    P.write_part = write_part
    B13.B8.finish_part = B30.finish_part
    B29.ACTS = ACTS
    B29.HEADING_FIXES_29 = []
    B15.setup(ACTS)
    for slug, page, *_ in ACTS:
        build = B29.cut_signatures(slug, B13.BUILDERS[slug])
        build = B24.with_close(page, build) if page in B24.REPEALS else build
        build = B26.with_stages(page, build) if page in B26.STAGES else build
        build = with_whole_repeal(page, build) if page in WHOLE_REPEAL else build
        build = with_partial_repeal(page, build) if page in PARTIAL_REPEAL else build
        build = with_partial_93(page, build) if page in PARTIAL_93 else build
        build = with_partial_94(page, build) if page in PARTIAL_94 else build
        B13.BUILDERS[slug] = with_title_gone(page, build) if page in TITLE_GONE else build
    value_decrees_98()  # (twenty-second session)
    B13.PART, B13.BATCH, B13.HEADING_FIXES_13 = PART, BATCH, HEADING_FIXES_58
    B13.main(argv)


if __name__ == "__main__":
    main(sys.argv[1:])
