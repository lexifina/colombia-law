"""Ley 794 de 2003's two early provisions, in the Código de Procedimiento Civil (coordinator decision, 2026-11-01,
twenty-seventh session).

Ley 794 de 2003 art. 70: 'La presente ley entrará a regir tres (3) meses después de su promulgación, salvo lo que se
dispone para los artículos 388 inciso final y parágrafo 2o del artículo 528, los cuales entrarán a regir a partir de la
promulgación de esta ley.' Promulgated in Diario Oficial No. 45.058 of 9 January 2003: the act applies from 9 April
2003, but the last inciso of CPC art. 388 (its art. 41) and parágrafo 2o of CPC art. 528 (its art. 58) from 9 January
2003. The CPC part (99s-batch27) dated all of Ley 794's changes 9 April 2003. Here those two lines (each checked on Ley
794's page and in the article's 9 April 2003 text, absent from the text before) are added on 9 January 2003 to the text
then in force, credited to Ley 794; the rest of the two articles changes on 9 April 2003 as before.

Idempotent (a unit already changed on 9 January 2003 by Ley 794 with the right text is left alone; the decision line is
written once). RE-RUN ORDER: after fix_law_entries.py, before fix_conditional_notes.py, after any re-parse of 99s-batch27.

Usage: python -X utf8 fix_ley794_start.py [corpus.d folder]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import fix_c253_deferral as C253  # noqa: E402  (page_text)

MARK = "Ley 794 de 2003, early provisions (2026-11-01)"
LAW, PUB, START = "ley-794-2003", "2003-01-09", "2003-04-09"
CLAUSE = ("La presente ley entrará a regir tres (3) meses después de su promulgación, salvo lo que se dispone para los "
          "artículos 388 inciso final y parágrafo 2o del artículo 528, los cuales entrarán a regir a partir de la "
          "promulgación de esta ley.")
L388 = ("Cuando haya lugar a remuneración o reembolso de honorarios por concepto de un dictamen pericial, en ningún caso "
        "se podrán exceder las tarifas señaladas por el Consejo Superior de la Judicatura, las cuales deberán ser fijadas "
        "dentro de los tres (3) meses siguientes a la promulgación de la presente ley.")
L528 = ("PARÁGRAFO 2o. La Superintendencia de Notariado y Registro fijará las tarifas de los derechos notariales que se "
        "cobrarán por la realización de las diligencias de remate. Las tarifas de las Cámaras de Comercio y Martillos "
        "serán fijadas por el Gobierno Nacional. Para estos efectos, las entidades dispondrán de un término de tres (3) "
        "meses contados a partir de la promulgación de la presente ley.")
ENTRIES = [
    {"part": "99s-batch27.json", "slug": "codigo-de-procedimiento-civil-1970", "unit": "art-0388", "line": L388,
     "page_line": L388},
    {"part": "99s-batch27.json", "slug": "codigo-de-procedimiento-civil-1970", "unit": "art-0528", "line": L528,
     "page_line": L528 + '"'},
]
DECISION = (f"{MARK}: Ley 794 de 2003 art. 70 starts the act three months after its promulgation (Diario Oficial No. "
            "45.058 of 9 January 2003: 9 April 2003) 'salvo lo que se dispone para los artículos 388 inciso final y "
            "parágrafo 2o del artículo 528, los cuales entrarán a regir a partir de la promulgación de esta ley': the "
            "last inciso of art. 388 (expert-opinion fees capped by the Consejo Superior de la Judicatura's tariffs) and "
            "parágrafo 2o of art. 528 (tariffs for auctions before notaries, chambers of commerce and auctioneers), as "
            "Ley 794 arts. 41 and 58 wrote them, are added on 9 January 2003 to the text then in force, credited to Ley "
            "794; the rest of both articles changes on 9 April 2003 with the rest of the act.")


def states(act, key):
    out, cur = [], None
    for v in act["versions"]:
        if "units" in v:
            cur = (v["units"].get(key) or {}).get("text")
        if key in (v.get("changes") or {}):
            u = v["changes"][key]
            cur = u and u.get("text")
        out.append(cur)
    return out


def unit_at(act, key, k):
    unit = None
    for v in act["versions"][:k + 1]:
        if "units" in v:
            unit = v["units"].get(key)
        if key in (v.get("changes") or {}):
            unit = v["changes"][key]
    return unit


def apply(act, e):
    vs, key = act["versions"], e["unit"]
    st = states(act, key)
    days = [v["from"] for v in vs]
    if PUB in days:
        v = vs[days.index(PUB)]
        if v["credits"].get(key) == [LAW]:
            t = st[days.index(PUB)]
            if t is None or e["line"] not in t.split("\n"):
                raise SystemExit(f"{key}: a change on {PUB} without the early line")
            return False
    if START not in days or vs[days.index(START)]["credits"].get(key) != [LAW]:
        raise SystemExit(f"{key}: no change on {START} credited to {LAW} alone")
    k_start = days.index(START)
    new = st[k_start].split("\n")
    if new.count(e["line"]) != 1 or new[-2] != e["line"] or new[-1] != "":
        raise SystemExit(f"{key}: the early line is not the last line of the {START} text")
    k = max(i for i, d in enumerate(days) if d < PUB)
    if any(PUB < d < START and key in (vs[i].get("changes") or {}) for i, d in enumerate(days)) \
            or any(PUB < d < START and key in vs[i]["credits"] for i, d in enumerate(days)):
        raise SystemExit(f"{key}: another change between {PUB} and {START}")
    old = st[k]
    if old is None or e["line"] in old.split("\n"):
        raise SystemExit(f"{key}: text before {PUB} missing or already holds the line")
    early = old.rstrip("\n") + "\n" + e["line"] + "\n"
    unit = dict(unit_at(act, key, k), text=early)
    if PUB in days:
        w = vs[days.index(PUB)]
    else:
        w = {"from": PUB, "credits": {}, "changes": {}}
        for f in ("source_url", "sha256"):
            if f in vs[k]:
                w[f] = vs[k][f]
        vs.insert(k + 1, w)
    if "units" in w:
        raise SystemExit(f"{key}: full-units version on {PUB}")
    w.setdefault("changes", {})[key] = unit
    w["credits"][key] = [LAW]
    after = states(act, key)
    want = st[:k + 1] + [early] + st[k + 2 if PUB in days else k + 1:]
    if after != want:
        raise SystemExit(f"{key}: states do not come out as wanted")
    return True


def main(argv):
    out = argv[0] if argv else os.path.join(HERE, "corpus.d")
    page = C253.page_text("ley_0794_2003")
    # (the page's text has a space before the comma after '528': a link ends there)
    for q in [CLAUSE.replace("528,", "528 ,")] + [e["page_line"] for e in ENTRIES]:
        if q not in page:
            raise SystemExit(f"ley_0794_2003: not quoted: {q[:80]}")
    for name in dict.fromkeys(e["part"] for e in ENTRIES):
        path = os.path.join(out, name)
        part = json.load(open(path, encoding="utf-8"))
        done = []
        for e in [e for e in ENTRIES if e["part"] == name]:
            act = next(a for a in part["acts"] if a["slug"] == e["slug"])
            if apply(act, e):
                done.append(e["unit"])
        if not done and part["decisions"].count(DECISION) == 1:
            print(name, "already applied")
            continue
        part["decisions"] = [d for d in part["decisions"] if d != DECISION] + [DECISION]
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as f:
            json.dump(part, f, ensure_ascii=False, separators=(",", ":"))
            f.write("\n")
        os.replace(tmp, path)
        print(name, "applied:", ", ".join(done) or "(decision line only)")


if __name__ == "__main__":
    main(sys.argv[1:])
