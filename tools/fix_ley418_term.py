"""Patch corpus.d/99l-batch20.json in place: Ley 418 de 1997 (orden-publico), the terms of its extending acts.

Ley 418 de 1997 was a temporary law (art. 131: two years) whose articles later acts extended one by one: Ley 548 de 1999
(three years from its sanction of 23 December 1999), Ley 782 de 2002 (four years from its promulgation of 23 December
2002, for the articles it extended or rewrote), Ley 1106 de 2006 (four years from 22 December 2006), Ley 1421 de 2010 (four
years from 21 December 2010), Ley 1738 de 2014, Ley 1941 de 2018 and Ley 2272 de 2022 (four years from 4 November 2022).
Coordinator decisions (2026-10-31): a term the law's own words date is a dated change; an article leaves the record on the
day after its last term ends, credited to the law whose term ran out.

1. Past lapses: the page marks 18 articles '<Opera la pérdida de fuerza ejecutoria por no haber sido prorrogado este
   artículo por la Ley N de AAAA>'. Each one's last term is the latest extension its Notas de Vigencia give (each term from
   that law's own date); it leaves on the day after that term ends, provided the marker names the next extending act
   after it (that is what lets the day be fixed). Art. 96 does not fit (its notes give no Ley 1106 extension, yet the
   marker names Ley 1421 de 2010): its day cannot be fixed and it is left as it was.
2. The current term: the 100 articles the page marks under Ley 2272 de 2022 art. 19 ('Plazo prorrogado cuatro (4) años
   más por el artículo 19 de la Ley 2272 de 2022' / 'Vigencia de cuatro años, según lo dispuesto en su artículo 19') leave
   on 5 November 2026 (future branch); a later extending act would replace that version.
Headings the lapses leave with no article leave titulos.md with them (termlapse.apply_lapses; headings already empty
stay as they were).
Idempotent (does nothing once the decision line is there); checks the page first.
RE-RUN after any re-parse of batch 20.
Usage: python -X utf8 fix_ley418_term.py
"""
import datetime
import json
import os
import re
import sys

C = os.path.dirname(os.path.abspath(__file__))
for d in ("batch21", "batch20", "batch19", "batch18", "batch17", "batch16", "batch15", "batch14", "batch13", "batch12",
          "batch11", "batch10", "batch9", "batch8", "batch7", "batch6", "batch5", "batch4", "batch3", "phase2"):
    sys.path.insert(0, os.path.join(C, d))
sys.path.insert(0, C)
import termlapse  # noqa: E402

PART = os.path.join(C, "corpus.d", "99l-batch20.json")
PAGE, SLUG = "ley_0418_1997", "orden-publico"
MARK = "terms of its extending acts (2026-10-31)"
TITLE = "Orden público y convivencia (Ley 418 de 1997)"

# the current term
TERM_LAW, TERM_DAY, N_TERM = "ley-2272-2022", "2026-11-05", 100
P1 = "Plazo prorrogado cuatro (4) años más por el artículo 19 de la Ley 2272 de 2022"
P2 = re.compile(r"Vigencia de cuatro años, según lo dispuesto en su art.culo 19")
TERM_NOTE = ("Ley 2272 de 2022, art. 19 (Diario Oficial No. 52.208 of 4 November 2022), extended these articles of Ley 418 de "
             "1997 'por el término de cuatro (4) años', and gave its own arts. 3 to 9 and 15, which rewrite or add others, "
             "'una vigencia de cuatro (4) años, a partir de su promulgación'. The four years end on 4 November 2026; from 5 "
             "November 2026 the articles under that term are out of force. The source names no act extending the term; one "
             "that does would replace this version.")

# past lapses
LAPSED = re.compile(r"<Opera la pérdida de fuerza ejecutoria por no haber sido prorrogado este artículo por la Ley (\d+) de "
                    r"(\d{4})>")
N_LAPSED = 18
MON = {m: i + 1 for i, m in enumerate("enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre "
                                     "diciembre".split())}
EXT = re.compile(r"El artículo 1 de la Ley (\d+) de (\d{4}), publicada en el Diario Oficial No\. [\d.]+,? de (\d+) de (\w+) "
                 r"de (\d{4}), prorroga la vigencia (?:de este artículo|del artículo \d+ de la Ley 782 de 2002),? por un "
                 r"término de cuatro \(4\) años")
MOD = re.compile(r"Artículo modificado por el artículo \d+ de la Ley (782) de (2002), publicada en el Diario Oficial No\. "
                 r"[\d.]+,? de (\d+) de (\w+) de (\d{4})\. Esta ley tiene una vigencia de cuatro \(4\) años a partir de la "
                 r"fecha de su promulgación")
L548 = ("La vigencia de esta ley fue prorrogada por tres (3) años, contados a partir de la sanción de la Ley 548 de 1999, "
        "diciembre 23 de 1999")
CHAIN = ["548", "782", "1106", "1421", "1738"]  # the extending acts in order (up to the past lapses)
YEARS = {"548": 1999, "782": 2002, "1106": 2006, "1421": 2010, "1738": 2014}
TERM_WORDS = {"548": "three years from its sanction (23 December 1999)",
              "782": "four years from its promulgation (Diario Oficial of 23 December 2002)",
              "1106": "four years from its promulgation (Diario Oficial of 22 December 2006)",
              "1421": "four years from its promulgation (Diario Oficial of 21 December 2010)"}


def page_units():
    import parse_batch21 as B
    return B.E, B.P.doc_units(PAGE)


def key_of(E, name):
    if name == "L418-49BBIS":
        return "art-0049b-bis"
    m = re.fullmatch(r"ley_0418_1997:NUEVO:132:(\d)", name)
    if m:
        return f"art-0132-nuevo-{m.group(1)}"
    return E.unit_key(name)[0]


def is_article(name):
    return bool(re.fullmatch(r"\d+[A-Z]*", name) or name == "L418-49BBIS" or name.startswith("ley_0418_1997:NUEVO:"))


def last_term(nv):
    """The extension terms the notes give: [(act number, start day, years)]."""
    terms = []
    if L548 in nv:
        terms.append(("548", datetime.date(1999, 12, 23), 3))
    for rx in (EXT, MOD):
        for x in rx.finditer(nv):
            terms.append((x.group(1), datetime.date(int(x.group(5)), MON[x.group(4)], int(x.group(3))), 4))
    return terms


def main():
    part = json.load(open(PART, encoding="utf-8"))
    if any(MARK in x for x in part["decisions"]):
        print("already applied")
        return
    E, units = page_units()
    order, term, lapses, unfixed = [], [], {}, []
    for u in units:
        n = u["name"] or ""
        if n == "_head":
            continue
        order.append((n, u["label"] or "", is_article(n)))
        if not is_article(n):
            continue
        nv = " ".join(E.plain(it[2]) for it in u["items"] if it[0] == "box" and it[1] == "Notas de Vigencia")
        p = " ".join(E.plain(it[1]) for it in u["items"] if it[0] == "p")
        if P1 in nv or P2.search(nv):
            term.append(n)
        m = LAPSED.search(p)
        if not m:
            continue
        terms = last_term(nv)
        last = max(terms, key=lambda t: t[1])
        nxt = CHAIN[CHAIN.index(last[0]) + 1]
        if (m.group(1), int(m.group(2))) != (nxt, YEARS[nxt]):
            unfixed.append((n, f"its notes give its last extension by Ley {last[0]} de {YEARS[last[0]]}, but the page's "
                               f"marker says it lapsed for want of extension by Ley {m.group(1)} de {m.group(2)} (which "
                               f"implies an extension by Ley {CHAIN[CHAIN.index(last[0]) + 1]} de "
                               f"{YEARS[CHAIN[CHAIN.index(last[0]) + 1]]} the page does not give)"))
            continue
        end = last[1].replace(year=last[1].year + last[2])
        lapses[n] = (last[0], end, (end + datetime.timedelta(days=1)).isoformat())
    if len(term) != N_TERM or len(lapses) + len(unfixed) != N_LAPSED or [n for n, _ in unfixed] != ["96"]:
        sys.exit(f"page check failed: {len(term)} under the term, {len(lapses)} lapses, unfixed {unfixed}")
    act = next(a for a in part["acts"] if a["slug"] == SLUG)
    state = termlapse.state_of(act["versions"])
    events = []
    by_day: dict = {}
    for n, (law, end, day) in lapses.items():
        by_day.setdefault((day, law, end), []).append(n)
    for (day, law, end), ns in sorted(by_day.items()):
        key = f"ley-{law}-{YEARS[law]}"
        if key not in part["laws"]:
            sys.exit(f"{key} not in the part's laws")
        ks = {key_of(E, n) for n in ns}
        if not ks <= set(state):
            sys.exit(f"lapsed articles not in force: {sorted(ks - set(state))}")
        nxt = CHAIN[CHAIN.index(law) + 1]
        note = (f"Ley {law} de {YEARS[law]} extended these articles of Ley 418 de 1997 for {TERM_WORDS[law]}, a term that "
                f"ended on {end.isoformat()}; Ley {nxt} de {YEARS[nxt]} did not extend them, so they lost force "
                f"(pérdida de fuerza ejecutoria) from {day}.")
        events.append((day, ks, key, note))
    gone = {key_of(E, n) for n in term}
    if not gone <= set(state) or gone & {k for _, ks, _, _ in events for k in ks}:
        sys.exit("term articles not in force, or also lapsed")
    events.append((TERM_DAY, gone, TERM_LAW, TERM_NOTE))
    dropped: list = []
    act["versions"] = termlapse.apply_lapses(act["versions"], events, order, lambda n: key_of(E, n), dropped)
    after = termlapse.state_of(act["versions"])
    if {key_of(E, n) for n in lapses} & set(after) or gone & set(after):
        sys.exit("lapsed articles still in force")
    for day, ks, law, note in events[:-1]:
        arts = ", ".join(sorted((n for n in lapses if key_of(E, n) in ks), key=lambda x: int(x)))
        num = law.split("-")[1]
        nxt = CHAIN[CHAIN.index(num) + 1]
        what = f"arts. {arts} leave" if ", " in arts else f"art. {arts} leaves"
        part["decisions"].append(f"{TITLE}, {MARK}: {what} on {day}, credited to Ley {num} de {YEARS[num]}: "
                                 f"{note} The page marks each '<Opera la pérdida de fuerza ejecutoria por no haber sido "
                                 f"prorrogado este artículo por la Ley {nxt} de {YEARS[nxt]}>' and its Notas de Vigencia give "
                                 "the extensions (each term counted from that act's own date, ending on its anniversary; "
                                 "the article leaves the day after). Coordinator decision (2026-10-31).")
    part["decisions"].append(f"{TITLE}, {MARK}: {TERM_NOTE} The version of {TERM_DAY} (future branch) takes out the "
                             f"{len(gone)} articles the page marks under that term ('Plazo prorrogado cuatro (4) años más "
                             "por el artículo 19 de la Ley 2272 de 2022' or 'Vigencia de cuatro años, según lo dispuesto "
                             "en su artículo 19'). Coordinator decision (2026-10-31): a term the law's own words date is a "
                             "dated change.")
    for n, why in unfixed:
        part["decisions"].append(f"{TITLE}, {MARK}: art. {n} is marked '<Opera la pérdida de fuerza ejecutoria ...>' but "
                                 f"stays in the record as printed: {why}, so the day it lost force cannot be fixed.")
    part["decisions"].append(f"{TITLE}, {MARK}: headings of titulos.md that these lapses leave with no article leave with "
                             "them, credited to the same act; headings already left with no article by earlier changes "
                             "stay as they were." + (f" Versions whose heading change the lapses cancel: {', '.join(dropped)}."
                                                    if dropped else ""))
    tmp = PART + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    os.replace(tmp, PART)
    for day, ks, law, _ in events:
        print(day, law, len(ks))
    print("unfixed:", [n for n, _ in unfixed], "dropped titulos changes:", dropped)
    print(after["titulos"]["text"])


if __name__ == "__main__":
    main()
